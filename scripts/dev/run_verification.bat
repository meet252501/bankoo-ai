@echo off
title Bankoo Verification Tool
color 0A

echo ---------------------------------------------------
echo      BANKOO AI - SYSTEM INTEGRITY CHECK
echo ---------------------------------------------------
echo 🔧 FORCING DEPENDENCY INSTALLATION...
pip install --upgrade huggingface_hub requests
if %errorlevel% neq 0 (
    echo ❌ PIP INSTALL FAILED! Please run 'pip install huggingface_hub' manually.
    pause
    exit
)
echo ✅ Dependencies ready.

echo.
echo 🕵️‍♀️  Scanning all AI Council Members...
echo.

python verify_system_integrity.py

echo.
pause
