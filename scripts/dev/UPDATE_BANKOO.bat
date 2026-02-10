@echo off
echo ==================================================
echo   BANKOO: HARD RESET & UPDATE
echo ==================================================
echo.
echo [1/3] Stopping all Bankoo processes...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM cmd.exe /T 2>nul

echo [2/3] Waiting for cleanup...
timeout /t 3 /nobreak >nul

echo [3/3] Starting FRESH Server...
start "Bankoo Server" cmd /k "python bankoo_launcher.py"

echo.
echo ==================================================
echo   UPDATE COMPLETE!
echo   The server is now running the latest code.
echo.
echo   Please wait 10 seconds, then run:
echo   test_smart_notes_full.bat
echo ==================================================
pause
