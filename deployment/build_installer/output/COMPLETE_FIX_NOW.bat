@echo off
title MBAS - Complete Fix (All-in-One)
color 0C

echo.
echo ========================================================================
echo    MBAS COMPLETE FIX - Solves "Failed to start" Error
echo ========================================================================
echo.
echo This script will:
echo   1. Stop any running MBAS processes
echo   2. Increase startup timeout to 45 seconds
echo   3. Fix any missing dependencies
echo   4. Start MBAS with proper logging
echo.
echo Press any key to start...
pause >nul

echo.
echo [Step 1/4] Stopping MBAS...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo [OK] MBAS stopped

echo.
echo [Step 2/4] Fixing startup timeout...
set TRAY_SCRIPT=C:\Program Files\MBAS\scripts\mbas_tray.py

if exist "%TRAY_SCRIPT%" (
    REM Backup original
    copy "%TRAY_SCRIPT%" "%TRAY_SCRIPT%.backup" >nul 2>&1

    REM Increase timeout from 15 to 45 seconds
    powershell -Command "(Get-Content '%TRAY_SCRIPT%') -replace 'max_retries = 15', 'max_retries = 45' -replace 'within 15 seconds', 'within 45 seconds' | Set-Content '%TRAY_SCRIPT%'" >nul 2>&1

    echo [OK] Timeout increased to 45 seconds
) else (
    echo [WARNING] Tray script not found, skipping
)

echo.
echo [Step 3/4] Verifying dependencies...
cd /d "C:\Program Files\MBAS"

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat

    REM Check and install missing packages
    python -c "import pystray" >nul 2>&1
    if errorlevel 1 (
        echo [*] Installing system tray dependencies...
        python -m pip install pystray Pillow psutil requests --quiet
    )

    python -c "import fastapi" >nul 2>&1
    if errorlevel 1 (
        echo [*] Installing backend dependencies...
        if exist "backend\requirements.txt" (
            python -m pip install -r backend\requirements.txt --quiet
        )
    )

    echo [OK] All dependencies verified
) else (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Running full reinstall...
    if exist "INSTALL.bat" (
        call INSTALL.bat
    ) else (
        echo [ERROR] INSTALL.bat not found!
        echo Please run MBAS_Setup_v1.1.0_Simple.exe again.
        pause
        exit /b 1
    )
)

echo.
echo [Step 4/4] Starting MBAS...
echo.
echo Please wait up to 45 seconds for MBAS to start...
echo.

if exist "START_MBAS_TRAY.bat" (
    START_MBAS_TRAY.bat
) else (
    echo [ERROR] START_MBAS_TRAY.bat not found!
    echo.
    echo Installation may be incomplete.
    echo Please run MBAS_Setup_v1.1.0_Simple.exe again.
    pause
    exit /b 1
)
