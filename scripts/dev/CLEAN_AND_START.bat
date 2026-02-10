@echo off
cls
echo ==================================================
echo   BANKOO AI: FORCE CLEAN & START
echo ==================================================
echo.
echo [1/3] Killing all Python processes (Force)...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM Bankoo.exe /T 2>nul
echo Done.

echo.
echo [2/3] Checking Port 5001...
netstat -ano | findstr :5001
if %errorlevel% equ 0 (
    echo [WARNING] Port 5001 is STILL in use by a stubborn process.
    echo Please identify the PID above and kill it in Task Manager.
    echo Or just try running this script again.
    pause
) else (
    echo [OK] Port 5001 is free.
)

echo.
echo [3/3] Launching Server...
start "Bankoo Core" cmd /c "python bankoo_launcher.py & pause"

echo.
echo ==================================================
echo   Server Launching...
echo   Please wait 15 seconds, then run TEST_FULL_SYSTEM.bat
echo ==================================================
pause
