#!/usr/bin/env python3
"""yt-brain: multi-agent YouTube history pipeline.

Stages:
1. Classify all history videos into AI / non-AI
2. Transcribe all videos
3. Summarize transcripts into key points and required items
4. Classify summarized notes and store clearly
5. Final review of all stored notes
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

import agents
import config
import ingest
import publish
import state

log = logging.getLogger("yt-brain")


def setup_logging(verbose: bool) -> None:
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    for d in (config.TRANSCRIPTS_DIR, config.NOTES_DIR, config.CLASSIFIED_DIR, config.REVIEWS_DIR, config.KB_DIR):
        d.mkdir(parents=True, exist_ok=True)
    handlers: list[logging.Handler] = [logging.FileHandler(config.BATCH_LOG, encoding="utf-8")]
    handlers.append(logging.StreamHandler(sys.stdout if verbose else sys.stderr))
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        handlers=handlers,
        force=True,
    )


def enrich_record(record):
    # attach any known classification for downstream prompts
    rec = state.get_video(record.video_id)
    record.history_class = rec.get("history_class")
    return record


def stage1_classify_history(queue) -> dict:
    log.info("=== Stage 1: classify history into AI / non-AI (%d videos) ===", len(queue))
    counts = {"ai": 0, "non-ai": 0, "skipped": 0, "error": 0}
    for i, rec in enumerate(queue, 1):
        existing = state.get_video(rec.video_id)
        if existing.get("history_class") in {"ai", "non-ai"}:
            counts[existing["history_class"]] += 1
            continue
        try:
            res = agents.classify_history(rec)
            state.update_video(
                rec.video_id,
                title=rec.slug_title,
                url=getattr(rec, "url", ""),
                watched_at=str(getattr(rec, "watched_at", "")),
                source=getattr(rec, "source", ""),
                history_class=res["history_class"],
                history_class_reason=res.get("reason", ""),
                stage1="ok",
            )
            counts[res["history_class"]] += 1
            log.info("[%d/%d] %s -> %s", i, len(queue), rec.video_id, res["history_class"])
        except Exception as exc:  # noqa: BLE001
            log.error("stage1 failed for %s: %s", rec.video_id, exc)
            state.update_video(rec.video_id, title=rec.slug_title, stage1="error", stage1_error=str(exc))
            counts["error"] += 1
    return counts


def stage2_transcribe(queue) -> dict:
    log.info("=== Stage 2: transcribe videos (%d videos) ===", len(queue))
    counts = {"ok": 0, "no_transcript": 0, "cached": 0, "error": 0}
    for i, rec in enumerate(queue, 1):
        existing = state.get_video(rec.video_id)
        tpath = agents.transcript_path(rec.video_id)
        if existing.get("transcript_status") == "ok" and tpath.exists():
            counts["cached"] += 1
            continue
        try:
            transcript = agents.fetch_transcript(rec.video_id)
            if len(transcript.strip()) < 80:
                state.update_video(rec.video_id, transcript_status="no_transcript", transcript_reason="too short")
                counts["no_transcript"] += 1
            else:
                path = agents.save_transcript(rec.video_id, transcript)
                state.update_video(rec.video_id, transcript_status="ok", transcript_path=str(path), transcript_chars=len(transcript))
                counts["ok"] += 1
                log.info("[%d/%d] transcribed %s (%d chars)", i, len(queue), rec.video_id, len(transcript))
        except Exception as exc:  # noqa: BLE001
            log.warning("stage2 no transcript for %s: %s", rec.video_id, exc)
            state.update_video(rec.video_id, transcript_status="no_transcript", transcript_error=f"{type(exc).__name__}: {exc}")
            counts["no_transcript"] += 1
    return counts


def stage3_summarize(queue) -> dict:
    log.info("=== Stage 3: summarize and store key points (%d videos) ===", len(queue))
    counts = {"ok": 0, "skipped": 0, "error": 0, "cached": 0}
    for i, rec in enumerate(queue, 1):
        enrich_record(rec)
        v = state.get_video(rec.video_id)
        if v.get("summary_status") == "ok" and v.get("note_path") and Path(v["note_path"]).exists():
            counts["cached"] += 1
            continue
        if v.get("transcript_status") != "ok":
            counts["skipped"] += 1
            continue
        transcript = agents.load_transcript(rec.video_id)
        if not transcript:
            counts["skipped"] += 1
            continue
        try:
            history_class = v.get("history_class") or "non-ai"
            rec.history_class = history_class
            summary = agents.summarize(rec, transcript)
            if not summary.strip():
                raise RuntimeError("empty summary")
            note = agents.write_summary_note(rec, summary, history_class, v.get("transcript_path", ""))
            state.update_video(rec.video_id, summary_status="ok", note_path=str(note))
            # legacy compatibility
            state.mark(rec.video_id, "saved", rec.slug_title, str(note))
            counts["ok"] += 1
            log.info("[%d/%d] summarized %s -> %s", i, len(queue), rec.video_id, note)
        except Exception as exc:  # noqa: BLE001
            log.error("stage3 failed for %s: %s", rec.video_id, exc)
            state.update_video(rec.video_id, summary_status="error", summary_error=str(exc))
            counts["error"] += 1
    return counts


def stage4_classify_notes(queue) -> dict:
    log.info("=== Stage 4: classify summarized notes and store clearly (%d videos) ===", len(queue))
    counts = {"ok": 0, "skipped": 0, "error": 0, "cached": 0}
    for i, rec in enumerate(queue, 1):
        v = state.get_video(rec.video_id)
        if v.get("note_class_status") == "ok" and v.get("classified_path"):
            counts["cached"] += 1
            continue
        note_path = v.get("note_path")
        if v.get("summary_status") != "ok" or not note_path or not Path(note_path).exists():
            counts["skipped"] += 1
            continue
        try:
            history_class = v.get("history_class") or "non-ai"
            summary = Path(note_path).read_text(encoding="utf-8")
            classification = agents.classify_note(rec, history_class, summary)
            cpath = agents.write_classified_record(rec, history_class, summary, classification, note_path)
            state.update_video(rec.video_id, note_class_status="ok", classified_path=str(cpath), classification=classification)
            counts["ok"] += 1
            log.info("[%d/%d] classified %s -> %s", i, len(queue), rec.video_id, cpath)
        except Exception as exc:  # noqa: BLE001
            log.error("stage4 failed for %s: %s", rec.video_id, exc)
            state.update_video(rec.video_id, note_class_status="error", note_class_error=str(exc))
            counts["error"] += 1
    return counts


def stage5_review() -> dict:
    log.info("=== Stage 5: final review of all notes ===")
    data = {"videos": state.list_videos(), "review": state.get_review()}
    try:
        report, path = agents.build_review_report(data)
        state.set_review("latest_path", str(path))
        state.set_review("latest_report_chars", len(report))
        state.set_review("error", None)
        log.info("review written: %s", path)
        return {"ok": 1, "path": str(path)}
    except Exception as exc:  # noqa: BLE001
        log.error("stage5 review failed: %s", exc)
        state.set_review("error", str(exc))
        return {"ok": 0, "error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--limit", type=int, default=config.MAX_VIDEOS_PER_RUN)
    parser.add_argument("--dry-run", action="store_true", help="list the queue, run no agents")
    parser.add_argument("--no-clear-buffer", action="store_true")
    parser.add_argument("--stage", choices=["1", "2", "3", "4", "5", "all"], default="all")
    args = parser.parse_args()

    setup_logging(args.verbose)
    started = time.time()
    state.init_state()

    queue = ingest.build_queue()
    log.info("history queue=%d videos", len(queue))

    if args.dry_run:
        for rec in queue[: args.limit]:
            v = state.get_video(rec.video_id)
            print(f"{getattr(rec,'watched_at','')}  {rec.video_id}  {v.get('history_class','?'):6}  {rec.slug_title}")
        print(f"\n{len(queue)} total in queue (dry run).")
        return 0

    # Respect limit per run for heavy stages by slicing worklist where appropriate
    work = queue[: args.limit] if args.limit and args.limit < len(queue) else queue

    results = {}
    if args.stage in ("1", "all"):
        results["stage1_classify"] = stage1_classify_history(queue)  # classify all history
    if args.stage in ("2", "all"):
        results["stage2_transcribe"] = stage2_transcribe(work)
    if args.stage in ("3", "all"):
        results["stage3_summarize"] = stage3_summarize(work)
    if args.stage in ("4", "all"):
        results["stage4_classify"] = stage4_classify_notes(work)
    if args.stage in ("5", "all"):
        results["stage5_review"] = stage5_review()

    if not args.no_clear_buffer:
        try:
            ingest.clear_buffer()
        except Exception:  # noqa: BLE001
            pass

    try:
        publish.publish()
    except Exception as exc:  # noqa: BLE001
        log.warning("publish step failed: %s", exc)

    log.info("pipeline done in %.1fs | %s", time.time() - started, results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
