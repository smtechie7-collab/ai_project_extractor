from PySide6.QtGui import QAction
from core.language_registry import LANGUAGE_PROFILES
from state.app_state import AppState


def build_menus(window, menubar):
    file_menu = menubar.addMenu("File")
    theme_menu = menubar.addMenu("Theme")
    lang_menu = menubar.addMenu("Language")

    open_action = QAction("Open Project", window)
    open_action.triggered.connect(window.select_project)
    file_menu.addAction(open_action)

    exit_action = QAction("Exit", window)
    exit_action.triggered.connect(window.close)
    file_menu.addAction(exit_action)

    for key, profile in LANGUAGE_PROFILES.items():
        act = QAction(profile["display"], window)
        act.triggered.connect(
            lambda checked, k=key: set_language(window, k)
        )
        lang_menu.addAction(act)


def set_language(window, lang_key):
    AppState.selected_language = lang_key
    window.status.showMessage(f"Language set: {lang_key}")
