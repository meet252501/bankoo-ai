@echo off
color 0A
title Bankoo AI - Diagnostic Launch

echo ============================================================
echo          BANKOO AI: DIAGNOSTIC LAUNCHER v3.6
echo ============================================================
echo.

REM Check if Python is available
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ and add it to your system PATH.
    pause
    exit /b 1
)
python --version
echo [OK] Python detected
echo.

REM Check if port 5001 is already in use
echo [2/4] Checking if port 5001 is available...
netstat -ano | findstr ":5001" >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Port 5001 is already in use. Attempting to kill the process...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5001"') do taskkill /F /PID %%a >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo [OK] Port cleared
) else (
    echo [OK] Port 5001 is available
)
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Check if bankoo_main.py exists
echo [3/4] Checking for bankoo_main.py...
if not exist "bankoo_main.py" (
    color 0C
    echo [ERROR] bankoo_main.py not found in current directory!
    echo Current directory: %CD%
    pause
    exit /b 1
)
echo [OK] bankoo_main.py found
echo.

REM Launch Bankoo with full error visibility
echo [4/4] Starting Bankoo AI...
echo ============================================================
echo.
color 0B
echo Starting Bankoo AI Native Engine...
echo All errors will be displayed below:
echo.
echo ============================================================
echo.

REM Run Python with unbuffered output to see errors immediately
python -u bankoo_main.py 2>&1

REM Check exit code
if errorlevel 1 (
    color 0C
    echo.
    echo ============================================================
    echo [ERROR] Bankoo AI exited with an error!
    echo Exit code: %ERRORLEVEL%
    echo ============================================================
    echo.
    echo Common fixes:
    echo 1. Check if all dependencies are installed: pip install -r requirements.txt
    echo 2. Check if API keys are configured in config.py
    echo 3. Review the error messages above
    echo 4. Check if vosk model is present
    echo.
) else (
    color 0A
    echo.
    echo ============================================================
    echo [OK] Bankoo AI closed successfully
    echo ============================================================
    echo.
)

echo.
echo ==================================================
echo   Session Ended.
echo ==================================================
pause
