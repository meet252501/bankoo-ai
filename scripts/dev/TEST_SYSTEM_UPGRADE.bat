@echo off
setlocal
title BANKOO VALIDATION SUITE
echo ================================================
echo  BANKOO AI - ENHANCED VALIDATION SYSTEM
echo ================================================
echo.

:: Check for python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH!
    pause
    exit /b 1
)

:: Run validation
python validate_core.py

echo.
echo Press any key to exit...
pause >nul
