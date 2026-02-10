@echo off
echo ============================================================
echo   BANKOO AI - INSTALLING .NET SDK (C#)
echo ============================================================
echo.
echo Installing .NET SDK 8...
winget install -e --id Microsoft.DotNet.SDK.8 --accept-package-agreements --accept-source-agreements --force
echo.
echo ============================================================
echo   INSTALLATION COMPLETE
echo ============================================================
echo.
pause
