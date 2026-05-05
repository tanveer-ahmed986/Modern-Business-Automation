@echo off
title MBAS - Fix Startup Timeout
color 0B

echo.
echo ========================================================================
echo    MBAS Startup Timeout Fix
echo    Increases startup timeout from 15 to 45 seconds
echo ========================================================================
echo.

set TRAY_SCRIPT=C:\Program Files\MBAS\scripts\mbas_tray.py

if not exist "%TRAY_SCRIPT%" (
    echo [ERROR] MBAS not found at C:\Program Files\MBAS
    echo.
    echo Please install MBAS first using MBAS_Setup_v1.1.0_Simple.exe
    pause
    exit /b 1
)

echo [*] Backing up original file...
copy "%TRAY_SCRIPT%" "%TRAY_SCRIPT%.backup" >nul 2>&1

echo [*] Updating timeout from 15 to 45 seconds...
powershell -Command "(Get-Content '%TRAY_SCRIPT%') -replace 'max_retries = 15  # 15 seconds max wait', 'max_retries = 45  # 45 seconds max wait' -replace 'Server failed to start within 15 seconds', 'Server failed to start within 45 seconds' | Set-Content '%TRAY_SCRIPT%'"

if errorlevel 1 (
    echo [ERROR] Failed to update file!
    echo.
    echo Restoring backup...
    copy "%TRAY_SCRIPT%.backup" "%TRAY_SCRIPT%" >nul 2>&1
    pause
    exit /b 1
)

echo [OK] Timeout increased to 45 seconds!
echo.
echo ========================================================================
echo    Fix Applied Successfully!
echo ========================================================================
echo.
echo The startup timeout has been increased from 15 to 45 seconds.
echo This should resolve the "Failed to start within 15 seconds" error.
echo.
echo Next step:
echo   1. Close any running MBAS instances
echo   2. Launch MBAS from desktop shortcut
echo   3. Wait up to 45 seconds for startup
echo.
echo Press any key to launch MBAS now...
pause >nul

cd /d "C:\Program Files\MBAS"
START_MBAS_TRAY.bat
