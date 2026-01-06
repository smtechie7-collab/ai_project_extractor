from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor

# ================= COLORS =================
ACCENT_COLOR = "#007acc"
ACCENT_HOVER = "#0098ff"
BG_DARK = "#252526"
TEXT_COLOR = "#ffffff"

class PrimaryButton(QPushButton):
    """
    Main Action Button (e.g., Start Analysis)
    Blue background, white text, bold.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedHeight(36)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_COLOR};
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
                padding: 0 16px;
            }}
            QPushButton:hover {{
                background-color: {ACCENT_HOVER};
            }}
            QPushButton:pressed {{
                background-color: #005a9e;
            }}
            QPushButton:disabled {{
                background-color: #3e3e42;
                color: #888888;
            }}
        """)

class SecondaryButton(QPushButton):
    """
    Secondary Actions (e.g., Copy, Export)
    Dark background, light border.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedHeight(32)
        self.setStyleSheet("""
            QPushButton {
                background-color: #3e3e42;
                color: #e0e0e0;
                border: 1px solid #505050;
                border-radius: 4px;
                font-size: 12px;
                padding: 0 12px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #2d2d30;
            }
        """)

class StatCard(QWidget):
    """
    A simple card to display key-value stats (e.g., Lines: 5000)
    """
    def __init__(self, label, value, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d30;
                border: 1px solid #3e3e42;
                border-radius: 6px;
            }
        """)

        lbl_title = QLabel(label)
        lbl_title.setStyleSheet("color: #aaaaaa; font-size: 11px; border:none;")
        
        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold; border:none;")

        layout.addWidget(lbl_title)
        layout.addWidget(self.lbl_value)

    def set_value(self, value):
        self.lbl_value.setText(str(value))