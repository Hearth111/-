from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from display_server import timestamp_logger
import display_server.main as main_module


def test_stream_provides_updates(tmp_path, monkeypatch):
    monkeypatch.setattr(timestamp_logger, "LOG_DIR", tmp_path)

    # initialize state
    st = main_module.state_module.get_state()
    st.current_topic = "initial"
    st.previous_text = None

    client = main_module.app.test_client()

    res = client.get("/stream")
    first = next(res.response).decode().strip()
    assert first == "data: initial"

    client.post("/submit", data={"text": "next"})
    second = next(res.response).decode().strip()
    assert second == "data: next"

    res.close()
