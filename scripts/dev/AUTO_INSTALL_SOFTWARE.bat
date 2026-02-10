@echo off
echo ============================================================
echo   BANKOO AI - Ultimate Software Installer
echo ============================================================
echo.
echo This will use PowerShell to download specific runtimes for ALL supported languages:
echo.
echo   [1] Node.js (JavaScript/TypeScript)
echo   [2] Java JDK 17 (Java)
echo   [3] XAMPP (PHP + MySQL + Apache)
echo   [4] .NET 8 SDK (C#)
echo   [5] Go (Golang)
echo   [6] Rust Toolchain
echo   [7] LLVM (C / C++ Compiler)
echo   [8] Ruby + Devkit
echo   [9] R Project (Data Science)
echo   [10] Git (Bash Shell)
echo   [11] Python Support
echo.
echo NOTE: You will need to click "Yes" on Windows UAC prompts.
echo.
pause

powershell -ExecutionPolicy Bypass -File install_runtimes.ps1
