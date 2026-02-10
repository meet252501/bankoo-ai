@echo off
SETLOCAL EnableDelayedExpansion

SET CMD=%1

if "%CMD%"=="sync" (
    echo 🚀 Syncing Awesome OpenClaw Skills...
    python "%~dp0skill_downloader.py"
    goto :eof
)

if "%CMD%"=="list" (
    echo 📦 Listing Awesome Skills Registry...
    set PYTHONPATH=%~dp0;%PYTHONPATH%
    python -c "import api_hub; print('\n'.join([f'• {s['skill']}: {s['desc']}' for s in api_hub.skill_hub.list_skills()]))"
    goto :eof
)

if "%CMD%"=="help" (
    echo.
    echo 🦞 BANKOO ZENITH SKILL MANAGER
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo Usage: skill [command]
    echo.
    echo Commands:
    echo   sync   - Download/Update external skills from GitHub
    echo   list   - Show all registered skills
    echo   help   - Show this message
    echo.
    goto :eof
)

echo ❌ Unknown command: %CMD%
echo Type 'skill help' for usage.
:eof
