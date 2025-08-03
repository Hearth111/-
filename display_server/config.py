"""Configuration parameters for the display server."""

# 話題検出のしきい値（Jaccard係数）。
# 値が小さいほど話題の切り替わりが起きにくくなる。
TOPIC_SIMILARITY_THRESHOLD: float = 0.5

__all__ = ["TOPIC_SIMILARITY_THRESHOLD"]

