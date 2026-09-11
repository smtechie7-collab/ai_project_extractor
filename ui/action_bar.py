from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QComboBox,
    QLabel, QMenu, QCheckBox
)
from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QCursor
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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # ---------- Select Project Button ----------
        self.project_btn = QPushButton("📂  Open Project")
        self.project_btn.setObjectName("actionProjectBtn")
        self.project_btn.setFixedHeight(34)
        self.project_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.project_btn.clicked.connect(select_project_cb)

        # ---------- Git Filter Checkbox ----------
        self.git_check = QCheckBox("Git Diff Only")
        self.git_check.setToolTip("Scan only uncommitted / modified files in repository")
        self.git_check.setEnabled(False)
        self.git_check.stateChanged.connect(self.on_git_toggle)

        # ---------- Language Selector ----------
        self.language_combo = QComboBox()
        self.language_combo.setFixedHeight(34)
        self.language_combo.setMinimumWidth(180)
        for key, profile in LANGUAGE_PROFILES.items():
            self.language_combo.addItem(profile["display"], key)

        last_lang = self.settings.value("language", AppState.selected_language)
        idx = self.language_combo.findData(last_lang)
        if idx != -1:
            self.language_combo.setCurrentIndex(idx)
            AppState.selected_language = last_lang

        # ---------- Theme Selector ----------
        self.theme_combo = QComboBox()
        self.theme_combo.setFixedHeight(34)
        self.theme_combo.setFixedWidth(90)
        self.theme_combo.addItem("🌙 Dark", "dark")
        self.theme_combo.addItem("☀️ Light", "light")
        self.theme_combo.currentIndexChanged.connect(self.on_theme_change)

        # ---------- Export Button ----------
        self.export_btn = QPushButton("⬇  Export")
        self.export_btn.setObjectName("actionExportBtn")
        self.export_btn.setFixedHeight(34)
        self.export_btn.setEnabled(False)
        self.export_btn.setCursor(QCursor(Qt.PointingHandCursor))

        menu = QMenu(self)
        menu.addAction("📄 Export Active View (.txt)", export_selected_cb)
        menu.addAction("📑 Export All Phase Reports", export_all_cb)
        menu.addSeparator()
        menu.addAction("📦 Export Full Project Archive (.zip)", export_zip_cb)
        self.export_btn.setMenu(menu)

        # Assemble layout
        layout.addWidget(self.project_btn)
        layout.addWidget(self.git_check)
        layout.addSpacing(6)
        
        lbl_lang = QLabel("Language:")
        layout.addWidget(lbl_lang)
        layout.addWidget(self.language_combo)
        
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
            self.git_check.setText("Git Diff Only")
            self.git_check.setToolTip("Scan only uncommitted / modified files")
        else:
            self.git_check.setText("No Git Repo")
            self.git_check.setChecked(False)

    def on_git_toggle(self, state):
        if self.git_toggle_cb:
            self.git_toggle_cb(self.git_check.isChecked())