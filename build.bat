@echo off
echo Building CBZ-Merger.exe...
pyinstaller --onefile --windowed --name "CBZ-Merger" cbz_merger.py
echo.
if exist dist\CBZ-Merger.exe (
    echo Done! Output: dist\CBZ-Merger.exe
) else (
    echo Build failed -- check output above.
)
pause
