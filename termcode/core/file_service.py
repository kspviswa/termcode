"""File service for termcode"""
from pathlib import Path
from typing import Optional


class FileService:
    """Service for file operations"""

    @staticmethod
    def read_file(path: Path) -> str:
        """Read file contents"""
        try:
            return path.read_text(errors="ignore")
        except Exception:
            return ""

    @staticmethod
    def get_language(path: Path) -> str:
        """Detect language from file extension"""
        ext = path.suffix.lower()
        lang_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".jsx": "javascript",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".md": "markdown",
            ".html": "html",
            ".css": "css",
            ".sh": "bash",
            ".bash": "bash",
            ".zsh": "bash",
            ".toml": "toml",
            ".xml": "xml",
            ".sql": "sql",
            ".go": "go",
            ".rs": "rust",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "c",
            ".hpp": "cpp",
        }
        return lang_map.get(ext, "")
