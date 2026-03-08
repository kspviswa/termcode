"""File explorer widget for termcode"""
from pathlib import Path
from typing import Optional

from textual.widgets import DirectoryTree, Static

from termcode.platform.git import GitIntegration


class FileIcon:
    """File type icons for the explorer"""

    @staticmethod
    def get_icon(path: Path, is_expanded: bool = False) -> str:
        if path.is_dir():
            return "📁" if is_expanded else "📂"
        ext = path.suffix.lower()
        icons = {
            ".py": "🐍",
            ".js": "📜",
            ".ts": "📘",
            ".tsx": "📘",
            ".jsx": "📜",
            ".json": "📋",
            ".md": "📝",
            ".yaml": "⚙️",
            ".yml": "⚙️",
            ".toml": "⚙️",
            ".txt": "📄",
            ".html": "🌐",
            ".css": "🎨",
            ".scss": "🎨",
            ".sh": "💻",
            ".bash": "💻",
            ".zsh": "💻",
            ".gitignore": "🔧",
            ".env": "🔐",
            "Dockerfile": "🐳",
        }
        if path.name == "Dockerfile":
            return "🐳"
        return icons.get(ext, "📄")


class FileExplorer(DirectoryTree):
    """File explorer widget with custom icons"""

    def __init__(self, path: str, git: Optional[GitIntegration] = None, **kwargs):
        super().__init__(path, **kwargs)
        self.git = git

    def filter_paths(self, paths: list[Path]) -> list[Path]:
        """Filter out hidden files and common ignore patterns"""
        filtered = []
        ignore_patterns = {
            ".git", "__pycache__", ".pytest_cache",
            "node_modules", ".venv", ".mypy_cache", ".ruff_cache"
        }
        for p in paths:
            if p.name.startswith(".") and p.name not in {".gitignore", ".env", ".bashrc", ".zshrc"}:
                continue
            if p.name in ignore_patterns:
                continue
            filtered.append(p)
        return sorted(filtered, key=lambda x: (not x.is_dir(), x.name.lower()))

    def get_label(self, path: Path, is_expanded: bool) -> str:
        """Get the label for a path with icon"""
        icon = FileIcon.get_icon(path, is_expanded)
        label = f"{icon} {path.name}"
        return label


class ExplorerSidebar(Static):
    """File explorer sidebar container"""

    DEFAULT_CSS = """
    ExplorerSidebar {
        width: 280;
        background: $surface;
    }
    """
