@echo off
cls
echo ==================================================
echo   SMART NOTES 4.0: AGGRESSIVE TESTER
echo ==================================================
echo.

set SERVER=http://127.0.0.1:5001

echo [1/4] Killing old server instances...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Bankoo Server*" >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/4] Starting FRESH Server...
start "Bankoo Server" cmd /k "python bankoo_launcher.py"
echo [WAIT] Waiting 10 seconds for AI Initialization...
timeout /t 10 /nobreak >nul

echo.
echo [TEST 1] Creating 'Work' Note for Auto-Sorter...
curl -X POST %SERVER%/api/notes/v3/create ^
     -H "Content-Type: application/json" ^
     -d "{\"title\": \"Quarterly Project Meeting\", \"content\": \"Discuss deadlines\", \"folderId\": \"f_default\"}"
echo.

echo [TEST 2] Creating 'Action' Note for Extractor...
curl -X POST %SERVER%/api/notes/v3/create ^
     -H "Content-Type: application/json" ^
     -d "{\"title\": \"Bug Report\", \"content\": \"TODO: Fix the login bug\", \"folderId\": \"f_default\"}"
echo.

echo [TEST 3] AI Summarization Check...
echo (Content: 'This is a long note about photosynthesis...')
curl -X POST %SERVER%/api/notes/v3/ai/summarize ^
     -H "Content-Type: application/json" ^
     -d "{\"content\": \"This is a long note about photosynthesis. Plants use sunlight to create energy from carbon dioxide and water.\"}"
echo.
echo.

echo [TEST 4] Verifying Results...
curl %SERVER%/api/notes/v3/all
echo.
echo.

echo ==================================================
echo   VERIFICATION COMPLETE
echo   - Check if 'Meeting' note moved to Work folder
echo   - Check if 'Bug Report' has 'Actionable' tag
echo   - Check if Summary Test returned a "summary" JSON
echo ==================================================
pause
