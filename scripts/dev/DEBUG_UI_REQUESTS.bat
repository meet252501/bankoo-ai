@echo off
cls
echo ===================================================================
echo   YOUTUBE COMMUNICATION DEBUGGER (SIMPLE MODE)
echo ===================================================================
echo.

set VIDEO_ID=pAnGwRiQ4-4
set TEST_URL=https://youtu.be/%VIDEO_ID%

echo [1/3] CHECKING BACKEND STATUS...
curl -s --fail http://127.0.0.1:5001/api/youtube/status
if errorlevel 1 (
    echo.
    echo ERROR: Backend Server is not running on Port 5001.
    echo Please start the server and run this test again.
    pause
    exit
)
echo.
echo SUCCESS: Backend is responding.
echo.

echo [2/3] SENDING TEST REQUEST...
echo Sending: %TEST_URL%
curl -s -X POST -H "Content-Type: application/json" -d "{\"url\":\"%TEST_URL%\"}" http://127.0.0.1:5001/api/youtube/summarize
echo.
echo.

echo [3/3] WAITING 2 SECONDS THEN CHECKING PROGRESS...
timeout /t 2 > nul
curl -s "http://127.0.0.1:5001/api/youtube/status?video_id=%VIDEO_ID%"
echo.
echo.

echo ===================================================================
echo   DEBUG COMPLETE - Check the responses above!
echo ===================================================================
pause
