@echo off
cls
echo ========================================================
echo   BANKOO.AI CONNECTION DIAGNOSTIC TOOL
echo ========================================================
echo.

echo [1/3] Checking if Backend Server is reachable...
curl -s http://127.0.0.1:5001/api/ping > NUL
if %errorlevel% equ 0 (
    echo [PASS] Backend is ONLINE (Port 5001)
) else (
    echo [FAIL] Backend is OFFLINE or blocking connections.
    echo        - Check if 'START_BANKOO.bat' is running.
    echo        - Check firewall settings.
    goto :end
)

echo.
echo [2/3] Verifying API Response...
for /f "tokens=*" %%i in ('curl -s http://127.0.0.1:5001/api/ping') do set RESPONSE=%%i
echo Server replied: %RESPONSE%

echo.
echo [3/3] Checking UI Files...
if exist "bankoo_ui.html" (
    echo [PASS] UI File 'bankoo_ui.html' found.
) else (
    echo [FAIL] 'bankoo_ui.html' is MISSING!
)

echo.
echo ========================================================
echo   DIAGNOSTIC COMPLETE
echo ========================================================
pause
:end
pause
