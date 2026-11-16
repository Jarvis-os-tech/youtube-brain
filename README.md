# YouTube Brain

YouTube watch history → filtered, transcribed, summarized Markdown notes →
exposed to JARVIS over the agent bus.

```
jarvis-yt-brain/
├── core_engine/          # Jarvis agent bus (broker + client library)
│   └── core_engine/agent_bus.py
├── yt_brain/             # the scraper/pipeline
│   ├── config.py         # paths, relevance criteria, limits
│   ├── state.py          # atomic processed_videos.json — 0-token short circuit
│   ├── ingest.py         # Chrome/Firefox history + userscript buffer → queue
│   ├── prompts.py        # gatekeeper + analyst system prompts
│   ├── agents.py         # the four agents, LLM backend via `opencode run`
│   ├── index.py          # SQLite FTS5 search over kb/
│   ├── main.py           # CLI entry point
│   ├── webhook.py        # loopback receiver for the userscript (:8767)
│   ├── userscript.js     # Tampermonkey — POSTs at 90% watch
│   ├── kb/               # the notes (source of truth)
│   └── run_pipeline.sh
├── systemd/              # unit files (installed to ~/.config/systemd/user/)
└── run/                  # agent bus socket
```

`~/yt-brain` is a symlink to `yt_brain/` so older paths keep working.

## Pipeline

| Agent | Job | LLM cost |
|---|---|---|
| 1 Gatekeeper | `{"is_relevant": bool}` from title alone | ~100 tok |
| 2 Researcher | captions via `youtube-transcript-api` | 0 |
| 3 Analyst | structured Markdown notes (map-reduce over long transcripts) | transcript-length |
| 4 Librarian | write `kb/YYYY-MM-DD-slug.md` + index | 0 |

`processed_videos.json` gates everything: a recorded video ID costs zero tokens
forever. Irrelevant videos are marked at step 1 and never transcribed.

## JARVIS bus API

Socket: `~/jarvis-yt-brain/run/agent_bus.sock` (override with `JARVIS_BUS_SOCKET`).
Worker registers as agent id **`yt-brain`**.

```python
from core_engine import AgentBusClient

async with AgentBusClient(agent_id="ceo") as c:
    r = await c.request("yt-brain.search", {"query": "tmux orchestration"}, timeout=20)
    r.payload["results"]      # [{title, url, watched, path, video_id, snippet}]
```

| Topic | Payload | Reply |
|---|---|---|
| `yt-brain.search` | `{query, limit=10}` | `{results: [...], query}` |
| `yt-brain.get` | `{video_id}` or `{path}` | `{content, meta}` |
| `yt-brain.list` | `{limit=20, date="YYYY-MM-DD"}` | `{notes: [...]}` |
| `yt-brain.run` | `{limit=15}` | `{exit_code, output}` — runs the pipeline now |
| `yt-brain.reindex` | `{}` | `{indexed: n}` |

Replies arrive as `task.complete` with `reply_to` set, or `task.failed` with an
`error` string. Bare search terms are ANDed; pass `OR` explicitly.

## Services

| Unit | Role |
|---|---|
| `jarvis-agent-bus.service` | bus broker |
| `jarvis-yt-brain-worker.service` | exposes the KB on the bus |
| `yt-webhook.service` | userscript receiver on 127.0.0.1:8767 |
| `yt-agents.timer` → `yt-agents.service` | runs the pipeline 5 min after login |

```sh
systemctl --user status jarvis-yt-brain-worker yt-webhook yt-agents.timer
journalctl --user -u yt-agents.service -f
```

## Manual use

```sh
cd ~/jarvis-yt-brain/yt_brain
./run_pipeline.sh --dry-run    # list queue, no LLM calls
./run_pipeline.sh --limit 3    # small batch
./run_pipeline.sh -v           # debug
.venv/bin/python index.py search "vector database"
.venv/bin/python index.py rebuild
```

## Tuning

`config.py` is the knob board:
- `RELEVANCE_CRITERIA` / `RELEVANCE_EXCLUSIONS` — widen the niche
- `MAX_VIDEOS_PER_RUN` (15), `LOOKBACK_HOURS` (30)
- `LLM_COMMAND` (`opencode`) — any `cli -p "prompt"`-shaped backend works

All are overridable by env var (`YT_MAX_VIDEOS`, `YT_LOOKBACK_HOURS`, …).

## Requirements

`cookies.txt` (mode 600) is required — YouTube blocks caption requests from this
workstation's IP:

```sh
yt-dlp --cookies-from-browser chrome --cookies ~/jarvis-yt-brain/yt_brain/cookies.txt \
  --skip-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Without it every transcript fetch raises `IpBlocked`.