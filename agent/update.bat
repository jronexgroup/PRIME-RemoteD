@echo off
echo ========================================
echo  PRIME REMOTE D - Auto Update
echo ========================================
echo.

set "SCRIPT_DIR=%~dp0"

echo [1/4] Stopping agent...
taskkill /IM pythonw.exe /F >nul 2>&1
taskkill /IM python.exe /F >nul 2>&1

echo [2/4] Pulling latest code...
cd /d "%SCRIPT_DIR%"
git pull origin main
if %errorLevel% neq 0 (
    echo WARNING: git pull failed. Check your internet connection.
)

echo [3/4] Installing dependencies...
pip install -r requirements.txt -q
if %errorLevel% neq 0 (
    echo WARNING: Some dependencies failed to install.
)

echo [4/4] Starting agent...
start /B pythonw.exe "%SCRIPT_DIR%agent.py"

echo.
echo ========================================
echo  Update complete! Agent is running.
echo ========================================
timeout /t 3 >nul
