@echo off
title MBAS - Installation
color 0A
setlocal enabledelayedexpansion

echo.
echo ================================================================
echo    MBAS - Modern Business Automation System
echo    Installation with Virtual Environment Isolation
echo ================================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.11 or 3.12:
    echo    1. Download from: https://www.python.org/downloads/
    echo    2. Run the installer
    echo    3. IMPORTANT: Check "Add Python to PATH"
    echo    4. Restart this script after installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

REM Check Python version (3.11 or 3.12 ONLY - 3.13 has compatibility issues)
python -c "import sys; v=sys.version_info; exit(0 if (v.major==3 and 11<=v.minor<=12) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Incompatible Python version detected!
    echo.
    echo MBAS requires Python 3.11 or 3.12 for maximum compatibility.
    echo Python 3.13+ has known issues with bcrypt and other packages.
    echo.
    echo Please install Python 3.11 or 3.12 from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo [OK] Python version compatible
echo.

REM Remove old virtual environment if exists
if exist "%~dp0venv" (
    echo [*] Removing old virtual environment...
    rmdir /s /q "%~dp0venv"
)

echo [Step 1/5] Creating isolated virtual environment...
python -m venv "%~dp0venv"
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment!
    echo.
    pause
    exit /b 1
)
echo [OK] Virtual environment created
echo.

echo [Step 2/5] Activating virtual environment...
call "%~dp0venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

echo [Step 3/5] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel --quiet
if errorlevel 1 (
    echo [WARN] Failed to upgrade pip, continuing anyway...
)
echo [OK] Package managers upgraded
echo.

echo [Step 4/5] Installing dependencies (this may take 2-4 minutes)...
echo.
echo     [*] Installing core packages with locked versions...
REM Try requirements-lock.txt first (exact versions for reliability)
if exist "%~dp0backend\requirements-lock.txt" (
    python -m pip install -r "%~dp0backend\requirements-lock.txt"
) else (
    python -m pip install -r "%~dp0backend\requirements.txt"
)
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies!
    echo.
    echo Common fixes:
    echo   1. Check your internet connection
    echo   2. Make sure you're using Python 3.11 or 3.12
    echo   3. Try running as Administrator
    echo   4. Try: python -m pip install --upgrade pip
    echo   5. Disable antivirus temporarily
    echo.
    pause
    exit /b 1
)
echo [OK] All dependencies installed
echo.

echo [Step 5/5] Initializing database and creating shortcuts...
cd /d "%~dp0backend"
python -c "from src.scripts.init_db import bootstrap; bootstrap()"
if errorlevel 1 (
    echo [WARN] Database initialization had issues.
    echo        The database will be created on first start.
)
cd /d "%~dp0"

REM Create desktop shortcut (Background Mode - Professional)
echo [*] Creating desktop shortcut for background mode...
if exist "%~dp0mbas_icon.ico" (
    cscript //nologo "%~dp0create_shortcut.vbs" "%~dp0START_MBAS_TRAY.bat" "MBAS" "%~dp0mbas_icon.ico" >nul 2>&1
) else (
    cscript //nologo "%~dp0create_shortcut.vbs" "%~dp0START_MBAS_TRAY.bat" "MBAS" >nul 2>&1
)
if not errorlevel 1 (
    echo [OK] Desktop shortcut created (Background Mode)
) else (
    echo [WARN] Could not create desktop shortcut
    echo        You can manually run START_MBAS_TRAY.bat
)

echo.
echo ================================================================
echo    [SUCCESS] Installation Complete!
echo ================================================================
echo.
echo MBAS is now installed in an isolated virtual environment.
echo This prevents conflicts with other Python packages on your system.
echo.
echo ================================================================
echo    PROFESSIONAL BACKGROUND MODE ENABLED
echo ================================================================
echo.
echo MBAS will run in the background with a system tray icon.
echo NO CMD window will appear - perfect for professional use!
echo.
echo Next steps:
echo    1. Double-click the "MBAS" icon on your desktop
echo       (This starts background mode automatically)
echo.
echo    2. Look for the system tray icon (near clock)
echo       - Green icon = Server running
echo       - Right-click icon for menu options
echo.
echo    3. Click "Open MBAS" from tray menu
echo       Browser will open to: http://localhost:8000
echo.
echo    4. Login: admin / admin123
echo       IMPORTANT: Change the password immediately!
echo.
echo    5. To stop MBAS:
echo       Right-click tray icon and select "Exit"
echo.
echo NOTE: The server runs silently in the background.
echo       You won't see any CMD window (professional mode).
echo.
echo Technical details:
echo    - Virtual environment: %~dp0venv
echo    - Backend: %~dp0backend
echo    - Database: %~dp0backend\mbas_database.db
echo.
pause
