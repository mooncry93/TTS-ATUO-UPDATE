#!/bin/bash
# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "===================================================================="
echo "           DIGITAL_TTS BY MR.THY - STARTING APPLICATION"
echo "===================================================================="

# Check if local virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "[LAUNCH] Activating virtual environment..."
    source venv/bin/activate
fi

# Run the app
python3 run_all.py

if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Application closed with errors."
    echo "Press Enter to exit..."
    read
fi
