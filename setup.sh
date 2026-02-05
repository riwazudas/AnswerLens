#!/bin/bash
# AnswerLens Setup Script for Linux/macOS
# This script creates a virtual environment and installs dependencies

echo "============================================"
echo "   AnswerLens - Setup Script"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/4] Checking Python version..."
python3 --version

echo ""
echo "[2/4] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully!"
fi

echo ""
echo "[3/4] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[4/4] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo ""
echo "============================================"
echo "   Setup Complete!"
echo "============================================"
echo ""
echo "To run AnswerLens:"
echo "   1. Run: ./run.sh"
echo "   OR"
echo "   2. Run: source venv/bin/activate && python app.py"
echo ""
echo "To activate the virtual environment manually:"
echo "   source venv/bin/activate"
echo ""
