@echo off
REM Run this on Windows 11 with Python 3.10+ installed.
pip install requests pillow pyinstaller
pyinstaller --onefile --windowed --name KawaiiMaidViewer app.py
echo.
echo Done! Your exe is in the dist folder: dist\KawaiiMaidViewer.exe
pause
