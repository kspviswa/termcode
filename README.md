# termcode

A lightweight TUI IDE inspired by VSCode, built with Python and Textual.

## Features

- **File Explorer** - Browse files with git integration indicators
- **Syntax Highlighting** - Support for Python, JavaScript, TypeScript, JSON, YAML, Bash, and more
- **VSCode-inspired Dark Theme** - Familiar look and feel
- **Keyboard Shortcuts**
  - `Ctrl+B` - Toggle sidebar
  - `Ctrl+S` - Save file
  - `Ctrl+Q` - Quit

## Installation

```bash
uv tool install -e .
```

## Usage

```bash
termcode .
```

Open a directory to start editing files.

## Supported Languages

- Python
- JavaScript / TypeScript
- JSON, YAML, TOML
- HTML, CSS
- Markdown
- Go, Rust, SQL
- Bash/Zsh

## Requirements

- Python 3.14+
- textual >= 0.93.0
- tree-sitter (with language grammars)
