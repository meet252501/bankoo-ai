@echo off
title Bankoo AETHER - Neural IDE Launcher
color 0b

echo ======================================================
echo   ✨ BANKOO AETHER: HIGH-FIDELITY IDE
echo ======================================================
echo.

:: 1. Force kill any existing python instances to avoid port conflicts
echo [1/3] Flushing previous sessions...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 1 /nobreak >nul

:: 2. Start the Backend
echo [2/3] Initializing Neural Engine...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] ERROR: Python is not found in your PATH.
    echo [!] Please install Python from python.org and check "Add to PATH".
    pause
    exit /b
)
start "Bankoo Backend" python bankoo_main.py

:: 3. Wait for Port 5001 to become active
echo [3/3] Waiting for Engine calibration (Port 5001)...
set /a timeout=0
:waitloop
netstat -ano | findstr :5001 >nul
if %errorlevel% neq 0 (
    set /a timeout=%timeout%+1
    if %timeout% gtr 30 (
        echo.
        echo [!] ERROR: Backend failed to start on Port 5001.
        echo [!] Please run 'debug_aether.py' to find the issue.
        pause
        exit /b
    )
    echo     ... waiting for brain (%timeout%/30) ...
    timeout /t 1 /nobreak >nul
    goto waitloop
)

echo.
echo ✅ AETHER ENGINE IS ONLINE!
echo.

:: Launch the IDE
start http://localhost:5001/ide

echo [SUCCESS] Bankoo AETHER is running at http://localhost:5001/ide
echo [NOTE] Keep the "Bankoo Backend" window open.
echo.
pause
