"""SQLite FTS5 index over the knowledge base.

Plain Markdown in yt_brain/kb stays the source of truth; this index exists
only so the assistant can search fast. Every file in kb/ is greppable without
this database.
"""

from __future__ import annotations

import json
import logging
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import config
import topics

log = logging.getLogger(__name__)

_DB = config.BASE / "kb.sqlite"
MASTER_JSON = config.KB_DIR / "master_index.json"
MASTER_MD = config.KB_DIR / "master_index.md"

# Standalone (not external-content) FTS5: simpler to keep correct, and the KB
# is small enough that the duplication costs nothing.
_SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    video_id   TEXT PRIMARY KEY,
    title      TEXT NOT NULL,
    url        TEXT,
    watched    TEXT,
    source     TEXT,
    path       TEXT NOT NULL,
    topic      TEXT,
    indexed_at TEXT
);
CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
    video_id, title, body, path UNINDEXED
);
"""

_FIELDS = re.compile(
    r'^(?P<key>video_id|title|url|watched|source|topic|indexed):\s*(?P<value>.*?)\s*$',
    re.MULTILINE,
)


def connect() -> sqlite3.Connection:
    config.KB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(_DB)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(_SCHEMA)
    _migrate(conn)
    return conn


def _migrate(conn: sqlite3.Connection) -> None:
    """Add columns introduced after a database was first created.

    `CREATE TABLE IF NOT EXISTS` silently keeps an old schema, so a KB built by
    a previous version would blow up on INSERT without this.
    """
    have = {row[1] for row in conn.execute("PRAGMA table_info(notes)")}
    if "topic" not in have:
        conn.execute("ALTER TABLE notes ADD COLUMN topic TEXT")
        conn.commit()
        log.info("migrated notes table: added topic column")


def _parse_note(text: str) -> dict:
    """Split YAML front matter from the body."""
    meta: dict = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            head, body = parts[1], parts[2]
            for m in _FIELDS.finditer(head):
                value = m.group("value")
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                meta[m.group("key")] = value
    if not meta.get("title"):
        h1 = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        meta["title"] = h1.group(1).strip() if h1 else "untitled"
    return {"meta": meta, "body": body.strip()}


def _relative(path_str: str) -> str:
    """Path relative to the KB root, tolerating rows already stored relative.

    `relative_to` raises on a path that is not under KB_DIR, which turns one
    odd row into a dead master index for the whole KB.
    """
    path = Path(path_str)
    try:
        return str(path.relative_to(config.KB_DIR))
    except ValueError:
        return str(path)


def note_topic(meta: dict, path: Path) -> str:
    """Topic for a note: front matter first, then the folder, then classify."""
    topic = (meta.get("topic") or "").strip()
    if topic:
        return topic
    parent = path.parent.name
    if parent and parent != config.KB_DIR.name:
        return parent
    return topics.classify(meta.get("title", ""))


def _upsert(conn: sqlite3.Connection, path: Path, fallback_id: str) -> None:
    text = path.read_text(encoding="utf-8")
    parsed = _parse_note(text)
    meta = parsed["meta"]
    video_id = meta.get("video_id") or fallback_id

    conn.execute("DELETE FROM notes_fts WHERE path = ?", (str(path),))
    conn.execute("DELETE FROM notes WHERE path = ?", (str(path),))
    conn.execute(
        "INSERT INTO notes (video_id, title, url, watched, source, path, topic, indexed_at)"
        " VALUES (?,?,?,?,?,?,?,?)",
        (
            video_id,
            meta.get("title", "untitled"),
            meta.get("url", ""),
            meta.get("watched", ""),
            meta.get("source", ""),
            str(path),
            note_topic(meta, path),
            # Trust the note's own `indexed:` stamp. Using now() here made
            # every rebuild relabel the whole KB with today's date.
            meta.get("indexed") or datetime.now(timezone.utc).isoformat(
                timespec="seconds"
            ),
        ),
    )
    conn.execute(
        "INSERT INTO notes_fts (video_id, title, body, path) VALUES (?,?,?,?)",
        (video_id, meta.get("title", "untitled"), parsed["body"], str(path)),
    )


def index_note(path: Path, record=None) -> None:
    with connect() as conn:
        _upsert(conn, path, record.video_id if record else path.stem)


def find_note_path(video_id: str) -> Path | None:
    """Path of an existing note for this video, if the KB already has one."""
    with connect() as conn:
        row = conn.execute(
            "SELECT path FROM notes WHERE video_id = ?", (video_id,)
        ).fetchone()
    return Path(row[0]) if row else None


def rebuild() -> int:
    with connect() as conn:
        conn.execute("DELETE FROM notes")
        conn.execute("DELETE FROM notes_fts")
        for path in sorted(kb_files()):
            _upsert(conn, path, path.stem)
        count = conn.execute("SELECT count(*) FROM notes").fetchone()[0]
    write_master_index()
    log.info("reindexed %d notes", count)
    return count


def kb_files() -> list[Path]:
    """Every note in the KB, topic subfolders included.

    `master_index.*` live at the KB root and are not notes, so they are
    excluded here to keep them out of the FTS index.
    """
    return sorted(
        p for p in config.KB_DIR.rglob("*.md") if p.name not in _MASTER_NAMES
    )


_MASTER_NAMES = {MASTER_JSON.name, MASTER_MD.name}


def list_notes(
    date: str | None = None, topic: str | None = None, limit: int = 20
) -> list[dict]:
    """Newest-first note metadata, optionally filtered by date and topic.

    Lists from the notes table, not FTS: FTS5 has no "match everything"
    expression, and the ordering here is by index date rather than relevance.

    Ordering is by indexed_at so "newest" means newest capture, which is what
    the caller wants after the date prefix moved from watch date to index date.
    """
    clauses: list[str] = []
    params: list[object] = []
    if date:
        clauses.append("path LIKE ?")
        params.append(f"%{date}-%")
    if topic:
        clauses.append("topic = ?")
        params.append(topic)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""

    sql = (
        "SELECT title, url, watched, path, video_id, topic FROM notes "
        f"{where} ORDER BY indexed_at DESC, path DESC LIMIT ?"
    )
    with connect() as conn:
        rows = conn.execute(sql, (*params, limit)).fetchall()
    return [
        {
            "title": r[0],
            "url": r[1],
            "watched": r[2],
            "path": r[3],
            "video_id": r[4],
            "topic": r[5],
        }
        for r in rows
    ]


def list_topics() -> dict[str, int]:
    """Note count per topic, for the worker and the README."""
    with connect() as conn:
        rows = conn.execute(
            "SELECT topic, count(*) FROM notes GROUP BY topic ORDER BY count(*) DESC"
        ).fetchall()
    return {r[0] or topics.DEFAULT_TOPIC: r[1] for r in rows}


def write_master_index() -> tuple[Path, Path]:
    """Regenerate `kb/master_index.md` and `kb/master_index.json`.

    One file to read instead of N. Rebuilt from the notes table after every
    pipeline run, so it never drifts from what search actually returns.
    """
    with connect() as conn:
        rows = conn.execute(
            "SELECT video_id, title, url, watched, source, path, topic, indexed_at "
            "FROM notes ORDER BY indexed_at DESC, title"
        ).fetchall()

    # Column order must match the SELECT above.
    entries = [
        {
            "video_id": r[0],
            "title": r[1],
            "url": r[2],
            "watched": r[3],
            "source": r[4],
            "path": _relative(r[5]),
            "topic": r[6] or topics.DEFAULT_TOPIC,
            "indexed": r[7],
        }
        for r in rows
    ]

    by_topic: dict[str, list[dict]] = {}
    for e in entries:
        by_topic.setdefault(e["topic"], []).append(e)

    payload = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_notes": len(entries),
        "topics": sorted(by_topic),
        "notes": entries,
    }
    MASTER_JSON.parent.mkdir(parents=True, exist_ok=True)
    MASTER_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# yt-brain Knowledge Base Index",
        "",
        f"Generated {payload['generated']} - {len(entries)} notes across "
        f"{len(by_topic)} topics.",
        "",
        "## Topics",
        "",
    ]
    for topic, items in sorted(by_topic.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        lines.append(f"- **{topic}** ({len(items)})")
    lines += ["", "## Notes", ""]
    for topic, items in sorted(by_topic.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        lines += [f"### {topic}", "", "| Indexed | Title | File |", "|---|---|---|"]
        for e in items:
            title = e["title"].replace("|", "\\|")
            lines.append(f"| {e['indexed'][:10]} | [{title}]({e['url']}) | `{e['path']}` |")
        lines.append("")

    MASTER_MD.write_text("\n".join(lines), encoding="utf-8")
    log.info("wrote master index: %d notes, %d topics", len(entries), len(by_topic))
    return MASTER_MD, MASTER_JSON


def _fts_term(token: str) -> str:
    """Quote one query token so FTS5 reads it as a word, not as syntax.

    Bare words join with AND. A hyphen is FTS5's NOT operator, so `fine-tuning`
    parsed as `fine NOT tuning` and matched nothing -- silently, because the
    failure surfaces as an OperationalError on an unrelated column. Quote any
    token containing punctuation.
    """
    if any(ch in token for ch in ' -"()'):
        return '"' + token.replace('"', '""') + '"'
    return token


def search(query: str, limit: int = 10) -> list[dict]:
    """Keyword search. `query` is an FTS5 MATCH expression.

    Bare words are joined with AND; use `OR` / `NEAR` explicitly if you want
    them.
    """
    terms = " ".join(_fts_term(t) for t in query.split() if t)
    if not terms:
        return []
    with connect() as conn:
        try:
            rows = conn.execute(
                """
                SELECT n.title, n.url, n.watched, n.path, n.video_id,
                       snippet(notes_fts, 2, '[', ']', ' … ', 24) AS frag
                FROM notes_fts
                JOIN notes n ON n.path = notes_fts.path
                WHERE notes_fts MATCH ?
                ORDER BY bm25(notes_fts)
                LIMIT ?
                """,
                (terms, limit),
            ).fetchall()
        except sqlite3.OperationalError as exc:
            log.error("bad FTS query %r: %s", query, exc)
            return []
    return [
        {"title": r[0], "url": r[1], "watched": r[2], "path": r[3], "video_id": r[4], "snippet": r[5]}
        for r in rows
    ]


if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    args = sys.argv[1:]
    cmd = args[0] if args else ""
    if cmd == "rebuild":
        rebuild()
    elif cmd == "master":
        md, js = write_master_index()
        print(f"wrote {md} and {js}")
    elif cmd == "topics":
        for name, count in list_topics().items():
            print(f"{count:4d}  {name}")
    elif cmd == "list":
        rest = args[1:]
        topic = None
        if rest and rest[0].startswith("topic="):
            topic = rest.pop(0).split("=", 1)[1]
        for n in list_notes(date=(rest[0] if rest else None), topic=topic, limit=50):
            print(f"[{n['topic']}] {n['title']}\n  {n['path']}")
    elif cmd == "search":
        hits = search(" ".join(args[1:]))
        if not hits:
            print("no matches")
        for h in hits:
            print(f"\n{h['title']}\n  {h['path']}\n  {h['snippet']}")
    else:
        print(
            "usage: index.py rebuild | master | topics | list [YYYY-MM-DD] [topic=NAME]"
            " | search <terms>"
        )
