import re
import os
from collections import defaultdict
from core.utils.file_reader import read_text_file
from state.app_state import AppState


def _get_rel_path(p: str) -> str:
    try:
        if AppState.project_root:
            return os.path.relpath(p, AppState.project_root).replace("\\", "/")
        return os.path.basename(p)
    except Exception:
        return os.path.basename(p)


# Hardware and External Integrations Patterns
PATTERNS = {
    "Thermal / ESC-POS Printing": [
        re.compile(r'navigator\.bluetooth\b', re.IGNORECASE),
        re.compile(r'navigator\.usb\b', re.IGNORECASE),
        re.compile(r'navigator\.serial\b', re.IGNORECASE),
        re.compile(r'\\x1b|\\x1d|ESC_POS|Printer|thermal', re.IGNORECASE),
        re.compile(r'window\.print\b', re.IGNORECASE)
    ],
    "Barcode & Camera Scanner": [
        re.compile(r'BarcodeDetector\b', re.IGNORECASE),
        re.compile(r'navigator\.mediaDevices\.getUserMedia\b', re.IGNORECASE),
        re.compile(r'barcode|scanner|imeiScanner', re.IGNORECASE)
    ],
    "Offline Storage (IndexedDB)": [
        re.compile(r'indexedDB\.open\b', re.IGNORECASE),
        re.compile(r'createObjectStore\b', re.IGNORECASE),
        re.compile(r'IDBTransaction\b', re.IGNORECASE),
        re.compile(r'offlineStore|localForage', re.IGNORECASE)
    ],
    "PWA & Service Worker": [
        re.compile(r'navigator\.serviceWorker\b', re.IGNORECASE),
        re.compile(r'caches\.open\b', re.IGNORECASE),
        re.compile(r'cache\.addAll\b', re.IGNORECASE),
        re.compile(r'self\.addEventListener\s*\(\s*["\']install["\']', re.IGNORECASE),
        re.compile(r'self\.addEventListener\s*\(\s*["\']fetch["\']', re.IGNORECASE)
    ],
    "Communication (WhatsApp / SMS / Email)": [
        re.compile(r'(?:api\.whatsapp\.com|wa\.me)', re.IGNORECASE),
        re.compile(r'mailto:', re.IGNORECASE),
        re.compile(r'sms:', re.IGNORECASE),
        re.compile(r'communicationService|sendInvoiceWhatsApp', re.IGNORECASE)
    ],
    "Local Device State (LocalStorage / Session)": [
        re.compile(r'localStorage\.(getItem|setItem|removeItem)\b', re.IGNORECASE),
        re.compile(r'sessionStorage\.(getItem|setItem|removeItem)\b', re.IGNORECASE)
    ]
}


def extract_hardware_services(tree_root):
    """
    Analyzes hardware peripherals, offline sync, PWA lifecycle, and external communication integrations.
    """
    findings = defaultdict(lambda: defaultdict(list))

    def walk(node):
        if not node.is_dir and node.name.endswith((".js", ".ts", ".html")):
            try:
                code = read_text_file(node.path)
            except Exception:
                return

            rel_file = _get_rel_path(node.path)

            for category, regex_list in PATTERNS.items():
                for rgx in regex_list:
                    matches = rgx.findall(code)
                    if matches:
                        findings[category][rel_file].append(rgx.pattern)

        for c in getattr(node, "children", []):
            walk(c)

    walk(tree_root)

    lines = []
    lines.append("=" * 60)
    lines.append("HARDWARE PERIPHERALS & EXTERNAL INTEGRATIONS AUDIT")
    lines.append("=" * 60)
    lines.append("")

    for cat, files_dict in sorted(findings.items()):
        lines.append(f"## {cat}")
        lines.append(f"• Active Implementations: {len(files_dict)} files")
        lines.append("")
        for f, patterns in sorted(files_dict.items()):
            lines.append(f"  • `{f}`")
            # Show simplified pattern tags
            clean_patterns = set()
            for p in patterns:
                # Clean up regex syntax for presentation
                clean_patterns.add(p.replace(r'\b', '').replace('\\', ''))
            lines.append(f"    - Signatures: {', '.join(sorted(list(clean_patterns))[:4])}")
        lines.append("")

    if not findings:
        lines.append("No specialized hardware or offline peripheral APIs detected.")

    lines.append("=" * 60)
    lines.append("AI AUDIT RECOMMENDATION FOR HARDWARE & OFFLINE:")
    lines.append("1. Verify Bluetooth reconnection handlers on mobile browser drops.")
    lines.append("2. Ensure ESC/POS thermal text alignments adhere to 58mm vs 80mm paper widths.")
    lines.append("3. Check IndexedDB schema version migrations to prevent client-side data loss.")
    lines.append("4. Confirm ServiceWorker cache-invalidation on new production deployments.")
    lines.append("=" * 60)

    return "\n".join(lines)
