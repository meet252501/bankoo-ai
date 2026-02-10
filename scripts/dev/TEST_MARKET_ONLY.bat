@echo off
color 0d
title MARKET WIDGET PRO TEST
cls

echo ========================================================
echo      MARKET WIDGET - ISOLATED TEST PROTOCOL
echo ========================================================
echo.

echo 🔍 Running Market Mechanics Tests (test_market_widget.py)...
python test_market_widget.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ TESTS FAILED! check error output above.
) else (
    echo.
    echo ✅ MARKET ENGINE OPERATIONAL.
)

echo.
pause
