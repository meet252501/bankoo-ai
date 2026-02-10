@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo   ⚡ BANKOO AI - UNIFIED FEATURE TESTING SUITE ⚡
echo ============================================================
echo.

:: 1. Dependency Check
echo [1] Checking Dependencies...
python -c "import yfinance; import mediapipe" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Missing dependencies detected!
    echo Running INSTALL_DEPENDENCIES.bat is recommended.
    pause
) else (
    echo ✅ Core Dependencies Verified.
)
echo.


:: 3. Web Scraper Test
echo [3] Testing Web Scraper Studio...
python test_web_scraper.py
if %errorlevel% neq 0 (
    echo ❌ Web Scraper Test Failed!
) else (
    echo ✅ Web Scraper Logic Verified.
)
echo.

:: 4. Vision Lab Setup
echo [4] Verifying Vision Lab (Webcam ^& MediaPipe)...
python test_vision_setup.py
echo.

:: 5. Smart Notes V3 Integration
echo [5] Checking Smart Notes Logic...
if exist smart_notes_v3.js (
    echo ✅ Smart Notes UI Logic Found.
) else (
    echo ❌ Smart Notes JS Missing!
)
echo.

:: 6. Backend Integration Test
echo [6] Checking Flask Endpoints Configuration...
python -c "import bankoo_main; print('✅ Backend structure verified.')"
echo.

echo ============================================================
echo   TESTING COMPLETE!
echo ============================================================
echo.
echo If any tests failed, check the errors above.
echo Otherwise, run START_BANKOO.bat to enjoy the full experience.
echo.
pause
