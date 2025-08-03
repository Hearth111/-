"""Handle audio input for transcription.

このモジュールは音声入力を抽象化し、呼び出し元に生の音声
バイト列を返す簡易的なユーティリティを提供する。実際のマイク
入力などは扱わず、ファイルパスやファイルオブジェクトからの
読み込みに対応している。テスト環境でも利用しやすい実装として
いる。
"""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Optional, Union
import sys


SourceType = Optional[Union[str, Path, BinaryIO]]


def listen(source: SourceType = None) -> bytes:
    """Read raw audio data from ``source``.

    Args:
        source: 音声データを取得する元。 ``None`` の場合は ``stdin`` から
            読み込む。文字列または ``Path`` の場合はそのパスのファイルを
            バイナリモードで開いて内容を読み込む。ファイルオブジェクトが
            渡された場合は ``read()`` で全データを取得する。

    Returns:
        bytes: 読み込まれた生の音声データ。
    """

    if source is None:
        # スタンドアロンでも扱いやすいよう、標準入力から読み込む。
        return sys.stdin.buffer.read()

    if isinstance(source, (str, Path)):
        with open(source, "rb") as fh:  # pragma: no cover - ファイル操作のため
            return fh.read()

    # ファイルライクオブジェクトを想定
    return source.read()


__all__ = ["listen", "SourceType"]
