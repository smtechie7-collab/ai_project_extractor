import os
import hashlib
import json

CACHE_FILE = ".analysis_cache.json"


class PerformanceCache:
    def __init__(self, project_root):
        self.path = os.path.join(project_root, CACHE_FILE)
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def has_changed(self, file_path):
        mtime = os.path.getmtime(file_path)
        old = self.data.get(file_path)
        return not old or old["mtime"] != mtime

    def update(self, file_path, content):
        self.data[file_path] = {
            "mtime": os.path.getmtime(file_path),
            "hash": hashlib.md5(content.encode()).hexdigest(),
        }
