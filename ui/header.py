from PySide6.QtWidgets import QLabel


class Header(QLabel):
    def __init__(self):
        super().__init__("No project loaded")
        self.setStyleSheet(
            "font-size:14px; font-weight:600; padding:4px;"
        )
        self.setMaximumHeight(30)  # 🔥 reduce wasted space

    def set_project(self, path: str):
        self.setText(f"Project: {path}")
