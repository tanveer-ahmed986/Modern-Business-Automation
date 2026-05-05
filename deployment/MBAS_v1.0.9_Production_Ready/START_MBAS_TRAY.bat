@echo off
setlocal enabledelayedexpansion

REM Hide this window quickly by minimizing it
if not "%1"=="min" (
    start /min cmd /c "%~f0" min
    exit /b
)

REM Check if virtual environment exists
if not exist "%~dp0venv\Scripts\python.exe" (
    msg * "MBAS Error: Virtual environment not found! Please run INSTALL.bat first."
    exit /b 1
)

REM Activate virtual environment silently
call "%~dp0venv\Scripts\activate.bat" >nul 2>&1

REM Install required packages for tray app (only if not already installed)
python -c "import pystray, PIL, psutil, requests" >nul 2>&1
if errorlevel 1 (
    REM First-time setup: Install tray dependencies (blocks until complete)
    python -m pip install pystray Pillow psutil requests --quiet --disable-pip-version-check

    REM Verify installation completed successfully
    python -c "import pystray, PIL, psutil, requests" >nul 2>&1
    if errorlevel 1 (
        msg * "MBAS Setup Error: Failed to install system tray dependencies. Please check your internet connection and try again."
        exit /b 1
    )
)

REM Ensure database is initialized before starting
cd /d "%~dp0backend"
python -c "from pathlib import Path; from src.scripts.init_db import bootstrap; import sys; db_exists = Path('mbas_database.db').exists(); bootstrap() if not db_exists else None; sys.exit(0)" >nul 2>&1
cd /d "%~dp0"

REM Wait a moment for any database initialization to complete
timeout /t 2 /nobreak >nul 2>&1

REM Start MBAS in system tray (completely hidden)
start /B pythonw "%~dp0scripts\mbas_tray.py"

REM Exit immediately (no visible window)
exit
