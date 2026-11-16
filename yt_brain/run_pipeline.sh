#!/usr/bin/env bash
# yt-brain daily batch run. Exits when done; no daemons are started here.
set -Eeuo pipefail

HOME_DIR="${YT_BRAIN_HOME:-$HOME/jarvis-yt-brain/yt_brain}"
PY="$HOME_DIR/.venv/bin/python"
LOG="$HOME_DIR/logs/pipeline.log"

mkdir -p "$HOME_DIR/logs"

if [[ ! -x "$PY" ]]; then
  echo "yt-brain: virtualenv missing at $PY" >&2
  echo "recreate with: uv venv --python 3.14 '$HOME_DIR' && uv pip install --python '$PY' youtube-transcript-api" >&2
  exit 1
fi

cd "$HOME_DIR"

# Timer output goes to the journal; keep a human-readable line too.
if ! "$PY" main.py "$@" 2>&1 | tee -a "$LOG"; then
  echo "yt-brain: pipeline exited non-zero" >&2
  exit 1
fi
