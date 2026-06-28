@echo off
echo ====================================================================
echo             DIGITAL_TTS BY MR.THY - 1-CLICK SUPER SETUP
echo ====================================================================
echo.

:: Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to your system PATH.
    echo Please install Python 3.12.x from python.org
    echo Make sure to check the box "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Check Python version is 3.12
python -c "import sys; sys.exit(0 if sys.version_info[:2] == (3, 12) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python version mismatch.
    echo This application requires Python 3.12.x to run securely.
    echo Please install Python 3.12.x from python.org.
    echo.
    pause
    exit /b 1
)

:: Create Virtual Environment
echo [SETUP] Creating local Python Virtual Environment (venv)...
python -m venv venv
if %errorlevel% neq 0 (
    echo [WARNING] Failed to create virtual environment via python -m venv.
    echo Attempting to install directly onto system Python environment...
) else (
    echo [SETUP] Activating Python Virtual Environment...
    call venv\Scripts\activate.bat
)

:: Install / Update Pip
echo [SETUP] Updating Pip installer...
python -m pip install --upgrade pip

:: Run setup_env.py script
echo [SETUP] Running Super Setup & Installer script...
python setup_env.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Environment setup encountered errors. Please check the logs above.
    pause
    exit /b %errorlevel%
)

echo.
echo ====================================================================
echo [SUCCESS] 1-Click Setup completed successfully!
echo.
echo To run the application, double-click run_all.bat or run:
echo    python run_all.py
echo ====================================================================
echo.
pause
