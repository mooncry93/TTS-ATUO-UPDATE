@echo off
setlocal
cd /d "%~dp0"

if not exist "voxcpm_runtime\python.exe" (
  echo Missing: voxcpm_runtime\python.exe
  echo This portable folder is incomplete.
  pause
  exit /b 1
)

"voxcpm_runtime\python.exe" "VoxCPM2_GUI.py"

