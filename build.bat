@echo off
pip install -r requirements.txt
pyinstaller --onefile --windowed --name "LatexDocxFixer" main.py
echo.
echo Build complete. Executable is at dist\LatexDocxFixer.exe
pause
