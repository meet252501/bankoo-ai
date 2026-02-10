@echo off
echo ========================================
echo  Vision Agent Dependencies Installer
echo ========================================
echo.
echo Installing OpenCV and MediaPipe...
echo.

pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.32

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo The Vision Agent is now ready to use.
echo Restart Bankoo to activate the Vision Lab.
echo.
pause
