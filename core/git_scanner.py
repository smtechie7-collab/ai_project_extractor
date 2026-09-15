import os
import subprocess


class GitScanner:
    @staticmethod
    def is_git_repo(path):
        return os.path.exists(os.path.join(path, ".git"))

    @staticmethod
    def get_changed_files(repo_root: str) -> set[str]:
        """
        Returns a set of normalized absolute paths for:
        1. Unstaged changes (modified/deleted/added)
        2. Staged changes (staged in index)
        3. Untracked files (new files)

        Uses `git status --porcelain=v1 -z -uall` for binary-safe,
        unicode-safe, space-safe change detection in a single command.
        """
        if not GitScanner.is_git_repo(repo_root):
            return set()

        try:
            raw = subprocess.check_output(
                ["git", "status", "--porcelain=v1", "-z", "-uall"],
                cwd=repo_root,
                stderr=subprocess.DEVNULL,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, PermissionError):
            return set()

        abs_files: set[str] = set()
        parts = raw.split(b"\0")
        i = 0
        while i < len(parts):
            entry = parts[i]
            if not entry:
                i += 1
                continue

            if len(entry) >= 3:
                status = entry[:2].decode("latin-1", errors="ignore")
                rel_path = entry[3:].decode("utf-8", errors="replace")

                # If rename or copy (status R or C), next entry is the original path
                if status[0] in ("R", "C") or status[1] in ("R", "C"):
                    i += 1

                full_path = os.path.normpath(os.path.join(repo_root, rel_path))
                if os.path.exists(full_path) and os.path.isfile(full_path):
                    abs_files.add(full_path)
            i += 1

        return abs_files
