from rules.role_rules import FOLDER_RULES, FILENAME_RULES, KEYWORD_RULES
import os


def classify_file(path: str, content: str) -> str:
    lower_path = path.lower()

    # 1️⃣ Folder-based rules (highest priority)
    for folder, role in FOLDER_RULES:
        if f"/{folder}/" in lower_path or f"\\{folder}\\" in lower_path:
            return role

    filename = os.path.basename(path)

    # 2️⃣ Filename-based rules
    for token, role in FILENAME_RULES:
        if token in filename:
            return role

    # 3️⃣ Content-based rules
    for role, keywords in KEYWORD_RULES.items():
        for keyword in keywords:
            if keyword in content:
                return role

    return "UNKNOWN"
