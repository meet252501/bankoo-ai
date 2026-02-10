@echo off
setlocal EnableDelayedExpansion
title Bankoo AI - GitHub Readiness Scanner
color 0b

echo ========================================================
echo       BANKOO AI - GITHUB READINESS SCANNER
echo ========================================================
echo.

set "MISSING_FILES=0"
set "SYNTAX_ERRORS=0"
set "SECURITY_WARNINGS=0"

echo [1/4] CHECKING CORE FILES...
echo --------------------------------------------

if exist "bankoo_main.py" ( echo [OK] bankoo_main.py found ) else ( echo [MISSING] bankoo_main.py & set /a MISSING_FILES+=1 )
if exist "bankoo_ui.html" ( echo [OK] bankoo_ui.html found ) else ( echo [MISSING] bankoo_ui.html & set /a MISSING_FILES+=1 )
if exist "web_scraper_brain.py" ( echo [OK] web_scraper_brain.py found ) else ( echo [MISSING] web_scraper_brain.py & set /a MISSING_FILES+=1 )
if exist "config.py" ( echo [OK] config.py found ) else ( echo [MISSING] config.py & set /a MISSING_FILES+=1 )
if exist "requirements.txt" ( echo [OK] requirements.txt found ) else ( echo [MISSING] requirements.txt - Recommended for GitHub & set /a MISSING_FILES+=1 )
if exist ".gitignore" ( echo [OK] .gitignore found ) else ( echo [MISSING] .gitignore - Recommended to hide secrets & set /a MISSING_FILES+=1 )

echo.
echo [2/4] PYTHON SYNTAX CHECK...
echo --------------------------------------------

rem Check bankoo_main.py
python -m py_compile bankoo_main.py >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] bankoo_main.py syntax is valid.
) else (
    echo [ERROR] bankoo_main.py has SYNTAX ERRORS!
    set /a SYNTAX_ERRORS+=1
)

rem Check web_scraper_brain.py
python -m py_compile web_scraper_brain.py >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] web_scraper_brain.py syntax is valid.
) else (
    echo [ERROR] web_scraper_brain.py has SYNTAX ERRORS!
    set /a SYNTAX_ERRORS+=1
)

rem Check config.py
python -m py_compile config.py >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] config.py syntax is valid.
) else (
    echo [ERROR] config.py has SYNTAX ERRORS!
    set /a SYNTAX_ERRORS+=1
)

echo.
echo [3/4] SECURITY SCAN (CREDENTIAL INCIDENTS)...
echo --------------------------------------------

set "FOUND_SECRETS=0"

rem Simple scan for common key prefixes
findstr /s /m /i "sk- ghp_ API_KEY" *.py >nul 2>&1
if %errorlevel% equ 0 (
    echo [WARNING] Potential API Keys found in code!
    findstr /s /n /i "sk- ghp_ API_KEY" *.py
    set /a SECURITY_WARNINGS+=1
) else (
    echo [SAFE] No obvious API keys detected in .py files.
)

echo.
echo [4/4] SUMMARY REPORT
echo ========================================================
if %MISSING_FILES% equ 0 ( echo [PASS] File Structure ) else ( echo [FAIL] Missing %MISSING_FILES% files )
if %SYNTAX_ERRORS% equ 0 ( echo [PASS] Syntax Check ) else ( echo [FAIL] %SYNTAX_ERRORS% Syntax Errors found! )
if %SECURITY_WARNINGS% equ 0 ( echo [PASS] Security Scan ) else ( echo [WARN] %SECURITY_WARNINGS% Potential security risks! )

echo.
if %MISSING_FILES% equ 0 if %SYNTAX_ERRORS% equ 0 if %SECURITY_WARNINGS% equ 0 (
    color 0a
    echo --------------------------------------------
    echo   READY FOR GITHUB UPLOAD!
    echo --------------------------------------------
) else (
    color 0c
    echo --------------------------------------------
    echo   PLEASE FIX ISSUES BEFORE UPLOAD.
    echo --------------------------------------------
)
echo.
pause
