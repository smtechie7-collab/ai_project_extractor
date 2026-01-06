import subprocess
import os

class GitScanner:
    @staticmethod
    def is_git_repo(path):
        return os.path.exists(os.path.join(path, ".git"))

    @staticmethod
    def get_changed_files(repo_root):
        """
        Returns a set of absolute paths for:
        1. Unstaged changes (modified)
        2. Staged changes (added/modified)
        3. Untracked files (newly created)
        """
        try:
            # 1. Unstaged Changes
            cmd_unstaged = ["git", "diff", "--name-only"]
            out_unstaged = subprocess.check_output(cmd_unstaged, cwd=repo_root).decode().splitlines()

            # 2. Staged Changes (Ready to commit)
            cmd_staged = ["git", "diff", "--name-only", "--cached"]
            out_staged = subprocess.check_output(cmd_staged, cwd=repo_root).decode().splitlines()

            # 3. Untracked Files (New files not yet added)
            cmd_untracked = ["git", "ls-files", "--others", "--exclude-standard"]
            out_untracked = subprocess.check_output(cmd_untracked, cwd=repo_root).decode().splitlines()

            # Combine all
            all_files = set(out_unstaged + out_staged + out_untracked)
            
            # Convert to absolute paths and normalize separators
            abs_files = set()
            for f in all_files:
                full_path = os.path.join(repo_root, f).replace("/", os.sep)
                abs_files.add(full_path)
                
            return abs_files

        except Exception as e:
            print(f"Git Scan Error: {e}")
            return set()