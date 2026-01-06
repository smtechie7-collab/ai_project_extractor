def classify_kotlin_role(file_name: str) -> str:
    name = file_name.lower()

    if "viewmodel" in name:
        return "viewmodel"
    if "screen" in name or "page" in name or "fragment" in name:
        return "ui"
    if "activity" in name:
        return "ui"
    if "usecase" in name:
        return "domain"
    if "repository" in name:
        return "data"
    if "dao" in name or "entity" in name:
        return "db"
    if "di" in name or "module" in name:
        return "di"

    return "other"
