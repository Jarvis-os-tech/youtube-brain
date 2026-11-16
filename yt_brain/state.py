"""Video-ID state store backed by an atomic JSON file.

Tracks per-video pipeline progress: history classification (AI/non-AI),
transcription, summarization, note classification, and final review.
Writes are atomic (temp file + os.replace).
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
import threading
from pathlib import Path

log = logging.getLogger(__name__)

_lock = threading.Lock()

# Resolved lazily so tests can point YT_BRAIN_STATE at a scratch file.
_STATE = Path(os.environ.get("YT_BRAIN_STATE", Path(__file__).resolve().parent / "processed_videos.json"))


def init_state(path: Path | None = None) -> None:
    global _STATE
    if path is not None:
        _STATE = path
    _STATE.parent.mkdir(parents=True, exist_ok=True)
    if not _STATE.exists():
        _write(_STATE, {"processed": {}, "videos": {}, "review": {}})
        log.info("initialized empty state at %s", _STATE)


def _read(path: Path) -> dict:
    if not path.exists():
        return {"processed": {}, "videos": {}, "review": {}}
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        log.error("state file %s unreadable (%s); starting fresh", path, exc)
        return {"processed": {}, "videos": {}, "review": {}}
    if not isinstance(data, dict):
        log.error("state file %s has unexpected shape; starting fresh", path)
        return {"processed": {}, "videos": {}, "review": {}}
    data.setdefault("processed", {})
    data.setdefault("videos", {})
    data.setdefault("review", {})
    return data


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".state-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1, sort_keys=True)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def _load() -> dict:
    return _read(_STATE)


def _save(data: dict) -> None:
    _write(_STATE, data)


def get_video(video_id: str) -> dict:
    with _lock:
        return dict(_load().get("videos", {}).get(video_id, {}))


def update_video(video_id: str, **fields) -> dict:
    """Merge fields into a video's record and return the updated record."""
    from datetime import datetime, timezone

    with _lock:
        data = _load()
        rec = data.setdefault("videos", {}).setdefault(video_id, {"video_id": video_id})
        rec.update({k: v for k, v in fields.items() if v is not None})
        rec["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        data["videos"][video_id] = rec
        _save(data)
        return dict(rec)


def list_videos() -> dict:
    with _lock:
        return dict(_load().get("videos", {}))


def set_review(key: str, value) -> None:
    from datetime import datetime, timezone

    with _lock:
        data = _load()
        rev = data.setdefault("review", {})
        if value is None:
            rev.pop(key, None)
        else:
            rev[key] = value
        rev["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        _save(data)


def get_review() -> dict:
    with _lock:
        return dict(_load().get("review", {}))


# ---- Backward-compatible helpers used by older code paths ----


def is_processed(video_id: str) -> bool:
    """Legacy terminal-state check."""
    with _lock:
        return video_id in _load().get("processed", {})


def mark(video_id: str, status: str, title: str = "", note: str = "") -> None:
    """Record a legacy terminal status."""
    with _lock:
        data = _load()
        data.setdefault("processed", {})[video_id] = {
            "status": status,
            "title": title,
            "note": note,
        }
        data.setdefault("videos", {}).setdefault(video_id, {"video_id": video_id})
        data["videos"][video_id]["status"] = status
        if title:
            data["videos"][video_id]["title"] = title
        if note:
            data["videos"][video_id]["note_path"] = note
        _save(data)


def mark_many(video_ids, status: str, note: str = "") -> None:
    if not video_ids:
        return
    with _lock:
        data = _load()
        for vid in video_ids:
            data.setdefault("processed", {})[vid] = {"status": status, "note": note}
            data.setdefault("videos", {}).setdefault(vid, {"video_id": vid})
            data["videos"][vid]["status"] = status
        _save(data)


def stats() -> dict:
    with _lock:
        data = _load()
        processed = data.get("processed", {})
        videos = data.get("videos", {})
    counts: dict[str, int] = {}
    for entry in processed.values():
        s = entry.get("status", "unknown")
        counts[s] = counts.get(s, 0) + 1
    ai = sum(1 for v in videos.values() if v.get("history_class") == "ai")
    non_ai = sum(1 for v in videos.values() if v.get("history_class") == "non-ai")
    return {
        "total": len(processed),
        "by_status": counts,
        "videos": len(videos),
        "ai": ai,
        "non_ai": non_ai,
        "transcribed": sum(1 for v in videos.values() if v.get("transcript_status") == "ok"),
        "summarized": sum(1 for v in videos.values() if v.get("summary_status") == "ok"),
        "reviewed": bool(data.get("review")) if isinstance(data, dict) else False,
    }
