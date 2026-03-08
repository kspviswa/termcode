"""Git integration for termcode"""
import subprocess
from pathlib import Path
from typing import Optional


class GitIntegration:
    """Simple git status integration"""

    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.git_path = root_path / ".git"
        self.status_cache: dict[str, str] = {}
        self.is_git_repo = self.git_path.is_dir()
        if self.is_git_repo:
            self._load_status()

    def _load_status(self):
        """Load git status using subprocess"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.root_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if not line:
                        continue
                    status = line[:2]
                    filepath = line[3:].strip()
                    self.status_cache[filepath] = status
        except Exception:
            pass

    def get_status(self, path: Path) -> Optional[str]:
        """Get git status for a path"""
        if not self.is_git_repo:
            return None
        rel_path = path.relative_to(self.root_path)
        return self.status_cache.get(str(rel_path))
