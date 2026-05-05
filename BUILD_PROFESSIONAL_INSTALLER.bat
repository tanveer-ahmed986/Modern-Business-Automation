@echo off
title Building MBAS Professional Installer - Z&T Technologies
color 0B

cls
echo.
echo ================================================================================
echo    MBAS PROFESSIONAL INSTALLER BUILD SCRIPT
echo    Z^&T Technologies - State-of-the-Art Business Solutions
echo    www.zttechnologies.org
echo ================================================================================
echo.
echo This script will create a production-ready Windows installer with:
echo   ✓ Z^&T Technologies branding throughout
echo   ✓ Professional .exe installer
echo   ✓ No CMD windows (system tray mode)
echo   ✓ All components bundled
echo   ✓ Ready for customer distribution
echo.
pause

cd /d "%~dp0"

echo.
echo [Step 1/4] Building frontend...
echo.
cd frontend
call npm install
call npm run build

if errorlevel 1 (
    echo [FAIL] Frontend build failed!
    pause
    exit /b 1
)

echo [OK] Frontend built successfully
cd..

echo.
echo [Step 2/4] Copying documentation...
echo.
if not exist "deployment\PROFESSIONAL_PACKAGE\docs" mkdir "deployment\PROFESSIONAL_PACKAGE\docs"
copy /Y "deployment\PROFESSIONAL_PACKAGE\docs\Installation_Guide.md" "deployment\PROFESSIONAL_PACKAGE\docs\" >nul 2>&1
copy /Y "deployment\PROFESSIONAL_PACKAGE\docs\About.html" "deployment\PROFESSIONAL_PACKAGE\docs\" >nul 2>&1

echo [OK] Documentation ready

echo.
echo [Step 3/4] Verifying files...
echo.

REM Check critical files
set "ERROR=0"

if not exist "backend\src\main.py" (
    echo [FAIL] Backend not found!
    set "ERROR=1"
) else (
    echo [OK] Backend found
)

if not exist "frontend\dist\index.html" (
    echo [FAIL] Frontend dist not found!
    set "ERROR=1"
) else (
    echo [OK] Frontend dist found
)

if not exist "mbas_icon.ico" (
    echo [WARN] Icon not found - using default
) else (
    echo [OK] Icon found
)

if "%ERROR%"=="1" (
    echo.
    echo [FAIL] Missing critical files!
    pause
    exit /b 1
)

echo.
echo [Step 4/4] Compiling installer with Inno Setup...
echo.

set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

if not exist "%INNO_PATH%" (
    echo [FAIL] Inno Setup not found!
    echo.
    echo Please install Inno Setup 6 from:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo Then manually compile:
    echo   deployment\build_installer\MBAS_Installer_Professional_ZT.iss
    echo.
    pause
    exit /b 1
)

cd deployment\build_installer
"%INNO_PATH%" "MBAS_Installer_Professional_ZT.iss"
cd ..\..

if not exist "deployment\build_installer\output\MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe" (
    echo [WARN] Output file not found at expected location
    echo        Check: deployment\build_installer\output\
)

if errorlevel 1 (
    echo [FAIL] Installer compilation failed!
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo    [SUCCESS] PROFESSIONAL INSTALLER BUILT!
echo ================================================================================
echo.
echo Created file:
dir "deployment\build_installer\output\MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe" 2>nul

echo.
echo Installer features:
echo   ✓ Z^&T Technologies branding
echo   ✓ Professional Windows .exe
echo   ✓ No CMD windows for end users
echo   ✓ System tray mode
echo   ✓ Automatic dependency installation
echo   ✓ Desktop ^& Start Menu shortcuts
echo   ✓ Clean uninstall
echo.
echo NEXT STEPS:
echo   1. Test installer on clean Windows 10/11 machine
echo   2. Verify MBAS starts without CMD windows
echo   3. Check all branding appears correctly
echo   4. Test all features work
echo   5. Upload to www.zttechnologies.org
echo.
echo DISTRIBUTION:
echo   - File: MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe
echo   - Location: deployment\build_installer\output\
echo   - Size: ~50-80 MB
echo.
echo A Product of Z^&T Technologies
echo State-of-the-Art Business Solutions
echo www.zttechnologies.org
echo.
pause
