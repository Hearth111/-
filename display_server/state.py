from __future__ import annotations

"""Thread-safe application state storage."""

from dataclasses import dataclass, field
from threading import Lock
from typing import Optional


@dataclass
class TopicState:
    """Represent mutable state for current and previous topics."""

    current_topic: str = ""
    previous_text: Optional[str] = None
    lock: Lock = field(default_factory=Lock, repr=False)


_state: TopicState | None = None


def get_state() -> TopicState:
    """Return a process-wide :class:`TopicState` instance.

    The object is created lazily to avoid issues during import time and is
    protected by a ``Lock`` to allow safe updates from concurrent requests.
    """

    global _state
    if _state is None:
        _state = TopicState()
    return _state


__all__ = ["TopicState", "get_state"]
