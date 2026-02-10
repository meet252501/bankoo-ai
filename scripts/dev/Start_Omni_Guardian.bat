@echo off
TITLE Bankoo Omni-Guardian Launcher 🦞
color 0b

echo ===================================================
echo    BANKOO AI + MOLTBOT OMNI-GUARDIAN SYSTEM
echo ===================================================
echo.
echo [1/2] Starting Bankoo Native UI (PyWebView)...
start "Bankoo Native UI" cmd /k "python bankoo_launcher.py"
echo    - UI Window Launching...

timeout /t 3 >nul

echo.
echo [2/2] Summoning Moltbot Guardian...
start "Moltbot Omni-Guardian" cmd /k "python bankoo_bridge.py"
echo    - Guardian Summoned.

echo.
echo ===================================================
echo    SYSTEM ONLINE. MINIMIZE THIS WINDOW.
echo ===================================================
timeout /t 10
exit
