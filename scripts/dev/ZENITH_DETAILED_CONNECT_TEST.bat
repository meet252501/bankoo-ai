@echo off
TITLE Bankoo Zenith: System Diagnostic
SETLOCAL EnableDelayedExpansion

echo =========================================================================
echo BANKOO ZENITH: SYSTEM CONNECTIVITY TEST
echo =========================================================================
echo Time: %date% %time%
echo.

:: 1. ENVIRONMENT CHECK
echo [1/6] Verifying Python Environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    pause
    exit /b
)
for /f "tokens=2" %%i in ('python --version') do set pyver=%%i
echo SUCCESS: Python !pyver! detected.
echo.

:: 2. DEPENDENCY AUDIT
echo [2/6] Auditing Critical Dependencies...
python -c "import flask; import flask_cors; import requests; import google.generativeai" >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Missing core dependencies. 
    echo Attempting to install required packages...
    pip install flask flask-cors requests google-generativeai edge-tts
) else (
    echo SUCCESS: Core dependencies verified.
)
echo.

:: 3. MODULE INTEGRITY
echo [3/6] Testing Neural Brain Modules...
if exist "assistant.py" (
    python -c "import assistant; import api_hub" >nul 2>&1
    if !errorlevel! neq 0 (
        echo ERROR: assistant.py exists but failed to load. Check for syntax errors.
    ) else (
        echo SUCCESS: Core modules are healthy.
    )
) else (
    echo ERROR: assistant.py NOT FOUND in current directory.
)
echo.

:: 4. CONFIGURATION CHECK
echo [4/6] Validating Configuration...
if exist "config.py" (
    echo SUCCESS: config.py found.
) else (
    echo WARNING: config.py missing.
)
echo.

:: 5. BACKEND CONNECTIVITY
echo [5/6] Testing Backend API Connectivity...
echo Attempting to reach Bankoo Server at http://127.0.0.1:5001...
powershell -Command "$ErrorActionPreference = 'Stop'; try { $res = Invoke-WebRequest -Uri 'http://127.0.0.1:5001/api/ping' -UseBasicParsing -TimeoutSec 5; Write-Host 'SUCCESS: Backend is REACHABLE.' -ForegroundColor Green; Write-Host ('Server Response: ' + $res.Content) } catch { Write-Host 'FAILURE: Backend UNREACHABLE.' -ForegroundColor Red; Write-Host 'Is START_BANKOO.bat running?' -ForegroundColor Yellow }"
echo.

:: 6. PORT VALIDATION
echo [6/6] Checking Port 5001...
netstat -ano | findstr LISTENING | findstr :5001 >nul 2>&1
if "%errorlevel%"=="0" (
    echo SUCCESS: Port 5001 is active and listening.
) else (
    echo FAILURE: Port 5001 is CLOSED.
)
echo.

echo =========================================================================
echo DIAGNOSTIC COMPLETE
echo =========================================================================
pause
