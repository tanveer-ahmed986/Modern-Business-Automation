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
) else (
    echo [OK] Python version is compatible (3.12.1)
    echo.
)

echo [STEP 3] Checking for MBAS deployment folder...
echo.

REM Try to find MBAS folder
set MBAS_DIR=
if exist "deployment\MBAS_v1.0.9_Production_Ready" (
    set MBAS_DIR=deployment\MBAS_v1.0.9_Production_Ready
    echo [OK] Found MBAS at: %MBAS_DIR%
) else if exist "MBAS_v1.0.9_Production_Ready" (
    set MBAS_DIR=MBAS_v1.0.9_Production_Ready
    echo [OK] Found MBAS at: %MBAS_DIR%
) else (
    echo [ERROR] Cannot find MBAS folder!
    echo.
    echo Please run this script from:
    echo   - The MBAS installation folder
    echo   - OR the parent folder containing MBAS
    echo.
    pause
    exit /b 1
)

cd /d "%MBAS_DIR%"
echo.

echo [STEP 4] Checking virtual environment...
echo.

if exist "venv\Scripts\python.exe" (
    echo [OK] Virtual environment exists
    echo     Location: %CD%\venv
    echo.
) else (
    echo [ERROR] Virtual environment is MISSING!
    echo.
    echo This is why MBAS failed to start.
    echo.
    echo FIXING NOW...
    echo.

    echo [*] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        echo.
        echo SOLUTIONS:
        echo   1. Close all Python/MBAS processes
        echo   2. Run this script as Administrator
        echo   3. Check if venv module is available: python -m venv --help
        echo.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
)

echo [STEP 5] Activating virtual environment...
echo.

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)

echo [OK] Virtual environment activated
echo.

echo [STEP 6] Checking core dependencies...
echo.

python -c "import fastapi, pydantic, uvicorn" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Core dependencies are MISSING!
    echo.
    echo FIXING NOW...
    echo.

    echo [*] Upgrading pip...
    python -m pip install --upgrade pip setuptools wheel --quiet

    echo [*] Installing dependencies (this may take 2-4 minutes)...
    echo     Please wait...
    echo.

    python -m pip install -r backend\requirements.txt

    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install dependencies!
        echo.
        echo Common fixes:
        echo   1. Check internet connection
        echo   2. Run as Administrator
        echo   3. Disable antivirus temporarily
        echo   4. Try: python -m pip install --upgrade pip
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependencies installed successfully
    echo.
) else (
    echo [OK] Core dependencies are installed
    echo     - FastAPI: OK
    echo     - Pydantic: OK
    echo     - Uvicorn: OK
    echo.
)

echo [STEP 7] Checking watchdog dependencies...
echo.

python -c "import requests, psutil" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Watchdog dependencies are MISSING!
    echo.
    echo FIXING NOW...
    echo.
    python -m pip install requests psutil --quiet

    if errorlevel 1 (
        echo [ERROR] Failed to install watchdog dependencies!
        pause
        exit /b 1
    )

    echo [OK] Watchdog dependencies installed
    echo.
) else (
    echo [OK] Watchdog dependencies are installed
    echo     - requests: OK
    echo     - psutil: OK
    echo.
)

echo [STEP 8] Checking tray dependencies...
echo.

python -c "import pystray, PIL" >nul 2>&1
if errorlevel 1 (
    echo [WARN] Tray dependencies are missing
    echo.
    echo FIXING NOW...
    python -m pip install pystray Pillow --quiet

    if not errorlevel 1 (
        echo [OK] Tray dependencies installed
    ) else (
        echo [WARN] Tray install failed - will retry on first start
    )
    echo.
) else (
    echo [OK] Tray dependencies are installed
    echo     - pystray: OK
    echo     - Pillow: OK
    echo.
)

echo [STEP 9] Checking database...
echo.

if exist "backend\mbas_database.db" (
    echo [OK] Database exists
    echo     Location: %CD%\backend\mbas_database.db
    echo.
) else (
    echo [WARN] Database is MISSING!
    echo.
    echo CREATING NOW...
    echo.

    cd backend
    python -c "from src.scripts.init_db import bootstrap; bootstrap()" 2>nul

    if exist "mbas_database.db" (
        echo [OK] Database created successfully
        echo.
    ) else (
        echo [WARN] Database creation may have had issues
        echo        Database will be created automatically on first start
        echo.
    )
    cd ..
)

echo [STEP 10] Checking port 8000 availability...
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
        echo.
        echo Process ID: %%a
        echo Process Name:
        tasklist /FI "PID eq %%a" /NH
        echo.
        echo To kill this process, run:
        echo   taskkill /F /PID %%a
        echo.
    )

    echo Do you want to kill the process now? (Y/N)
    choice /c YN /n /m "Choice: "
    if errorlevel 2 (
        echo.
        echo Process not killed. Please close it manually.
        echo.
    ) else (
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000.*LISTENING"') do (
            taskkill /F /PID %%a
        )
        echo [OK] Process killed
        echo.
    )
)

echo [STEP 11] Verifying all components...
echo.

set ALL_OK=1

if not exist "venv\Scripts\python.exe" (
    echo [X] Virtual environment: MISSING
    set ALL_OK=0
) else (
    echo [OK] Virtual environment: EXISTS
)

python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [X] FastAPI: NOT INSTALLED
    set ALL_OK=0
) else (
    echo [OK] FastAPI: INSTALLED
)

python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [X] Requests: NOT INSTALLED
    set ALL_OK=0
) else (
    echo [OK] Requests: INSTALLED
)

python -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo [X] Psutil: NOT INSTALLED
    set ALL_OK=0
) else (
    echo [OK] Psutil: INSTALLED
)

if not exist "backend\src\main.py" (
    echo [X] Backend code: MISSING
    set ALL_OK=0
) else (
    echo [OK] Backend code: EXISTS
)

if not exist "scripts\mbas_tray.py" (
    echo [X] Tray app: MISSING
    set ALL_OK=0
) else (
    echo [OK] Tray app: EXISTS
)

echo.

if %ALL_OK%==1 (
    echo ================================================================
    echo    [SUCCESS] All checks PASSED!
    echo ================================================================
    echo.
    echo MBAS is ready to start!
    echo.
    echo Next steps:
    echo   1. Close this window
    echo   2. Double-click: START_MBAS_TRAY.bat
    echo      OR
    echo      Double-click the "MBAS" desktop shortcut
    echo.
    echo The system tray icon should appear (green)
    echo Browser will open automatically
    echo.
    echo Login credentials:
    echo   Username: admin
    echo   Password: admin123
    echo.
) else (
    echo ================================================================
    echo    [WARNING] Some checks FAILED
    echo ================================================================
    echo.
    echo Some components are still missing.
    echo.
    echo Recommended actions:
    echo   1. Run INSTALL.bat again
    echo   2. Check for error messages
    echo   3. Run this diagnostic again
    echo.
)

echo ================================================================
echo.
pause
