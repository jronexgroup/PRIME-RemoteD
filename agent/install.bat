@echo off
echo ========================================
echo  PRIME REMOTE D - Agent Installer
echo ========================================
echo.

set "SCRIPT_DIR=%~dp0"

echo Checking Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python not found in PATH!
    echo Please install Python and add it to PATH.
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r "%SCRIPT_DIR%requirements.txt"
if %errorLevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('where pythonw') do (
    set "PYTHONW_PATH=%%i"
    goto :found_pythonw
)
:found_pythonw

if not defined PYTHONW_PATH (
    for /f "tokens=*" %%i in ('where python') do (
        set "PYTHON_PATH=%%i"
        goto :found_python
    )
)
:found_python

if defined PYTHONW_PATH (
    set "PYTHON_EXE=%PYTHONW_PATH%"
) else if defined PYTHON_PATH (
    set "PYTHON_EXE=%PYTHON_PATH%"
) else (
    echo ERROR: Cannot find Python executable!
    pause
    exit /b 1
)

echo Using Python: %PYTHON_EXE%
echo Creating auto-start task...

schtasks /delete /tn "PRIMERemoteDAgent" /f >nul 2>&1
schtasks /create /tn "PRIMERemoteDAgent" /tr "\"%PYTHON_EXE%\" \"%SCRIPT_DIR%agent.py\"" /sc onlogon /rl highest /f
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
