"""Main TUI application for termcode"""
from pathlib import Path
from typing import Optional

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Static, DirectoryTree, TextArea

from termcode.platform.git import GitIntegration
from termcode.ui.explorer import FileExplorer
from termcode.ui.statusbar import StatusBar


CSS = """
/* VSCode-inspired dark theme */
Screen {
    background: #1e1e1e;
    padding: 0;
}

/* Header - docked to top */
Header {
    dock: top;
    height: auto;
    padding: 0 2;
    background: #252526;
    color: #cccccc;
}

/* Main container */
#main-container {
    width: 100%;
    height: 1fr;
}

/* Sidebar */
#sidebar {
    width: 25%;
    height: 100%;
    background: #252526;
    border-right: solid #3c3c3c;
}

/* Sidebar header */
.sidebar-header {
    height: auto;
    background: #2d2d30;
    color: #858585;
    padding: 1 2;
    text-style: bold;
}

/* Tree container - explicit size for DirectoryTree */
#tree-container {
    width: 100%;
    height: 1fr;
}

/* Explorer tree */
DirectoryTree {
    width: 100%;
    height: 1fr;
    background: #252526;
    color: #cccccc;
}

/* Editor container */
#editor-pane {
    width: 75%;
    height: 100%;
    background: #1e1e1e;
}

/* Editor header */
.editor-header {
    height: auto;
    background: #2d2d30;
    color: #cccccc;
    padding: 1 2;
}

/* TextArea */
TextArea {
    width: 100%;
    height: 1fr;
    background: #1e1e1e;
    color: #cccccc;
    border: none;
}

/* Scrollbars */
ScrollBar {
    background: #2d2d30;
}

/* Status bar - docked to bottom */
#status-bar {
    dock: bottom;
    height: auto;
    padding: 0 2;
    background: #007acc;
}

#status-bar > * {
    color: #cccccc;
}
"""


class TermcodeApp(App):
    """Main TUI IDE application"""

    CSS = CSS

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+b", "toggle_sidebar", "Toggle Sidebar"),
        ("ctrl+s", "save_file", "Save"),
    ]

    def __init__(self, root_path: Path, **kwargs):
        super().__init__(**kwargs)
        self.root_path = root_path
        self.git_integration = GitIntegration(root_path)
        self.current_file: Optional[Path] = None
        self.original_content: str = ""
        self.is_modified: bool = False
        self.sidebar_visible = True

    def compose(self) -> ComposeResult:
        # Main header
        yield Header(show_clock=True)

        # Main content - Horizontal
        with Horizontal(id="main-container"):
            # Left sidebar
            with Vertical(id="sidebar"):
                yield Static("EXPLORER", classes="sidebar-header")
                # Use a Container to wrap DirectoryTree with explicit size
                with Vertical(id="tree-container"):
                    yield FileExplorer(str(self.root_path), git=self.git_integration)

            # Right - Editor pane
            with Vertical(id="editor-pane"):
                yield Static(" No file open", classes="editor-header")
                yield TextArea(id="editor", language="", theme="vscode_dark", show_line_numbers=True)

        # Status bar
        yield StatusBar(id="status-bar")

    def on_mount(self) -> None:
        """Initialize on mount"""
        tree = self.query_one(DirectoryTree)
        tree.focus()

    @on(TextArea.Changed)
    def on_editor_change(self, event: TextArea.Changed) -> None:
        """Handle editor content changes"""
        if self.current_file:
            self._update_modified_status()

    @on(DirectoryTree.FileSelected)
    def on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle file selection"""
        path = Path(event.path)
        if path.is_file() and path.exists():
            self.current_file = path
            self._load_file(path)

            # Update status bar
            status = self.query_one(StatusBar)
            status.file_opened(path)

    def _load_file(self, path: Path):
        """Load file into editor"""
        from termcode.core.file_service import FileService

        content = FileService.read_file(path)
        editor = self.query_one("#editor", TextArea)

        # Set language BEFORE content to enable syntax highlighting
        editor.language = FileService.get_language(path)
        editor.text = content

        # Track original content for dirty checking
        self.original_content = content
        self.is_modified = False

        # Update header
        header = self.query_one(".editor-header", Static)
        header.update(f" {path.name}")

    def _update_modified_status(self):
        """Update modified status in header"""
        editor = self.query_one("#editor", TextArea)
        self.is_modified = editor.text != self.original_content
        header = self.query_one(".editor-header", Static)
        if self.current_file:
            modified_marker = " *" if self.is_modified else ""
            header.update(f" {self.current_file.name}{modified_marker}")

    def action_save_file(self) -> None:
        """Save current file"""
        if not self.current_file:
            return

        editor = self.query_one("#editor", TextArea)
        try:
            self.current_file.write_text(editor.text)
            self.original_content = editor.text
            self.is_modified = False

            # Update header to remove modified marker
            header = self.query_one(".editor-header", Static)
            header.update(f" {self.current_file.name}")

            # Update status bar
            status = self.query_one(StatusBar)
            status.update_message("File saved")
        except Exception as e:
            self.notify(f"Failed to save: {e}", severity="error")

    def action_toggle_sidebar(self) -> None:
        """Toggle sidebar visibility"""
        sidebar = self.query_one("#sidebar")
        if self.sidebar_visible:
            sidebar.styles.display = "none"
            self.sidebar_visible = False
        else:
            sidebar.styles.display = "block"
            self.sidebar_visible = True
