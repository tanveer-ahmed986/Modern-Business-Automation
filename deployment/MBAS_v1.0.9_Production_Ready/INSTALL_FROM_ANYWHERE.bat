@echo off
REM This script can be run from anywhere and will navigate to the correct folder
title MBAS Installation

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Change to script directory
cd /d "%SCRIPT_DIR%"

REM Check if we're in the right place
if not exist "INSTALL.bat" (
    echo ERROR: INSTALL.bat not found in %SCRIPT_DIR%
    echo.
    echo Please ensure this script is in the MBAS installation folder.
    pause
    exit /b 1
)

echo.
echo Starting MBAS installation from: %SCRIPT_DIR%
echo.
pause

REM Run the actual installer
call INSTALL.bat

pause
