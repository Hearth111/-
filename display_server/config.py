"""Configuration parameters for the display server."""

from __future__ import annotations

import os


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except ValueError:
        return default


# 話題検出のしきい値。値が小さいほど話題の切り替わりが起きにくくなる。
TOPIC_SIMILARITY_THRESHOLD: float = _env_float(
    "TOPIC_SIMILARITY_THRESHOLD", 0.5
)

# ログレベルを環境変数から設定できるようにする。
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()


__all__ = ["TOPIC_SIMILARITY_THRESHOLD", "LOG_LEVEL"]

