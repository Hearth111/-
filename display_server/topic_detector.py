"""Detect topic changes in text.

このモジュールでは、直前の文章と現在の文章を比較し、
話題が切り替わったかどうかを簡易的に判定する。
`previous` が ``None`` または空文字の場合は常に話題が
変わったとみなす。
"""

from __future__ import annotations

import re
from typing import Optional

_WORD_RE = re.compile(r"\w+")


def _tokenize(text: str) -> set[str]:
    """文章を単語の集合へ変換する。

    正規表現で単語を抽出し、小文字化して返す。
    """

    return set(_WORD_RE.findall(text.lower()))


def detect(previous: Optional[str], current: str, *, threshold: float = 0.5) -> bool:
    """前後の文章を比較して話題の切り替わりを判定する。

    Args:
        previous: 直前の文章。 ``None`` や空文字の場合は常に ``True`` を返す。
        current: 現在の文章。
        threshold: ジャッカード係数の閾値。値が小さいほど厳密に判定する。

    Returns:
        bool: 話題が変わったと判定された場合 ``True``。
    """

    if not previous:
        return True

    prev_tokens = _tokenize(previous)
    curr_tokens = _tokenize(current)

    if not prev_tokens or not curr_tokens:
        # どちらかが空集合なら話題が変わったとみなす
        return True

    intersection = prev_tokens & curr_tokens
    union = prev_tokens | curr_tokens

    similarity = len(intersection) / len(union)

    return similarity < threshold


__all__ = ["detect"]
