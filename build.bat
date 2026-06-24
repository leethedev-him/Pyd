@echo off
pip install -r requirements.txt

for /f "delims=" %%i in ('python -c "import latex2mathml, os; print(os.path.join(os.path.dirname(latex2mathml.__file__), 'unimathsymbols.txt'))"') do set LATEX_DATA=%%i

pyinstaller --onefile --windowed ^
  --add-data "%LATEX_DATA%;latex2mathml" ^
  --hidden-import latex2mathml.symbols_parser ^
  --hidden-import latex2mathml.commands ^
  --hidden-import latex2mathml.tokenizer ^
  --hidden-import latex2mathml.walker ^
  --hidden-import latex2mathml.exceptions ^
  --name "LatexDocxFixer" main.py

echo.
echo Build complete. Executable is at dist\LatexDocxFixer.exe
pause
