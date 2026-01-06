from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit,
    QPushButton, QHBoxLayout, QComboBox, QProgressBar
)
from state.output_registry import OutputRegistry


class Workspace(QWidget):
    def __init__(self, start_cb, open_project_cb):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        # ---------- TOP ----------
        top = QHBoxLayout()
        self.phase_selector = QComboBox()
        self.phase_selector.currentTextChanged.connect(self.load_output)

        self.copy_btn = QPushButton("📋 Copy")
        self.copy_btn.clicked.connect(self.copy_output)

        top.addWidget(QLabel("Output:"))
        top.addWidget(self.phase_selector, 1)
        top.addWidget(self.copy_btn)

        # ---------- OUTPUT ----------
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        # ---------- PROGRESS ----------
        self.progress = QProgressBar()
        self.progress.setValue(0)

        # ---------- ACTIONS ----------
        self.start_btn = QPushButton("▶ Start Analysis")
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(start_cb)

        self.open_btn = QPushButton("📂 Open Project")
        self.open_btn.clicked.connect(open_project_cb)

        layout.addLayout(top)
        layout.addWidget(self.output, 1)
        layout.addWidget(self.progress)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.open_btn)

    # ---------- PROJECT ----------
    def project_loaded(self):
        self.start_btn.setEnabled(True)
        self.progress.setValue(0)

    # ---------- OUTPUT ----------
    def add_output(self, phase, content):
        OutputRegistry.add(phase, content)
        if self.phase_selector.findText(phase) == -1:
            self.phase_selector.addItem(phase)
        self.phase_selector.setCurrentText(phase)

    def load_output(self, phase):
        self.output.setPlainText(OutputRegistry.get(phase))

    def copy_output(self):
        self.output.copy()

    def current_phase(self):
        return self.phase_selector.currentText()

    # ---------- 🔥 REQUIRED BY WORKER ----------
    def update_progress(self, value: int, phase: str):
        self.progress.setValue(value)
        self.progress.setFormat(f"{phase} — {value}%")
