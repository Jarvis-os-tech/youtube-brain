#!/usr/bin/env python3
"""Jarvis yt-brain worker agent.

Exposes the YouTube knowledge base over the Jarvis Agent Bus so the CEO
(Gemini Live / main JARVIS loop) can query video notes, search transcripts,
and trigger pipeline runs.
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add project roots to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core_engine"))
sys.path.insert(0, str(ROOT / "yt_brain"))

from core_engine import AgentBusClient, AgentMessage, MessageType

import index

log = logging.getLogger("jarvis.yt_brain")

TOPIC_SEARCH = "yt-brain.search"
TOPIC_GET = "yt-brain.get"
TOPIC_LIST = "yt-brain.list"
TOPIC_RUN = "yt-brain.run"
TOPIC_REINDEX = "yt-brain.reindex"
TOPIC_TOPICS = "yt-brain.topics"
TOPIC_STATUS = "yt-brain.status"


async def handle_search(client: AgentBusClient, msg: AgentMessage) -> None:
    """Search the KB and reply with results."""
    query = msg.payload.get("query", "")
    limit = msg.payload.get("limit", 10)
    if not query:
        await client.send_task_failed(msg.msg_id, "missing 'query' in payload", target=msg.source)
        return
    results = index.search(query, limit)
    await client.publish(
        msg_type=MessageType.TASK_COMPLETE,
        payload={"results": results, "query": query},
        target=msg.source,
        reply_to=msg.msg_id,
    )


async def handle_get(client: AgentBusClient, msg: AgentMessage) -> None:
    """Return full note content by video_id or path."""
    video_id = msg.payload.get("video_id")
    path = msg.payload.get("path")
    if not video_id and not path:
        await client.send_task_failed(msg.msg_id, "need video_id or path", target=msg.source)
        return
    with index.connect() as conn:
        if video_id:
            rows = conn.execute(
                "SELECT title, url, watched, path, video_id FROM notes WHERE video_id = ?", (video_id,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT title, url, watched, path, video_id FROM notes WHERE path = ?", (path,)
            ).fetchall()
    if not rows:
        await client.send_task_failed(msg.msg_id, "note not found", target=msg.source)
        return
    r = rows[0]
    meta = {"title": r[0], "url": r[1], "watched": r[2], "path": r[3], "video_id": r[4]}
    note_path = Path(r[3])
    content = note_path.read_text(encoding="utf-8") if note_path.exists() else ""
    await client.publish(
        msg_type=MessageType.TASK_COMPLETE,
        payload={"content": content, "meta": meta},
        target=msg.source,
        reply_to=msg.msg_id,
    )


async def handle_list(client: AgentBusClient, msg: AgentMessage) -> None:
    """List recent notes (optionally filtered by date and/or topic)."""
    limit = msg.payload.get("limit", 20)
    date = msg.payload.get("date")  # YYYY-MM-DD
    topic = msg.payload.get("topic")
    notes = index.list_notes(date=date, topic=topic, limit=limit)
    await client.publish(
        msg_type=MessageType.TASK_COMPLETE,
        payload={"notes": notes, "topics": index.list_topics()},
        target=msg.source,
        reply_to=msg.msg_id,
    )


async def handle_topics(client: AgentBusClient, msg: AgentMessage) -> None:
    """Report topic names and note counts, plus where the master index lives."""
    md, js = index.write_master_index()
    await client.publish(
        msg_type=MessageType.TASK_COMPLETE,
        payload={
            "topics": index.list_topics(),
            "master_index_md": str(md),
            "master_index_json": str(js),
        },
        target=msg.source,
        reply_to=msg.msg_id,
    )


async def handle_status(client: AgentBusClient, msg: AgentMessage) -> None:
    """Report KB stats, latest indexed video, and status."""
    with index.connect() as conn:
        total_notes = conn.execute("SELECT count(*) FROM notes").fetchone()[0]
        latest = conn.execute(
            "SELECT title, url, watched, topic FROM notes ORDER BY watched DESC LIMIT 1"
        ).fetchone()
    latest_info = (
        {"title": latest[0], "url": latest[1], "watched": latest[2], "topic": latest[3]}
        if latest
        else None
    )
    await client.publish(
        msg_type=MessageType.TASK_COMPLETE,
        payload={
            "status": "online",
            "total_notes": total_notes,
            "topics": index.list_topics(),
            "latest_note": latest_info,
        },
        target=msg.source,
        reply_to=msg.msg_id,
    )


async def handle_run(client: AgentBusClient, msg: AgentMessage) -> None:
    """Trigger a pipeline run."""
    limit = msg.payload.get("limit", 15)
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "main.py", "--limit", str(limit),
        cwd=ROOT / "yt_brain",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    stdout, _ = await proc.communicate()
    output = stdout.decode(errors="replace") if stdout else ""
    await client.publish(
        msg_type=MessageType.TASK_COMPLETE,
        payload={"exit_code": proc.returncode, "output": output[-2000:]},
        target=msg.source,
        reply_to=msg.msg_id,
    )


async def handle_reindex(client: AgentBusClient, msg: AgentMessage) -> None:
    """Rebuild the FTS5 index."""
    count = index.rebuild()
    await client.publish(
        msg_type=MessageType.TASK_COMPLETE,
        payload={"indexed": count},
        target=msg.source,
        reply_to=msg.msg_id,
    )


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    )

    socket_path = os.environ.get("JARVIS_BUS_SOCKET") or None
    client_kwargs = {"agent_id": "yt-brain", "auto_reconnect": True}
    if socket_path:
        client_kwargs["socket_path"] = socket_path
    async with AgentBusClient(**client_kwargs) as client:
        await client.subscribe(
            [
                TOPIC_SEARCH,
                TOPIC_GET,
                TOPIC_LIST,
                TOPIC_RUN,
                TOPIC_REINDEX,
                TOPIC_TOPICS,
                TOPIC_STATUS,
            ]
        )

        client.on(TOPIC_SEARCH, lambda m: asyncio.create_task(handle_search(client, m)))
        client.on(TOPIC_GET, lambda m: asyncio.create_task(handle_get(client, m)))
        client.on(TOPIC_LIST, lambda m: asyncio.create_task(handle_list(client, m)))
        client.on(TOPIC_RUN, lambda m: asyncio.create_task(handle_run(client, m)))
        client.on(TOPIC_REINDEX, lambda m: asyncio.create_task(handle_reindex(client, m)))
        client.on(TOPIC_TOPICS, lambda m: asyncio.create_task(handle_topics(client, m)))
        client.on(TOPIC_STATUS, lambda m: asyncio.create_task(handle_status(client, m)))

        client.start_heartbeat_loop(interval=15.0)

        log.info("yt-brain worker ready on agent bus")
        try:
            while True:
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    asyncio.run(main())
