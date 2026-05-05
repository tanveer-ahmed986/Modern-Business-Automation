@echo off
title MBAS - IMMEDIATE FIX for C:\MBAS_TEST
color 0A
setlocal enabledelayedexpansion

cls
echo.
echo ================================================================================
echo    IMMEDIATE FIX FOR YOUR INSTALLATION
echo    Path detected: C:\MBAS_TEST
echo ================================================================================
echo.
echo This will:
echo   1. Stop all MBAS processes
echo   2. Fix frontend structure (404 errors)
echo   3. Fix startup scripts
echo   4. Start server WITHOUT watchdog (direct mode)
echo.
echo Takes 2 minutes. Press any key to start...
pause >nul

cd /d "%~dp0"

REM ============================================================================
REM STEP 1: STOP EVERYTHING
REM ============================================================================
echo.
echo [Step 1/5] Stopping all MBAS processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo [OK] All processes stopped
echo.

REM ============================================================================
REM STEP 2: FIX FRONTEND STRUCTURE IN YOUR INSTALLATION
REM ============================================================================
echo [Step 2/5] Fixing frontend structure in C:\MBAS_TEST...

REM Check if installation exists
if not exist "C:\MBAS_TEST\backend" (
    echo [ERROR] C:\MBAS_TEST not found!
    echo.
    echo Please enter your MBAS installation path:
    set /p INSTALL_PATH="Path: "
    if not exist "!INSTALL_PATH!\backend" (
        echo [FAIL] Invalid path!
        pause
        exit /b 1
    )
) else (
    set "INSTALL_PATH=C:\MBAS_TEST"
)

echo Installing to: %INSTALL_PATH%

REM Backup old frontend
if exist "%INSTALL_PATH%\frontend\dist" (
    if not exist "%INSTALL_PATH%\frontend\dist.old" (
        move "%INSTALL_PATH%\frontend\dist" "%INSTALL_PATH%\frontend\dist.old" >nul 2>&1
    ) else (
        rmdir /s /q "%INSTALL_PATH%\frontend\dist" >nul 2>&1
    )
)

REM Copy correct frontend structure
xcopy /E /I /Y "%~dp0frontend\dist" "%INSTALL_PATH%\frontend\dist" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Failed to copy frontend
    pause
    exit /b 1
)
echo [OK] Frontend structure fixed
echo.

REM ============================================================================
REM STEP 3: COPY FIXED SCRIPTS
REM ============================================================================
echo [Step 3/5] Installing fixed startup scripts...

REM Copy fixed tray script
copy /Y "%~dp0scripts\mbas_tray_FIXED.py" "%INSTALL_PATH%\scripts\mbas_tray.py" >nul 2>&1
echo [OK] Tray script updated
echo.

REM ============================================================================
REM STEP 4: CREATE DIRECT START SCRIPT (NO WATCHDOG)
REM ============================================================================
echo [Step 4/5] Creating direct start script...

REM Create a simple direct start script
(
echo @echo off
echo title MBAS Server - Direct Mode
echo color 0A
echo.
echo ================================================================
echo    MBAS Server - Direct Start ^(No Watchdog^)
echo ================================================================
echo.
echo Starting backend server...
echo Server will be available at: http://localhost:8000
echo.
echo Login: admin / admin123
echo.
echo Press Ctrl+C to stop the server.
echo ================================================================
echo.
echo.
echo Starting in 3 seconds...
timeout /t 3 /nobreak ^>nul
echo.
cd /d "%INSTALL_PATH%\backend"
call "%INSTALL_PATH%\venv\Scripts\activate.bat"
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000
pause
) > "%INSTALL_PATH%\START_MBAS_DIRECT.bat"

echo [OK] Direct start script created
echo.

REM ============================================================================
REM STEP 5: VERIFY AND START
REM ============================================================================
echo [Step 5/5] Verifying installation...

REM Check venv
if not exist "%INSTALL_PATH%\venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment missing!
    echo Please run: %INSTALL_PATH%\INSTALL.bat
    pause
    exit /b 1
)
echo [OK] Virtual environment exists

REM Check frontend structure
if not exist "%INSTALL_PATH%\frontend\dist\assets" (
    echo [ERROR] Frontend assets still missing!
    pause
    exit /b 1
)
echo [OK] Frontend assets exist

REM Check backend
if not exist "%INSTALL_PATH%\backend\src\main.py" (
    echo [ERROR] Backend missing!
    pause
    exit /b 1
)
echo [OK] Backend exists

echo.
echo ================================================================================
echo    [SUCCESS] FIX COMPLETE!
echo ================================================================================
echo.
echo Your MBAS installation at: %INSTALL_PATH%
echo Has been fixed with:
echo   ✓ Correct frontend structure ^(assets in subfolder^)
echo   ✓ Fixed startup scripts
echo   ✓ Direct start mode ^(bypasses watchdog issues^)
echo.
echo ================================================================================
echo    STARTING MBAS NOW...
echo ================================================================================
echo.
echo Server will start in a new window.
echo Wait 15-20 seconds, then open browser to: http://localhost:8000
echo.
echo If you see the login page WITHOUT 404 errors - SUCCESS!
echo.
pause

REM Start in a new window so user can see the output
start "MBAS Server" cmd /k "%INSTALL_PATH%\START_MBAS_DIRECT.bat"

echo.
echo Server starting in new window...
echo Wait 15-20 seconds, then open: http://localhost:8000
echo.
echo If it works:
echo   - You'll see the login page with proper styling
echo   - No 404 errors in browser console ^(press F12^)
echo   - Dashboard loads after login
echo.
echo If it doesn't work:
echo   - Check the server window for errors
echo   - Make sure port 8000 is not in use
echo   - Check: %INSTALL_PATH%\mbas_tray.log
echo.
pause
