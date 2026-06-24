[Setup]
AppName=LaTeX DOCX Fixer
AppVersion=1.0
AppPublisher=OpenCode
DefaultDirName={pf}\LaTeXDocxFixer
DefaultGroupName=LaTeX DOCX Fixer
OutputDir=.
OutputBaseFilename=LaTeXDocxFixer_Setup
UninstallDisplayIcon={app}\LatexDocxFixer.exe
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\LatexDocxFixer.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\LaTeX DOCX Fixer"; Filename: "{app}\LatexDocxFixer.exe"
Name: "{group}\Uninstall LaTeX DOCX Fixer"; Filename: "{uninstallexe}"

[UninstallRun]
Filename: "{app}\LatexDocxFixer.exe"; RunOnceId: "LatexDocxFixerUninstall"
