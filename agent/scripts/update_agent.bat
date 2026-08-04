@echo off
echo ========================================
echo  PRIME REMOTE D - Agent Update Script
echo ========================================
echo.

set "AGENT_DIR=%~dp0.."

echo [1/4] Stopping agent...
taskkill /IM pythonw.exe /F >nul 2>&1
taskkill /IM python.exe /F >nul 2>&1
timeout /t 2 >nul

echo [2/4] Pulling latest code...
cd /d "%AGENT_DIR%"
git pull origin main
if %errorLevel% neq 0 (
    echo ERROR: git pull failed!
    pause
    exit /b 1
)

echo [3/4] Installing dependencies...
pip install -r requirements.txt -q
if %errorLevel% neq 0 (
    echo WARNING: Some dependencies failed to install.
)

echo [4/4] Starting agent...
start /B pythonw.exe "%AGENT_DIR%\agent.py"

echo.
echo ========================================
echo  Update complete! Agent restarted.
echo ========================================
timeout /t 3 >nul
