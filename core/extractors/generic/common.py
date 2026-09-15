"""
core/extractors/generic/common.py
=================================
Shared helpers for the language-neutral (generic) extractors.
"""

from __future__ import annotations

import os
from collections.abc import Iterable, Iterator

from core.language_registry import LANGUAGE_PROFILES
from core.utils.file_reader import read_text_file
from state.app_state import AppState


def get_rel_path(path: str) -> str:
    """Return a project-root relative path, falling back to the basename."""
    try:
        base = AppState.project_root or os.getcwd()
        return os.path.relpath(path, start=base).replace("\\", "/")
    except (ValueError, OSError):
        return os.path.basename(path)


def profile_extensions(lang: str | None = None) -> tuple[str, ...]:
    """Extensions for a language profile.

    An empty tuple means "all files" (the ``all`` profile).
    """
    key = (lang or AppState.selected_language or "all").lower()
    profile = LANGUAGE_PROFILES.get(key) or {}
    return tuple(profile.get("extensions") or ())


def is_source_file(path: str, extensions: Iterable[str] | None = None) -> bool:
    """True when the file matches the given extensions (empty/None = any file)."""
    exts = tuple(extensions) if extensions is not None else profile_extensions()
    if not exts:
        return True
    return path.lower().endswith(tuple(e.lower() for e in exts))


def iter_source_files(
    tree_root,
    extensions: Iterable[str] | None = None,
) -> Iterator[str]:
    """Depth-first iterator over source file paths matching the given extensions."""
    exts = tuple(extensions) if extensions is not None else profile_extensions()

    stack = [tree_root]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        if getattr(node, "is_dir", False):
            stack.extend(getattr(node, "children", []) or [])
        elif is_source_file(node.path, exts):
            yield node.path


def read_or_marker(path: str) -> str:
    """Read a text file, returning a readable marker for skipped/binary files."""
    return read_text_file(path)
