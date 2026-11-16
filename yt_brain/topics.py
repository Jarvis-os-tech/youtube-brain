"""Deterministic topic routing for knowledge-base notes.

Notes land in `kb/<topic>/YYYY-MM-DD-slug.md`. The classifier is keyword-based
on purpose: it costs zero tokens, never fails a pipeline run, and gives the
same answer for the same input every time (so re-running the backfill is
idempotent). The gatekeeper already spends an LLM call deciding *whether* a
video is worth keeping; spending a second one deciding *where* to file it buys
nothing but latency and bill.

Ordering matters: the first topic whose keywords hit wins, so the narrow
topics are listed before the broad ones.
"""

from __future__ import annotations

import re

# (topic, keywords) in priority order. Keywords are matched against the
# lowercased title plus the note's Core Concept paragraph.
TOPICS: list[tuple[str, tuple[str, ...]]] = [
    (
        "agents",
        (
            "agent", "agentic", "orchestrat", "mcp", "claude code", "codex",
            "cursor", "hermes", "tool call", "multi-agent", "copilot",
            "subagent", "workflow", "squad", "a2a",
        ),
    ),
    (
        "ml-training",
        (
            "fine-tun", "finetun", "rlhf", "reinforcement learning", "grpo",
            "ppo", "reward model", "distillation", "distill", "quantiz",
            "lora", "training run", "fine tuning", "rl ", "pretraining",
            "pre-training", "epoch", "loss curve", "dataset",
        ),
    ),
    (
        "llm-core",
        (
            "llm", "gpt", "gemini", "claude", "transformer", "attention",
            "context window", "token", "prompt", "rag", "embedding", "vector",
            "inference", "open weights", "agi", "rsi", "reasoning model",
            "benchmark",
        ),
    ),
    (
        "linux-infra",
        (
            "linux", "ubuntu", "arch ", "omarchy", "hyprland", "systemd",
            "docker", "kubernetes", "container", "server", "homelab",
            "self-host", "selfhost", "bash", "shell", "terminal", "ssh",
            "networking", "nixos", "wayland", "kernel", "distro", "hosting",
            "deploy", "openshell",
        ),
    ),
    (
        "security",
        (
            "security", "sandbox", "vulnerab", "exploit", "malware", "firewall",
            "encrypt", "auth", "permission", "threat", "isolation", "zero trust",
        ),
    ),
    (
        "dev-craft",
        (
            "rust", "python", "javascript", "typescript", "compiler",
            "database", "postgres", "sqlite", "testing", "git", "ide",
            "editor", "neovim", "vim", "code review", "refactor", "api design",
            "architecture", "open source", "github", "tooling", "debugging",
        ),
    ),
]

DEFAULT_TOPIC = "general"

# Display names for the Obsidian MOC pages. `str.title()` would render
# "llm-core" as "Llm Core", which is wrong for every acronym here.
LABELS = {
    "agents": "AI Agents & Orchestration",
    "ml-training": "ML Training & Fine-Tuning",
    "llm-core": "LLMs & Model Behaviour",
    "linux-infra": "Linux & Infrastructure",
    "security": "Security & Sandboxing",
    "dev-craft": "Software Engineering Craft",
    DEFAULT_TOPIC: "General",
}


def label(topic: str) -> str:
    """Human-readable name for a topic slug."""
    return LABELS.get(topic, topic.replace("-", " ").title())

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(title: str, max_len: int = 60) -> str:
    slug = _SLUG_RE.sub("-", title.lower()).strip("-")
    return (slug[:max_len].rstrip("-")) or "video"


def classify(title: str, body: str = "") -> str:
    """Return the topic slug for a note.

    Scored, not first-match. Nearly every title in this KB contains the word
    "agent", so a first-match-wins rule that checks `agents` first swept 2/3 of
    the library into one folder. Instead each topic accumulates a score and the
    highest wins, with title hits worth 3x body hits: the title is what the
    video is *about*, the body is context that drifts.

    Only the first ~1200 chars of the body are read, which covers the
    `## Core Concept` paragraph without letting a late transcript section
    outvote the title.
    """
    head = title.lower()
    tail = body[:1200].lower()

    best_topic = DEFAULT_TOPIC
    best_score = 0.0
    for order, (topic, keywords) in enumerate(TOPICS):
        score = 0.0
        for kw in keywords:
            if kw in head:
                score += 3.0
            elif kw in tail:
                score += 1.0
        # Order breaks ties in favour of the earlier (narrower) topic.
        score -= order * 0.01
        if score > best_score:
            best_topic, best_score = topic, score

    return best_topic if best_score > 0 else DEFAULT_TOPIC


def note_filename(date: str, title: str) -> str:
    """`YYYY-MM-DD-slug.md`, the note filename inside a topic folder."""
    return f"{date}-{slugify(title)}.md"
