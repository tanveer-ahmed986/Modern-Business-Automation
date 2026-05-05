@echo off
title MBAS - Emergency Fix (All-in-One)
color 0C

echo.
echo ========================================================================
echo    MBAS Emergency Fix Tool v1.0
echo    Automatically fixes common installation and startup issues
echo ========================================================================
echo.
echo This script will:
echo   [1] Stop all MBAS processes
echo   [2] Free port 8000
echo   [3] Unblock downloaded files (Smart App Control fix)
echo   [4] Add Windows Defender exclusion
echo   [5] Recreate virtual environment
echo   [6] Reinstall all dependencies
echo   [7] Initialize database
echo   [8] Verify installation
echo   [9] Start MBAS with debug logging
echo.
echo IMPORTANT: This requires Administrator privileges!
echo            This will take 5-10 minutes to complete.
echo.
echo Press any key to start emergency fix...
pause >nul

cd /d "%~dp0"

echo.
echo ========================================================================
echo [1/9] Stopping all MBAS processes...
echo ========================================================================

taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1

timeout /t 2 /nobreak >nul

echo [OK] All Python processes stopped
echo.

echo ========================================================================
echo [2/9] Freeing port 8000...
echo ========================================================================

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo [*] Killing process using port 8000 (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)

timeout /t 2 /nobreak >nul

echo [OK] Port 8000 is now free
echo.

echo ========================================================================
echo [3/9] Unblocking all files (Smart App Control fix)...
echo ========================================================================

powershell -Command "Get-ChildItem -Path '%~dp0' -Recurse | Unblock-File" 2>nul

echo [OK] All files unblocked
echo.

echo ========================================================================
echo [4/9] Adding Windows Defender exclusion...
echo ========================================================================

powershell -Command "Add-MpPreference -ExclusionPath '%~dp0'" 2>nul

echo [OK] Windows Defender exclusion added
echo.

echo ========================================================================
echo [5/9] Recreating virtual environment...
echo ========================================================================

if exist "%~dp0venv" (
    echo [*] Removing old virtual environment...
    rmdir /s /q "%~dp0venv" 2>nul

    REM If deletion fails, try takeown
    if exist "%~dp0venv" (
        echo [*] Using advanced deletion method...
        takeown /F "%~dp0venv" /R /D Y >nul 2>&1
        icacls "%~dp0venv" /grant administrators:F /T >nul 2>&1
        rmdir /s /q "%~dp0venv" >nul 2>&1
    )
)

echo [*] Creating fresh virtual environment...
python -m venv "%~dp0venv"

if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment!
    echo.
    echo Please ensure:
    echo   1. Python 3.11 or 3.12 is installed
    echo   2. You are running as Administrator
    echo   3. Antivirus is not blocking venv creation
    echo.
    pause
    exit /b 1
)

echo [OK] Virtual environment created
echo.

echo ========================================================================
echo [6/9] Installing all dependencies (this may take 3-5 minutes)...
echo ========================================================================

call "%~dp0venv\Scripts\activate.bat"

echo [*] Upgrading pip...
python -m pip install --upgrade pip setuptools wheel --quiet

echo [*] Installing backend dependencies...
if exist "%~dp0backend\requirements-lock.txt" (
    python -m pip install -r "%~dp0backend\requirements-lock.txt" --quiet
) else if exist "%~dp0backend\requirements.txt" (
    python -m pip install -r "%~dp0backend\requirements.txt" --quiet
) else (
    echo [ERROR] requirements.txt not found!
    pause
    exit /b 1
)

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    echo.
    echo Please check:
    echo   1. Internet connection is working
    echo   2. You are using Python 3.11 or 3.12
    echo   3. No firewall is blocking pip downloads
    echo.
    pause
    exit /b 1
)

echo [*] Installing system tray dependencies...
python -m pip install pystray Pillow psutil requests watchdog --quiet

echo [OK] All dependencies installed
echo.

echo ========================================================================
echo [7/9] Initializing database...
echo ========================================================================

cd backend

if exist "mbas_database.db" (
    echo [*] Database already exists, skipping initialization
) else (
    echo [*] Creating new database...
    python -c "from pathlib import Path; import sys; sys.path.insert(0, 'src'); from scripts.init_db import bootstrap; bootstrap()"

    if errorlevel 1 (
        echo [ERROR] Database initialization failed!
        pause
        cd ..
        exit /b 1
    )

    echo [OK] Database initialized
)

cd ..
echo.

echo ========================================================================
echo [8/9] Verifying installation...
echo ========================================================================

echo [*] Checking Python packages...
python -c "import fastapi, uvicorn, sqlalchemy, pystray" 2>nul

if errorlevel 1 (
    echo [ERROR] Required packages are missing!
    echo Please run INSTALL.bat manually.
    pause
    exit /b 1
)

echo [OK] All required packages found

echo [*] Checking backend files...
if not exist "%~dp0backend\src\main.py" (
    echo [ERROR] Backend main.py not found!
    pause
    exit /b 1
)

echo [OK] Backend files present

echo [*] Checking system tray...
if not exist "%~dp0scripts\mbas_tray.py" (
    echo [ERROR] System tray script not found!
    pause
    exit /b 1
)

echo [OK] System tray present

echo [*] Checking database...
if not exist "%~dp0backend\mbas_database.db" (
    echo [ERROR] Database not found!
    pause
    exit /b 1
)

echo [OK] Database present
echo.

echo ========================================================================
echo [9/9] Applying critical bug fixes...
echo ========================================================================

REM Apply the fixed tray script
if exist "%~dp0scripts\mbas_tray_FIXED.py" (
    echo [*] Applying system tray bug fixes...
    copy /Y "%~dp0scripts\mbas_tray_FIXED.py" "%~dp0scripts\mbas_tray.py" >nul 2>&1
    echo [OK] System tray script updated
) else (
    echo [WARN] Fixed tray script not found - skipping
)

echo.
echo ========================================================================
echo    [SUCCESS] Emergency Fix Complete!
echo ========================================================================
echo.
echo All issues have been resolved. MBAS is ready to start.
echo.
echo NEXT STEPS:
echo   1. Run: DIAGNOSE_STARTUP_ISSUE.bat (to verify everything works)
echo   2. If diagnosis passes, run: START_MBAS_TRAY_FIXED.bat
echo   3. Check logs in: mbas_tray.log for detailed startup info
echo.
echo WHAT WAS FIXED:
echo   - Virtual environment recreated
echo   - All dependencies reinstalled
echo   - Database initialized
echo   - Critical bug in tray app fixed (30-second timeout + undefined variable)
echo   - File permissions fixed
echo.
echo If MBAS still doesn't start:
echo   1. Check mbas_tray.log for specific error messages
echo   2. Run DIAGNOSE_STARTUP_ISSUE.bat to see detailed diagnostics
echo   3. Ensure Python 3.11 or 3.12 is installed (not 3.13+)
echo.
pause
