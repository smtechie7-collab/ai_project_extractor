import os
import zipfile

class OutputRegistry:
    _outputs = {}

    @classmethod
    def clear(cls):
        cls._outputs.clear()

    @classmethod
    def add(cls, phase, content):
        cls._outputs[phase] = content

    # 🔥 FIX: Added missing 'get' method
    @classmethod
    def get(cls, phase):
        return cls._outputs.get(phase, "")

    @classmethod
    def export_selected(cls, folder, phase):
        if phase not in cls._outputs:
            return

        # Sanitize filename
        safe_name = phase.lower().replace(" ", "_").replace("(", "").replace(")", "")
        path = os.path.join(folder, f"{safe_name}.txt")

        with open(path, "w", encoding="utf-8") as f:
            f.write(cls._outputs[phase])

    @classmethod
    def export_all(cls, folder):
        for phase, content in cls._outputs.items():
            safe_name = phase.lower().replace(" ", "_").replace("(", "").replace(")", "")
            path = os.path.join(folder, f"{safe_name}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

    @classmethod
    def export_markdown(cls, folder):
        path = os.path.join(folder, "project_context.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write("# AI Project Context\n\n")
            for phase, content in cls._outputs.items():
                f.write(f"## {phase}\n")
                f.write("```text\n")
                f.write(content)
                f.write("\n```\n\n")

    @classmethod
    def export_zip(cls, zip_path):
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for phase, content in cls._outputs.items():
                safe_name = phase.lower().replace(" ", "_").replace("(", "").replace(")", "") + ".txt"
                zipf.writestr(safe_name, content)