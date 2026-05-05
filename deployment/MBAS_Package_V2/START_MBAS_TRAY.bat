@echo off
setlocal enabledelayedexpansion

REM Hide this window quickly by minimizing it
if not "%1"=="min" (
    start /min cmd /c "%~f0" min
    exit /b
)

REM Check if virtual environment exists
if not exist "%~dp0..\venv\Scripts\python.exe" (
    msg * "MBAS Error: Virtual environment not found! Please run INSTALL.bat first."
    exit /b 1
)

REM Activate virtual environment silently
call "%~dp0..\venv\Scripts\activate.bat" >nul 2>&1

REM Install required packages for tray app (only if not already installed)
python -c "import pystray, PIL, psutil" >nul 2>&1
if errorlevel 1 (
    python -m pip install pystray Pillow psutil --quiet --disable-pip-version-check >nul 2>&1
)

REM Start MBAS in system tray (completely hidden)
start /B pythonw "%~dp0mbas_tray.py"

REM Exit immediately (no visible window)
exit
