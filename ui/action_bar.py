from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QComboBox,
    QLabel, QMenu
)
from PySide6.QtCore import QSettings
from state.app_state import AppState
from core.language_registry import LANGUAGE_PROFILES
from ui.theme_manager import ThemeManager


class ActionBar(QWidget):
    def __init__(
        self,
        select_project_cb,
        export_selected_cb,
        export_all_cb,
        export_zip_cb,
    ):
        super().__init__()

        self.settings = QSettings("AIProjectExtractor", "App")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(12)

        # ---------- Project ----------
        self.project_btn = QPushButton("📂 Select Project")
        self.project_btn.setFixedHeight(36)
        self.project_btn.clicked.connect(select_project_cb)

        # ---------- Language ----------
        self.language_combo = QComboBox()
        self.language_combo.setFixedHeight(36)
        for key, profile in LANGUAGE_PROFILES.items():
            self.language_combo.addItem(profile["display"], key)

        last_lang = self.settings.value("language", AppState.selected_language)
        idx = self.language_combo.findData(last_lang)
        if idx != -1:
            self.language_combo.setCurrentIndex(idx)
            AppState.selected_language = last_lang

        self.language_combo.currentIndexChanged.connect(self.on_language_change)

        # ---------- Theme ----------
        self.theme_combo = QComboBox()
        self.theme_combo.setFixedHeight(36)
        self.theme_combo.addItem("Dark", "dark")
        self.theme_combo.addItem("Light", "light")

        last_theme = self.settings.value("theme", "dark")
        t_idx = self.theme_combo.findData(last_theme)
        if t_idx != -1:
            self.theme_combo.setCurrentIndex(t_idx)

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
        layout.addWidget(QLabel("Language:"))
        layout.addWidget(self.language_combo)
        layout.addWidget(QLabel("Theme:"))
        layout.addWidget(self.theme_combo)
        layout.addStretch(1)
        layout.addWidget(self.export_btn)

    def on_language_change(self, index):
        lang = self.language_combo.itemData(index)
        AppState.selected_language = lang
        self.settings.setValue("language", lang)

    def on_theme_change(self, index):
        theme = self.theme_combo.itemData(index)
        ThemeManager.apply(theme)

    def enable_export(self):
        self.export_btn.setEnabled(True)
