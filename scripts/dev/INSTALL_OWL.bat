@echo off
echo ========================================
echo   BANKOO AI - OWL INTEGRATION SETUP
echo ========================================
echo.

echo [1/3] Installing CAMEL Framework...
pip install camel-ai[all] --quiet

echo.
echo [2/3] Installing Additional Dependencies...
pip install playwright --quiet

echo.
echo [3/3] Installing Playwright Browsers (Optional)...
echo NOTE: This downloads ~200MB of browser binaries
echo Press Ctrl+C to skip, or any key to continue...
pause >nul
playwright install chromium

echo.
echo ========================================
echo   INSTALLATION COMPLETE!
echo ========================================
echo.
echo OWL Multi-Agent Mode is now available in Bankoo.
echo Say: "Bankoo, autonomously [task]" to use it.
echo.
pause
