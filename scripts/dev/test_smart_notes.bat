@echo off
cls
echo ==================================================
echo   SMART NOTES 3.0 DIAGNOSTIC TEST (v3 API)
echo ==================================================
echo.

set SERVER=http://127.0.0.1:5001

echo [TEST 1] Creating a Test Note via API...
curl -X POST %SERVER%/api/notes/v3/create ^
     -H "Content-Type: application/json" ^
     -d "{\"title\": \"Diagnostic Note\", \"content\": \"System verification test\", \"folderId\": \"f_code\"}"
echo.
echo.

echo [TEST 2] Fetching All Notes (v3 Engine)...
curl %SERVER%/api/notes/v3/all
echo.
echo.

echo [TEST 3] Deleting Test Note...
rem This step would need the ID from Test 1, skipping auto-delete for now.
rem You can manually check the UI to see if "Diagnostic Note" appeared.
echo.
echo ==================================================
echo   DIAGNOSTIC COMPLETE
echo   1. check the output above for errors
echo   2. Open Bankoo UI to see if "Diagnostic Note" exists
echo ==================================================
pause
