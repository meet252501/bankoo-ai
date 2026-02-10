@echo off
title Bankoo AI - Polyglot Evaluator
color 0b

echo ==================================================
echo      BANKOO AI - MULTI-TIER EVALUATOR TOOL
echo ==================================================
echo.
echo [1/3] Checking Environment...

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.10+
    pause
    exit /b
)

echo [DONE] Python detected.
echo.
echo [2/3] Choose Evaluation Tier:
echo --------------------------------------------------
echo  1. Grandmaster Tier (Hardest Architecture)
echo  2. Intermediate Tier (Practical Utility)
echo --------------------------------------------------
set /p tier_choice="Enter choice (1 or 2): "

set TIER_FLAG=
if "%tier_choice%"=="2" (
    set TIER_FLAG=--tier intermediate
    echo [INFO] Selected: INTERMEDIATE TIER
) else (
    echo [INFO] Selected: GRANDMASTER TIER
)

echo.
echo [3/3] Installing Dependencies (if missing)...

:: Install critical libs required by assistant.py / api_hub.py
pip install pandas numpy requests colorama python-dotenv openai google-generativeai --quiet

echo [DONE] Dependencies ready.
echo.
echo [LAUNCH] Starting Auto-Evaluator...
echo.
echo [INFO] Sit back and watch the sparks fly! ⚡
echo.

python evaluate_grandmaster.py %TIER_FLAG%

echo.
echo ==================================================
echo      EVALUATION COMPLETE - Check Report
echo ==================================================
pause

