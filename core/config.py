"""
core/config.py
==============
Immutable ScanConfig dataclass representing configuration for an analysis run.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ScanConfig:
    project_root: Path
    language: str = "kotlin"
    git_only: bool = False
    max_file_kb: int = 500
    whitelist: frozenset[str] = field(default_factory=frozenset)
    include_tests: bool = True
