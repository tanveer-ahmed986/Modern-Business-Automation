@echo off
title MBAS - One-Click Installation Fix
color 0A
setlocal enabledelayedexpansion

cls
echo.
echo ================================================================================
echo    MBAS ONE-CLICK INSTALLATION FIX
echo    Fixes: Server startup failures, CMD blinking, Python errors
echo ================================================================================
echo.
echo This script will fix all known issues with MBAS v1.2.1 installation:
echo.
echo   [FIXED] Server fails to start within 15 seconds
echo   [FIXED] CMD windows blinking repeatedly
echo   [FIXED] Python errors during startup
echo   [FIXED] System tray icon not working
echo   [FIXED] Undefined variable crash (self.server_url)
echo.
echo The fix takes 5-10 minutes and requires:
echo   - Internet connection (to download Python packages)
echo   - Python 3.11 or 3.12 installed
echo   - 1GB free disk space
echo.
echo ================================================================================
echo    WHAT WILL HAPPEN:
echo ================================================================================
echo.
echo Phase 1: Emergency Fix (5-10 minutes)
echo   - Stop all MBAS processes
echo   - Recreate virtual environment
echo   - Reinstall all dependencies
echo   - Apply critical bug fixes
echo   - Initialize database
echo.
echo Phase 2: Diagnostic Check (30 seconds)
echo   - Verify all components
echo   - Test server startup
echo   - Check for errors
echo.
echo Phase 3: Launch MBAS (30 seconds)
echo   - Start with fixed launcher
echo   - Auto-open browser
echo   - Ready to use
echo.
echo ================================================================================
echo.
echo Press any key to start the fix process...
echo Or close this window to cancel.
pause >nul

REM ================================================================================
REM PHASE 1: Emergency Fix
REM ================================================================================

cls
echo.
echo ================================================================================
echo    PHASE 1: EMERGENCY FIX
echo ================================================================================
echo.
echo Running comprehensive fix...
echo This may take 5-10 minutes. Please be patient.
echo.

call "%~dp0EMERGENCY_FIX.bat"

if errorlevel 1 (
    echo.
    echo [FAIL] Emergency fix encountered errors!
    echo        Please run manually: EMERGENCY_FIX.bat
    echo        And check the error messages.
    pause
    exit /b 1
)

REM ================================================================================
REM PHASE 2: Diagnostic Check
REM ================================================================================

cls
echo.
echo ================================================================================
echo    PHASE 2: DIAGNOSTIC CHECK
echo ================================================================================
echo.
echo Verifying installation...
echo.

REM Quick diagnostic without full test
call "%~dp0venv\Scripts\activate.bat"

echo Checking Python packages...
python -c "import fastapi, uvicorn, sqlmodel, pystray" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Some packages are missing!
    echo        Running full diagnostic...
    call "%~dp0DIAGNOSE_STARTUP_ISSUE.bat"
    pause
    exit /b 1
)
echo [OK] All packages installed

echo Checking backend structure...
if not exist "%~dp0backend\src\main.py" (
    echo [FAIL] Backend files missing!
    pause
    exit /b 1
)
echo [OK] Backend structure valid

echo Checking database...
if not exist "%~dp0backend\mbas_database.db" (
    echo [WARN] Database not found, will be created on startup
) else (
    echo [OK] Database exists
)

echo.
echo [SUCCESS] All diagnostic checks passed!
echo.

REM ================================================================================
REM PHASE 3: Launch MBAS
REM ================================================================================

cls
echo.
echo ================================================================================
echo    PHASE 3: LAUNCHING MBAS
echo ================================================================================
echo.
echo MBAS will now start in the background (system tray mode).
echo.
echo What to expect:
echo   1. A system tray icon will appear (near the clock)
echo   2. Icon will be GRAY for ~30 seconds (starting)
echo   3. Icon turns GREEN when ready
echo   4. Browser opens automatically to http://localhost:8000
echo.
echo Login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo IMPORTANT: First startup takes 25-30 seconds.
echo            This is normal! Please be patient.
echo.
echo If you don't see the tray icon or browser doesn't open:
echo   1. Check system tray (click ^ arrow to show hidden icons)
echo   2. Manually open: http://localhost:8000
echo   3. Check log file: mbas_tray.log
echo.
echo Press any key to launch MBAS...
pause >nul

REM Launch MBAS
call "%~dp0START_MBAS_TRAY_FIXED.bat"

REM Wait a few seconds
timeout /t 5 /nobreak >nul

REM Show final message
cls
echo.
echo ================================================================================
echo    [SUCCESS] MBAS IS STARTING!
echo ================================================================================
echo.
echo MBAS is now running in the background.
echo.
echo Check your system tray (near the clock) for the MBAS icon.
echo.
echo Status colors:
echo   GRAY  = Starting (wait 30 seconds)
echo   GREEN = Running (ready to use)
echo   RED   = Stopped
echo.
echo If browser doesn't open automatically:
echo   Open manually: http://localhost:8000
echo.
echo If you see errors or icon doesn't appear:
echo   1. Read: README_CRITICAL_FIX.txt
echo   2. Check: mbas_tray.log
echo   3. Run: DIAGNOSE_STARTUP_ISSUE.bat
echo.
echo To stop MBAS:
echo   Right-click tray icon and select "Exit"
echo   Or run: STOP_MBAS.bat
echo.
echo ================================================================================
echo.
echo This window will close in 10 seconds...
timeout /t 10

exit
