import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtWidgets import QApplication

from css_editor.editor import CSSEditor, CSS_PATH


def test_save_css(tmp_path, monkeypatch):
    monkeypatch.setattr('css_editor.editor.CSS_PATH', tmp_path / 'style.css')
    app = QApplication.instance() or QApplication([])
    editor = CSSEditor()
    editor.text_edit.setPlainText("body { color: red; }")
    editor.save_css()
    content = (tmp_path / 'style.css').read_text(encoding='utf-8')
    assert "color: red" in content
