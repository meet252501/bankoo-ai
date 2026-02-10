@echo off
setlocal
echo ==========================================
echo    BANKOO AI - GITHUB PUSH AUTOMATION
echo ==========================================
echo.

:: 1. Initialize if needed
if not exist ".git" (
    echo [!] Initializing new Git repository...
    git init
    git branch -M main
)

:: 2. Check remote
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] Setting remote to: https://github.com/meet252501/bankoo-ai.git
    git remote add origin https://github.com/meet252501/bankoo-ai.git
) else (
    echo.
    echo [!] Remote already exists. Updating to ensure correctness...
    git remote set-url origin https://github.com/meet252501/bankoo-ai.git
)

:: 3. Add files - FORCE add everything
echo.
echo [1/3] Adding all files...
git add .

:: 4. Commit
echo.
echo [2/3] Committing changes...
git commit -m "feat: initial release of Bankoo AI v2.0"

:: 5. Push
echo.
echo [3/3] Pushing to GitHub...
git push -u origin main

echo.
echo ==========================================
echo    DONE! Check your repo at:
echo    https://github.com/meet252501/bankoo-ai
echo ==========================================
pause
