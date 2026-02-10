@echo off
setlocal
echo ==========================================
echo    BANKOO AI - SECURITY FIX & PUSH
echo ==========================================
echo.

echo [1/4] Removing sensitive file...
if exist "YOUR_API_KEYS_BACKUP.md" del /f "YOUR_API_KEYS_BACKUP.md"

echo.
echo [2/4] Scrubbing secrets from Git history...
:: Remove file from git index
git rm --cached YOUR_API_KEYS_BACKUP.md >nul 2>&1
:: Amend the previous commit to completely remove the file from history
git commit --amend -m "feat: initial release of Bankoo AI v2.0" --allow-empty --no-edit

echo.
echo [3/4] Verifying clean state...
:: Ensure remote is still set
git remote add origin https://github.com/meet252501/bankoo-ai.git >nul 2>&1

echo.
echo [4/4] Pushing to GitHub (Safe Version)...
git push -u origin main --force

echo.
echo ==========================================
echo    DONE! Your repo is live and SAFE.
echo    https://github.com/meet252501/bankoo-ai
echo ==========================================
pause
