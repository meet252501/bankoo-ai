@echo off
echo ========================================
echo Bankoo AI - Unified Integration Setup
echo ========================================
echo.

echo [1/4] Installing Python dependencies...
pip install -r requirements_moltbot.txt

echo.
echo [2/4] Installing Playwright browsers...
playwright install chromium

echo.
echo [3/4] Installing Moltbot dependencies...
cd "C:\Users\Meet Sutariya\.gemini\antigravity\scratch\molten_bridge"
call pnpm install

echo.
echo [4/4] Creating skills directory...
cd "C:\Users\Meet Sutariya\Desktop\final banko.ai"
if not exist "skills" mkdir skills

echo.
echo ========================================
echo ✅ Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Configure Moltbot platforms in molten_bridge\.env
echo 2. Run START_BANKOO_AUTOCLEAN.bat to launch
echo.
pause
