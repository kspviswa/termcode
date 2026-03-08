"""Status bar widget for termcode"""
from pathlib import Path
from typing import Optional

from textual.widgets import Static


class StatusBar(Static):
    """Status bar at the bottom of the screen"""

    DEFAULT_CSS = """
    StatusBar {
        dock: bottom;
        height: 1;
        background: $primary;
    }

    StatusBar > * {
        color: $text;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_file: Optional[Path] = None

    def compose(self):
        """Compose the status bar"""
        yield Static("termcode", id="status-left")
        yield Static("", id="status-right")

    def file_opened(self, path: Path):
        """Update status when a file is opened"""
        self.current_file = path
        left = self.query_one("#status-left", Static)
        left.update(f" {path.name}")

        right = self.query_one("#status-right", Static)
        right.update("UTF-8")

    def update_message(self, message: str, duration: float = 2.0):
        """Show a temporary message"""
        right = self.query_one("#status-right", Static)
        right.update(message)

        # Reset after duration
        self.set_timer(duration, lambda: self._reset_right())

    def _reset_right(self):
        """Reset right status to default"""
        if self.current_file:
            right = self.query_one("#status-right", Static)
            right.update("UTF-8")
