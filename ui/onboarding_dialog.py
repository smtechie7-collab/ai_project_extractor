from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QCheckBox
)
from PySide6.QtCore import QSettings


class OnboardingDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("AIProjectExtractor", "App")
        self.setWindowTitle("Welcome to AI Project Extractor")
        self.resize(520, 300)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(
            "<h2>Welcome 👋</h2>"
            "<p>This tool analyzes your project structure, "
            "dependencies, and risks, and prepares AI-ready outputs.</p>"
            "<ul>"
            "<li>📂 Select your project</li>"
            "<li>🌐 Choose language</li>"
            "<li>▶ Run analysis</li>"
            "<li>⬇ Export & share with AI</li>"
            "</ul>"
        ))

        self.skip = QCheckBox("Don't show this again")
        layout.addWidget(self.skip)

        btn = QPushButton("Get Started")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

    def closeEvent(self, e):
        if self.skip.isChecked():
            self.settings.setValue("onboarding_done", True)
        super().closeEvent(e)
