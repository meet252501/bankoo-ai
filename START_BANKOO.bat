@echo off
cls
echo ==================================================
echo   BANKOO AI: STANDARD LAUNCHER
echo ==================================================
echo.

echo [STEP 1] Cleaning Workspace...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1
echo Done.
echo.

echo [STEP 2] Launching Bankoo AI...
python bankoo_launcher.py

echo.
echo ==================================================
echo   Session Ended.
echo ==================================================
pause
