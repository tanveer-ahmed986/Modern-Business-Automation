@echo off
title MBAS - Install Dependencies
color 0A

echo.
echo ================================================================
echo    MBAS - Modern Business Automation System
echo    Dependency Installation
echo ================================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.11 or higher:
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

REM Check Python version (3.11 or 3.12 recommended)
python -c "import sys; exit(0 if sys.version_info >= (3, 11) and sys.version_info < (3, 13) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [WARN] Python 3.13+ detected. We recommend Python 3.11 or 3.12 for best compatibility.
    echo        If installation fails, please install Python 3.11 or 3.12.
    echo.
    timeout /t 3 /nobreak >nul
)
echo.

echo [Step 1/4] Upgrading pip and setuptools...
python -m pip install --upgrade pip setuptools wheel --quiet
echo [OK] pip upgraded
echo.

echo [Step 2/4] Installing dependencies...
echo            This may take 1-3 minutes...
echo.
python -m pip install -r "%~dp0backend\requirements.txt" --only-binary :all: 2>nul
if errorlevel 1 (
    echo     Retrying with source builds allowed for small packages...
    python -m pip install -r "%~dp0backend\requirements.txt"
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install dependencies.
        echo         Please check your internet connection and try again.
        echo.
        pause
        exit /b 1
    )
)
echo [OK] All dependencies installed
echo.

echo [Step 3/4] Initializing database...
cd /d "%~dp0backend"
python -c "from src.scripts.init_db import bootstrap; bootstrap()"

if errorlevel 1 (
    echo [WARN] Database initialization had issues.
    echo        The database will be created automatically on first start.
)

cd /d "%~dp0"

echo.
echo [Step 4/4] Creating desktop shortcut...
if exist "%~dp0mbas_icon.ico" (
    cscript //nologo "%~dp0create_shortcut.vbs" "%~dp0START_MBAS.bat" "MBAS" "%~dp0mbas_icon.ico" >nul 2>&1
) else (
    cscript //nologo "%~dp0create_shortcut.vbs" "%~dp0START_MBAS.bat" "MBAS" >nul 2>&1
)
if errorlevel 1 (
    echo [WARN] Could not create desktop shortcut.
    echo        You can manually create a shortcut to START_MBAS.bat
) else (
    echo [OK] Desktop shortcut created!
)

echo.
echo ================================================================
echo    [OK] Installation Complete!
echo ================================================================
echo.
echo Next steps:
echo    1. Double-click the "MBAS" icon on your desktop
echo       (or double-click START_MBAS.bat in this folder)
echo    2. Your browser will open to: http://localhost:8000
echo    3. Login with: admin / admin123
echo    4. IMPORTANT: Change the admin password immediately!
echo.
pause
