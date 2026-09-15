"""
tests/unit/test_scanner.py
==========================
Unit tests for iterative directory scanning.
"""

from __future__ import annotations

import os
from pathlib import Path

from core.scanner import scan_directory
from state.app_state import AppState


def test_scan_directory_discovers_supported_files(sample_repo: Path):
    AppState.selected_language = "python"
    root_node = scan_directory(str(sample_repo))

    assert root_node.is_dir
    assert root_node.name == "sample_project"

    # Verify src/api/routes.py is included
    all_paths = []
    def collect(node):
        all_paths.append(node.path)
        for c in node.children:
            collect(c)
    collect(root_node)

    normalized = [os.path.normpath(p) for p in all_paths]
    assert os.path.normpath(str(sample_repo / "src" / "api" / "routes.py")) in normalized
    assert os.path.normpath(str(sample_repo / "src" / "api" / "service.py")) in normalized


def test_scan_directory_prunes_ignored_directories(sample_repo: Path):
    AppState.selected_language = "python"
    root_node = scan_directory(str(sample_repo))

    all_names = []
    def collect(node):
        all_names.append(node.name)
        for c in node.children:
            collect(c)
    collect(root_node)

    assert "__pycache__" not in all_names
    assert "stray.pyc" not in all_names


def test_scan_directory_whitelist_filtering(sample_repo: Path):
    AppState.selected_language = "python"
    target = os.path.normpath(str(sample_repo / "src" / "api" / "routes.py"))
    whitelist = {target}

    root_node = scan_directory(str(sample_repo), whitelist_files=whitelist)

    all_files = []
    def collect(node):
        if not node.is_dir:
            all_files.append(os.path.normpath(node.path))
        for c in node.children:
            collect(c)
    collect(root_node)

    assert all_files == [target]


def test_scan_directory_handles_deep_nesting(tmp_path: Path):
    AppState.selected_language = "python"
    # Create 25 levels of short directory names (fits Windows MAX_PATH)
    curr = tmp_path / "d"
    for _ in range(25):
        curr = curr / "x"
    curr.mkdir(parents=True)
    (curr / "leaf.py").write_text("print('deep')\n", encoding="utf-8")

    root_node = scan_directory(str(tmp_path / "d"))
    assert root_node.is_dir
    assert len(root_node.children) == 1
