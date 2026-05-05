@echo off
REM ============================================================================
REM  MBAS Professional Launcher (System Tray Mode)
REM  Z&T Technologies - State-of-the-Art Business Solutions
REM  Requires admin to write database in Program Files
REM ============================================================================

cd /d "%~dp0"

REM Request admin elevation if not already admin
net session >nul 2>&1
if errorlevel 1 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM Check if venv exists
if not exist "%~dp0venv\Scripts\pythonw.exe" (
    if not exist "%~dp0venv\Scripts\python.exe" (
        msg * "MBAS installation incomplete. Please run INSTALL_MBAS.bat first."
        exit /b 1
    )
)

REM Use venv pythonw (no console window) to launch tray app
if exist "%~dp0venv\Scripts\pythonw.exe" (
    start "" "%~dp0venv\Scripts\pythonw.exe" "%~dp0scripts\mbas_tray.py"
) else (
    start "" "%~dp0venv\Scripts\python.exe" "%~dp0scripts\mbas_tray.py"
)

exit
