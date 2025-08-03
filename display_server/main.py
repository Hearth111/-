"""Entry point for the display server.

このサンプル実装では、音声データを読み込んで簡易的な文字起こし
結果を標準出力へ表示するだけの最小構成となっている。実際のWeb
サーバーやOBS連携機能は未実装だが、モジュール間の結合方法を
示す参考例として機能する。"""

from __future__ import annotations

from . import audio_listener, transcriber


def main(source: audio_listener.SourceType = None) -> None:
    """Run a minimal demonstration of the display server pipeline.

    ``source`` から音声データを読み込み、テキストへ変換して
    ``print`` するだけの処理を行う。
    """

    audio = audio_listener.listen(source)
    text = transcriber.transcribe(audio)
    print(text)


if __name__ == "__main__":  # pragma: no cover - CLI 実行時のみ
    main()
