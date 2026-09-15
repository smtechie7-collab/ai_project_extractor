"""
core/extractors/generic
=======================
Language-neutral extractors used for:

* ``cpp`` (C / C++) profiles,
* the ``all`` (All Languages) profile,
* ``java`` for the phases Kotlin-specific extractors cannot serve,
* any language/profile that has no dedicated extractor.

These exist so that an unsupported profile never silently produces misleading
Python-derived output (previously the catch-all ``else`` branch in
``ui/main_window.py`` reused the Python exporters).
"""

from .ai_code_exporter import export_generic_ai_code
from .call_graph import export_generic_call_graph
from .code_exporter import export_generic_modules
from .risk_analyzer import analyze_generic_risks

__all__ = [
    "export_generic_modules",
    "export_generic_ai_code",
    "analyze_generic_risks",
    "export_generic_call_graph",
]
