from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor


class PrimaryButton(QPushButton):
    """
    High-visibility primary action button (e.g., Run Analysis).
    Styled dynamically via ThemeManager using #primaryBtn / #startBtn.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        if not self.objectName():
            self.setObjectName("primaryBtn")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedHeight(38)


class SecondaryButton(QPushButton):
    """
    Subtle action button for secondary controls (Copy, Open Project, Clear).
    Styled dynamically via ThemeManager using #secondaryBtn.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        if not self.objectName():
            self.setObjectName("secondaryBtn")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedHeight(34)


class StatCard(QWidget):
    """
    Refined stat card displaying key metrics in modern card layout.
    Styled dynamically via ThemeManager using #statCard, #statCardTitle, #statCardValue.
    """
    def __init__(self, label, value, parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        lbl_title = QLabel(label.upper())
        lbl_title.setObjectName("statCardTitle")
        
        self.lbl_value = QLabel(value)
        self.lbl_value.setObjectName("statCardValue")

        layout.addWidget(lbl_title)
        layout.addWidget(self.lbl_value)