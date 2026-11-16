#!/usr/bin/env python3
"""Publish the knowledge base into an Obsidian vault and wire up the graph.

Plain Markdown in `yt_brain/kb/` is the source of truth. This script mirrors it
into `<vault>/youtube/` and rewrites each note so Obsidian's graph view shows a
connected cluster instead of 30 orphans:

  - `[[youtube/<topic>]]`  -> a map-of-content note per topic
  - `[[youtube/index]]`    -> one hub page for the whole KB
  - `[[index]]`            -> back into the main JARVIS vault, so the YouTube
                              cluster is attached to the existing graph and not
                              floating beside it
  - `[[youtube/...]]`      -> related notes, chosen by IDF-weighted keyword
                              overlap so the links mean something
  - `tags: [youtube, youtube/<topic>]` -> for the tag pane and graph colouring

The related-notes block is fenced by sentinel comments and regenerated on every
publish, so re-running is idempotent and hand-written prose below the block
survives.
"""

from __future__ import annotations

import json
import logging
import math
import os
import re
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import index  # noqa: E402
import topics  # noqa: E402

log = logging.getLogger("publish")

VAULT_DIR = Path(
    os.environ.get("YT_VAULT_DIR", "/home/g0pi/Documents/JARVIS Memory")
).expanduser()
SUBFOLDER = "youtube"


def get_target_vaults() -> list[Path]:
    if "YT_VAULT_DIR" in os.environ:
        return [Path(os.environ["YT_VAULT_DIR"]).expanduser()]
    vaults: list[Path] = []
    main_vault = Path("/home/g0pi/Documents/JARVIS Memory")
    if main_vault.exists():
        vaults.append(main_vault)
    local_vault = Path("/home/g0pi/jarvis-yt-brain/vault")
    if local_vault.exists() and local_vault not in vaults:
        vaults.append(local_vault)
    return vaults

# The hub gets a unique, readable filename rather than `index.md`: the vault
# root already has an index.md, and Obsidian cannot disambiguate two notes with
# the same basename, so `[[index]]` from our notes would resolve to the wrong
# one and the other becomes a dead node in the graph.
HUB_NAME = "YouTube Knowledge Base"

BEGIN = "<!-- yt-brain:related -->"
END = "<!-- /yt-brain:related -->"

_TOKEN = re.compile(r"[a-z0-9]+")
_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "on", "with", "is",
    "it", "this", "that", "how", "why", "what", "you", "your", "we", "i", "as",
    "at", "by", "be", "from", "not", "but", "can", "will", "its", "are", "was",
    "new", "use", "using", "does", "do", "my", "me",
}


def tokens(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOP and len(t) > 2]


def front_matter(lines: list[str]) -> tuple[dict, list[str]]:
    """Split front matter into a dict, preserving key order and unknowns."""
    meta: dict[str, str] = {}
    order: list[str] = []
    for line in lines:
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        if key not in order:
            order.append(key)
        meta[key] = value.strip()
    return meta, order


def read_note(path: Path) -> tuple[dict, list[str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, [], text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, [], text
    lines = parts[1].strip().splitlines()
    meta, order = front_matter(lines)
    return meta, order, parts[2]


def render_note(
    meta: dict,
    order: list[str],
    body: str,
    *,
    topic: str,
    video_id: str,
    url: str,
) -> str:
    """Front matter with vault-native properties, then the body."""
    meta = dict(meta)
    meta["type"] = "youtube-note"
    meta["topic"] = topic
    meta["video_id"] = video_id
    meta["source_url"] = url
    meta["tags"] = f"[youtube, youtube/{topic}]"
    if "title" in meta:
        meta["title"] = json.dumps(meta["title"].strip('"'), ensure_ascii=False)

    keys = order + [k for k in ("type", "topic", "video_id", "source_url", "tags") if k not in order]
    lines = [f"{k}: {meta[k]}" for k in dict.fromkeys(keys) if k in meta]
    return "---\n" + "\n".join(lines) + "\n---\n" + body


def strip_block(body: str) -> str:
    start = body.find(BEGIN)
    end = body.find(END)
    if start != -1 and end != -1 and end > start:
        return (body[:start].rstrip() + "\n")
    return body


def core_concept(body: str) -> str:
    m = re.search(r"^##\s*Core Concept\s*\n+(.*?)(?=\n##\s|\Z)", body, re.S | re.M)
    return m.group(1).strip() if m else ""


def related_block(
    *,
    topic: str,
    ranked: list[tuple[str, str, float]],
) -> str:
    """The wikilink block that makes one note a node in the graph.

    `ranked` paths are already vault-root-relative (they come from the note's
    own `path` record), so they must not be prefixed again.
    """
    out = [BEGIN, "", "## Related", ""]
    out.append(f"- [[{SUBFOLDER}/{HUB_NAME}|◻️ YouTube Knowledge Base]]")
    out.append(f"- [[{SUBFOLDER}/{topic}|📁 {topics.label(topic)}]]")
    out.append("- [[index|🏛️ JARVIS Memory Vault]]")
    if ranked:
        out += ["", "### Related notes", ""]
        for title, path, score in ranked:
            safe = title.replace("|", "\\|")
            out.append(f"- [[{path}|{safe}]] · relevance {score:.2f}")
    out += ["", END]
    return "\n".join(out)


def build_related(notes: list[dict]) -> dict[str, list[tuple[str, str, float]]]:
    """IDF-weighted cosine similarity over note tokens, best 4 per note.

    Plain bag-of-words IDF: a term shared by every note (say "ai") carries no
    information, so it must not create links. Deterministic and free, which
    matters because this runs on every pipeline run.
    """
    docs = {n["path"]: Counter(tokens(f"{n['title']} {n['concept']}")) for n in notes}
    n_docs = len(docs) or 1
    df: Counter = Counter()
    for tf in docs.values():
        df.update(tf.keys())

    def weight(term: str) -> float:
        return math.log(1 + n_docs / (1 + df[term]))

    vectors = {
        path: {t: (1 + math.log(c)) * weight(t) for t, c in tf.items()}
        for path, tf in docs.items()
    }
    norms = {
        path: math.sqrt(sum(v * v for v in vec.values())) or 1.0
        for path, vec in vectors.items()
    }

    titles = {n["path"]: n["title"] for n in notes}
    out: dict[str, list[tuple[str, str, float]]] = {}
    for path, vec in vectors.items():
        scores: list[tuple[str, str, float]] = []
        for other, ovec in vectors.items():
            if other == path:
                continue
            shared = set(vec) & set(ovec)
            score = sum(vec[t] * ovec[t] for t in shared) / (norms[path] * norms[other])
            if score > 0.02:
                scores.append((titles[other], other, score))
        scores.sort(key=lambda s: -s[2])
        out[path] = scores[:4]
    return out


def topic_moc(topic: str, notes: list[dict], master: str) -> str:
    """Map-of-content page: one per topic, the hub of its cluster."""
    lines = [
        "---",
        "type: moc",
        f'title: "{topics.label(topic)}"',
        f"tags: [youtube, youtube/{topic}]",
        f"updated_at: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "---",
        "",
        f"# 📁 {topics.label(topic)}",
        "",
        f"{len(notes)} notes in the YouTube knowledge base.",
        "",
        f"Up: [[{SUBFOLDER}/{HUB_NAME}|◻️ YouTube Knowledge Base]] · [[index|🏛️ JARVIS Memory Vault]]",
        "",
        "| Indexed | Note |",
        "|---|---|",
    ]
    for n in sorted(notes, key=lambda x: x["indexed"], reverse=True):
        safe = n["title"].replace("|", "\\|")
        lines.append(f"| {n['indexed'][:10]} | [[{n['path']}\\|{safe}]] |")
    lines += ["", "---", "", f"Machine-readable: `{master}`", ""]
    return "\n".join(lines)


def hub(by_topic: dict[str, list[dict]], master_md: Path, master_json: Path) -> str:
    total = sum(len(v) for v in by_topic.values())
    lines = [
        "---",
        "type: moc",
        'title: "YouTube Knowledge Base"',
        "tags: [youtube, moc]",
        f"updated_at: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "---",
        "",
        "# ◻️ YouTube Knowledge Base",
        "",
        (
            f"{total} notes distilled from YouTube watch history, grouped into "
            f"{len(by_topic)} topics. Refreshed hourly by the `yt-agents` timer."
        ),
        "",
        "Up: [[index|🏛️ JARVIS Memory Vault]]",
        "",
        "## Topics",
        "",
    ]
    for topic, notes in sorted(by_topic.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        lines.append(f"- [[{SUBFOLDER}/{topic}|{topics.label(topic)}]] ({len(notes)})")
    lines += ["", "## All notes", ""]
    for topic, notes in sorted(by_topic.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        lines += [f"### {topics.label(topic)}", ""]
        for n in sorted(notes, key=lambda x: x["indexed"], reverse=True):
            safe = n["title"].replace("|", "\\|")
            lines.append(f"- [[{n['path']}|{safe}]] · {n['indexed'][:10]}")
        lines.append("")
    lines += [
        "---",
        "",
        f"Generated index: `{master_md.name}`, `{master_json.name}`",
        "",
    ]
    return "\n".join(lines)


def collect() -> list[dict]:
    """Read every note from the KB and build the records used for linking."""
    records = []
    for path in index.kb_files():
        meta, order, body = read_note(path)
        rel = index._relative(str(path))
        # Wikilinks drop the .md extension: Obsidian's convention, and it keeps
        # the graph from showing a rename as a delete plus a create.
        vault_path = f"{SUBFOLDER}/{rel.removesuffix('.md')}"
        topic = meta.get("topic") or index.note_topic(meta, path)
        records.append(
            {
                "src": path,
                "path": vault_path,
                "title": (meta.get("title") or path.stem).strip('"'),
                "url": meta.get("url", ""),
                "video_id": meta.get("video_id", ""),
                "watched": meta.get("watched", ""),
                "indexed": meta.get("indexed", ""),
                "topic": topic,
                "concept": core_concept(body),
                "meta": meta,
                "order": order,
                "body": body,
            }
        )
    return records


def update_dashboard_link(vault_dir: Path) -> None:
    home_file = vault_dir / "00 HOME.md"
    if not home_file.exists():
        return
    text = home_file.read_text(encoding="utf-8")
    if "YouTube Knowledge Base" in text or "YouTube Brain" in text:
        return
    nav_marker = "| [[Knowledge/INDEX|🧠 Knowledge Ledger]] | Structured projects, decisions, tasks, and durable facts | `58 Items Recorded` |"
    if nav_marker in text:
        replacement = (
            nav_marker
            + "\n| [[youtube/YouTube Knowledge Base|📺 YouTube Brain]] | Transcripts, deep notes, key takeaways & topics from watched videos | `Active & Synced` |"
        )
        home_file.write_text(text.replace(nav_marker, replacement), encoding="utf-8")
        log.info("added YouTube Brain navigation link to %s", home_file)


def _publish_to_vault(
    target_vault: Path,
    records: list[dict],
    related: dict,
    by_topic: dict,
    master_md: Path,
    master_json: Path,
) -> None:
    root = target_vault / SUBFOLDER
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)

    for r in records:
        dest = target_vault / f"{r['path']}.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        ranked = list(related.get(r["path"], []))
        block = related_block(topic=r["topic"], ranked=ranked)
        front = render_note(
            r["meta"],
            r["order"],
            r["body"],
            topic=r["topic"],
            video_id=r["video_id"],
            url=r["url"],
        )
        dest.write_text(f"{front.rstrip()}\n{block}\n", encoding="utf-8")

    for topic, notes in by_topic.items():
        (root / f"{topic}.md").write_text(
            topic_moc(topic, notes, master_json.name), encoding="utf-8"
        )

    (root / f"{HUB_NAME}.md").write_text(
        hub(by_topic, master_md, master_json), encoding="utf-8"
    )

    graph = target_vault / ".obsidian" / "graph.json"
    if graph.exists():
        try:
            cfg = json.loads(graph.read_text(encoding="utf-8"))
            cfg["showTags"] = True
            groups = {(g.get("query") or "") for g in cfg.get("colorGroups", [])}
            palette = [
                "#8b5cf6", "#06b6d4", "#22c55e", "#f59e0b", "#ec4899", "#3b82f6",
                "#ef4444", "#14b8a6", "#a855f7", "#84cc16",
            ]
            for i, topic in enumerate(sorted(by_topic)):
                query = f"tag:#youtube/{topic}"
                if query in groups:
                    continue
                cfg.setdefault("colorGroups", []).append(
                    {"query": query, "color": {"a": 1, "rgb": int(palette[i % len(palette)][1:], 16)}}
                )
            graph.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
        except Exception as e:
            log.warning("could not update obsidian graph config for %s: %s", target_vault, e)

    update_dashboard_link(target_vault)


def publish() -> int:
    target_vaults = get_target_vaults()
    if not target_vaults:
        log.error("no valid vault directory found (set YT_VAULT_DIR)")
        return 0

    records = collect()
    if not records:
        log.warning("no notes to publish")
        return 0

    # Regenerate the machine-readable index first so the vault can link to it.
    master_md, master_json = index.write_master_index()
    related = build_related(records)

    by_topic: dict[str, list[dict]] = {}
    for r in records:
        r["body"] = strip_block(r["body"]).rstrip()
        by_topic.setdefault(r["topic"], []).append(r)

    total_published = 0
    for vault in target_vaults:
        if not vault.exists():
            log.warning("vault path does not exist: %s", vault)
            continue
        _publish_to_vault(vault, records, related, by_topic, master_md, master_json)
        total_published += len(records)
        log.info("published %d notes into %s/%s", len(records), vault, SUBFOLDER)

    linked = sum(1 + len(related.get(r["path"], [])) for r in records)
    log.info(
        "published across %d vaults (%d notes, %d topics, %d graph edges)",
        len(target_vaults),
        len(records),
        len(by_topic),
        linked,
    )
    return total_published


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    publish()
