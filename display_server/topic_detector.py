"""Detect topic changes in text.

このモジュールでは、直前の文章と現在の文章を比較し、
話題が切り替わったかどうかを簡易的に判定する。
`previous` が ``None`` または空文字の場合は常に話題が
変わったとみなす。
"""

from __future__ import annotations

from typing import Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_vectorizer = TfidfVectorizer()


def _similarity(a: str, b: str) -> float:
    """Return cosine similarity between two texts using TF-IDF."""

    vectors = _vectorizer.fit_transform([a, b])
    sim_matrix = cosine_similarity(vectors[0:1], vectors[1:2])
    return float(sim_matrix[0, 0])


def detect(previous: Optional[str], current: str, *, threshold: float = 0.5) -> bool:
    """前後の文章を比較して話題の切り替わりを判定する。"""

    if not previous:
        return True

    try:
        similarity = _similarity(previous, current)
    except ValueError:
        # 片方が空だった等でベクトル化できない場合は話題が変わったとみなす
        return True

    return similarity < threshold


__all__ = ["detect"]
