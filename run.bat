@echo off
REM AnswerLens Run Script for Windows

REM Check if virtual environment exists
if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first to install AnswerLens.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment and run the app
call venv\Scripts\activate.bat
python app.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo [ERROR] Application encountered an error
    pause
)
