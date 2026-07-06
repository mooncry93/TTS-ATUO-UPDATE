@echo off
setlocal
cd /d "%~dp0"

if not exist "voxcpm_runtime\python.exe" (
  echo Missing: voxcpm_runtime\python.exe
  pause
  exit /b 1
)

echo Installing PyQt5 into this portable runtime...
echo Note: this needs internet access (or you must provide offline wheels).
echo.

"voxcpm_runtime\python.exe" -m pip install --upgrade pip
"voxcpm_runtime\python.exe" -m pip install PyQt5

echo.
echo Done. You can now run:
echo   start_voxcpm2_gui.bat
pause

