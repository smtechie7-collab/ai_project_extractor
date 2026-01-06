from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings


DARK_THEME = """
QMainWindow { background-color: #1e1e1e; }
QWidget { background-color: #1e1e1e; color: #e6e6e6; }
QTextEdit { background-color: #252526; color: #d4d4d4; }
QPushButton { background-color: #3a3a3a; padding:6px; }
"""

LIGHT_THEME = """
QMainWindow { background-color: #ffffff; }
QWidget { background-color: #ffffff; color: #000000; }
QTextEdit { background-color: #ffffff; color: #000000; }
QPushButton { background-color: #f0f0f0; padding:6px; }
"""


class ThemeManager:
    settings = QSettings("AIProjectExtractor", "App")

    @classmethod
    def apply(cls, theme: str):
        app = QApplication.instance()
        if not app:
            return

        if theme == "dark":
            app.setStyleSheet(DARK_THEME)
        else:
            app.setStyleSheet(LIGHT_THEME)

        cls.settings.setValue("theme", theme)

    @classmethod
    def load(cls):
        theme = cls.settings.value("theme", "dark")
        cls.apply(theme)
