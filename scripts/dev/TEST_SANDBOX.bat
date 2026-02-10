@echo off
echo ==================================================
echo      🧪 TESTING BANKOO SMART SANDBOX (ULTIMATE)
echo ==================================================
echo.
echo [1] Target Script: test_autoinstall.py
echo [2] Requirement:   'pyfiglet' library (Likely missing)
echo [3] Expected:      Auto-Install -> Execution -> "IT WORKS!"
echo.
echo Running Smart Runner...
echo --------------------------------------------------
python "%~dp0smart_runner.py" "%~dp0test_autoinstall.py"
echo --------------------------------------------------
echo.
pause
