@echo off
echo Starting Mozart Dueling AI...
cd /d "%~dp0"
python LAUNCH_GUI.py
if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to start Mozart Dueling AI
    echo Please run setup.py first to install dependencies.
    pause
)
