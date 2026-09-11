from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont


class PhaseSidebar(QListWidget):
    phase_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(260)
        self.phases = []
        
        self.setFont(QFont("Segoe UI", 10))
        self.setStyleSheet("""
            QListWidget {
                background-color: #161616;
                color: #dcdcdc;
                border-right: 1px solid #2d2d2d;
                padding: 6px;
            }
            QListWidget::item {
                height: 34px;
                padding-left: 10px;
                border-radius: 4px;
                margin-bottom: 2px;
            }
            QListWidget::item:hover {
                background-color: #242424;
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #094771;
                color: #4fc3f7;
                font-weight: bold;
            }
        """)

        self.itemClicked.connect(self._on_item_clicked)

    def load_phases(self, phase_list):
        self.clear()
        self.phases = list(phase_list)
        for phase in self.phases:
            item = QListWidgetItem(f"⚪ {phase}")
            item.setData(Qt.UserRole, phase)
            self.addItem(item)

    def mark_phase_running(self, phase: str):
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.UserRole) == phase:
                item.setText(f"⏳ {phase}")
                break

    def mark_phase_done(self, phase: str):
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.UserRole) == phase:
                item.setText(f"✔ {phase}")
                break

    def mark_all_done(self):
        for i in range(self.count()):
            item = self.item(i)
            phase = item.data(Qt.UserRole)
            if phase:
                item.setText(f"✔ {phase}")

    def select_phase(self, phase: str):
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.UserRole) == phase:
                self.setCurrentItem(item)
                break

    def _on_item_clicked(self, item: QListWidgetItem):
        phase = item.data(Qt.UserRole)
        if phase:
            self.phase_clicked.emit(phase)

