"""Central configuration for the yt-brain pipeline."""

from __future__ import annotations

import os
from pathlib import Path

BASE = Path(os.environ.get("YT_BRAIN_HOME", Path(__file__).resolve().parent))

KB_DIR = BASE / "kb"
LOG_DIR = BASE / "logs"
STATE_FILE = BASE / "processed_videos.json"
BUFFER_FILE = Path(os.environ.get("YT_BUFFER_FILE", BASE / "buffer.txt"))

# Pipeline artifacts
TRANSCRIPTS_DIR = BASE / "transcripts"
NOTES_DIR = BASE / "notes"
CLASSIFIED_DIR = BASE / "classified"
REVIEWS_DIR = BASE / "reviews"

# Webhook receiver port (default 8767, avoids conflict with agent-reach on 8765)
WEBHOOK_PORT = int(os.environ.get("YT_WEBHOOK_PORT", "8767"))

# Optional Netscape cookie file exported from Chrome. Needed because YouTube
# blocks this workstation's IP for caption requests.
COOKIE_FILE = Path(os.environ.get("YT_COOKIE_FILE", BASE / "cookies.txt"))

VENV_BIN = BASE / ".venv" / "bin"

# --- Ingestion ---------------------------------------------------------------

# Chrome-family history databases, most-recently-used first. Paths that do not
# exist are skipped, so listing several profiles is harmless.
BROWSER_HISTORY_GLOBS = [
    "~/.config/google-chrome/*/History",
    "~/.config/google-chrome-beta/*/History",
    "~/.config/chromium/*/History",
    "~/.config/BraveSoftware/*/History",
    "~/.config/microsoft-edge/*/History",
]

FIREFOX_PROFILES = Path("~/.mozilla/firefox").expanduser()

# How far back to look for watch history on each run.
LOOKBACK_HOURS = int(os.environ.get("YT_LOOKBACK_HOURS", "30"))

# YouTube watch pages are noise: the home page, search, subscriptions, Shorts
# shelves and the live "history" index itself all match the hostname filter.
URL_ALLOW = "/watch?v="
URL_DENY_SUBSTRINGS = (
    "&list=",
    "/shorts/",
    "/feed/",
    "/playlist",
    "music.youtube",
)

# --- Agent 1: Gatekeeper -----------------------------------------------------

# Widen this list over time. Matching is done by the LLM, not by string match.
RELEVANCE_CRITERIA = """
- AI / ML engineering: LLMs, agents, RAG, fine-tuning, training, inference,
  evaluation, MLOps, vector databases, model serving.
- Linux / self-hosting / infrastructure: system administration, networking,
  servers, homelab, containers, storage, security, performance tuning.
- Systems and software engineering craft: programming languages, compilers,
  databases, testing, tooling, architecture, code review practice.
- Open-source and developer tooling that supports the above.
""".strip()

RELEVANCE_EXCLUSIONS = """
- Entertainment, gaming, comedy, music, vlogs, politics, sports, vlog footage.
- General news, drama, celebrity, reaction content, autoplay-only uploads.
- Content that merely mentions AI in a thumbnail or title but delivers none.
- Academic study material, exam prep, coursework, homework, quizzes, and
  data-structures / algorithms / computer-science-fundamentals deep dives
  (DSA, B-tree, knapsack, memory hierarchy, operating-systems coursework).
""".strip()

# --- Agent 3: Analyst --------------------------------------------------------

MAX_TRANSCRIPT_CHARS = int(os.environ.get("YT_MAX_TRANSCRIPT_CHARS", "120000"))
CHARS_PER_SUMMARY_CHUNK = int(os.environ.get("YT_CHUNK_CHARS", "24000"))
SUMMARY_MAX_TOKENS = int(os.environ.get("YT_SUMMARY_TOKENS", "1500"))
GATEKEEPER_MAX_TOKENS = int(os.environ.get("YT_GATEKEEPER_TOKENS", "100"))

# --- LLM backend -------------------------------------------------------------

LLM_COMMAND = os.environ.get("YT_LLM_COMMAND", "opencode")
LLM_TIMEOUT = int(os.environ.get("YT_LLM_TIMEOUT", "600"))
LLM_CWD = BASE

# Optional primary model and fallbacks for `opencode run -m provider/model`.
# If unset, all available opencode free models are tried in order.
LLM_MODEL = os.environ.get("YT_LLM_MODEL", "").strip() or None
_fallback_env = os.environ.get("YT_LLM_FALLBACK_MODELS", "").strip()
LLM_FALLBACK_MODELS = [m.strip() for m in _fallback_env.replace(",", " ").split() if m.strip()] or [
    "opencode/beam-free",
    "opencode/deepseek-v4.1-flash-free",
    "opencode/flint-40b-free",
    "opencode/glm-5.3-flash-free",
    "opencode/iceman-free",
    "opencode/inkling-2-small-free",
    "opencode/longcat-2.5-free",
    "opencode/mimo-v2.6-flash-free",
    "opencode/minimax-m3.1-flash-free",
    "opencode/nemotron-3.5-lightning-free",
    "opencode/nemotron-3.5-super-vl-free",
]

# --- Operational limits ------------------------------------------------------

# Stop the batch after this many *new* videos so a bad afternoon of YouTube
# cannot run for hours or blow up the token bill.
MAX_VIDEOS_PER_RUN = int(os.environ.get("YT_MAX_VIDEOS", "15"))

# Minimum watch duration, in seconds, for a browser history row to count as a
# real watch rather than a stray click. Videos shorter than this are skipped
# without being marked processed, so they are re-evaluated next run.
MIN_WATCH_SECONDS = int(os.environ.get("YT_MIN_WATCH_SECONDS", "30"))

BATCH_LOG = LOG_DIR / "pipeline.log"
