from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

DARK_THEME = """
/* ===================================================================
   OBSIDIAN / GITHUB PRO DARK DESIGN SYSTEM
   =================================================================== */

QMainWindow, QWidget#centralWidget {
    background-color: #0d1117;
    color: #f0f6fc;
}

QWidget {
    color: #f0f6fc;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'SF Pro Display', Roboto, sans-serif;
    font-size: 13px;
}

/* --- Navigation Bar --- */
QFrame#headerFrame {
    background-color: #161b22;
    border-bottom: 1px solid #30363d;
}

QLabel#logoIcon {
    font-size: 20px;
    border: none;
    background: transparent;
}

QLabel#mainAppTitle {
    font-size: 15px;
    font-weight: 800;
    color: #f0f6fc;
    letter-spacing: -0.2px;
    border: none;
    background: transparent;
}

QLabel#proBadge {
    background-color: #1f6feb;
    color: #ffffff;
    font-size: 10px;
    font-weight: 800;
    border-radius: 4px;
    padding: 2px 6px;
    border: none;
}

QLabel#projectTitle {
    background-color: #0f141c;
    color: #58a6ff;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton#sponsorBtn {
    background-color: #21262d;
    color: #f0883e;
    border: 1px solid #30363d;
    border-radius: 6px;
    font-weight: 600;
    font-size: 12px;
    padding: 0 12px;
}
QPushButton#sponsorBtn:hover {
    background-color: #30363d;
    border-color: #f0883e;
    color: #ffa657;
}

/* --- Menus --- */
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

/* --- Action Bar Controls --- */
QPushButton#actionProjectBtn, QPushButton#actionExportBtn {
    background-color: #21262d;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 0 14px;
    font-weight: 600;
    font-size: 12.5px;
}
QPushButton#actionProjectBtn:hover, QPushButton#actionExportBtn:hover {
    background-color: #30363d;
    border-color: #8b949e;
}
QPushButton#actionProjectBtn:pressed, QPushButton#actionExportBtn:pressed {
    background-color: #161b22;
}

/* --- Common Buttons --- */
QPushButton {
    background-color: #21262d;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 500;
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

/* Primary Run & Action Buttons */
QPushButton#startBtn, QPushButton#primaryBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1f6feb, stop:1 #238636);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    font-weight: 700;
    font-size: 13px;
    padding: 0 18px;
}
QPushButton#startBtn:hover, QPushButton#primaryBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #388bfd, stop:1 #2ea043);
    border: 1px solid rgba(255, 255, 255, 0.3);
}
QPushButton#startBtn:disabled, QPushButton#primaryBtn:disabled {
    background: #21262d;
    color: #484f58;
    border: 1px solid #30363d;
}

/* Secondary Button */
QPushButton#secondaryBtn {
    background-color: #21262d;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 6px;
    font-size: 12.5px;
    font-weight: 500;
    padding: 0 14px;
}
QPushButton#secondaryBtn:hover {
    background-color: #30363d;
    border-color: #8b949e;
    color: #ffffff;
}
QPushButton#secondaryBtn:pressed {
    background-color: #161b22;
}
QPushButton#secondaryBtn:disabled {
    background-color: #161b22;
    color: #484f58;
    border-color: #21262d;
}

/* Stat Card */
QWidget#statCard {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
}
QLabel#statCardTitle {
    color: #8b949e;
    font-size: 10px;
    font-weight: 600;
    border: none;
    letter-spacing: 0.5px;
}
QLabel#statCardValue {
    color: #f0f6fc;
    font-size: 15px;
    font-weight: 700;
    border: none;
}

/* Dialogs */
QDialog {
    background-color: #161b22;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 12px;
}
QLabel#aboutTitle {
    font-size: 18px;
    font-weight: 800;
    color: #58a6ff;
}
QLabel#sponsorDialogTitle {
    font-size: 18px;
    font-weight: 800;
    color: #f0883e;
}
QLabel#dialogSubtitle {
    color: #8b949e;
    font-size: 12px;
}
QLabel#aboutDesc {
    font-size: 13px;
    line-height: 1.6;
    color: #c9d1d9;
    padding: 10px 0;
}
QFrame#qrFrame {
    background-color: #ffffff;
    border-radius: 8px;
    border: 2px solid #30363d;
}


/* --- Sidebar --- */
QWidget#sidebarHeader {
    background-color: #161b22;
    border-bottom: 1px solid #30363d;
    border-right: 1px solid #30363d;
}
QLabel#sidebarTitle {
    font-size: 11px;
    font-weight: 700;
    color: #8b949e;
    letter-spacing: 0.8px;
}
QLabel#sidebarBadge {
    background-color: #21262d;
    color: #8b949e;
    border-radius: 10px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 600;
    border: 1px solid #30363d;
}
QListWidget#sidebarList {
    background-color: #0d1117;
    color: #c9d1d9;
    border: none;
    border-right: 1px solid #30363d;
    padding: 6px 8px;
    outline: none;
}
QListWidget#sidebarList::item {
    height: 36px;
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 6px;
    margin-bottom: 3px;
    border: 1px solid transparent;
}
QListWidget#sidebarList::item:hover {
    background-color: #161b22;
    color: #f0f6fc;
    border: 1px solid #30363d;
}
QListWidget#sidebarList::item:selected {
    background-color: #1f242c;
    color: #58a6ff;
    font-weight: 600;
    border-left: 3px solid #2f81f7;
    border-radius: 4px;
}

/* --- Feature Search Bar --- */
QFrame#searchFrame {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
}
QLineEdit#searchInput {
    background-color: #0f141c;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12.5px;
}
QLineEdit#searchInput:focus {
    border-color: #58a6ff;
}
QPushButton#searchBtn {
    background-color: #1f6feb;
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    padding: 0 16px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton#searchBtn:hover {
    background-color: #388bfd;
}

/* --- Workspace --- */
QFrame#workspaceTopFrame {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
}
QTextEdit#codeEditor {
    background-color: #0f141c;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px;
    font-family: 'Cascadia Code', 'JetBrains Mono', 'Consolas', monospace;
    font-size: 12.5px;
    selection-background-color: #264f78;
}
QProgressBar#analysisProgress {
    background-color: #161b22;
    border: none;
    border-radius: 2px;
}
QProgressBar#analysisProgress::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1f6feb, stop:1 #238636);
    border-radius: 2px;
}
QLabel#metaLabel {
    color: #8b949e;
    font-size: 12px;
}

/* --- ComboBoxes --- */
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

/* --- Scrollbars --- */
QScrollBar:vertical {
    background-color: transparent;
    width: 8px;
}
QScrollBar::handle:vertical {
    background-color: #30363d;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background-color: #484f58;
}
QScrollBar:horizontal {
    background-color: transparent;
    height: 8px;
}
QScrollBar::handle:horizontal {
    background-color: #30363d;
    border-radius: 4px;
    min-width: 24px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #484f58;
}

/* --- Status Bar --- */
QStatusBar {
    background-color: #161b22;
    color: #8b949e;
    border-top: 1px solid #30363d;
    padding: 3px 10px;
}
QStatusBar QLabel {
    color: #8b949e;
}
QSplitter::handle {
    background-color: #30363d;
    width: 1px;
}
"""


LIGHT_THEME = """
/* ===================================================================
   CLEAN MODERN LIGHT DESIGN SYSTEM (GitHub / macOS Style)
   =================================================================== */

QMainWindow, QWidget#centralWidget {
    background-color: #f6f8fa;
    color: #1f2328;
}

QWidget {
    color: #1f2328;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'SF Pro Display', Roboto, sans-serif;
    font-size: 13px;
}

/* --- Navigation Bar --- */
QFrame#headerFrame {
    background-color: #ffffff;
    border-bottom: 1px solid #d0d7de;
}

QLabel#logoIcon {
    font-size: 20px;
    border: none;
    background: transparent;
}

QLabel#mainAppTitle {
    font-size: 15px;
    font-weight: 800;
    color: #1f2328;
    letter-spacing: -0.2px;
    border: none;
    background: transparent;
}

QLabel#proBadge {
    background-color: #0969da;
    color: #ffffff;
    font-size: 10px;
    font-weight: 800;
    border-radius: 4px;
    padding: 2px 6px;
    border: none;
}

QLabel#projectTitle {
    background-color: #f3f4f6;
    color: #0969da;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton#sponsorBtn {
    background-color: #ffffff;
    color: #bf8700;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    font-weight: 600;
    font-size: 12px;
    padding: 0 12px;
}
QPushButton#sponsorBtn:hover {
    background-color: #fff8c5;
    border-color: #bf8700;
}

/* --- Menus --- */
QMenuBar {
    background-color: #ffffff;
    color: #656d76;
    border-bottom: 1px solid #d0d7de;
    padding: 2px 6px;
    font-size: 12px;
}
QMenuBar::item {
    background: transparent;
    padding: 4px 10px;
    border-radius: 4px;
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
QMenu::item {
    padding: 6px 24px 6px 12px;
    border-radius: 4px;
}
QMenu::item:selected {
    background-color: #0969da;
    color: #ffffff;
}
QMenu::separator {
    height: 1px;
    background: #d0d7de;
    margin: 4px 6px;
}

/* --- Action Bar Controls --- */
QPushButton#actionProjectBtn, QPushButton#actionExportBtn {
    background-color: #ffffff;
    color: #1f2328;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 0 14px;
    font-weight: 600;
    font-size: 12.5px;
}
QPushButton#actionProjectBtn:hover, QPushButton#actionExportBtn:hover {
    background-color: #f3f4f6;
    border-color: #8c959f;
}
QPushButton#actionProjectBtn:pressed, QPushButton#actionExportBtn:pressed {
    background-color: #eaeef2;
}

/* --- Common Buttons --- */
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
QPushButton:disabled {
    background-color: #f6f8fa;
    color: #8c959f;
    border-color: #d0d7de;
}

/* Primary Run & Action Buttons */
QPushButton#startBtn, QPushButton#primaryBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0969da, stop:1 #1a7f37);
    color: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 6px;
    font-weight: 700;
    font-size: 13px;
    padding: 0 18px;
}
QPushButton#startBtn:hover, QPushButton#primaryBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1177ee, stop:1 #22863a);
}
QPushButton#startBtn:disabled, QPushButton#primaryBtn:disabled {
    background: #eaeef2;
    color: #8c959f;
    border: 1px solid #d0d7de;
}

/* Secondary Button */
QPushButton#secondaryBtn {
    background-color: #ffffff;
    color: #1f2328;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    font-size: 12.5px;
    font-weight: 500;
    padding: 0 14px;
}
QPushButton#secondaryBtn:hover {
    background-color: #f3f4f6;
    border-color: #8c959f;
    color: #1f2328;
}
QPushButton#secondaryBtn:pressed {
    background-color: #eaeef2;
}
QPushButton#secondaryBtn:disabled {
    background-color: #f6f8fa;
    color: #8c959f;
    border-color: #d0d7de;
}

/* Stat Card */
QWidget#statCard {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 6px;
}
QLabel#statCardTitle {
    color: #656d76;
    font-size: 10px;
    font-weight: 600;
    border: none;
    letter-spacing: 0.5px;
}
QLabel#statCardValue {
    color: #1f2328;
    font-size: 15px;
    font-weight: 700;
    border: none;
}

/* Dialogs */
QDialog {
    background-color: #ffffff;
    color: #1f2328;
    border: 1px solid #d0d7de;
    border-radius: 12px;
}
QLabel#aboutTitle {
    font-size: 18px;
    font-weight: 800;
    color: #0969da;
}
QLabel#sponsorDialogTitle {
    font-size: 18px;
    font-weight: 800;
    color: #bf8700;
}
QLabel#dialogSubtitle {
    color: #656d76;
    font-size: 12px;
}
QLabel#aboutDesc {
    font-size: 13px;
    line-height: 1.6;
    color: #24292f;
    padding: 10px 0;
}
QFrame#qrFrame {
    background-color: #ffffff;
    border-radius: 8px;
    border: 2px solid #d0d7de;
}


/* --- Sidebar --- */
QWidget#sidebarHeader {
    background-color: #ffffff;
    border-bottom: 1px solid #d0d7de;
    border-right: 1px solid #d0d7de;
}
QLabel#sidebarTitle {
    font-size: 11px;
    font-weight: 700;
    color: #656d76;
    letter-spacing: 0.8px;
}
QLabel#sidebarBadge {
    background-color: #f3f4f6;
    color: #656d76;
    border-radius: 10px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 600;
    border: 1px solid #d0d7de;
}
QListWidget#sidebarList {
    background-color: #ffffff;
    color: #1f2328;
    border: none;
    border-right: 1px solid #d0d7de;
    padding: 6px 8px;
    outline: none;
}
QListWidget#sidebarList::item {
    height: 36px;
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 6px;
    margin-bottom: 3px;
    border: 1px solid transparent;
}
QListWidget#sidebarList::item:hover {
    background-color: #f3f4f6;
    color: #1f2328;
    border: 1px solid #d0d7de;
}
QListWidget#sidebarList::item:selected {
    background-color: #ddf4ff;
    color: #0969da;
    font-weight: 600;
    border-left: 3px solid #0969da;
    border-radius: 4px;
}

/* --- Feature Search Bar --- */
QFrame#searchFrame {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 8px;
}
QLineEdit#searchInput {
    background-color: #ffffff;
    color: #1f2328;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12.5px;
}
QLineEdit#searchInput:focus {
    border-color: #0969da;
}
QPushButton#searchBtn {
    background-color: #0969da;
    color: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 6px;
    padding: 0 16px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton#searchBtn:hover {
    background-color: #1177ee;
}

/* --- Workspace --- */
QFrame#workspaceTopFrame {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 8px;
}
QTextEdit#codeEditor {
    background-color: #ffffff;
    color: #1f2328;
    border: 1px solid #d0d7de;
    border-radius: 8px;
    padding: 12px;
    font-family: 'Cascadia Code', 'JetBrains Mono', 'Consolas', monospace;
    font-size: 12.5px;
    selection-background-color: #b6e3ff;
}
QProgressBar#analysisProgress {
    background-color: #eaeef2;
    border: none;
    border-radius: 2px;
}
QProgressBar#analysisProgress::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0969da, stop:1 #1a7f37);
    border-radius: 2px;
}
QLabel#metaLabel {
    color: #656d76;
    font-size: 12px;
}

/* --- ComboBoxes --- */
QComboBox {
    background-color: #ffffff;
    color: #1f2328;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
}
QComboBox:hover {
    border-color: #8c959f;
    background-color: #f3f4f6;
}
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #1f2328;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 4px;
    selection-background-color: #0969da;
    selection-color: #ffffff;
    outline: none;
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
    border-top: 5px solid #656d76;
    margin-right: 8px;
}

/* --- CheckBoxes --- */
QCheckBox {
    color: #656d76;
    spacing: 6px;
    font-size: 12px;
}
QCheckBox:hover {
    color: #1f2328;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #d0d7de;
    border-radius: 4px;
    background-color: #ffffff;
}
QCheckBox::indicator:hover {
    border-color: #0969da;
}
QCheckBox::indicator:checked {
    background-color: #0969da;
    border-color: #0969da;
    image: none;
}

/* --- Scrollbars --- */
QScrollBar:vertical {
    background-color: transparent;
    width: 8px;
}
QScrollBar::handle:vertical {
    background-color: #d0d7de;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background-color: #afb8c1;
}
QScrollBar:horizontal {
    background-color: transparent;
    height: 8px;
}
QScrollBar::handle:horizontal {
    background-color: #d0d7de;
    border-radius: 4px;
    min-width: 24px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #afb8c1;
}

/* --- Status Bar --- */
QStatusBar {
    background-color: #ffffff;
    color: #656d76;
    border-top: 1px solid #d0d7de;
    padding: 3px 10px;
}
QStatusBar QLabel {
    color: #656d76;
}
QSplitter::handle {
    background-color: #d0d7de;
    width: 1px;
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
