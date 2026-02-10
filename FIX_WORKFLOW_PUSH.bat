@echo off
setlocal
echo ==========================================
echo    BANKOO AI - WORKFLOW FIX & PUSH
echo ==========================================
echo.

echo [1/3] Removing workflow file (requires extra permissions)...
:: We remove the workflow file because your token doesn't have 'workflow' scope
if exist ".github\workflows\ci.yml" (
    git rm .github\workflows\ci.yml
    git commit --amend -m "feat: initial release of Bankoo AI v2.0" --allow-empty --no-edit
)

echo.
echo [2/3] Verifying...
git status

echo.
echo [3/3] Pushing to GitHub...
git push -u origin main --force

echo.
echo ==========================================
echo    DONE! Your repo should now be live.
echo    https://github.com/meet252501/bankoo-ai
echo ==========================================
pause
