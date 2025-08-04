from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from display_server import audio_listener


def test_listen_microphone(monkeypatch):
    class DummyAudio:
        def get_wav_data(self):
            return b"abc"

    class DummyRecognizer:
        def listen(self, source):
            return DummyAudio()

    class DummyMic:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass

    dummy_sr = types.SimpleNamespace(Recognizer=lambda: DummyRecognizer(), Microphone=DummyMic)
    monkeypatch.setattr(audio_listener, "sr", dummy_sr)
    assert audio_listener.listen("microphone") == b"abc"
