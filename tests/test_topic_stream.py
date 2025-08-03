from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import display_server.main as main_module
from display_server import timestamp_logger


def test_topic_stream_emits_updates(tmp_path, monkeypatch):
    monkeypatch.setattr(timestamp_logger, "LOG_DIR", tmp_path)
    client = main_module.app.test_client()
    main_module.app.config["CURRENT_TOPIC"] = ""
    main_module.app.config["PREVIOUS_TEXT"] = None

    client.post("/submit", data={"text": "stream topic"})

    with client.get("/topic-stream") as resp:
        event = next(resp.response).decode("utf-8").strip()
        assert event == "data: stream topic"
