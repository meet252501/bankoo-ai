@echo off
echo ============================================================
echo   BANKOO AI - INSTALL ALL MISSING LANGUAGES
echo ============================================================
echo.
echo This will install 6 missing languages via 5 packages:
echo   [1] Java JDK (Java compiler)
echo   [2] Ruby
echo   [3] Git (includes Bash shell)
echo   [4] MinGW (GCC for C, G++ for C++)
echo   [5] TypeScript (via npm)
echo.
pause

echo.
echo [1/5] Installing Java JDK 17...
winget install -e --id Microsoft.OpenJDK.17 --accept-package-agreements --accept-source-agreements --force

echo.
echo [2/5] Installing Ruby...
winget install -e --id RubyInstallerTeam.RubyWithDevKit.3.2 --accept-package-agreements --accept-source-agreements --force

echo.
echo [3/5] Installing Git (Bash)...
winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements --force

echo.
echo [4/5] Installing MinGW (GCC/G++)...
winget install -e --id Mingw-w64.Mingw-w64 --accept-package-agreements --accept-source-agreements --force

echo.
echo [5/5] Installing TypeScript...
call npm install -g typescript ts-node

echo.
echo ============================================================
echo   INSTALLATION COMPLETE!
echo ============================================================
echo.
echo Next steps:
echo 1. Run FIX_SYSTEM_PATH.bat
echo 2. Restart your computer
echo 3. Run CHECK_RUNTIMES.bat to verify
echo.
pause
