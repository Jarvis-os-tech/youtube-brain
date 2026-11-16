"""Dual ingestion: Chrome/Firefox history databases plus the userscript buffer.

Both sources emit the same `WatchRecord`, and the merge is deduplicated by video
ID keeping the most recent watch timestamp.
"""

from __future__ import annotations

import json
import logging
import re
import shutil
import sqlite3
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import config

log = logging.getLogger(__name__)

# Chrome stores time as microseconds since 1601-01-01 (WebKit epoch).
_CHROME_EPOCH_OFFSET = 11_644_473_600

_VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
_TITLE_NOISE_RE = re.compile(r"\s*-\s*YouTube(\s*\(.*?\))?\s*$", re.IGNORECASE)
_LEADING_COUNT_RE = re.compile(r"^\(\d+\)\s*")


@dataclass
class WatchRecord:
    video_id: str
    title: str
    url: str
    watched_at: datetime
    source: str
    duration_s: int | None = None
    meta: dict = field(default_factory=dict)

    @property
    def slug_title(self) -> str:
        return clean_title(self.title)


def clean_title(title: str) -> str:
    """Strip YouTube's '(2) ' prefix and ' - YouTube' suffix."""
    title = _LEADING_COUNT_RE.sub("", title or "").strip()
    title = _TITLE_NOISE_RE.sub("", title).strip()
    return title or "untitled"


def video_id_from_url(url: str) -> str | None:
    try:
        parsed = urlparse(url)
    except ValueError:
        return None
    if "youtube.com" not in parsed.netloc and "youtu.be" not in parsed.netloc:
        return None
    qs = parse_qs(parsed.query)
    candidates = qs.get("v") or []
    if candidates:
        vid = candidates[0]
        return vid if _VIDEO_ID_RE.match(vid) else None
    if parsed.netloc == "youtu.be":
        vid = parsed.path.lstrip("/")
        return vid if _VIDEO_ID_RE.match(vid) else None
    return None


def _acceptable(url: str) -> bool:
    if config.URL_ALLOW not in url:
        return False
    return not any(bad in url for bad in config.URL_DENY_SUBSTRINGS)


# --- Source A: browser history databases -------------------------------------


def _chrome_profiles() -> list[Path]:
    paths: list[Path] = []
    for pattern in config.BROWSER_HISTORY_GLOBS:
        if any(ch in pattern for ch in "*?["):
            # Split at the last wildcard so the parent is the real directory
            # (~/.config/google-chrome), not one containing '*'.
            base = re.split(r"[*?\[]", pattern, maxsplit=1)[0]
            patterns = pattern.split(base, 1)[1]
            paths.extend(sorted(Path(base).expanduser().glob(patterns)))
        else:
            paths.append(Path(pattern).expanduser())
    return sorted({p for p in paths if p.is_file()})


def _query_chrome(db: Path, since_ts: int) -> list[tuple[str, str, int, int]]:
    """Return (url, title, last_visit_us, visit_count) for recent YouTube pages."""
    try:
        conn = sqlite3.connect(f"file:{db}?immutable=1", uri=True)
    except sqlite3.Error as exc:
        log.warning("cannot open %s: %s", db, exc)
        return []
    try:
        # `visits` is the authoritative watch log: `urls` only keeps the last
        # visit, so watching 5 videos in a day collapses to 1 row.
        rows = conn.execute(
            """
            SELECT u.url, u.title, v.visit_time, u.visit_count
            FROM visits v
            JOIN urls u ON u.id = v.url
            WHERE v.visit_time >= ?
              AND u.url LIKE '%youtube.com%'
            ORDER BY v.visit_time DESC
            """,
            (since_ts,),
        ).fetchall()
    except sqlite3.Error as exc:
        log.warning("query failed on %s: %s", db, exc)
        return []
    finally:
        conn.close()
    return rows


def _firefox_profiles() -> list[Path]:
    root = config.FIREFOX_PROFILES
    if not root.is_dir():
        return []
    return [p / "places.sqlite" for p in sorted(root.iterdir()) if (p / "places.sqlite").is_file()]


def _query_firefox(db: Path, since_ts: int) -> list[tuple[str, str, int, int]]:
    try:
        conn = sqlite3.connect(f"file:{db}?immutable=1", uri=True)
    except sqlite3.Error as exc:
        log.warning("cannot open %s: %s", db, exc)
        return []
    try:
        rows = conn.execute(
            """
            SELECT moz_places.url, moz_places.title, moz_historyvisits.visit_date, 1
            FROM moz_historyvisits
            JOIN moz_places ON moz_places.id = moz_historyvisits.place_id
            WHERE moz_historyvisits.visit_date >= ?
              AND moz_places.url LIKE '%youtube.com%'
            ORDER BY moz_historyvisits.visit_date DESC
            """,
            (since_ts,),
        ).fetchall()
    except sqlite3.Error as exc:
        log.warning("query failed on %s: %s", db, exc)
        return []
    finally:
        conn.close()
    return rows


def _visit_to_datetime(raw: int, chrome: bool) -> datetime:
    seconds = (raw / 1_000_000 - _CHROME_EPOCH_OFFSET) if chrome else (raw / 1_000_000)
    return datetime.fromtimestamp(seconds)


def read_browser_history() -> list[WatchRecord]:
    """Open every browser history DB read-only. No copying needed on Linux —
    the immutable=1 flag gives a lock-free snapshot and the source file is
    never modified."""
    cutoff_time = time.time() - config.LOOKBACK_HOURS * 3600
    since_chrome = int((cutoff_time + _CHROME_EPOCH_OFFSET) * 1_000_000)
    since_firefox = int(cutoff_time * 1_000_000)
    records: list[WatchRecord] = []
    db_label = {}

    for db in _chrome_profiles():
        db_label[db] = True
        for url, title, visit_time, _count in _query_chrome(db, since_chrome):
            vid = video_id_from_url(url) if _acceptable(url) else None
            if not vid:
                continue
            records.append(
                WatchRecord(
                    video_id=vid,
                    title=clean_title(title),
                    url=url,
                    watched_at=_visit_to_datetime(visit_time, chrome=True),
                    source=f"chrome:{db.parent.name}",
                )
            )

    for db in _firefox_profiles():
        db_label[db] = False
        for url, title, visit_time, _count in _query_firefox(db, since_firefox):
            vid = video_id_from_url(url) if _acceptable(url) else None
            if not vid:
                continue
            records.append(
                WatchRecord(
                    video_id=vid,
                    title=clean_title(title),
                    url=url,
                    watched_at=_visit_to_datetime(visit_time, chrome=False),
                    source=f"firefox:{db.parent.name}",
                )
            )

    if not db_label:
        log.warning("no browser history database found in %s", config.BROWSER_HISTORY_GLOBS)
    return records


# --- Source B: userscript buffer ---------------------------------------------

_TITLE_UNESCAPE = {"&amp;": "&", "&quot;": '"', "&#39;": "'", "&lt;": "<", "&gt;": ">"}


def read_buffer() -> list[WatchRecord]:
    """Parse the newline-delimited JSON log written by userscript.js."""
    path = config.BUFFER_FILE
    if not path.is_file():
        return []
    records: list[WatchRecord] = []
    try:
        raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        log.warning("cannot read buffer %s: %s", path, exc)
        return []

    for line in raw_lines:
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            log.debug("skipping malformed buffer line")
            continue
        url = payload.get("url", "")
        if not _acceptable(url):
            continue
        vid = payload.get("video_id") or video_id_from_url(url)
        if not vid:
            continue
        title = payload.get("title") or "untitled"
        for esc, ch in _TITLE_UNESCAPE.items():
            title = title.replace(esc, ch)
        watched = None
        if payload.get("timestamp"):
            try:
                watched = datetime.fromtimestamp(float(payload["timestamp"]))
            except (TypeError, ValueError):
                watched = None
        records.append(
            WatchRecord(
                video_id=vid,
                title=clean_title(title),
                url=url,
                watched_at=watched or datetime.now(),
                source="buffer",
                duration_s=payload.get("duration"),
            )
        )
    return records


def clear_buffer() -> None:
    """Truncate the buffer only after a successful run (see main.py)."""
    try:
        config.BUFFER_FILE.write_text("", encoding="utf-8")
    except OSError as exc:
        log.warning("could not clear buffer: %s", exc)


def build_queue() -> list[WatchRecord]:
    """Merge both sources, newest first, one record per video ID."""
    merged: dict[str, WatchRecord] = {}
    for rec in read_browser_history() + read_buffer():
        existing = merged.get(rec.video_id)
        if existing is None or rec.watched_at > existing.watched_at:
            merged[rec.video_id] = rec
    queue = sorted(merged.values(), key=lambda r: r.watched_at, reverse=True)
    log.info("queue: %d unique videos from browser history + buffer", len(queue))
    return queue
