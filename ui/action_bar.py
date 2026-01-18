from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QComboBox,
    QLabel, QMenu, QCheckBox
)
from PySide6.QtCore import QSettings
from state.app_state import AppState
from core.language_registry import LANGUAGE_PROFILES
from ui.theme_manager import ThemeManager
from core.git_scanner import GitScanner

class ActionBar(QWidget):
    def __init__(
        self,
        select_project_cb,
        export_selected_cb,
        export_all_cb,
        export_zip_cb,
        git_toggle_cb=None
    ):
        super().__init__()

        self.settings = QSettings("AIProjectExtractor", "App")
        self.git_toggle_cb = git_toggle_cb

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(15)

        # ---------- Project ----------
        self.project_btn = QPushButton("📂 Select Project")
        self.project_btn.setFixedHeight(36)
        self.project_btn.clicked.connect(select_project_cb)
        
        # ---------- Git Filter ----------
        self.git_check = QCheckBox("Git Changes Only")
        self.git_check.setStyleSheet("""
            QCheckBox { color: #e0e0e0; font-weight: bold; }
            QCheckBox::indicator { width: 14px; height: 14px; }
            QCheckBox::indicator:checked { background-color: #dcdcaa; border-radius: 2px; }
            QCheckBox::indicator:unchecked { background-color: #3e3e42; border-radius: 2px; }
        """)
        self.git_check.setToolTip("Only scan uncommitted/staged files")
        self.git_check.setEnabled(False) 
        self.git_check.stateChanged.connect(self.on_git_toggle)

        # ---------- Language ----------
        self.language_combo = QComboBox()
        self.language_combo.setFixedHeight(36)
        self.language_combo.setMinimumWidth(150)
        for key, profile in LANGUAGE_PROFILES.items():
            self.language_combo.addItem(profile["display"], key)

        # Load last selected language
        last_lang = self.settings.value("language", AppState.selected_language)
        idx = self.language_combo.findData(last_lang)
        if idx != -1:
            self.language_combo.setCurrentIndex(idx)
            AppState.selected_language = last_lang

        # Note: Signal connection ab MainWindow me handle hoga taaki re-scan ho sake

        # ---------- Theme ----------
        self.theme_combo = QComboBox()
        self.theme_combo.setFixedHeight(36)
        self.theme_combo.addItem("Dark", "dark")
        self.theme_combo.addItem("Light", "light")
        self.theme_combo.currentIndexChanged.connect(self.on_theme_change)

        # ---------- Export ----------
        self.export_btn = QPushButton("⬇ Export")
        self.export_btn.setFixedHeight(36)
        self.export_btn.setEnabled(False)

        menu = QMenu(self)
        menu.addAction("Export Selected Output", export_selected_cb)
        menu.addAction("Export All Outputs", export_all_cb)
        menu.addAction("Export ZIP", export_zip_cb)
        self.export_btn.setMenu(menu)

        # ---------- Layout ----------
        layout.addWidget(self.project_btn)
        layout.addWidget(self.git_check)
        layout.addWidget(QLabel("|"))
        layout.addWidget(QLabel("Lang:"))
        layout.addWidget(self.language_combo)
        layout.addWidget(QLabel("Theme:"))
        layout.addWidget(self.theme_combo)
        layout.addStretch(1)
        layout.addWidget(self.export_btn)

    def on_theme_change(self, index):
        theme = self.theme_combo.itemData(index)
        ThemeManager.apply(theme)

    def enable_export(self):
        self.export_btn.setEnabled(True)
    
    def check_git_status(self, root_path):
        is_repo = GitScanner.is_git_repo(root_path)
        self.git_check.setEnabled(is_repo)
        if is_repo:
            self.git_check.setText("Git Changes Only")
            self.git_check.setToolTip("Scan only modified files")
        else:
            self.git_check.setText("No Git Repo")
            self.git_check.setChecked(False)

    def on_git_toggle(self, state):
        if self.git_toggle_cb:
            self.git_toggle_cb(self.git_check.isChecked())