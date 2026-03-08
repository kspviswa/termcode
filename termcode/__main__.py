"""Main entry point for termcode"""
import sys
from pathlib import Path

from termcode.app import TermcodeApp


def main():
    """Main entry point for the termcode CLI."""
    # Get the directory to open (default to current directory)
    if len(sys.argv) > 1:
        path = Path(sys.argv[1]).resolve()
    else:
        path = Path.cwd()

    if not path.exists():
        print(f"Error: Path does not exist: {path}")
        sys.exit(1)

    if not path.is_dir():
        print(f"Error: Path is not a directory: {path}")
        sys.exit(1)

    # Run the TUI app
    app = TermcodeApp(root_path=path)
    app.run()


if __name__ == "__main__":
    main()
