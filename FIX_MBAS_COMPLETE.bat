@echo off
REM ============================================================================
REM MBAS v2.1.0 - Complete Fix Script
REM Fixes: 1) Port conflict dialog, 2) License validation, 3) Install STANDARD license
REM Run this from your development folder
REM ============================================================================

echo.
echo ===============================================================
echo  MBAS v2.1.0 - Complete Fix Utility
echo  Z^&T Technologies
echo ===============================================================
echo.
echo This script will fix your installed MBAS:
echo  1. Remove annoying "MBAS already running" dialog
echo  2. Enable license validation (no more bypass)
echo  3. Install STANDARD perpetual license
echo  4. Restart MBAS with all features enabled
echo.
echo IMPORTANT: This must be run as Administrator!
echo.
pause

REM Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] This script requires Administrator privileges!
    echo.
    echo Please right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

REM Try to find MBAS installation
set INSTALL_DIR=

if exist "C:\Program Files\MBAS\START_MBAS_PWA_SILENT.vbs" (
    set INSTALL_DIR=C:\Program Files\MBAS
    goto FOUND
)

if exist "C:\Program Files (x86)\MBAS\START_MBAS_PWA_SILENT.vbs" (
    set INSTALL_DIR=C:\Program Files (x86)\MBAS
    goto FOUND
)

echo.
echo Could not auto-detect MBAS installation.
echo Please enter the full path where MBAS is installed:
echo.
echo Example: C:\Program Files\MBAS
echo.
set /p INSTALL_DIR="MBAS Installation Path: "

:FOUND
if not exist "%INSTALL_DIR%\START_MBAS_PWA_SILENT.vbs" (
    echo.
    echo [ERROR] Invalid installation directory!
    echo File not found: %INSTALL_DIR%\START_MBAS_PWA_SILENT.vbs
    echo.
    pause
    exit /b 1
)

echo.
echo ===============================================================
echo  Found MBAS at: %INSTALL_DIR%
echo ===============================================================
echo.

REM Stop any running MBAS instances
echo [1/4] Stopping any running MBAS instances...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq MBAS*" >nul 2>&1
if %errorlevel% equ 0 (
    echo       MBAS server stopped successfully
) else (
    echo       No MBAS server was running
)
timeout /t 2 /nobreak >nul

REM Backup old files
echo.
echo [2/4] Backing up old files...
if not exist "%INSTALL_DIR%\backup" mkdir "%INSTALL_DIR%\backup"
copy /Y "%INSTALL_DIR%\START_MBAS_PWA_SILENT.vbs" "%INSTALL_DIR%\backup\START_MBAS_PWA_SILENT.vbs.old" >nul 2>&1
if exist "%INSTALL_DIR%\mbas.license" (
    copy /Y "%INSTALL_DIR%\mbas.license" "%INSTALL_DIR%\backup\mbas.license.old" >nul 2>&1
    echo       Old license backed up
)
echo       Backups saved to: %INSTALL_DIR%\backup\

REM Install fixed launcher
echo.
echo [3/4] Installing fixed launcher...
copy /Y "deployment\build_installer\START_MBAS_PWA_SILENT.vbs" "%INSTALL_DIR%\START_MBAS_PWA_SILENT.vbs"
if %errorlevel% equ 0 (
    echo       Launcher updated successfully
    echo       - Port conflict dialog: REMOVED
    echo       - License validation: ENABLED
) else (
    echo       [ERROR] Failed to copy launcher!
    echo       Check if the file exists at:
    echo       deployment\build_installer\START_MBAS_PWA_SILENT.vbs
    pause
    exit /b 1
)

REM Install STANDARD license
echo.
echo [4/4] Installing STANDARD license...
copy /Y "license\mbas_production_standard.license" "%INSTALL_DIR%\mbas.license"
if %errorlevel% equ 0 (
    echo       STANDARD license installed successfully
    echo       Licensee: Beta Tester - Production License
    echo       Tier: STANDARD (Perpetual)
    echo       Features: All Standard features enabled
) else (
    echo       [ERROR] Failed to copy license!
    echo       Check if the file exists at:
    echo       license\mbas_production_standard.license
    pause
    exit /b 1
)

echo.
echo ===============================================================
echo  ALL FIXES APPLIED SUCCESSFULLY!
echo ===============================================================
echo.
echo Changes made:
echo  [OK] Launcher updated (no more port conflict dialog)
echo  [OK] License validation enabled
echo  [OK] STANDARD license installed
echo  [OK] Backups saved to: %INSTALL_DIR%\backup\
echo.
echo Your MBAS now has STANDARD tier with these features:
echo  - Dashboard
echo  - Inventory Management
echo  - Point of Sale (Billing)
echo  - Customer Management
echo  - Supplier Management
echo  - Purchase Orders
echo  - Advanced Reports (STANDARD feature)
echo  - Backup ^& Restore
echo.
echo ===============================================================
echo  TESTING INSTRUCTIONS
echo ===============================================================
echo.
echo 1. Double-click your MBAS desktop shortcut
echo.
echo 2. What should happen:
echo    - No "MBAS already running" dialog
echo    - Browser opens automatically
echo    - Login page appears
echo.
echo 3. Login with: admin / admin123
echo.
echo 4. Go to Settings (gear icon) to verify license:
echo    - Should show: LICENSE: STANDARD
echo    - Should show: STATUS: ACTIVE
echo    - Should show: TYPE: PERPETUAL
echo.
echo 5. Test Advanced Reports (now available with STANDARD):
echo    - Go to Reports section
echo    - All report types should be accessible
echo.
echo ===============================================================
echo.
set /p TEST="Start MBAS now? (Y/N): "
if /i "%TEST%"=="Y" (
    echo.
    echo Starting MBAS...
    cd /d "%INSTALL_DIR%"
    start "" wscript.exe "START_MBAS_PWA_SILENT.vbs"
    echo.
    echo MBAS is starting...
    echo Browser should open in 5-7 seconds
    echo.
)

echo.
echo ===============================================================
echo  Fix script completed!
echo ===============================================================
echo.
echo If you encounter any issues:
echo  1. Backups are in: %INSTALL_DIR%\backup\
echo  2. To restore: Copy .old files back to main directory
echo  3. Contact: support@zttechnologies.org
echo.
pause
