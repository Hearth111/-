from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from display_server import config, timestamp_logger
import display_server.main as main_module


def test_submit_respects_config_threshold(tmp_path, monkeypatch):
    monkeypatch.setattr(timestamp_logger, "LOG_DIR", tmp_path)
    monkeypatch.setattr(config, "TOPIC_SIMILARITY_THRESHOLD", 0.9)

    client = main_module.app.test_client()
    main_module.app.config["CURRENT_TOPIC"] = ""
    main_module.app.config["PREVIOUS_TEXT"] = None

    client.post("/submit", data=b"hello world")
    client.post("/submit", data=b"hello world again")

    res = client.get("/topic")
    assert res.get_json()["topic"] == "hello world again"

    log_files = list(tmp_path.glob("topics_*.txt"))
    assert len(log_files) == 1
    lines = log_files[0].read_text(encoding="utf-8").strip().splitlines()
    assert lines[0].endswith("hello world")
    assert lines[1].endswith("hello world again")
