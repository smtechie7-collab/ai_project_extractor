from dataclasses import dataclass, field
from typing import List


@dataclass
class TreeNode:
    name: str
    path: str
    is_dir: bool
    children: List["TreeNode"] = field(default_factory=list)
