"""
models/tree_node.py
===================
Unified hierarchical node model representing files and directories.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import os


@dataclass
class TreeNode:
    path: str
    is_dir: bool
    name: str = ""
    children: list[TreeNode] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name:
            self.name = os.path.basename(self.path)


# Backward compatibility alias
Node = TreeNode
