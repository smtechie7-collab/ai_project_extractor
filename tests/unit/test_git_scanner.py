"""
tests/unit/test_git_scanner.py
==============================
Unit tests for GitScanner change detection.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from core.git_scanner import GitScanner


def test_is_git_repo_true(tmp_path: Path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    assert GitScanner.is_git_repo(str(tmp_path))


def test_is_git_repo_false(tmp_path: Path):
    assert not GitScanner.is_git_repo(str(tmp_path))


def test_get_changed_files_empty_on_non_git(tmp_path: Path):
    assert GitScanner.get_changed_files(str(tmp_path)) == set()


def test_get_changed_files_detects_untracked(tmp_path: Path):
    # Initialize a clean git repo in tmp_path
    try:
        subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    except Exception:
        return  # Skip if git executable unavailable

    new_file = tmp_path / "hello.py"
    new_file.write_text("x = 1\n", encoding="utf-8")

    changed = GitScanner.get_changed_files(str(tmp_path))
    assert os.path.normpath(str(new_file)) in changed
