"""
core/context.py
===============
AnalysisContext object bundling tree root, scan configuration, logger, and outputs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import logging
from typing import Any

from core.config import ScanConfig
from core.logging_setup import get_logger
from models.tree_node import TreeNode


@dataclass
class AnalysisContext:
    config: ScanConfig
    tree_root: TreeNode | None = None
    logger: logging.Logger = field(default_factory=lambda: get_logger("aice.analysis"))
    outputs: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def project_root(self) -> str:
        return str(self.config.project_root)

    @property
    def language(self) -> str:
        return self.config.language
