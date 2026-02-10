@echo off
echo ============================================================
echo   BANKOO AI - RUNTIME ORGANIZER
echo ============================================================
echo.
echo This will:
echo  1. Find all language compilers/interpreters on your system
echo  2. Create shortcuts in 'portable_runtimes' folder
echo  3. Generate RUNTIME_MANIFEST.txt with all locations
echo.
pause

powershell -ExecutionPolicy Bypass -File organize_runtimes.ps1
