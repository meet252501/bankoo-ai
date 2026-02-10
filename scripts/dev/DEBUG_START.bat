@echo off
echo ========================================
echo   BANKOO DEBUG MODE - LAUNCHER
echo ========================================
echo.
echo Starting Backend...
echo If it crashes, this window will STAY OPEN so you can see the error!
echo.
set PYTHONUNBUFFERED=1
cd /d "%~dp0"

echo [DEBUG] Checking Python Environment...
where python
python -V

echo [DEBUG] Running Brain Health Check...
python TEST_BRAIN_LOAD.py
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ CRITICAL: BRAIN CHECK FAILED!
    echo The application is missing 'pandas' or other dependencies.
    echo.
    pause
    exit /b
)

echo.
echo [DEBUG] Starting Bankoo Main...
python bankoo_main.py
echo.
echo ========================================
echo   CRASH DETECTED! SEE ERROR ABOVE
echo ========================================
pause
