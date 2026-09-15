"""
tests/ui/test_main_window.py
============================
PySide6 GUI smoke tests using pytest-qt.
"""

from __future__ import annotations

from ui.main_window import AboutDialog, MainWindow, SponsorDialog


def test_main_window_init(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() != ""
    assert window.workspace is not None
    assert window.sidebar is not None
    assert window.action_bar is not None


def test_about_dialog(qtbot):
    dlg = AboutDialog()
    qtbot.addWidget(dlg)
    assert "About" in dlg.windowTitle()


def test_sponsor_dialog(qtbot):
    dlg = SponsorDialog()
    qtbot.addWidget(dlg)
    assert "Sponsor" in dlg.windowTitle()
