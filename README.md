# Pyd — LaTeX DOCX Fixer

A desktop utility that converts LaTeX math expressions inside Microsoft Word `.docx` files into native, editable Office Math Markup Language (OMML) equations.

## Overview

Word documents that contain LaTeX math (e.g., papers exported from Overleaf, ArXiv, or Pandoc) display the raw LaTeX source text rather than rendered equations. Pyd parses the DOCX XML, finds inline (`$...$`) and display (`$$...$$`) LaTeX expressions, and replaces them with proper Word math objects that render and edit natively in Microsoft Word.

## Features

- **Inline & display math** — handles both `$...$` and `$$...$$` syntax
- **Formatting preservation** — retains bold, italic, font size, color, and other run-level formatting from the original LaTeX text
- **Standalone GUI** — minimal tkinter window; open a DOCX, get a `_fixed.docx` back
- **CI/CD** — GitHub Actions builds a Windows `.exe` on every push to `main`
- **Installer-ready** — Inno Setup script included for creating a setup executable

## How It Works

1. Opens the `.docx` (a ZIP archive) and reads `word/document.xml`.
2. Scans paragraph text for LaTeX math patterns via regex.
3. Converts each expression through a two-step pipeline:
   - **latex2mathml** — LaTeX source → MathML
   - **mathml2omml** — MathML → Office Math Markup Language (OMML)
4. Replaces the raw LaTeX text with the equivalent `<m:oMath>` or `<m:oMathPara>` XML elements.
5. Writes a new DOCX as `<original>_fixed.docx`.

## Requirements

- Python 3.12+
- Windows (for the packaged `.exe`; the Python script works cross-platform)

## Installation

### From source

```bash
git clone https://github.com/leethedev-him/Pyd.git
cd Pyd
pip install -r requirements.txt
python main.py
```

### Pre-built executable

Download the latest `LatexDocxFixer.exe` from the [Releases](https://github.com/leethedev-him/Pyd/releases) page (or grab the build artifact from the latest CI run).

Or run `build.bat` on Windows to produce your own executable.

## Usage

1. Run the application.
2. Click **Open DOCX** and select a `.docx` file containing LaTeX math.
3. The fixed file (`<original>_fixed.docx`) is saved in the same folder.
4. Open the new file in Microsoft Word — the equations should render natively.

## Building

### Executable (PyInstaller)

```bash
pip install pyinstaller
.\build.bat
```

The output is `dist/LatexDocxFixer.exe`.

### Installer (Inno Setup)

Open `installer.iss` in Inno Setup Compiler and compile, or use the CI pipeline which does this automatically.

## Project Structure

```
Pyd/
├── main.py               # GUI entry point (tkinter)
├── latex_docx.py         # Core LaTeX-to-OMML conversion engine
├── requirements.txt      # Python dependencies
├── build.bat             # Windows PyInstaller build script
├── installer.iss         # Inno Setup installer script
├── .github/workflows/    # GitHub Actions CI configuration
└── README.md
```

## Dependencies

| Package | Purpose |
|---|---|
| [latex2mathml](https://pypi.org/project/latex2mathml/) | LaTeX → MathML conversion |
| [mathml2omml](https://pypi.org/project/mathml2omml/) | MathML → OMML conversion |
| [lxml](https://pypi.org/project/lxml/) | XML parsing and manipulation |

## License

MIT
