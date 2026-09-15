"""
tests/unit/test_generic_extractors.py
====================================
Unit tests for generic language extractors (C++, All, Fallbacks).
"""

from __future__ import annotations

from pathlib import Path

from core.extractors.generic import (
    analyze_generic_risks,
    export_generic_ai_code,
    export_generic_call_graph,
    export_generic_modules,
)
from core.scanner import scan_directory
from state.app_state import AppState


def test_generic_extractors_run_on_cpp_tree(sample_repo: Path):
    AppState.project_root = str(sample_repo)
    AppState.selected_language = "cpp"

    tree = scan_directory(str(sample_repo))

    # 1. Module export
    modules_out = export_generic_modules(tree)
    assert "MODULE CLASSIFICATION" in modules_out
    assert "cpp" in modules_out

    # 2. AI code export
    ai_out = export_generic_ai_code(tree)
    assert "cpp_src" in ai_out

    # 3. Call graph
    call_out = export_generic_call_graph(tree)
    assert ("Call Graph" in call_out or "No cross-file call relationships" in call_out)

    # 4. Risk analysis
    risk_out = analyze_generic_risks(tree)
    assert "GENERIC RISK & CODE QUALITY ANALYSIS" in risk_out
