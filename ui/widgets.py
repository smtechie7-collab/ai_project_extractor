from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor


class PrimaryButton(QPushButton):
    """
    High-visibility primary action button (e.g., Run Analysis).
    Features smooth subtle elevation, modern green/indigo accent, and tactile feedback.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedHeight(38)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1f6feb, stop:1 #238636);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
                padding: 0 18px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #388bfd, stop:1 #2ea043);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background: #196127;
                padding-top: 1px;
            }
            QPushButton:disabled {
                background: #21262d;
                color: #484f58;
                border: 1px solid #30363d;
            }
        """)


class SecondaryButton(QPushButton):
    """
    Subtle action button for secondary controls (Copy, Open Project, Clear).
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedHeight(34)
        self.setStyleSheet("""
            QPushButton {
                background-color: #21262d;
                color: #f0f6fc;
                border: 1px solid #30363d;
                border-radius: 6px;
                font-size: 12.5px;
                font-weight: 500;
                padding: 0 14px;
            }
            QPushButton:hover {
                background-color: #30363d;
                border-color: #8b949e;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #161b22;
                padding-top: 1px;
            }
            QPushButton:disabled {
                background-color: #161b22;
                color: #484f58;
                border-color: #21262d;
            }
        """)


class StatCard(QWidget):
    """
    Refined stat card displaying key metrics in modern card layout.
    """
    def __init__(self, label, value, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        self.setStyleSheet("""
            QWidget {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 6px;
            }
        """)

        lbl_title = QLabel(label.upper())
        lbl_title.setStyleSheet("color: #8b949e; font-size: 10px; font-weight: 600; border: none; letter-spacing: 0.5px;")
        
        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet("color: #f0f6fc; font-size: 15px; font-weight: 700; border: none;")

        layout.addWidget(lbl_title)
        layout.addWidget(self.lbl_value)