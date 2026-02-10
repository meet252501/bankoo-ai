@echo off
echo ============================================================
echo   BANKOO AI - Dependency Installer
echo ============================================================
echo.
echo This will install all required packages for Bankoo AI agents:
echo   - Doc-Genius (PDF RAG)
echo   - Cine-Match (Movies)
echo   - Vision Lab (Hand Tracking)
echo   - Market Insight (Stocks)
echo   - Zenith Analytics (ML)
echo.
echo This may take 5-10 minutes...
echo.
pause

echo.
echo [1/6] Installing Core AI Libraries...
pip install langchain langchain-community langchain-core langchain-text-splitters

echo.
echo [2/6] Installing PDF Processing...
pip install PyPDF2 faiss-cpu sentence-transformers

echo.
echo [3/6] Installing Movie Intelligence...
pip install tmdbv3api

echo.
echo [4/6] Installing Vision Processing...
pip install opencv-python mediapipe

echo.
echo [5/6] Installing Market Data Tools...
pip install yfinance pandas numpy

echo.
echo [6/6] Installing Desktop Integration...
pip install pywin32 pillow psutil requests flask youtube-transcript-api

echo.
echo ============================================================
echo   Installation Complete!
echo ============================================================
echo.
echo Next Steps:
echo 1. Close this window
echo 2. Run START_BANKOO.bat to launch the app
echo.
pause
