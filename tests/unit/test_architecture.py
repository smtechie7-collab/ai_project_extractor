"""
tests/unit/test_architecture.py
===============================
Unit tests for core architecture abstractions (ScanConfig, AnalysisContext, Extractor registry).
"""

from __future__ import annotations

from pathlib import Path

from core.config import ScanConfig
from core.context import AnalysisContext
from core.extractors.base import Extractor, REGISTRY, get_extractor, register
from core.summary.executive_summary import ExecutiveSummary
from core.summary.executive_summary_v2 import ExecutiveSummaryV2
from models.tree_node import Node, TreeNode


def test_scan_config_immutability():
    config = ScanConfig(project_root=Path("/sample"), language="python")
    assert config.language == "python"
    assert config.max_file_kb == 500

    # Frozen dataclass should reject modification
    try:
        config.language = "kotlin"  # type: ignore
        assert False, "ScanConfig must be frozen"
    except Exception:
        pass


def test_analysis_context_init():
    config = ScanConfig(project_root=Path("/sample"), language="cpp")
    node = TreeNode(path="/sample", is_dir=True)
    ctx = AnalysisContext(config=config, tree_root=node)

    assert ctx.language == "cpp"
    assert ctx.project_root.replace("\\", "/") == "/sample"
    assert ctx.tree_root is node


def test_tree_node_auto_name():
    node = Node(path="/path/to/my_file.py", is_dir=False)
    assert node.name == "my_file.py"
    assert not node.is_dir


def test_extractor_registry():
    class DummyExtractor:
        phase = "Dummy Phase"
        languages = ("python", "cpp")

        def run(self, ctx: AnalysisContext) -> str:
            return f"Processed {ctx.language}"

    dummy = DummyExtractor()
    assert isinstance(dummy, Extractor)

    register(dummy)
    retrieved = get_extractor("Dummy Phase")
    assert retrieved is dummy


def test_executive_summary_unified():
    # Verify backward compatible alias
    assert ExecutiveSummary is ExecutiveSummaryV2

    result = ExecutiveSummary.build("test_proj", [], [])
    assert "AI CONTEXT ARCHITECTURAL AUDIT" in result
    assert "TEST_PROJ" in result
