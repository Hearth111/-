import importlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))


def test_threshold_env(monkeypatch):
    monkeypatch.setenv("TOPIC_SIMILARITY_THRESHOLD", "0.1")
    import display_server.config as config
    importlib.reload(config)
    assert config.TOPIC_SIMILARITY_THRESHOLD == 0.1
