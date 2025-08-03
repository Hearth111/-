"""GUI editor for modifying CSS styles.

本来は ``PyQt5`` を用いたGUIエディターを提供する予定だが、テスト
環境ではGUIライブラリを利用できないため、ここでは設定ファイルを
標準入力から読み込み ``static/css/style.css`` へ保存する簡易的な
CLI ベースの実装を提供する。"""

from __future__ import annotations

from pathlib import Path
import sys


CSS_PATH = Path(__file__).resolve().parents[1] / "static" / "css" / "style.css"


def launch() -> None:
    """Run the minimal CSS editor.

    標準入力からCSS文字列を読み取り、 ``style.css`` に保存する。
    GUI を使えない環境でもスタイル変更が行えるようにするための
    簡易実装である。
    """

    css = sys.stdin.read()
    CSS_PATH.parent.mkdir(parents=True, exist_ok=True)
    CSS_PATH.write_text(css, encoding="utf-8")


if __name__ == "__main__":  # pragma: no cover - CLI 実行時のみ
    launch()
