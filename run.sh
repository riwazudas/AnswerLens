#!/bin/bash
# AnswerLens Run Script for Linux/macOS

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run ./setup.sh first to install AnswerLens."
    echo ""
    exit 1
fi

# Activate virtual environment and run the app
source venv/bin/activate
python app.py
