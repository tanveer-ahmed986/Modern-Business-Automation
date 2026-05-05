@echo off
REM This script can be run from anywhere and will navigate to the correct folder
title MBAS Startup

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Change to script directory
cd /d "%SCRIPT_DIR%"

REM Check if we're in the right place
if not exist "START_MBAS_TRAY.bat" (
    echo ERROR: START_MBAS_TRAY.bat not found in %SCRIPT_DIR%
    echo.
    echo Please ensure this script is in the MBAS installation folder.
    pause
    exit /b 1
)

echo.
echo Starting MBAS from: %SCRIPT_DIR%
echo.

REM Run the actual startup script
call START_MBAS_TRAY.bat
