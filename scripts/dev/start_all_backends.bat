@echo off
echo ========================================
echo   BANKOO.AI COMPLETE SYSTEM STARTUP
echo ========================================
echo.
echo Starting all AI agent backends...
echo.

REM Change to project directory
cd /d "C:\Users\Meet Sutariya\Desktop\final banko.ai"

REM Start Main Bankoo Backend (Port 5001) - CRITICAL
echo [1/4] Starting Main Bankoo Backend on port 5001...
start "Bankoo Main (5001)" cmd /k "python bankoo_main.py"
timeout /t 3 >nul

REM Start Movies Agent Backend (Port 5000)
echo [2/4] Starting Movies Agent (Cine-Match) on port 5000...
start "Movies Agent (5000)" cmd /k "cd backend\movies && python app.py"
timeout /t 2 >nul

REM Start Analytics Agent Backend (Port 8080)
echo [3/4] Starting Analytics Agent (Zenith) on port 8080...
start "Analytics Agent (8080)" cmd /k "cd backend\analytics && python app.py"
timeout /t 2 >nul

REM Start Market Insight Agent Backend (Port 8000)
echo [4/4] Starting Market Insight Agent on port 8000...
start "Market Agent (8000)" cmd /k "cd backend\market && python main.py"
timeout /t 2 >nul

echo.
echo ========================================
echo   ALL SERVICES STARTED!
echo ========================================
echo.
echo Service Status:
echo   [PRIMARY]
echo   - Main Bankoo UI: http://127.0.0.1:5001
echo.
echo   [AI AGENTS - Active]
echo   - Movies (Cine-Match):      http://127.0.0.1:5000
echo   - Analytics (Zenith):       http://127.0.0.1:8080
echo   - Market Insight:           http://127.0.0.1:8000
echo.
echo   [AI AGENTS - Standalone]
echo   - Doc Genius: Run manually with 'streamlit run backend\doc_genius\app.py'
echo   - Vision Lab: Standalone camera app (run backend\vision\app.py if needed)
echo.
echo Opening main Bankoo UI in 5 seconds...
timeout /t 5 >nul

REM Open the main UI
start "" http://127.0.0.1:5001

echo.
echo System is ready! All terminals must stay open.
echo.
echo Press any key to STOP ALL SERVICES...
pause >nul

REM Kill all related processes
echo.
echo Shutting down all services...
taskkill /FI "WINDOWTITLE eq Bankoo*" /F /T 2>nul
taskkill /FI "WINDOWTITLE eq Movies*" /F /T 2>nul
taskkill /FI "WINDOWTITLE eq Analytics*" /F /T 2>nul
taskkill /FI "WINDOWTITLE eq Market*" /F /T 2>nul

echo All services stopped.
timeout /t 2 >nul

