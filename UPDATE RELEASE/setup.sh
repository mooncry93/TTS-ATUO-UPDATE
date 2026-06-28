#!/bin/bash
echo "===================================================================="
echo "           DIGITAL_TTS BY MR.THY - 1-CLICK SUPER SETUP"
echo "===================================================================="
echo

# Check Python installation
if ! command -v python3 &> /dev/null
# fallback to python
then
    if ! command -v python &> /dev/null
    then
        echo "[ERROR] Python is not installed. Please install Python 3.10+."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "[SETUP] Creating local Python Virtual Environment (venv)..."
$PYTHON_CMD -m venv venv
if [ $? -ne 0 ]; then
    echo "[WARNING] Failed to create virtual environment. Installing to current Python environment..."
else
    echo "[SETUP] Activating Python Virtual Environment..."
    source venv/bin/activate
fi

echo "[SETUP] Updating Pip installer..."
$PYTHON_CMD -m pip install --upgrade pip

echo "[SETUP] Running Super Setup & Installer script..."
$PYTHON_CMD setup_env.py

if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Environment setup encountered errors."
    exit 1
fi

echo
echo "===================================================================="
echo "[SUCCESS] 1-Click Setup completed successfully!"
echo
echo "To run the application, run:"
echo "   python3 run_all.py"
echo "===================================================================="
echo
