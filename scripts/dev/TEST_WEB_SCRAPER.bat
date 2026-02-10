@echo off
echo ================================================
echo  WEB SCRAPER STUDIO - TEST LAUNCHER
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
python -c "import requests, bs4, lxml" >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Required packages not found
    echo Installing dependencies...
    pip install requests beautifulsoup4 lxml
)

echo [2/3] Checking if Bankoo is running...
curl -s http://127.0.0.1:5001 >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Bankoo server is not running!
    echo Please start Bankoo first (START_BANKOO.bat)
    echo.
    echo Press any key to run tests anyway (some will fail)...
    pause >nul
)

echo [3/3] Running comprehensive tests...
echo.
python test_web_scraper.py

echo.
echo ================================================
echo Test results saved to: test_results.json
echo ================================================
echo.
pause
