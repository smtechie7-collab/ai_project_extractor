from rules.role_rules import FOLDER_RULES, FILENAME_RULES, KEYWORD_RULES
import os

def classify_file(path: str, content: str) -> str:
    lower_path = path.lower()
    filename = os.path.basename(path)

    # --- 1. Python Specific Rules ---
    if filename.endswith(".py"):
        if filename == "__init__.py":
            return "INIT"
        if "django" in content or "flask" in content or "fastapi" in content:
            return "BACKEND_FRAMEWORK"
        if "def test_" in content or "class Test" in content:
            return "TEST"
        if "model" in lower_path or "schema" in lower_path:
            return "MODEL"
        if "service" in lower_path:
            return "SERVICE"
        if "utils" in lower_path or "helper" in lower_path:
            return "UTILS"
        if "import " in content and "from " in content: 
            return "MODULE" # Generic Python Module

    # --- 2. Folder-based rules (Standard) ---
    for folder, role in FOLDER_RULES:
        if f"/{folder}/" in lower_path or f"\\{folder}\\" in lower_path:
            return role

    # --- 3. Filename-based rules ---
    for token, role in FILENAME_RULES:
        if token in filename:
            return role

    # --- 4. Content-based rules ---
    for role, keywords in KEYWORD_RULES.items():
        for keyword in keywords:
            if keyword in content:
                return role

    return "UNKNOWN"