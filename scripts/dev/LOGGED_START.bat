@echo off
echo ==================================================
echo   BANKOO AI: LOGGED STARTUP
echo ==================================================
echo.
echo Launching server and capturing output to 'startup_log.txt'...
echo Please wait 10 seconds...

python bankoo_launcher.py > startup_log.txt 2>&1

echo.
echo Process exited. Check startup_log.txt for errors.
pause
