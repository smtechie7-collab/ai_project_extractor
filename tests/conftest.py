"""
tests/conftest.py
=================
Pytest fixtures and test environment configuration.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.utils.file_reader import clear_cache
from state.app_state import AppState
from state.output_registry import OutputRegistry


@pytest.fixture(autouse=True)
def reset_global_state():
    """Reset AppState, OutputRegistry and file cache between tests."""
    AppState.project_root = None
    AppState.tree_root = None
    AppState.selected_language = "python"
    OutputRegistry.clear()
    clear_cache()
    yield
    AppState.project_root = None
    AppState.tree_root = None
    OutputRegistry.clear()
    clear_cache()


@pytest.fixture
def sample_repo(tmp_path: Path) -> Path:
    """Creates a temporary multi-language dummy project."""
    repo = tmp_path / "sample_project"
    repo.mkdir()

    # Python files
    py_dir = repo / "src" / "api"
    py_dir.mkdir(parents=True)
    (py_dir / "routes.py").write_text("def get_users(): return []\n", encoding="utf-8")
    (py_dir / "service.py").write_text("class UserService: pass\n", encoding="utf-8")

    # C++ files
    cpp_dir = repo / "cpp_src"
    cpp_dir.mkdir()
    (cpp_dir / "main.cpp").write_text("#include <iostream>\nint main() { return 0; }\n", encoding="utf-8")
    (cpp_dir / "util.hpp").write_text("#pragma once\nvoid log_msg();\n", encoding="utf-8")

    # Ignored directory
    junk_dir = repo / "__pycache__"
    junk_dir.mkdir()
    (junk_dir / "stray.pyc").write_bytes(b"\x00\x01\x02")

    return repo
