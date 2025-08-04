"""Entry point for the display server.

Flaskベースの簡易サーバーを提供し、POSTされたテキストから
話題の切り替わりを検出してOBSに表示できる構造を示す。
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
import threading
import typing
from queue import Queue

from flask import (
    Flask,
    Response,
    request,
    render_template,
    jsonify,
    stream_with_context,
)

from . import (
    audio_listener,
    transcriber,
    topic_detector,
    timestamp_logger,
    config,
    state as state_module,
)

app = Flask(__name__)

logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)


# connected SSE clients
_clients: list[Queue[str]] = []


def handle_audio(raw: transcriber.AudioInput) -> None:
    """Transcribe ``raw`` audio/text and update the topic state."""
    text = transcriber.transcribe(raw)
    st = state_module.get_state()

    # allow tests to reset state via app.config
    st.current_topic = app.config.get("CURRENT_TOPIC", st.current_topic)
    st.previous_text = app.config.get("PREVIOUS_TEXT", st.previous_text)

    with st.lock:
        previous = st.previous_text

        if topic_detector.detect(
            previous, text, threshold=config.TOPIC_SIMILARITY_THRESHOLD
        ):
            st.current_topic = text
            logger.info("Topic changed: %s", text)
            timestamp_logger.log(text, datetime.now(timezone.utc))
            for q in list(_clients):
                q.put(st.current_topic)

        st.previous_text = text


def _microphone_worker(stop_event: threading.Event) -> None:
    """Continuously listen to the microphone and process audio."""
    while not stop_event.is_set():
        try:
            audio = audio_listener.listen("microphone")
        except Exception as exc:  # pragma: no cover - hardware dependent
            logger.exception("microphone listen failed: %s", exc)
            continue
        handle_audio(audio)


@app.route("/")
def index() -> str:
    """OBSブラウザソースとして読み込むHTMLを返す."""
    return render_template("display.html")


@app.route("/stream")
def stream() -> Response:
    """現在の話題をSSEでストリーム配信する."""
    q: Queue[str] = Queue()
    _clients.append(q)

    @stream_with_context
    def event_stream() -> typing.Iterator[str]:
        st = state_module.get_state()
        yield f"data: {st.current_topic}\n\n"
        try:
            while True:
                topic = q.get()
                yield f"data: {topic}\n\n"
        finally:
            _clients.remove(q)

    return Response(event_stream(), mimetype="text/event-stream")


@app.route("/topic")
def topic() -> Response:
    """現在の話題をJSON形式で返す."""
    st = state_module.get_state()
    return jsonify({"topic": st.current_topic})


@app.route("/submit", methods=["POST"])
def submit() -> Response:
    """音声(テキスト)を受け取り、話題が変われば更新してログを残す."""
    if "text" in request.form:
        raw = request.form["text"]
    else:
        json_payload = request.get_json(silent=True) or {}
        if "text" in json_payload:
            raw = json_payload["text"]
        else:
            raw = request.get_data()

    handle_audio(raw)
    return Response(status=204)


def main() -> None:
    """Run the Flask development server with background microphone thread."""
    stop_event = threading.Event()
    thread = threading.Thread(
        target=_microphone_worker, args=(stop_event,), daemon=True
    )
    thread.start()
    try:
        app.run(debug=False)
    finally:
        stop_event.set()
        thread.join()


if __name__ == "__main__":  # pragma: no cover - CLI 実行時のみ
    main()
