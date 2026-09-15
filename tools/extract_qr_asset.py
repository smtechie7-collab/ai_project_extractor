"""
tools/extract_qr_asset.py
=========================
One-off utility: extracts the inline base64 sponsor QR from ``ui/main_window.py``
and writes it to ``assets/sponsor_qr.png`` so the blob no longer lives in source.

Run from the repository root:  python tools/extract_qr_asset.py
"""

from __future__ import annotations

import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN_WINDOW = ROOT / "ui" / "main_window.py"
OUT = ROOT / "assets" / "sponsor_qr.png"

B64_RE = re.compile(r'QR_DATA_BASE64\s*=\s*"([^"]+)"')


def main() -> int:
    if not MAIN_WINDOW.exists():
        print(f"[ERROR] not found: {MAIN_WINDOW}")
        return 1

    match = B64_RE.search(MAIN_WINDOW.read_text(encoding="utf-8", errors="ignore"))
    if not match:
        print("[SKIP] no inline QR_DATA_BASE64 found (already extracted?)")
        return 0

    data = base64.b64decode(match.group(1))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(data)
    print(f"[OK] wrote {OUT} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
