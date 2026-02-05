@echo off
REM AnswerLens Setup Script for Windows
REM This script creates a virtual environment and installs dependencies

echo ============================================
echo    AnswerLens - Setup Script
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version

echo.
echo [2/4] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)

echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [4/4] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ============================================
echo    Setup Complete!
echo ============================================
echo.
echo To run AnswerLens:
echo    1. Run: run.bat
echo    OR
echo    2. Double-click run.bat
echo.
echo To activate the virtual environment manually:
echo    venv\Scripts\activate
echo.
pause
