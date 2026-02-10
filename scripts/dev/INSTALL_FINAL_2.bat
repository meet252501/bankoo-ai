@echo off
echo ============================================================
echo   BANKOO AI - INSTALL FINAL 2 LANGUAGES
echo ============================================================
echo.
echo Installing Java JDK and GCC to reach 14/14 languages!
echo.
pause

echo.
echo [1/2] Installing Java JDK (with javac compiler)...
echo Note: You already have JRE, this adds the compiler tools.
winget install -e --id Oracle.JDK.17 --accept-package-agreements --accept-source-agreements --force

echo.
echo [2/2] Installing TDM-GCC (Minimal C/C++ Compiler)...
winget install -e --id jmeubank.tdm-gcc --accept-package-agreements --accept-source-agreements --force

echo.
echo ============================================================
echo   INSTALLATION COMPLETE!
echo ============================================================
echo.
echo Next steps:
echo 1. Run FIX_SYSTEM_PATH.bat
echo 2. Restart your computer
echo 3. Run CHECK_RUNTIMES.bat to verify 14/14!
echo.
pause
