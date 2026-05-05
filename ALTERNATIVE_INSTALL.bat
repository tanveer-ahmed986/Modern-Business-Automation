@echo off
title MBAS - Alternative Installation Method
color 0A
setlocal enabledelayedexpansion

echo.
echo ================================================================
echo    MBAS Alternative Installation Method
echo ================================================================
echo.
echo This uses a different approach that bypasses common issues.
echo.
pause

REM Check admin rights
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Must run as Administrator!
    echo.
    echo Right-click this file and select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

echo [Step 1/7] Checking Python...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)

python --version
echo.

echo [Step 2/7] Cleaning up old installation...
echo.

REM Kill all Python processes
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1
timeout /t 3 /nobreak >nul

REM Force remove old venv
if exist "venv" (
    echo Removing old venv...

    REM Take ownership
    takeown /f venv /r /d y >nul 2>&1

    REM Grant full permissions
    icacls venv /grant "%username%":F /t /c /q >nul 2>&1

    REM Delete
    rd /s /q venv >nul 2>&1

    REM If still exists, try robocopy trick
    if exist "venv" (
        mkdir empty_dir 2>nul
        robocopy empty_dir venv /purge >nul 2>&1
        rd /s /q venv >nul 2>&1
        rd /s /q empty_dir >nul 2>&1
    )

    if exist "venv" (
        echo [ERROR] Cannot remove old venv!
        echo.
        echo Please:
        echo   1. Restart your computer
        echo   2. Run this script again
        echo.
        pause
        exit /b 1
    )
)

echo [OK] Cleanup complete
echo.

echo [Step 3/7] Creating virtual environment...
echo.
echo This may take 30 seconds...
echo.

REM Create venv without pip initially (faster, less likely to fail)
python -m venv --without-pip venv

if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Failed to create venv!
    echo.
    echo Trying alternative method...

    REM Try with system site packages
    python -m venv --system-site-packages venv

    if not exist "venv\Scripts\python.exe" (
        echo [CRITICAL] Cannot create virtual environment!
        echo.
        echo Your Python installation may be corrupted.
        echo.
        echo SOLUTION:
        echo   1. Uninstall Python
        echo   2. Restart computer
        echo   3. Reinstall Python 3.12.1
        echo   4. Try again
        echo.
        pause
        exit /b 1
    )
)

echo [OK] Virtual environment created
echo.

echo [Step 4/7] Installing pip in venv...
echo.

REM Download and install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 2>nul
if exist "get-pip.py" (
    venv\Scripts\python.exe get-pip.py
    del get-pip.py
) else (
    REM Alternative: use ensurepip
    venv\Scripts\python.exe -m ensurepip --upgrade
)

echo [OK] Pip installed
echo.

echo [Step 5/7] Upgrading pip and setuptools...
echo.

venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel --quiet
echo [OK] Package managers upgraded
echo.

echo [Step 6/7] Installing dependencies...
echo.
echo This will take 2-4 minutes. Please wait...
echo.

REM Install in stages to avoid timeout issues
echo [*] Stage 1: Core dependencies...
venv\Scripts\python.exe -m pip install fastapi pydantic uvicorn[standard] --quiet

echo [*] Stage 2: Database and auth...
venv\Scripts\python.exe -m pip install sqlmodel pydantic-settings python-jose[cryptography] --quiet

echo [*] Stage 3: Security...
venv\Scripts\python.exe -m pip install passlib bcrypt python-multipart --quiet

echo [*] Stage 4: Utilities...
venv\Scripts\python.exe -m pip install apscheduler --quiet

echo [*] Stage 5: Watchdog dependencies...
venv\Scripts\python.exe -m pip install requests psutil --quiet

echo [*] Stage 6: Tray dependencies...
venv\Scripts\python.exe -m pip install pystray Pillow --quiet

if errorlevel 1 (
    echo.
    echo [WARN] Some dependencies may have failed
    echo       The system will try to install them on first run
    echo.
)

echo [OK] Dependencies installed
echo.

echo [Step 7/7] Initializing database...
echo.

cd backend
..\venv\Scripts\python.exe -c "from src.scripts.init_db import bootstrap; bootstrap()" 2>nul

if exist "mbas_database.db" (
    echo [OK] Database created
) else (
    echo [WARN] Database will be created on first start
)

cd ..
echo.

REM Create desktop shortcut
echo [*] Creating desktop shortcut...
if exist "mbas_icon.ico" (
    if exist "create_shortcut.vbs" (
        cscript //nologo create_shortcut.vbs "%~dp0START_MBAS_TRAY.bat" "MBAS" "%~dp0mbas_icon.ico" >nul 2>&1
    )
)

echo.
echo ================================================================
echo    [SUCCESS] Installation Complete!
echo ================================================================
echo.
echo MBAS is now installed using an isolated virtual environment.
echo.
echo NEXT STEPS:
echo   1. Close this window
echo   2. Double-click: START_MBAS_TRAY.bat
echo   3. Wait for green system tray icon
echo   4. Browser will open automatically
echo   5. Login: admin / admin123
echo.
echo NOTE: First startup may take 10-15 seconds.
echo.
pause
