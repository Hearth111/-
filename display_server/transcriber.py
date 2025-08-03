"""Convert audio into text.

本モジュールは高度な音声認識エンジンを利用しない代わりに、入力
されたバイト列や文字列をそのままテキスト化する単純な関数を提供
する。バイト列は UTF-8 としてデコードを試み、失敗した場合は
Base64 文字列に変換する。"""

from __future__ import annotations

import base64
import logging
from typing import Union

try:  # pragma: no cover - whisper is optional during tests
    import whisper
except Exception:  # pragma: no cover - missing optional dependency
    whisper = None


AudioInput = Union[bytes, bytearray, memoryview, str]

logger = logging.getLogger(__name__)
_model: "whisper.Whisper" | None = None


def _load_model() -> "whisper.Whisper" | None:
    global _model
    if _model is None and whisper is not None:
        try:
            _model = whisper.load_model("tiny")
        except Exception as exc:  # pragma: no cover - network/model errors
            logger.exception("failed to load whisper model: %s", exc)
            _model = None
    return _model


def transcribe(audio: AudioInput) -> str:
    """Return a textual representation of ``audio``.

    If ``whisper`` が利用可能であれば音声認識を行い、失敗時はログを残して
    フォールバックとして従来のデコード処理を用いる。
    """

    if isinstance(audio, str):
        return audio

    data = bytes(audio)

    model = _load_model()
    if model is not None:
        try:
            result = model.transcribe(data, fp16=False)
            return result.get("text", "").strip()
        except Exception as exc:  # pragma: no cover - runtime errors
            logger.exception("whisper transcription failed: %s", exc)

    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        # バイナリデータを安全に文字列化するため Base64 にする
        return base64.b64encode(data).decode("ascii")


__all__ = ["transcribe", "AudioInput"]
