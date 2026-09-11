from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings


DARK_THEME = """
/* ===================================================================
   PRODUCTION-GRADE MODERN DARK DESIGN SYSTEM (Obsidian / GitHub Pro)
   =================================================================== */

QMainWindow {
    background-color: #0d1117;
    color: #f0f6fc;
}

QWidget {
    color: #f0f6fc;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'SF Pro Display', Roboto, sans-serif;
    font-size: 13px;
}

/* --- Menus & Toolbars --- */
QMenuBar {
    background-color: #161b22;
    color: #8b949e;
    border-bottom: 1px solid #30363d;
    padding: 2px 6px;
    font-size: 12px;
}
QMenuBar::item {
    background: transparent;
    padding: 4px 10px;
    border-radius: 4px;
}
QMenuBar::item:selected {
    background-color: #21262d;
    color: #f0f6fc;
}

QMenu {
    background-color: #161b22;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 4px;
}
QMenu::item {
    padding: 6px 24px 6px 12px;
    border-radius: 4px;
}
QMenu::item:selected {
    background-color: #1f6feb;
    color: #ffffff;
}
QMenu::separator {
    height: 1px;
    background: #30363d;
    margin: 4px 6px;
}

/* --- Buttons --- */
QPushButton {
    background-color: #21262d;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 500;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #30363d;
    border-color: #8b949e;
}
QPushButton:pressed {
    background-color: #161b22;
}
QPushButton:disabled {
    background-color: #161b22;
    color: #484f58;
    border-color: #21262d;
}

/* --- Inputs & Dropdowns --- */
QLineEdit {
    background-color: #0f141c;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    selection-background-color: #1f6feb;
}
QLineEdit:focus {
    border-color: #58a6ff;
    background-color: #0d1117;
}

QComboBox {
    background-color: #161b22;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
}
QComboBox:hover {
    border-color: #8b949e;
    background-color: #21262d;
}
QComboBox:focus {
    border-color: #58a6ff;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: none;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #8b949e;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #161b22;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 4px;
    selection-background-color: #1f6feb;
    selection-color: #ffffff;
    outline: none;
}

/* --- Text Editor / Output --- */
QTextEdit {
    background-color: #0f141c;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px;
    font-family: 'JetBrains Mono', 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
    font-size: 12.5px;
    line-height: 1.5;
    selection-background-color: #264f78;
}

/* --- Splitter & Frames --- */
QSplitter::handle {
    background-color: #21262d;
    width: 1px;
}

/* --- Scrollbars (Slim Modern) --- */
QScrollBar:vertical {
    background-color: transparent;
    width: 8px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background-color: #30363d;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background-color: #484f58;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 8px;
    margin: 0;
}
QScrollBar::handle:horizontal {
    background-color: #30363d;
    border-radius: 4px;
    min-width: 24px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #484f58;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* --- CheckBoxes --- */
QCheckBox {
    color: #8b949e;
    spacing: 6px;
    font-size: 12px;
}
QCheckBox:hover {
    color: #f0f6fc;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #30363d;
    border-radius: 4px;
    background-color: #161b22;
}
QCheckBox::indicator:hover {
    border-color: #58a6ff;
}
QCheckBox::indicator:checked {
    background-color: #1f6feb;
    border-color: #1f6feb;
    image: none;
}

/* --- Status Bar --- */
QStatusBar {
    background-color: #161b22;
    color: #8b949e;
    border-top: 1px solid #30363d;
    padding: 3px 10px;
    font-size: 12px;
}
QStatusBar QLabel {
    color: #8b949e;
}

/* --- Tooltips --- */
QToolTip {
    background-color: #161b22;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}
"""


LIGHT_THEME = """
/* ===================================================================
   PRODUCTION-GRADE MODERN LIGHT DESIGN SYSTEM (Clean Modern)
   =================================================================== */

QMainWindow {
    background-color: #f6f8fa;
    color: #1f2328;
}

QWidget {
    color: #1f2328;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'SF Pro Display', Roboto, sans-serif;
    font-size: 13px;
}

QMenuBar {
    background-color: #ffffff;
    color: #656d76;
    border-bottom: 1px solid #d0d7de;
    padding: 2px 6px;
    font-size: 12px;
}
QMenuBar::item:selected {
    background-color: #f3f4f6;
    color: #1f2328;
}

QMenu {
    background-color: #ffffff;
    color: #1f2328;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 4px;
}
QMenu::item:selected {
    background-color: #0969da;
    color: #ffffff;
}

QPushButton {
    background-color: #ffffff;
    color: #1f2328;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #f3f4f6;
    border-color: #8c959f;
}
QPushButton:pressed {
    background-color: #eaeef2;
}

QLineEdit {
    background-color: #ffffff;
    color: #1f2328;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 6px 10px;
}

QComboBox {
    background-color: #ffffff;
    color: #1f2328;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 5px 12px;
}

QTextEdit {
    background-color: #ffffff;
    color: #1f2328;
    border: 1px solid #d0d7de;
    border-radius: 8px;
    padding: 12px;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 12.5px;
}

QStatusBar {
    background-color: #ffffff;
    color: #656d76;
    border-top: 1px solid #d0d7de;
}
"""


class ThemeManager:
    settings = QSettings("AIProjectExtractor", "App")

    @classmethod
    def apply(cls, theme: str):
        app = QApplication.instance()
        if not app:
            return

        if theme == "light":
            app.setStyleSheet(LIGHT_THEME)
        else:
            app.setStyleSheet(DARK_THEME)

        cls.settings.setValue("theme", theme)

    @classmethod
    def load(cls):
        theme = cls.settings.value("theme", "dark")
        cls.apply(theme)
