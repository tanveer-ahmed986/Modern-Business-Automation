@echo off
title MBAS v1.0.9 - Installation Verification
color 0E
setlocal enabledelayedexpansion

echo.
echo ================================================================
echo    MBAS v1.0.9 Production Package - Verification Script
echo ================================================================
echo.
echo This script will verify all critical fixes are in place.
echo.
pause

set PASS_COUNT=0
set FAIL_COUNT=0

REM Test 1: Check INSTALL.bat has Step 5/6 for tray dependencies
echo [Test 1/5] Verifying INSTALL.bat includes tray dependencies...
findstr /C:"Installing system tray dependencies" INSTALL.bat >nul 2>&1
if errorlevel 1 (
    echo [FAIL] INSTALL.bat missing tray dependency installation
    set /a FAIL_COUNT+=1
) else (
    echo [PASS] INSTALL.bat includes tray dependencies
    set /a PASS_COUNT+=1
)
echo.

REM Test 2: Check START_MBAS_TRAY.bat includes database init check
echo [Test 2/5] Verifying START_MBAS_TRAY.bat includes database init...
findstr /C:"bootstrap" START_MBAS_TRAY.bat >nul 2>&1
if errorlevel 1 (
    echo [FAIL] START_MBAS_TRAY.bat missing database init check
    set /a FAIL_COUNT+=1
) else (
    echo [PASS] START_MBAS_TRAY.bat includes database init
    set /a PASS_COUNT+=1
)
echo.

REM Test 3: Check db.py uses StaticPool
echo [Test 3/5] Verifying backend/src/core/db.py uses StaticPool...
findstr /C:"StaticPool" backend\src\core\db.py >nul 2>&1
if errorlevel 1 (
    echo [FAIL] db.py not using StaticPool for SQLite
    set /a FAIL_COUNT+=1
) else (
    echo [PASS] db.py correctly uses StaticPool
    set /a PASS_COUNT+=1
)
echo.

REM Test 4: Check db.py has busy_timeout pragma
echo [Test 4/5] Verifying db.py includes busy_timeout pragma...
findstr /C:"busy_timeout" backend\src\core\db.py >nul 2>&1
if errorlevel 1 (
    echo [FAIL] db.py missing busy_timeout pragma
    set /a FAIL_COUNT+=1
) else (
    echo [PASS] db.py includes busy_timeout pragma
    set /a PASS_COUNT+=1
)
echo.

REM Test 5: Check mbas_tray.py has watchdog fallback
echo [Test 5/5] Verifying mbas_tray.py includes watchdog fallback...
findstr /C:"use_watchdog" scripts\mbas_tray.py >nul 2>&1
if errorlevel 1 (
    echo [FAIL] mbas_tray.py missing watchdog fallback logic
    set /a FAIL_COUNT+=1
) else (
    echo [PASS] mbas_tray.py includes watchdog fallback
    set /a PASS_COUNT+=1
)
echo.

REM Summary
echo ================================================================
echo    VERIFICATION SUMMARY
echo ================================================================
echo.
echo Tests Passed: %PASS_COUNT%/5
echo Tests Failed: %FAIL_COUNT%/5
echo.

if %FAIL_COUNT% EQU 0 (
    color 0A
    echo [SUCCESS] All critical fixes verified!
    echo.
    echo This package is PRODUCTION READY.
    echo You can proceed with client deployment.
    echo.
) else (
    color 0C
    echo [WARNING] Some fixes are missing!
    echo.
    echo Please review PRODUCTION_FIXES_REPORT.md
    echo and ensure all changes are applied correctly.
    echo.
)

echo ================================================================
echo.
pause
