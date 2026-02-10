@echo off
color 0b
title BANKOO AI - FULL SYSTEM LAUNCHER & TEST
cls

echo ========================================================
echo      BANKOO AI - ULTIMATE STARTUP SEQUENCE
echo ========================================================
echo.

echo [1/3] 🔍 Running System Diagnostics (test_details.py)...
python test_details.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ TESTS FAILED! Please check the errors above.
    echo Press any key to continue ANYWAY or Close to abort...
    pause
) else (
    echo.
    echo ✅ ALL SYSTEMS NOMINAL.
)

echo.
echo [2/3] 🔌 Booting Backend Engine...
start "Bankoo Core" cmd /k "python bankoo_main.py"

echo.
echo [3/3] 💻 Launching User Interface...
timeout /t 3 >nul
explorer bankoo_ui.html

echo.
echo ========================================================
echo      🚀 BANKOO AI IS LIVE
echo ========================================================
echo.
pause
