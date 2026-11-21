@echo off
REM ============================================================================
REM  MBAS Installer Builder - Version 2.0.8
REM  Z&T Technologies - State-of-the-Art Business Solutions
REM
REM  This script builds the professional installer with:
REM  - Phase 1-3 backend hardening (stability, data-correctness, security/licensing)
REM  - Phase 4 professional UI overhaul (theming, app shell, DataTable, charts)
REM  - POS: fixed Complete Sale button incorrectly staying disabled
REM  - POS: new Hold Sale / Resume Sale (park an in-progress cart)
REM ============================================================================

echo.
echo ================================================================================
echo   MBAS Installer Builder v2.0.8
echo   Z^&T Technologies - State-of-the-Art Business Solutions
echo ================================================================================
echo.
echo This will build the MBAS Professional Setup installer.
echo.
echo Changes in v2.0.8:
echo   - Backend stability, data-correctness, and security/licensing hardening
echo   - Professional UI overhaul (theming, app shell, charts, shared DataTable)
echo   - FIXED: Complete Sale button could stay disabled with items in the cart
echo   - NEW: Hold Sale / Resume Sale for parking an in-progress POS transaction
echo.
echo Prerequisites:
echo   - Inno Setup 6 installed (https://jrsoftware.org/isdl.php)
echo   - Frontend built in ../../frontend/dist
echo   - Backend files in ../../backend
echo.
pause

REM Check if Inno Setup is installed
set "INNO_COMPILER=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

if not exist "%INNO_COMPILER%" (
    echo.
    echo [ERROR] Inno Setup 6 not found!
    echo Please install from: https://jrsoftware.org/isdl.php
    echo Expected location: %INNO_COMPILER%
    echo.
    pause
    exit /b 1
)

REM Check frontend build
if not exist "..\..\frontend\dist\index.html" (
    echo.
    echo [ERROR] Frontend not built!
    echo Please run: cd frontend ^&^& npm run build
    echo.
    pause
    exit /b 1
)

echo.
echo Building installer...
echo.

"%INNO_COMPILER%" "MBAS_Installer_Professional_ZT_v2.0.8.iss"

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    echo Check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo   Build Complete!
echo ================================================================================
echo.
echo Installer created in: output\
echo Filename: MBAS_Professional_Setup_v2.0.8_ZT_Technologies.exe
echo.
echo Next steps:
echo   1. Test the installer on a clean Windows machine
echo   2. Verify Complete Sale works immediately with items in the cart
echo   3. Verify Hold Sale / Resume Sale on the Billing page
echo   4. Test server start/stop functionality
echo   5. Check system tray icon behavior
echo.
pause
