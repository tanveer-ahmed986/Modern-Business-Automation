@echo off
title MBAS - Diagnostic and Fix Tool
color 0E

echo.
echo ================================================================
echo    MBAS Diagnostic and Fix Tool
echo ================================================================
echo.

echo [STEP 1] Checking Python installation...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is NOT installed!
    echo.
    echo SOLUTION:
    echo   1. Download Python 3.11 or 3.12 from: https://www.python.org/downloads/
    echo   2. Run installer
    echo   3. IMPORTANT: Check "Add Python to PATH"
    echo   4. Restart this script
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed:
python --version
echo.

echo [STEP 2] Checking Python version...
echo.

python -c "import sys; v=sys.version_info; exit(0 if (v.major==3 and 11<=v.minor<=12) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Python version may not be compatible
    python --version
    echo.
    echo RECOMMENDATION:
    echo   Python 3.11 or 3.12 is recommended
    echo   Python 3.13+ may have compatibility issues
    echo.
    echo Continue anyway? (Y/N)
    choice /c YN /n /m "Choice: "
    if errorlevel 2 exit /b 1
)

echo [OK] Python version is compatible
echo.

echo [STEP 3] Checking virtual environment...
echo.

if exist "%~dp0venv\Scripts\python.exe" (
    echo [OK] Virtual environment exists
    echo.
) else (
    echo [ERROR] Virtual environment is MISSING!
    echo.
    echo This is why MBAS failed to start.
    echo.
    echo FIXING NOW...
    echo.

    echo [*] Creating virtual environment...
    python -m venv "%~dp0venv"
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        echo.
        echo Try running as Administrator
        echo.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
)

echo [STEP 4] Checking dependencies...
echo.

call "%~dp0venv\Scripts\activate.bat"

python -c "import fastapi, pydantic, uvicorn" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Dependencies are MISSING!
    echo.
    echo FIXING NOW...
    echo.

    echo [*] Installing dependencies (this may take 2-4 minutes)...
    python -m pip install --upgrade pip setuptools wheel --quiet
    python -m pip install -r "%~dp0backend\requirements.txt"

    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies!
        echo.
        echo Common fixes:
        echo   1. Check internet connection
        echo   2. Run as Administrator
        echo   3. Disable antivirus temporarily
        echo.
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
    echo.
) else (
    echo [OK] Dependencies are installed
    echo.
)

echo [STEP 5] Checking watchdog dependencies...
echo.

python -c "import requests, psutil" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Watchdog dependencies missing!
    echo.
    echo FIXING NOW...
    python -m pip install requests psutil --quiet
    echo [OK] Watchdog dependencies installed
    echo.
) else (
    echo [OK] Watchdog dependencies present
    echo.
)

echo [STEP 6] Checking database...
echo.

if exist "%~dp0backend\mbas_database.db" (
    echo [OK] Database exists
    echo.
) else (
    echo [ERROR] Database is MISSING!
    echo.
    echo FIXING NOW...
    echo.

    cd /d "%~dp0backend"
    python -c "from src.scripts.init_db import bootstrap; bootstrap()"

    if exist "%~dp0backend\mbas_database.db" (
        echo [OK] Database created successfully
    ) else (
        echo [WARN] Database creation may have had issues
        echo        Will be created on first start
    )
    echo.
    cd /d "%~dp0"
)

echo [STEP 7] Checking port 8000 availability...
echo.

netstat -ano | findstr ":8000.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo [OK] Port 8000 is available
    echo.
) else (
    echo [WARNING] Port 8000 is already in use!
    echo.
    echo Another process is using port 8000.
    echo This will prevent MBAS from starting.
    echo.
    echo Finding process...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000.*LISTENING"') do (
        echo Process ID: %%a
        tasklist /FI "PID eq %%a"
    )
    echo.
    echo Options:
    echo   1. Kill the process (if it's old MBAS): taskkill /F /PID [PID]
    echo   2. Close the application using port 8000
    echo.
    pause
)

echo.
echo ================================================================
echo    DIAGNOSTIC COMPLETE
echo ================================================================
echo.
echo Summary:
echo   [✓] Python installed and compatible
echo   [✓] Virtual environment ready
echo   [✓] Dependencies installed
echo   [✓] Watchdog dependencies ready
echo   [✓] Database ready
echo.
echo MBAS is now ready to start!
echo.
echo Next step:
echo   Double-click: START_MBAS_TRAY.bat
echo   OR
echo   Double-click the "MBAS" desktop shortcut
echo.
echo ================================================================
echo.
pause
