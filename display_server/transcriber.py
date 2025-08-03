"""Convert audio into text.

本モジュールは高度な音声認識エンジンを利用しない代わりに、入力
されたバイト列や文字列をそのままテキスト化する単純な関数を提供
する。バイト列は UTF-8 としてデコードを試み、失敗した場合は
Base64 文字列に変換する。"""

from __future__ import annotations

import base64
from typing import Union


AudioInput = Union[bytes, bytearray, memoryview, str]


def transcribe(audio: AudioInput) -> str:
    """Return a textual representation of ``audio``.

    Args:
        audio: 音声データ。バイト列または文字列を受け付ける。

    Returns:
        str: 変換されたテキスト。
    """

    if isinstance(audio, str):
        return audio

    data = bytes(audio)
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        # バイナリデータを安全に文字列化するため Base64 にする
        return base64.b64encode(data).decode("ascii")


__all__ = ["transcribe", "AudioInput"]
