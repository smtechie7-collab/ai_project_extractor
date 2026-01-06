import os
from core.risk_analyzer import detect_fragile_classes
from core.layer_violation_detector import detect_layer_violations
from core.missing_reference_detector import detect_missing_references


def export_risk_analysis(tree_root, project_root):
    os.makedirs("output", exist_ok=True)

    # -------- Fragile / God Classes --------
    fragile = detect_fragile_classes(tree_root)
    with open("output/R01_fragile_and_god_classes.txt", "w", encoding="utf-8") as f:
        f.write("### FRAGILE / GOD CLASSES ###\n")
        for item in fragile:
            rel = os.path.relpath(item["path"], project_root)
            f.write(
                f"\n--- FILE: {rel} | Lines: {item['lines']} | Roles: {item['roles']} ---\n"
            )
            f.write(item["content"])

    # -------- Layer Violations --------
    violations = detect_layer_violations(tree_root)
    with open("output/R02_layer_violation_report.txt", "w", encoding="utf-8") as f:
        f.write("### LAYER VIOLATIONS ###\n")
        for v in violations:
            rel = os.path.relpath(v["path"], project_root)
            f.write(
                f"\n--- FILE: {rel} ---\nVIOLATION: {v['violation']}\n"
            )
            f.write(v["content"])

    # -------- Missing References --------
    missing = detect_missing_references(tree_root)
    with open("output/R03_missing_or_dangling_references.txt", "w", encoding="utf-8") as f:
        f.write("### MISSING / DANGLING REFERENCES ###\n\n")
        for m in missing:
            f.write(f"- {m}\n")

    # -------- High Risk Async --------
    with open("output/R04_high_risk_async_and_transaction_zones.txt", "w", encoding="utf-8") as f:
        f.write(
            "### HIGH RISK ASYNC / TRANSACTION ZONES ###\n"
            "Refer to C04_async_flow_and_transactions.txt\n"
            "Focus on files combining async + DB + UI triggers.\n"
        )
