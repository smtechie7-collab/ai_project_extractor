import os
import zipfile


class OutputRegistry:
    outputs = {}

    @classmethod
    def clear(cls):
        cls.outputs = {}

    @classmethod
    def add(cls, phase: str, content: str):
        cls.outputs[phase] = content

    @classmethod
    def get(cls, phase: str) -> str:
        return cls.outputs.get(phase, "")

    @classmethod
    def all(cls):
        return cls.outputs

    @classmethod
    def export_selected(cls, folder: str, phase: str):
        os.makedirs(folder, exist_ok=True)
        content = cls.outputs.get(phase)
        if content is None:
            return False

        safe = phase.replace(" ", "_").lower()
        path = os.path.join(folder, f"{safe}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    @classmethod
    def export_all(cls, folder: str):
        os.makedirs(folder, exist_ok=True)
        for phase, content in cls.outputs.items():
            safe = phase.replace(" ", "_").lower()
            path = os.path.join(folder, f"{safe}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

    @classmethod
    def export_zip(cls, zip_path: str):
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for phase, content in cls.outputs.items():
                safe = phase.replace(" ", "_").lower()
                zf.writestr(f"{safe}.txt", content)
