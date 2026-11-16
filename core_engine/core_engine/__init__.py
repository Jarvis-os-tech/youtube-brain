"""Jarvis OS Core Engine Package."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .agent_bus import (
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


def __getattr__(name: str):
    if name in __all__:
        import importlib
        module = importlib.import_module(".agent_bus", package=__name__)
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
