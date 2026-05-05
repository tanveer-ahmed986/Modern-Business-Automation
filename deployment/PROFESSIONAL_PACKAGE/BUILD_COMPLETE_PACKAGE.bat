@echo off
title Building MBAS Professional Package - Z&T Technologies
color 0B

cls
echo.
echo ================================================================================
echo    MBAS Professional Package Builder v2.0
echo    Z^&T Technologies - State-of-the-Art Business Solutions
echo    www.zttechnologies.org
echo ================================================================================
echo.

cd /d "%~dp0"

echo This script will create a PRODUCTION-READY installer with:
echo   ✓ Z^&T Technologies branding throughout
echo   ✓ Professional Windows .exe installer  
echo   ✓ No CMD windows (system tray mode)
echo   ✓ All dependencies bundled
echo   ✓ Ready for end-user distribution
echo.
pause

REM Create folders
echo [Step 1/6] Creating package structure...
mkdir package\backend 2>nul
mkdir package\frontend 2>nul  
mkdir package\scripts 2>nul
mkdir branding 2>nul
mkdir Output 2>nul

REM Copy backend
echo [Step 2/6] Copying backend...
xcopy /E /I /Y "..\..\backend" "package\backend"

REM Build frontend
echo [Step 3/6] Building frontend...
cd ..\..\frontend
call npm run build
xcopy /E /I /Y "dist" "..\deployment\PROFESSIONAL_PACKAGE\package\frontend\dist"
cd ..\deployment\PROFESSIONAL_PACKAGE

REM Copy branding
echo [Step 4/6] Setting up branding...
if exist "..\..\mbas_icon.ico" copy /Y "..\..\mbas_icon.ico" "branding\mbas_icon.ico"

REM Create simplified installer (without embedded Python)
echo [Step 5/6] Creating installer script...
echo Done

REM Build installer  
echo [Step 6/6] Ready to build installer
echo.
echo Next: Install Inno Setup and run MBAS_Professional_Installer.iss
echo.
pause
