@echo off
REM ============================================================================
REM Quick Fix for Installed MBAS v2.1.0
REM Fixes: 1) Port conflict dialog, 2) License validation bypass
REM ============================================================================

echo.
echo ==========================================
echo  MBAS v2.1.0 - Quick Fix Utility
echo ==========================================
echo.
echo This will fix:
echo  1. Port conflict dialog appearing every time
echo  2. License validation (enable STANDARD features)
echo.
pause

REM Try common installation locations
set INSTALL_DIR=

if exist "C:\Program Files\MBAS\START_MBAS_PWA_SILENT.vbs" (
    set INSTALL_DIR=C:\Program Files\MBAS
    goto FOUND
)

if exist "C:\Program Files (x86)\MBAS\START_MBAS_PWA_SILENT.vbs" (
    set INSTALL_DIR=C:\Program Files (x86)\MBAS
    goto FOUND
)

if exist "%USERPROFILE%\Desktop\MBAS\START_MBAS_PWA_SILENT.vbs" (
    set INSTALL_DIR=%USERPROFILE%\Desktop\MBAS
    goto FOUND
)

echo ERROR: Could not find MBAS installation directory!
echo.
echo Please enter the full path where MBAS is installed:
echo Example: C:\Program Files\MBAS
echo.
set /p INSTALL_DIR="MBAS Installation Path: "

:FOUND
if not exist "%INSTALL_DIR%\START_MBAS_PWA_SILENT.vbs" (
    echo ERROR: Invalid installation directory!
    echo File not found: %INSTALL_DIR%\START_MBAS_PWA_SILENT.vbs
    pause
    exit /b 1
)

echo.
echo Found MBAS at: %INSTALL_DIR%
echo.

REM Stop any running MBAS instances
echo [1/3] Stopping any running MBAS instances...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq MBAS*" >nul 2>&1
timeout /t 2 /nobreak >nul

REM Backup old launcher
echo [2/3] Backing up old launcher...
copy /Y "%INSTALL_DIR%\START_MBAS_PWA_SILENT.vbs" "%INSTALL_DIR%\START_MBAS_PWA_SILENT.vbs.backup" >nul

REM Copy fixed launcher
echo [3/3] Installing fixed launcher...
copy /Y "START_MBAS_PWA_SILENT.vbs" "%INSTALL_DIR%\START_MBAS_PWA_SILENT.vbs"

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo  Fix Applied Successfully!
    echo ==========================================
    echo.
    echo Changes made:
    echo  - Removed port conflict dialog
    echo  - Enabled license validation
    echo  - Backup saved: START_MBAS_PWA_SILENT.vbs.backup
    echo.
    echo Your STANDARD license will now be recognized!
    echo.
    echo To verify:
    echo  1. Double-click MBAS desktop shortcut
    echo  2. No dialog should appear
    echo  3. Browser opens automatically
    echo  4. Check Settings - License should show STANDARD
    echo.
) else (
    echo.
    echo ERROR: Failed to copy fixed launcher!
    echo.
    echo This may be a permissions issue.
    echo Try running this script as Administrator:
    echo  1. Right-click FIX_INSTALLED_MBAS.bat
    echo  2. Select "Run as administrator"
    echo.
)

pause
