# Predefined prompts to wrap the context
# {content} will be replaced by the actual code/analysis

PROMPT_TEMPLATES = {
    "📋 Raw (No Prompt)": "{content}",
    
    "🐛 Find Bugs": (
        "Act as a Senior QA Engineer. Analyze the following code/architecture for:\n"
        "1. Logical errors\n"
        "2. Potential crashes (null pointers, exceptions)\n"
        "3. Edge cases handling\n\n"
        "CONTEXT:\n{content}"
    ),
    
    "🛡️ Security Audit": (
        "Act as a Security Researcher. Audit the following project context for vulnerabilities:\n"
        "1. Injection flaws (SQLi, XSS)\n"
        "2. Exposed secrets/keys\n"
        "3. Insecure dependencies or patterns\n\n"
        "CONTEXT:\n{content}"
    ),
    
    "🧹 Refactor Code": (
        "Act as a Clean Code Expert. Suggest refactoring for the following code to improve:\n"
        "1. Readability\n"
        "2. Performance\n"
        "3. Modularity (following SOLID principles)\n\n"
        "CONTEXT:\n{content}"
    ),
    
    "📖 Write Documentation": (
        "Act as a Technical Writer. Generate professional documentation (Markdown) for the following:\n"
        "- Module Purpose\n"
        "- Key Classes/Functions\n"
        "- Usage Examples\n\n"
        "CONTEXT:\n{content}"
    ),
    
    "👨‍🏫 Explain to Junior": (
        "Explain the following architecture/code in simple terms suitable for a Junior Developer.\n"
        "Use analogies where possible.\n\n"
        "CONTEXT:\n{content}"
    )
}