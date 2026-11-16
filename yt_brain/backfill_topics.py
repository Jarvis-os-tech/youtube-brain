#!/usr/bin/env python3
"""One-off migration: file the existing flat KB into topic subfolders.

Three things change for every note that already exists:

  1. `kb/2026-10-03-slug.md` -> `kb/<topic>/<index-date>-slug.md`, so the flat
     folder stops being the only place a note can live.
  2. The date prefix becomes the note's original `indexed:` date instead of its
     `watched:` date. Notes written before the change carry a watch-date prefix
     that put them a day behind reality.
  3. A `topic:` line is added to the front matter so the classification is
     visible in the file itself, not just implied by the folder.

Idempotent: a note already in a topic folder with a `topic:` front-matter line
is left alone. `--dry-run` prints the plan and touches nothing.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config  # noqa: E402
import index  # noqa: E402
import topics  # noqa: E402

log = logging.getLogger("backfill_topics")

_DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})-")


def front_matter_parts(text: str) -> tuple[list[str], str]:
    """Split a note into its front-matter lines and its body."""
    if not text.startswith("---"):
        return [], text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return [], text
    return parts[1].strip().splitlines(), parts[2]


def field(lines: list[str], key: str) -> str:
    prefix = f"{key}:"
    for line in lines:
        if line.startswith(prefix):
            return line[len(prefix) :].strip().strip('"')
    return ""


def index_date(lines: list[str], path: Path) -> str:
    """Prefer the recorded index timestamp; fall back to the file mtime.

    File mtime is the honest answer for the note's capture time and is always
    available, whereas `indexed:` may be missing on a hand-edited note.
    """
    stamp = field(lines, "indexed")
    if stamp:
        try:
            from datetime import datetime

            return datetime.fromisoformat(stamp).astimezone().strftime("%Y-%m-%d")
        except ValueError:
            pass
    from datetime import datetime

    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")


def migrate(path: Path, dry_run: bool) -> tuple[str, str, Path] | None:
    """Return (old_rel, new_rel, topic) for a note that needs moving."""
    text = path.read_text(encoding="utf-8")
    lines, body = front_matter_parts(text)

    if path.parent != config.KB_DIR and field(lines, "topic"):
        return None  # already migrated

    title = field(lines, "title")
    if not title:
        h1 = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        title = h1.group(1).strip() if h1 else path.stem

    topic = field(lines, "topic") or topics.classify(title, body)
    date = index_date(lines, path)
    slug = _DATE_PREFIX.sub("", path.name)
    dest = config.KB_DIR / topic / f"{date}-{slug}"

    if dest == path:
        return None

    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        new_lines = [ln for ln in lines if not ln.startswith("topic:")]
        new_lines.append(f"topic: {topic}")
        dest.write_text(
            f"---\n" + "\n".join(new_lines) + f"\n---\n{body}", encoding="utf-8"
        )
        path.unlink()

    return (
        str(path.relative_to(config.KB_DIR)),
        str(dest.relative_to(config.KB_DIR)),
        topic,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    handlers = [logging.FileHandler(config.BATCH_LOG, encoding="utf-8")]
    logging.getLogger().handlers = handlers

    # Every .md under kb/ except the generated master index.
    paths = [
        p
        for p in sorted(config.KB_DIR.rglob("*.md"))
        if p.name not in {index.MASTER_MD.name}
    ]

    moved = 0
    for path in paths:
        result = migrate(path, args.dry_run)
        if result is None:
            continue
        old, new, topic = result
        moved += 1
        print(f"[{topic}] {old} -> {new}")

    print(f"\n{moved} note(s) {'would move' if args.dry_run else 'moved'}")

    if not args.dry_run:
        # Prune topic folders left empty by the move.
        for folder in sorted(config.KB_DIR.iterdir()):
            if folder.is_dir() and not any(folder.iterdir()):
                folder.rmdir()
                print(f"removed empty folder {folder.name}/")
        count = index.rebuild()
        md, js = index.write_master_index()
        print(f"reindexed {count} notes; wrote {md.name} and {js.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())