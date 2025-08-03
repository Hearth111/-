from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from display_server import timestamp_logger
import display_server.main as main_module


def test_submit_accepts_form_text(tmp_path, monkeypatch):
    monkeypatch.setattr(timestamp_logger, "LOG_DIR", tmp_path)

    client = main_module.app.test_client()
    main_module.app.config["CURRENT_TOPIC"] = ""
    main_module.app.config["PREVIOUS_TEXT"] = None

    client.post("/submit", data={"text": "form topic"})

    res = client.get("/topic")
    assert res.get_json()["topic"] == "form topic"

    log_files = list(tmp_path.glob("topics_*.txt"))
    assert len(log_files) == 1
    content = log_files[0].read_text(encoding="utf-8").strip()
    assert content.endswith("form topic")
