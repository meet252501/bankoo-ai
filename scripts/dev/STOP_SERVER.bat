@echo off
echo.
echo ========================================
echo   STOP BANKOO SERVER (Port 5001)
echo ========================================
echo.

REM Find the process ID using port 5001
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5001 ^| findstr LISTENING') do (
    set PID=%%a
    goto :found
)

:found
if not defined PID (
    echo [INFO] No server running on port 5001
    pause
    exit /b 0
)

echo [FOUND] Process ID: %PID%
echo [ACTION] Stopping server...
taskkill /F /PID %PID%

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Server stopped successfully!
) else (
    echo.
    echo [ERROR] Failed to stop server
)

echo.
pause
