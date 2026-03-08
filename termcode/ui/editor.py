"""Editor widget for termcode"""
from pathlib import Path
from typing import Optional

from textual.widgets import Static, TextArea


class EditorPane(Static):
    """Text editor pane"""

    def __init__(self, file_path: Optional[Path] = None, **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self._editor: Optional[TextArea] = None

    def get_editor(self) -> TextArea:
        """Get the text area widget"""
        if self._editor is None:
            self._editor = self.query_one("#editor", TextArea)
        return self._editor

    def load_file(self, path: Path):
        """Load a file into the editor"""
        self.file_path = path

        from termcode.core.file_service import FileService
        content = FileService.read_file(path)

        editor = self.get_editor()
        editor.text = content
        editor.language = FileService.get_language(path)

        # Update header
        header = self.query_one(".editor-header", Static)
        header.update(f" {path.name}")

    def compose(self):
        """Compose the editor pane"""
        # Editor header
        if self.file_path:
            header_text = f" {self.file_path.name}"
        else:
            header_text = " No file open"
        yield Static(header_text, classes="editor-header")

        # Editor content
        yield TextArea(id="editor", language="", show_line_numbers=True)
