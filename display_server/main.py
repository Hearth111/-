"""Entry point for the display server.

Flaskベースの簡易サーバーを提供し、POSTされたテキストから
話題の切り替わりを検出してOBSに表示できる構造を示す。
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from flask import Flask, Response, request, render_template, jsonify

from . import transcriber, topic_detector, timestamp_logger, config

app = Flask(__name__)

_current_topic: str = ""
_previous_text: Optional[str] = None


@app.route("/")
def index() -> str:
    """OBSブラウザソースとして読み込むHTMLを返す."""
    return render_template("display.html")


@app.route("/topic")
def topic() -> Response:
    """現在の話題をJSON形式で返す."""
    return jsonify({"topic": _current_topic})


@app.route("/submit", methods=["POST"])
def submit() -> Response:
    """音声(テキスト)を受け取り、話題が変われば更新してログを残す."""
    global _current_topic, _previous_text

    audio = request.data or request.form.get("text", "")
    text = transcriber.transcribe(audio)

    if topic_detector.detect(
        _previous_text, text, threshold=config.TOPIC_SIMILARITY_THRESHOLD
    ):
        _current_topic = text
        timestamp_logger.log(_current_topic, datetime.utcnow())

    _previous_text = text
    return Response(status=204)


def main() -> None:
    """Run the Flask development server."""
    app.run(debug=False)


if __name__ == "__main__":  # pragma: no cover - CLI 実行時のみ
    main()
