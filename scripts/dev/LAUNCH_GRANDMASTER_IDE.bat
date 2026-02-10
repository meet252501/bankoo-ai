@echo off
title Bankoo AI - Grandmaster IDE Launcher
color 0b

echo 🚀 Launching Bankoo God-Mode IDE...
echo [INFO] Ensuring Neural Brain is active...

:: Start the main server in the background if not already running
:: (This assumes bankoo_main.py handles port conflicts gracefully or is the entry point)
start /B "" "C:\Users\Meet Sutariya\AppData\Local\Programs\Python\Python312\pythonw.exe" bankoo_main.py

:: Wait for server to warm up
timeout /t 3 /nobreak >nul

:: Launch browser to IDE endpoint
start http://localhost:5000/ide

echo ✅ IDE is now running at http://localhost:5000/ide
echo [HINT] Keep this window open if you want to see backend logs.
pause
