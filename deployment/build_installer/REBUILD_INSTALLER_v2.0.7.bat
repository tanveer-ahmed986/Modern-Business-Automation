@echo off
REM ============================================================================
REM  MBAS Installer Builder - Version 2.0.7
REM  Z&T Technologies - State-of-the-Art Business Solutions
REM
REM  This script builds the professional installer with:
REM  - FIXED: Categories now created during installation
REM  - FIXED: CMD window blinking completely eliminated
REM ============================================================================

echo.
echo ================================================================================
echo   MBAS Installer Builder v2.0.7
echo   Z^&T Technologies - State-of-the-Art Business Solutions
echo ================================================================================
echo.
echo This will build the MBAS Professional Setup installer.
echo.
echo Changes in v2.0.7:
echo   - FIXED: Categories now created during installation
echo   - FIXED: CMD window blinking completely eliminated
echo   - Watchdog uses pythonw.exe with hidden window flags
echo   - Sample categories auto-created on first start
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

"%INNO_COMPILER%" "MBAS_Installer_Professional_ZT_v2.0.7.iss"

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
echo Filename: MBAS_Professional_Setup_v2.0.7_ZT_Technologies.exe
echo.
echo Changes in this version:
echo   - Categories automatically created during installation
echo   - No CMD window blinking during any operations
echo   - Watchdog auto-restart works silently
echo   - Professional user experience throughout
echo.
echo Next steps:
echo   1. Test the installer on a clean Windows machine
echo   2. Verify categories appear in product dropdown
echo   3. Verify no CMD window appears at any time
echo   4. Test server start/stop functionality
echo   5. Check system tray icon behavior
echo.
pause
