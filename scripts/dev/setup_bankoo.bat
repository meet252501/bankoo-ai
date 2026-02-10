@echo off
title Bankoo AI - System Launcher
color 0b
cls

echo ===================================================
echo          BANKOO AI: SYSTEM INITIALIZATION
echo ===================================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is NOT installed or not in PATH.
    echo     Please install Python 3.10+ from python.org
    pause
    exit
)

:: 2. Install Dependencies
echo [*] Checking Dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [!] Failed to install dependencies.
    pause
    exit
)

:: 3. Check FFmpeg (Crucial for Voice)
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] WARNING: FFmpeg is NOT found in PATH!
    echo     Moltbot Voice features will NOT work without FFmpeg.
    echo     Please install FFmpeg and add it to your PATH.
    echo.
    pause
)

:: 4. Launch
cls
echo ===================================================
echo          🦞 MOLTBOT ASCENSION SYSTEM
echo ===================================================
echo.
echo [*] Launching Main Core...
start "Bankoo Core" cmd /k python bankoo_launcher.py

echo.
echo [*] Systems Active. You may close this window.
timeout /t 5
exit
