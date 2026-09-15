"""
tools/strip_inline_qr.py
========================
Removes the inline `QR_DATA_BASE64 = "..."` blob from ui/main_window.py.
The sponsor QR is now loaded from assets/ (see app_meta.sponsor_qr_path()).

Run from the repository root:  python tools/strip_inline_qr.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN_WINDOW = ROOT / "ui" / "main_window.py"

BLOCK_RE = re.compile(
    r'#\s*Default QR Data \(Base64\)\s*\r?\n\s*QR_DATA_BASE64\s*=\s*"[^"]*"\s*\r?\n',
    re.MULTILINE,
)

REPLACEMENT = (
    "# Sponsor QR image is loaded from assets/ at runtime (see app_meta.sponsor_qr_path).\n"
)


def main() -> int:
    text = MAIN_WINDOW.read_text(encoding="utf-8")
    new_text, count = BLOCK_RE.subn(REPLACEMENT, text)

    if count == 0:
        print("[SKIP] inline QR blob not found (already removed?)")
        return 0

    MAIN_WINDOW.write_text(new_text, encoding="utf-8")
    removed = len(text) - len(new_text)
    print(f"[OK] removed inline QR blob ({removed} bytes) from {MAIN_WINDOW.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
