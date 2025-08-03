from __future__ import annotations

"""PyQt5 based CSS style editor with preview and theme/font selection."""

from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFontComboBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtCore import Qt

CSS_PATH = Path(__file__).resolve().parents[1] / "static" / "css" / "style.css"
THEMES_DIR = Path(__file__).resolve().with_name("themes")


class CSSEditor(QMainWindow):
    """Simple editor window."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("CSS Editor")

        self.theme_box = QComboBox()
        self.theme_box.addItems([p.name for p in THEMES_DIR.glob("*.css")])
        self.theme_box.currentTextChanged.connect(self.load_theme)

        self.font_box = QFontComboBox()
        self.font_box.currentFontChanged.connect(self.update_preview)

        self.text_edit = QTextEdit()
        self.preview = QLabel("Preview")
        self.preview.setAlignment(Qt.AlignCenter)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_css)

        layout = QVBoxLayout()
        layout.addWidget(self.theme_box)
        layout.addWidget(self.font_box)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.preview)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_theme(self.theme_box.currentText())

    def load_theme(self, name: str) -> None:
        path = THEMES_DIR / name
        if path.exists():
            css = path.read_text(encoding="utf-8")
            self.text_edit.setPlainText(css)
            self.update_preview()

    def update_preview(self) -> None:
        css = self.text_edit.toPlainText()
        font = self.font_box.currentFont()
        self.preview.setStyleSheet(css)
        self.preview.setFont(font)

    def save_css(self) -> None:
        CSS_PATH.parent.mkdir(parents=True, exist_ok=True)
        CSS_PATH.write_text(self.text_edit.toPlainText(), encoding="utf-8")


def launch() -> None:
    """Launch the editor application."""

    import os

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication.instance() or QApplication([])
    editor = CSSEditor()
    editor.show()
    app.exec_()


if __name__ == "__main__":  # pragma: no cover
    launch()
