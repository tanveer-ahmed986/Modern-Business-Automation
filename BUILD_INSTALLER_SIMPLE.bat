@echo off
title Build MBAS Installer - Z&T Technologies
color 0B

cls
echo.
echo ================================================================================
echo    BUILDING MBAS PROFESSIONAL INSTALLER
echo    Z^&T Technologies - www.zttechnologies.org
echo ================================================================================
echo.

cd /d "%~dp0"

REM Check if frontend is built
if not exist "frontend\dist\index.html" (
    echo [Step 1/3] Building frontend...
    cd frontend
    call npm install
    call npm run build
    cd ..

    if not exist "frontend\dist\index.html" (
        echo [FAIL] Frontend build failed!
        pause
        exit /b 1
    )
    echo [OK] Frontend built
) else (
    echo [Step 1/3] Frontend already built - skipping
)

echo.
echo [Step 2/3] Verifying files...
echo.

set "ALL_OK=1"

if exist "backend\src\main.py" (
    echo [OK] Backend found
) else (
    echo [FAIL] Backend not found!
    set "ALL_OK=0"
)

if exist "frontend\dist\index.html" (
    echo [OK] Frontend dist found
) else (
    echo [FAIL] Frontend dist not found!
    set "ALL_OK=0"
)

if exist "deployment\build_installer\branding\mbas_icon.ico" (
    echo [OK] Icon found
) else (
    echo [WARN] Icon not found, copying default...
    if exist "mbas_icon.ico" (
        copy "mbas_icon.ico" "deployment\build_installer\branding\" >nul
        echo [OK] Icon copied
    )
)

if exist "deployment\build_installer\branding\zt_logo.png" (
    echo [OK] Logo found
) else (
    echo [OK] Logo optional
)

if "%ALL_OK%"=="0" (
    echo.
    echo [FAIL] Missing required files!
    pause
    exit /b 1
)

echo.
echo [Step 3/3] Compiling installer...
echo.

set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

if not exist "%INNO_PATH%" (
    echo [FAIL] Inno Setup not found!
    echo.
    echo Please install Inno Setup 6:
    echo   https://jrsoftware.org/isdl.php
    echo.
    echo Or manually compile:
    echo   deployment\build_installer\MBAS_Installer_Professional_ZT.iss
    echo.
    pause
    exit /b 1
)

REM Change to build_installer directory
cd deployment\build_installer

REM Compile
echo Compiling with Inno Setup...
"%INNO_PATH%" "MBAS_Installer_Professional_ZT.iss"

if errorlevel 1 (
    echo.
    echo [FAIL] Compilation failed!
    echo        Check errors above
    cd ..\..
    pause
    exit /b 1
)

cd ..\..

echo.
echo ================================================================================
echo    [SUCCESS] INSTALLER BUILT!
echo ================================================================================
echo.

if exist "deployment\build_installer\output\MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe" (
    echo Created:
    echo   deployment\build_installer\output\MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe
    echo.
    dir "deployment\build_installer\output\MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe" | findstr "MBAS"
    echo.
    echo Branding:
    echo   ✓ Company: Z^&T Technologies
    echo   ✓ Website: www.zttechnologies.org
    echo   ✓ Email: zttechnologies12@gmail.com
    echo   ✓ Logo: Included
    echo   ✓ Version: 2.0.0
    echo.
    echo Ready for distribution!
) else (
    echo [WARN] Output file not found at expected location
    echo        Check: deployment\build_installer\output\
)

echo.
pause
