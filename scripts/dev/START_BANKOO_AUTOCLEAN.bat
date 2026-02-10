@echo off
title Bankoo AI - Auto-Clean Launcher
color 0b

echo ========================================================
echo       BANKOO AI - AUTO-CLEAN LAUNCHER
echo ========================================================
echo.

echo [1/3] Clearing Python cache for fresh startup...
del /s /q __pycache__ >nul 2>&1
del /s /q *.pyc >nul 2>&1
echo     [OK] Cache cleared

echo [2/3] Starting Bankoo AI...
python bankoo_launcher.py

echo [3/3] Cleanup complete on exit
pause
