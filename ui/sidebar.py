from PySide6.QtWidgets import QListWidget, QListWidgetItem


class PhaseSidebar(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(260)
        self.setEnabled(False)
        self.phases = []

    def load_phases(self, phase_list):
        self.clear()
        self.phases = phase_list
        for phase in phase_list:
            self.addItem(QListWidgetItem(f"🔒 {phase}"))

    def unlock(self):
        self.setEnabled(True)
        if self.count() > 0:
            self.item(0).setText(f"▶ {self.phases[0]}")

    def mark_done(self, index):
        item = self.item(index)
        base = item.text().replace("🔒", "").replace("▶", "").replace("✔", "").strip()
        item.setText(f"✔ {base}")

        if index + 1 < self.count():
            self.item(index + 1).setText(f"▶ {self.phases[index + 1]}")
