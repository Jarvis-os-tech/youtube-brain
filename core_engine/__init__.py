"""Forwarding root for core_engine when accessed from repository root."""

from __future__ import annotations

import sys
from pathlib import Path

_pkg_dir = Path(__file__).resolve().parent / "core_engine"
if str(_pkg_dir) not in sys.path:
    sys.path.insert(0, str(_pkg_dir))

from .core_engine import (  # noqa: E402
    DEFAULT_SOCKET_PATH,
    AgentBusClient,
    AgentBusServer,
    AgentMessage,
    MessageType,
)

__all__ = [
    "DEFAULT_SOCKET_PATH",
    "AgentBusClient",
    "AgentBusServer",
    "AgentMessage",
    "MessageType",
]
