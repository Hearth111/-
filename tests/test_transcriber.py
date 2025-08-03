from pathlib import Path
import sys
import base64

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from display_server import transcriber


def test_transcribe_fallback(monkeypatch):
    # Avoid loading whisper model
    monkeypatch.setattr(transcriber, "_load_model", lambda: None)
    data = b"\xff\xff"
    text = transcriber.transcribe(data)
    assert text == base64.b64encode(data).decode("ascii")


def test_transcribe_string(monkeypatch):
    assert transcriber.transcribe("hello") == "hello"
