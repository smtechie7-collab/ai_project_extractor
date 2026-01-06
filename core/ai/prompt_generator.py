def generate_ai_prompt(project_name, language, outputs):
    lines = []
    lines.append("=" * 60)
    lines.append("AI ARCHITECTURE PROMPT")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Project: {project_name}")
    lines.append(f"Language: {language}")
    lines.append("")
    lines.append("TASK FOR AI:")
    lines.append(
        "- Analyze the project architecture\n"
        "- Identify risks and anti-patterns\n"
        "- Suggest refactors WITHOUT breaking behavior\n"
        "- Recommend improvements module-wise\n"
    )
    lines.append("")

    for phase, content in outputs.items():
        lines.append("#" * 60)
        lines.append(f"SECTION: {phase.upper()}")
        lines.append("#" * 60)
        lines.append(content)
        lines.append("")

    return "\n".join(lines)
