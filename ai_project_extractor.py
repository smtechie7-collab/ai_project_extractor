"""
ai_project_extractor.py
=======================
Application entry point.

This module intentionally performs NO dependency installation at runtime. If a
required dependency is missing it reports the problem and how to fix it, then
exits cleanly. (Previous versions silently ran `pip install PySide6` and restarted
the process via `os.execv`, which mutates the host environment and is blocked or
flagged in many corporate/offline environments.)
"""

from __future__ import annotations

import sys

# ── Dependency check (no auto-install) ──
try:
    import PySide6  # noqa: F401
except ModuleNotFoundError:
    print(
        "\n[FATAL] PySide6 is not installed.\n\n"
        "Install the project dependencies first:\n\n"
        "    python -m pip install -r requirements.txt\n\n"
        "or install just PySide6:\n\n"
        "    python -m pip install PySide6\n",
        file=sys.stderr,
    )
    sys.exit(1)


def main() -> int:
    from core.logging_setup import get_logger, setup_logging
    setup_logging()
    logger = get_logger("aice.main")

    from PySide6.QtWidgets import QApplication

    from ui.main_window import MainWindow
    from ui.theme_manager import ThemeManager

    app = QApplication(sys.argv)

    try:
        ThemeManager.load()
    except Exception as exc:  # noqa: BLE001 - theme failure must never block startup
        logger.warning(f"Theme load failed: {exc}")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
