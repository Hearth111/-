"""Log topic timestamps.

提供された話題とタイムスタンプを、日付ごとのログファイルに追記する。
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Union

# ルートディレクトリの ``logs`` フォルダを指すパス
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"


def log(topic: str, timestamp: Union[datetime, str]) -> Path:
    """話題とタイムスタンプをログに書き出す。

    Args:
        topic: 記録する話題。
        timestamp: ログに書き出すタイムスタンプ。 ``datetime`` または ISO 形式の文字列。

    Returns:
        Path: 書き込んだログファイルのパス。
    """

    # タイムスタンプを ``datetime`` オブジェクトに変換
    if isinstance(timestamp, str):
        ts = datetime.fromisoformat(timestamp)
    else:
        ts = timestamp

    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / f"topics_{ts:%Y-%m-%d}.txt"
    line = f"{ts.isoformat()} - {topic}\n"

    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(line)

    return log_file


__all__ = ["log", "LOG_DIR"]
