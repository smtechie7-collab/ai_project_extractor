from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QHBoxLayout
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont


class PhaseSidebar(QWidget):
    phase_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(275)
        self.phases = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setFixedHeight(46)
        header.setStyleSheet("""
            QWidget {
                background-color: #161b22;
                border-bottom: 1px solid #30363d;
                border-right: 1px solid #30363d;
            }
        """)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(16, 0, 16, 0)

        title = QLabel("ANALYSIS PHASES")
        title.setStyleSheet("font-size: 11px; font-weight: 700; color: #8b949e; letter-spacing: 0.8px; border: none;")

        self.count_badge = QLabel("0")
        self.count_badge.setStyleSheet("""
            background-color: #21262d;
            color: #8b949e;
            border-radius: 10px;
            padding: 2px 8px;
            font-size: 11px;
            font-weight: 600;
            border: 1px solid #30363d;
        """)

        h_layout.addWidget(title)
        h_layout.addStretch()
        h_layout.addWidget(self.count_badge)
        layout.addWidget(header)

        # List Widget
        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont("Segoe UI", 10))
        self.list_widget.setFocusPolicy(Qt.NoFocus)
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #0d1117;
                color: #c9d1d9;
                border: none;
                border-right: 1px solid #30363d;
                padding: 6px 8px;
                outline: none;
            }
            QListWidget::item {
                height: 36px;
                padding-left: 10px;
                padding-right: 10px;
                border-radius: 6px;
                margin-bottom: 3px;
                border: 1px solid transparent;
            }
            QListWidget::item:hover {
                background-color: #161b22;
                color: #f0f6fc;
                border: 1px solid #30363d;
            }
            QListWidget::item:selected {
                background-color: #1f242c;
                color: #58a6ff;
                font-weight: 600;
                border-left: 3px solid #2f81f7;
                border-radius: 4px;
            }
        """)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.list_widget, 1)

    def load_phases(self, phase_list):
        self.list_widget.clear()
        self.phases = list(phase_list)
        self.count_badge.setText(str(len(self.phases)))
        for phase in self.phases:
            item = QListWidgetItem(f"⚪  {phase}")
            item.setData(Qt.UserRole, phase)
            self.list_widget.addItem(item)

    def mark_phase_running(self, phase: str):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.data(Qt.UserRole) == phase:
                item.setText(f"⏳  {phase}")
                self.list_widget.setCurrentItem(item)
                break

    def mark_phase_done(self, phase: str):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.data(Qt.UserRole) == phase:
                item.setText(f"✔  {phase}")
                break

    def reset_status(self):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            orig = item.data(Qt.UserRole)
            item.setText(f"⚪  {orig}")

    def count(self):
        return self.list_widget.count()

    def _on_item_clicked(self, item: QListWidgetItem):
        phase_name = item.data(Qt.UserRole)
        if phase_name:
            self.phase_clicked.emit(phase_name)
