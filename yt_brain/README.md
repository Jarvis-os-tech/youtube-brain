# yt-brain

Daily YouTube watch history → filtered, transcribed, summarized notes in a local
Markdown knowledge base. Batch process, runs once a day, exits.

## How it works

Two independent capture sources feed one deduplicated queue:

- **Chrome/Firefox history** — read-only, lock-free via SQLite `immutable=1`.
  Uses the `visits` table, not `urls`, so watching five videos in a day yields
  five rows instead of one.
- **Userscript webhook** — Tampermonkey posts to `127.0.0.1:8767` when a video
  crosses 90% watched. Higher precision than history rows, which include stray
  clicks.

Each un-processed video then runs through four agents:

| Agent | Job | LLM cost |
|---|---|---|
| 1 Gatekeeper | Classify relevance, output `{"is_relevant": bool}` | ~100 tokens |
| 2 Researcher | Pull captions via `youtube-transcript-api` | 0 |
| 3 Analyst | Structured Markdown study notes | transcript-length |
| 4 Librarian | Write `kb/<topic>/YYYY-MM-DD-slug.md` + FTS5 index | 0 |

Agents 1 and 3 short-circuit: irrelevant videos are marked and never reach the
transcript or summary stage.

## Files

```
config.py      paths, relevance criteria, limits, env overrides
state.py       atomic processed_videos.json — the 0-token short circuit
ingest.py      Chrome/Firefox history + userscript buffer -> one queue
prompts.py     gatekeeper and analyst system prompts
agents.py      the four agents + LLM backend (opencode run)
topics.py     keyword topic classifier -> kb/<topic>/ folders
index.py       SQLite FTS5 search + master index over kb/
publish.py     mirror kb/ into the Obsidian vault with graph wikilinks
main.py        CLI entry point
backfill_topics.py  one-off migration into topic folders
webhook.py     loopback receiver for the userscript
userscript.js  Tampermonkey payload buffer
```

## Setup

### 1. Cookies (required)

YouTube blocks caption requests from this workstation's IP. Export your
logged-in cookies once:

```sh
yt-dlp --cookies-from-browser chrome --cookies ~/yt-brain/cookies.txt \
  --skip-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
chmod 600 ~/yt-brain/cookies.txt
```

Without this, every transcript fetch fails with `IpBlocked` and the pipeline
marks videos `no_transcript`. Cookies are never sent anywhere except
`youtube.com`.

### 2. Userscript (optional, improves signal)

Install `userscript.js` in Tampermonkey and make sure the webhook runs:

```sh
systemctl --user enable --now yt-webhook.service
```

If the webhook is down, the script buffers to `localStorage` and flushes on the
next page load.

### 3. Daily timer

```sh
cp ~/yt-brain/yt-agents.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now yt-agents.timer
systemctl --user list-timers yt-agents.timer
```

Runs at 22:00 with a 10-minute random offset, catches up after suspend.

## Usage

```sh
cd ~/yt-brain

./run_pipeline.sh                  # full run, up to MAX_VIDEOS_PER_RUN
./run_pipeline.sh --dry-run        # show the queue, call no LLM
./run_pipeline.sh --limit 2        # small batch while tuning
./run_pipeline.sh -v               # debug logging

.venv/bin/python index.py search "vector database"   # query the KB
.venv/bin/python index.py rebuild                   # reindex after editing notes
```

## Notes layout

Notes are filed as `kb/<topic>/YYYY-MM-DD-slug.md`. The date prefix is the
**index** date, not the watch date: a video watched at 23:50 is normally
summarized hours later, and watch-date prefixes made every note look like it
belonged to the day before it was captured.

Topics are assigned by `topics.py`, a zero-token keyword scorer — title hits
count 3x body hits, and the highest-scoring topic wins. Current topics:
`agents`, `ml-training`, `llm-core`, `linux-infra`, `security`, `dev-craft`,
and `general` as the fallback.

Every note carries a `topic:` line in its front matter, so the classification is
visible in the file and not only implied by its folder.

## Searching from your assistant

`kb/**/*.md` is plain Markdown — greppable directly. `index.py search` adds
FTS5 ranking and snippets:

```sh
.venv/bin/python index.py search "tmux OR sandbox"
```

Terms are ANDed by default; pass `OR` explicitly for broader recall. Tokens
containing punctuation (`fine-tuning`, `multi-agent`) are quoted automatically,
since FTS5 would otherwise read the hyphen as NOT and silently match nothing.

Other subcommands:

```sh
.venv/bin/python index.py rebuild          # reindex every note from disk
.venv/bin/python index.py topics           # topic -> note count
.venv/bin/python index.py list             # newest notes
.venv/bin/python index.py list topic=agents
.venv/bin/python index.py master           # regenerate master_index.{md,json}
```

`kb/master_index.md` and `kb/master_index.json` are regenerated at the end of
every pipeline run, so a single file lists every note grouped by topic without
opening 30 separate ones.

## Tuning

Edit `config.py`:

- `RELEVANCE_CRITERIA` / `RELEVANCE_EXCLUSIONS` — widen the niche. This is the
  main knob as your interests grow.
- `MAX_VIDEOS_PER_RUN` (default 15) — daily spend ceiling.
- `LOOKBACK_HOURS` (default 30) — wider window catches days you were offline.
- `MAX_TRANSCRIPT_CHARS` / `CHARS_PER_SUMMARY_CHARS` — long videos map-reduce
  above `CHARS_PER_SUMMARY_CHUNK`.
- `LLM_COMMAND` — swap the backend (`opencode` by default; any
  `llm -p "prompt"`-shaped CLI works).

Every value is also an env var (`YT_MAX_VIDEOS`, `YT_LOOKBACK_HOURS`, …).

## Cost model

`processed_videos.json` gates everything. A video already recorded costs zero
tokens forever. A typical day is 10–30 new history rows, of which the gatekeeper
rejects most at ~100 tokens each; only survivors pay for a transcript summary.

## Troubleshooting

| Symptom | Cause |
|---|---|
| `IpBlocked` on every video | cookies missing or expired — redo step 1 |
| `empty output` from LLM | `opencode run` needs auth; run `opencode run "hi"` |
| Timer runs but log is empty | `journalctl --user -u yt-agents.service` |
| Notes exist, search finds nothing | `index.py rebuild` |
| Nothing new every day | raise `LOOKBACK_HOURS`, or your browser isn't Chrome |

Logs: `logs/pipeline.log` (batch), `logs/webhook.log` (webhook).

## Obsidian vault

`publish.py` mirrors the KB into an Obsidian vault at `youtube/` and wires the
graph view so the notes are a connected cluster rather than 30 orphans. It runs
automatically at the end of every pipeline run.

```sh
.venv/bin/python publish.py          # publish now
YT_VAULT_DIR=/path/to/vault .venv/bin/python publish.py   # different vault
```

Default vault: `/home/g0pi/jarvis-yt-brain/vault` (override with `YT_VAULT_DIR`). The pipeline's systemd unit whitelists this path, so the automatic run can publish here.

What lands there:

```
youtube/index.md              hub, linked from the vault's own index.md
youtube/<topic>.md            one map-of-content page per topic
youtube/<topic>/<note>.md     the notes
```

Every note gets a generated `## Related` block containing:

- `[[youtube/index]]` and `[[youtube/<topic>]]` — up-links to the hub and MOC
- `[[index]]` — back into the main JARVIS vault, so the cluster attaches to the
  existing graph instead of floating next to it
- up to 4 related notes, chosen by IDF-weighted keyword overlap over title and
  Core Concept. Terms common to every note ("ai") carry no weight, so they
  cannot manufacture links.

Notes also gain `tags: [youtube, youtube/<topic>]` and `.obsidian/graph.json`
gains a matching colour group per topic with `showTags: true`.

The KB in `kb/` stays the source of truth; the vault is a generated mirror. The
related block is fenced by `<!-- yt-brain:related -->` sentinels and regenerated
each publish, so republishing is idempotent and hand-written prose below the
block survives.
