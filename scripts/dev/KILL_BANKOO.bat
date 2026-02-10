@echo off
echo [BANKOO] Terminating ALL Active Processes...

taskkill /F /IM python.exe /T
taskkill /F /IM node.exe /T
taskkill /F /IM "bankoo_launcher.py" /T

echo.
echo [SUCCESS] Bankoo session has been force-quit.
echo You can now restart smoothly.
pause
