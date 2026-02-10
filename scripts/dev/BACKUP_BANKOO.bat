@echo off
set "SOURCE=C:\Users\Meet Sutariya\Desktop\final banko.ai"
set "DEST=C:\Users\Meet Sutariya\Desktop\old backup banko"

echo 🚀 Checking destination: %DEST%
if not exist "%DEST%" (
    echo 📁 Creating destination folder...
    mkdir "%DEST%"
)

echo 🗑️ Cleaning old backup...
powershell -Command "Remove-Item -Path '%DEST%\*' -Recurse -Force -ErrorAction SilentlyContinue"

echo 📦 Copying files...
echo From: %SOURCE%
echo To:   %DEST%

robocopy "%SOURCE%" "%DEST%" /MIR /R:0 /W:0 /XF *.git* *.venv* /XD .git .venv

echo ✅ Backup Complete!
pause
