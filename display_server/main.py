"""Entry point for the display server.

Flaskベースの簡易サーバーを提供し、POSTされたテキストから
話題の切り替わりを検出してOBSに表示できる構造を示す。
"""

from __future__ import annotations

from datetime import datetime, timezone

from flask import Flask, Response, request, render_template, jsonify

from . import transcriber, topic_detector, timestamp_logger, config

app = Flask(__name__)

# アプリケーションの状態は ``app.config`` に保存し、
# グローバル変数による競合を避ける
app.config.setdefault("CURRENT_TOPIC", "")
app.config.setdefault("PREVIOUS_TEXT", None)


@app.route("/")
def index() -> str:
    """OBSブラウザソースとして読み込むHTMLを返す."""
    return render_template("display.html")


@app.route("/topic")
def topic() -> Response:
    """現在の話題をJSON形式で返す."""
    return jsonify({"topic": app.config.get("CURRENT_TOPIC", "")})


@app.route("/submit", methods=["POST"])
def submit() -> Response:
    """音声(テキスト)を受け取り、話題が変われば更新してログを残す."""
    audio = request.data or request.form.get("text", "")
    text = transcriber.transcribe(audio)

    previous = app.config.get("PREVIOUS_TEXT")

    if topic_detector.detect(
        previous, text, threshold=config.TOPIC_SIMILARITY_THRESHOLD
    ):
        app.config["CURRENT_TOPIC"] = text
        timestamp_logger.log(text, datetime.now(timezone.utc))

    app.config["PREVIOUS_TEXT"] = text
    return Response(status=204)


def main() -> None:
    """Run the Flask development server."""
    app.run(debug=False)


if __name__ == "__main__":  # pragma: no cover - CLI 実行時のみ
    main()
