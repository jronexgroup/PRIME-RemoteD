@echo off
echo ========================================
echo  PRIME REMOTE D - Agent Installer
echo ========================================
echo.

:: Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Run this as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

:: Install Python dependencies
echo Installing dependencies...
pip install -r "%SCRIPT_DIR%requirements.txt"
if %errorLevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

:: Create Task Scheduler task
echo Creating auto-start task...
schtasks /create /tn "PRIMERemoteDAgent" /tr "pythonw.exe \"%SCRIPT_DIR%agent.py\"" /sc onlogon /rl highest /f
if %errorLevel% neq 0 (
    echo ERROR: Failed to create task!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Installation complete!
echo  Agent will start on next login.
echo  To start now, run: start.bat
echo ========================================
pause
