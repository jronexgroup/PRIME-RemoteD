@echo off
echo Starting PRIME REMOTE D Agent...

for /f "tokens=*" %%i in ('where pythonw 2^>nul') do (
    set "PYTHONW_PATH=%%i"
    goto :found
)
for /f "tokens=*" %%i in ('where python 2^>nul') do (
    set "PYTHONW_PATH=%%i"
    goto :found
)
:found

if defined PYTHONW_PATH (
    start "" "%PYTHONW_PATH%" "%~dp0agent.py"
) else (
    start "" pythonw "%~dp0agent.py"
)

echo Agent started in background.
