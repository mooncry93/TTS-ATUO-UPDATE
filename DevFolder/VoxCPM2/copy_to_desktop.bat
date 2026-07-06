@echo off
setlocal
cd /d "%~dp0"

set "TARGET=C:\Users\%USERNAME%\Desktop\VoxCPM2"
echo Copying portable VoxCPM2 folder to:
echo   %TARGET%
echo.

if exist "%TARGET%" (
  echo Deleting old folder...
  rmdir /s /q "%TARGET%"
)

mkdir "%TARGET%" >nul 2>&1

echo Copying files (this can take a long time because the model is large)...
robocopy "%~dp0" "%TARGET%" /E /NFL /NDL /NJH /NJS /NP

echo.
echo Done. You can run:
echo   %TARGET%\start_voxcpm2_gui.bat
pause

