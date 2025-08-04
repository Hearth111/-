"""Handle audio input for transcription.

このモジュールは音声入力を抽象化し、呼び出し元に生の音声
バイト列を返すユーティリティを提供する。従来はファイルや
標準入力のみを扱っていたが、`speech_recognition` ライブラリが
利用可能な場合はマイク入力も取得できるようになった。
"""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Optional, Union
import sys

try:  # pragma: no cover - optional dependency
    import speech_recognition as sr
except Exception:  # pragma: no cover - library not installed
    sr = None


SourceType = Optional[Union[str, Path, BinaryIO]]


def listen(source: SourceType = None) -> bytes:
    """Read raw audio data from ``source``.

    Args:
        source: 音声データを取得する元。 ``None`` の場合は ``stdin`` から
            読み込む。文字列または ``Path`` の場合はそのパスのファイルを
            バイナリモードで開いて内容を読み込む。ファイルオブジェクトが
            渡された場合は ``read()`` で全データを取得する。文字列で
            ``"microphone"`` が指定された場合は、デフォルトマイクから
            音声を録音して返す。

    Returns:
        bytes: 読み込まれた生の音声データ。
    """

    if source in (None, "stdin"):
        # スタンドアロンでも扱いやすいよう、標準入力から読み込む。
        return sys.stdin.buffer.read()

    if source == "microphone":
        if sr is None:
            raise RuntimeError("speech_recognition is not available")
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:  # pragma: no cover - requires hardware
            audio = recognizer.listen(mic)
        return audio.get_wav_data()

    if isinstance(source, (str, Path)):
        with open(source, "rb") as fh:  # pragma: no cover - ファイル操作のため
            return fh.read()

    # ファイルライクオブジェクトを想定
    return source.read()


__all__ = ["listen", "SourceType"]
