@echo off
chcp 65001 >nul
color 0B
cls

echo ════════════════════════════════════════════════════════════
echo   SMART NOTES ADVANCED FEATURES - INSTALLER
echo ════════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

echo 📁 Current directory: %CD%
echo.

python install_notes_features.py

echo.
echo ════════════════════════════════════════════════════════════
echo.
pause
