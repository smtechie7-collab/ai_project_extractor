"""
core/extractors/base.py
=======================
Extractor protocol and central registry for analysis phases.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from core.context import AnalysisContext


@runtime_checkable
class Extractor(Protocol):
    phase: str
    languages: tuple[str, ...]

    def run(self, ctx: AnalysisContext) -> str:
        ...


REGISTRY: dict[str, Extractor] = {}


def register(extractor: Extractor) -> Extractor:
    """Registers an extractor instance in the global registry."""
    REGISTRY[extractor.phase] = extractor
    return extractor


def get_extractor(phase: str) -> Extractor | None:
    """Retrieves an extractor by phase name."""
    return REGISTRY.get(phase)
