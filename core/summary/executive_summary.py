from state.output_registry import OutputRegistry


def build_executive_summary(project_name: str, language: str) -> str:
    outputs = OutputRegistry.all()

    lines = []
    lines.append("=" * 40)
    lines.append("EXECUTIVE PROJECT SUMMARY")
    lines.append("=" * 40)
    lines.append("")
    lines.append(f"Project       : {project_name}")
    lines.append(f"Language      : {language}")
    lines.append(f"Phases Run    : {len(outputs)}")
    lines.append("")

    for phase, content in outputs.items():
        size = len(content.splitlines())
        lines.append(f"- {phase}: {size} lines extracted")

    lines.append("")
    lines.append("ARCHITECTURAL NOTES")
    lines.append("-" * 40)

    if language == "kotlin":
        lines.append("• Android / Kotlin project detected")
        if "DI Graph" in outputs:
            lines.append("• Dependency Injection present")
        if "UI Map" in outputs:
            lines.append("• UI layer mapped (Compose / XML)")
        if "Risk Analysis" in outputs:
            lines.append("• Risk analysis performed")

    if language == "python":
        lines.append("• Python backend project")
        lines.append("• Module-wise source code extracted")

    lines.append("")
    lines.append("RECOMMENDED NEXT STEPS")
    lines.append("-" * 40)
    lines.append("• Review risk findings")
    lines.append("• Share module exports with AI for refactoring")
    lines.append("• Use graphs to validate architecture")

    return "\n".join(lines)
