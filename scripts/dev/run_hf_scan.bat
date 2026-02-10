@echo off
title Hugging Face Model Scanner - Bankoo AI
color 0b
echo ---------------------------------------------------
echo      BANKOO AI - HUGGING FACE SCANNER TOOL
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
echo ⚠️  WARNING: MASSIVE SCAN MODE ENABLED
echo This will scan hundreds of models. Do not close the window.
echo Results saved to: good_models.txt
echo.

python scan_massive.py

echo.
pause
