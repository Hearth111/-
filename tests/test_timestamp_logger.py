from datetime import datetime
from pathlib import Path
import sys

# ルートディレクトリをパスに追加してパッケージをインポート
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from display_server import timestamp_logger


def test_log_creates_file(tmp_path, monkeypatch):
    # LOG_DIR を一時ディレクトリに切り替え
    monkeypatch.setattr(timestamp_logger, "LOG_DIR", tmp_path)
    ts = datetime(2024, 1, 1, 12, 0, 0)

    log_path = timestamp_logger.log("test topic", ts)

    assert log_path.exists()
    assert log_path.parent == tmp_path

    content = log_path.read_text(encoding="utf-8").strip()
    assert "test topic" in content
    assert "2024-01-01T12:00:00" in content
