@echo off
echo ========================================
echo   Bankoo AI - Easy Setup Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

echo Python detected!
echo.
echo Installing PyQt5 (if not already installed)...
python -m pip install PyQt5 --quiet

echo.
echo Launching Bankoo Setup Wizard...
python installer\setup_wizard.py

pause
