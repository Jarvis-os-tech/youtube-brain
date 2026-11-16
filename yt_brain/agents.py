"""LLM access, transcripts, and pipeline agents."""

from __future__ import annotations

import json
import logging
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import config
import prompts
import topics

log = logging.getLogger(__name__)


# --- LLM backend -------------------------------------------------------------


def _llm_model_candidates() -> list[str | None]:
    """Primary model followed by configured fallbacks.

    When no primary is set, skip the CLI default and use fallbacks directly.
    """
    candidates: list[str | None] = []
    if config.LLM_MODEL:
        candidates.append(config.LLM_MODEL)
    elif not config.LLM_FALLBACK_MODELS:
        candidates.append(None)
    for model in config.LLM_FALLBACK_MODELS:
        if model not in candidates:
            candidates.append(model)
    return candidates


def call_llm(prompt: str, system: str, max_tokens: int | None = None) -> str:
    """Run one LLM turn via `opencode run`, trying fallback models on failure."""
    if not shutil.which(config.LLM_COMMAND):
        raise RuntimeError(f"LLM command {config.LLM_COMMAND!r} not found on PATH")

    payload = f"{system.strip()}\n\n---\n\n{prompt.strip()}"
    errors: list[str] = []

    for model in _llm_model_candidates():
        cmd = [config.LLM_COMMAND, "run"]
        if model:
            cmd += ["-m", model]
        cmd.append(payload)
        label = model or "default"
        log.debug("llm call model=%s (%d prompt chars)", label, len(payload))
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=config.LLM_TIMEOUT,
                cwd=str(config.LLM_CWD),
            )
        except subprocess.TimeoutExpired:
            msg = f"timeout after {config.LLM_TIMEOUT}s"
            log.warning("LLM %s failed: %s", label, msg)
            errors.append(f"{label}: {msg}")
            raise
        except Exception as exc:  # noqa: BLE001
            log.warning("LLM %s failed: %s", label, exc)
            errors.append(f"{label}: {exc}")
            continue

        if proc.returncode == 0:
            out = (proc.stdout or "").strip()
            if out:
                if model != config.LLM_MODEL:
                    log.info("LLM succeeded with fallback model %s", label)
                return out
            msg = "empty output"
        else:
            msg = f"exit {proc.returncode}: {(proc.stderr or proc.stdout or '').strip()[:300]}"

        log.warning("LLM %s failed: %s", label, msg)
        errors.append(f"{label}: {msg}")

    raise RuntimeError("all LLM attempts failed: " + " | ".join(errors[:6]))


def extract_json(text: str) -> dict:
    stripped = text.strip()
    # Fenced block first, then every balanced {...} span.
    for block in re.findall(r"```(?:json)?\s*(.+?)```", stripped, re.DOTALL):
        try:
            return json.loads(block.strip())
        except json.JSONDecodeError:
            pass
    starts = [i for i, ch in enumerate(stripped) if ch == "{"]
    for start in starts:
        depth = 0
        in_string = False
        escaped = False
        for idx in range(start, len(stripped)):
            ch = stripped[idx]
            if in_string:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(stripped[start : idx + 1])
                    except json.JSONDecodeError:
                        break
    raise ValueError(f"no valid JSON object in LLM output: {text[:300]!r}")


def call_llm_json(prompt: str, system: str, max_tokens: int | None = None) -> dict:
    return extract_json(call_llm(prompt, system, max_tokens))


# --- Agent 1: classify history into AI / non-AI ------------------------------


def classify_history(record) -> dict:
    prompt = (
        f"Title: {record.slug_title}\n"
        f"URL: {record.url}\n"
        f"Source: {getattr(record, 'source', '')}\n"
        f"Watched: {getattr(record, 'watched_at', '')}\n"
    )
    data = call_llm_json(prompt, prompts.HISTORY_CLASSIFIER_SYSTEM, config.GATEKEEPER_MAX_TOKENS)
    cls = str(data.get("history_class", "")).strip().lower()
    if cls not in {"ai", "non-ai"}:
        # best-effort normalization
        cls = "ai" if "ai" in cls else "non-ai"
    return {"history_class": cls, "reason": str(data.get("reason", ""))[:120]}


# --- Agent 2: transcribe videos ---------------------------------------------


def _cookie_jar_path() -> Path | None:
    path = config.COOKIE_FILE
    if path and Path(path).is_file():
        return Path(path)
    return None


def _build_api():
    from youtube_transcript_api import YouTubeTranscriptApi

    jar_path = _cookie_jar_path()
    if not jar_path:
        return YouTubeTranscriptApi()

    import http.cookiejar
    import requests

    jar = http.cookiejar.MozillaCookieJar(str(jar_path))
    try:
        jar.load(ignore_discard=True, ignore_expires=True)
    except (http.cookiejar.LoadError, OSError) as exc:
        log.warning("cookie file %s unreadable (%s); trying unauthenticated", jar_path, exc)
        return YouTubeTranscriptApi()

    session = requests.Session()
    session.cookies.update(jar)
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
    )
    return YouTubeTranscriptApi(http_client=session)


def fetch_transcript(video_id: str) -> str:
    api = _build_api()
    last_error: Exception | None = None

    for language in ("en", "en-US", "en-GB"):
        try:
            fetched = api.fetch(video_id, languages=[language])
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            continue
        text = " ".join(snippet.text.strip() for snippet in fetched)
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            log.info("transcript ok: %s (%d chars, %s)", video_id, len(text), language)
            return text

    try:
        listing = api.list(video_id)
        transcript = listing.find_transcript(["en"]).fetch()
        text = re.sub(r"\s+", " ", " ".join(s.text for s in transcript)).strip()
        if text:
            return text
    except Exception:  # noqa: BLE001
        pass

    raise last_error or RuntimeError("no transcript available")


def transcript_path(video_id: str) -> Path:
    config.TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    return config.TRANSCRIPTS_DIR / f"{video_id}.txt"


def save_transcript(video_id: str, text: str) -> Path:
    path = transcript_path(video_id)
    path.write_text(text, encoding="utf-8")
    return path


def load_transcript(video_id: str) -> str | None:
    path = transcript_path(video_id)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return None


# --- Agent 3: summarize and store key points ---------------------------------


def summarize(record, transcript: str) -> str:
    text = transcript[: config.MAX_TRANSCRIPT_CHARS]
    if len(transcript) > config.MAX_TRANSCRIPT_CHARS:
        log.warning("%s: transcript truncated from %d to %d chars", record.video_id, len(transcript), len(text))
        text += "\n\n[transcript truncated]"

    prompt = (
        f"Title: {record.slug_title}\n"
        f"URL: {getattr(record, 'url', '')}\n"
        f"History class: {getattr(record, 'history_class', 'unknown')}\n\n"
        f"Transcript:\n{text}\n\n{prompts.SUMMARY_INSTRUCTIONS}"
    )

    if len(text) <= config.CHARS_PER_SUMMARY_CHUNK:
        return call_llm(prompt, prompts.SUMMARY_SYSTEM, config.SUMMARY_MAX_TOKENS)

    chunks = [text[i : i + config.CHARS_PER_SUMMARY_CHUNK] for i in range(0, len(text), config.CHARS_PER_SUMMARY_CHUNK)]
    partials = []
    for n, chunk in enumerate(chunks, 1):
        try:
            partials.append(
                call_llm(
                    f"Title: {record.slug_title}\nPart {n}/{len(chunks)}\n\nTranscript:\n{chunk}\n\n"
                    "Write key points and required/actionable items for this part only. Markdown, no preamble.",
                    prompts.SUMMARY_SYSTEM,
                    900,
                )
            )
        except Exception as exc:  # noqa: BLE001
            log.warning("summary chunk %d/%d failed for %s: %s", n, len(chunks), record.video_id, exc)
    if not partials:
        raise RuntimeError("every summary chunk failed")
    return call_llm(
        f"Title: {record.slug_title}\nHistory class: {getattr(record, 'history_class', 'unknown')}\n\n"
        f"Combine these part notes into final sections ## Key Points, ## Required / Actionable Items, ## Important Details.\n\n"
        + "\n\n".join(partials),
        prompts.SUMMARY_SYSTEM,
        config.SUMMARY_MAX_TOKENS,
    )


def note_path(record, history_class: str) -> Path:
    bucket = "ai" if history_class == "ai" else "non-ai"
    config.NOTES_DIR.joinpath(bucket).mkdir(parents=True, exist_ok=True)
    date = datetime.now().astimezone().strftime("%Y-%m-%d")
    return config.NOTES_DIR / bucket / topics.note_filename(date, record.slug_title)


def write_summary_note(record, summary: str, history_class: str, transcript_ref: str) -> Path:
    path = note_path(record, history_class)
    watched = getattr(record, "watched_at", None)
    watched_s = watched.astimezone().strftime("%Y-%m-%d %H:%M") if watched else ""
    front_matter = "\n".join(
        [
            "---",
            f"video_id: {record.video_id}",
            f"title: {json.dumps(record.slug_title, ensure_ascii=False)}",
            f"url: {getattr(record, 'url', '')}",
            f"watched: {watched_s}",
            f"history_class: {history_class}",
            f"transcript: {json.dumps(transcript_ref)}",
            f"indexed: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
            "---",
        ]
    )
    path.write_text(f"{front_matter}\n\n{summary.strip()}\n", encoding="utf-8")
    return path


# --- Agent 4: classify stored notes clearly ----------------------------------


def classify_note(record, history_class: str, summary: str) -> dict:
    prompt = (
        f"Title: {record.slug_title}\n"
        f"History class: {history_class}\n\n"
        f"Summary:\n{summary[:12000]}"
    )
    data = call_llm_json(prompt, prompts.NOTE_CLASSIFIER_SYSTEM, config.GATEKEEPER_MAX_TOKENS)
    tags = data.get("tags") or []
    if not isinstance(tags, list):
        tags = [str(tags)]
    return {
        "primary_category": str(data.get("primary_category", "general"))[:60],
        "tags": [str(t)[:40] for t in tags[:10]],
        "priority": str(data.get("priority", "medium")).lower(),
        "keep": bool(data.get("keep", True)),
        "reason": str(data.get("reason", ""))[:120],
    }


def write_classified_record(record, history_class: str, summary: str, classification: dict, note_path_str: str) -> Path:
    bucket = "ai" if history_class == "ai" else "non-ai"
    out_dir = config.CLASSIFIED_DIR / bucket / str(classification.get("primary_category", "general")).replace("/", "-")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{record.video_id}.json"
    payload = {
        "video_id": record.video_id,
        "title": record.slug_title,
        "url": getattr(record, "url", ""),
        "history_class": history_class,
        "classification": classification,
        "note_path": note_path_str,
        "summary_excerpt": summary[:1000],
        "classified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # append to per-class index
    index_path = config.CLASSIFIED_DIR / bucket / "_index.jsonl"
    with index_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return out_path


# --- Agent 5: final review ---------------------------------------------------


def build_review_report(state_data: dict) -> tuple[str, Path]:
    videos = state_data.get("videos", {})
    total = len(videos)
    ai = [v for v in videos.values() if v.get("history_class") == "ai"]
    non_ai = [v for v in videos.values() if v.get("history_class") == "non-ai"]
    transcribed = [v for v in videos.values() if v.get("transcript_status") == "ok"]
    summarized = [v for v in videos.values() if v.get("summary_status") == "ok"]
    classified = [v for v in videos.values() if v.get("note_class_status") == "ok"]
    no_transcript = [v for v in videos.values() if v.get("transcript_status") in {"no_transcript", "error"}]

    def sample(items, n=12):
        out = []
        for v in items[:n]:
            out.append(f"- [{v.get('history_class','?')}] {v.get('title','')} ({v.get('video_id','')}) status={v.get('status','')} note={v.get('classified_path') or v.get('note_path') or ''}")
        return "\n".join(out) or "- (none)"

    prompt = (
        f"Total videos: {total}\nAI: {len(ai)}\nNon-AI: {len(non_ai)}\n"
        f"Transcribed: {len(transcribed)}\nSummarized: {len(summarized)}\nClassified: {len(classified)}\n"
        f"Transcript unavailable/errors: {len(no_transcript)}\n\n"
        f"AI samples:\n{sample(ai)}\n\nNon-AI samples:\n{sample(non_ai)}\n\n"
        f"No-transcript/error samples:\n{sample(no_transcript)}\n\n"
        "Write the final review report."
    )
    report = call_llm(prompt, prompts.REVIEW_SYSTEM, config.SUMMARY_MAX_TOKENS)
    config.REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    path = config.REVIEWS_DIR / f"review-{ts}.md"
    path.write_text(report.strip() + "\n", encoding="utf-8")
    latest = config.REVIEWS_DIR / "latest.md"
    latest.write_text(report.strip() + "\n", encoding="utf-8")
    return report, path


# --- Legacy compatibility wrappers ------------------------------------------


def gatekeep(record) -> bool:
    res = classify_history(record)
    # legacy behavior: "relevant" meant worth full processing
    return res.get("history_class") == "ai"


def write_note(record, summary: str) -> Path:
    history_class = getattr(record, "history_class", "ai")
    return write_summary_note(record, summary, history_class, "")
