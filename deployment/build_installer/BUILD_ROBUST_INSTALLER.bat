@echo off
title Build MBAS Robust Installer
color 0B

echo.
echo ========================================================================
echo    Building MBAS Robust Installer v1.2.0
echo ========================================================================
echo.

REM Check if Inno Setup is installed
set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe

if not exist "%INNO_PATH%" (
    echo [ERROR] Inno Setup 6 not found!
    echo.
    echo Please install Inno Setup 6 from:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo Install to: C:\Program Files (x86)\Inno Setup 6\
    echo.
    pause
    exit /b 1
)

echo [OK] Found Inno Setup at: %INNO_PATH%
echo.

REM Check if source files exist
if not exist "..\MBAS_v1.0.9_Production_Ready" (
    echo [ERROR] Source files not found!
    echo.
    echo Expected location: ..\MBAS_v1.0.9_Production_Ready
    echo.
    pause
    exit /b 1
)

echo [OK] Source files found
echo.

REM Create output directory
if not exist ".\output" mkdir ".\output"

echo ========================================================================
echo    Building Installer...
echo ========================================================================
echo.
echo This may take 2-5 minutes depending on your system.
echo.

REM Compile the Inno Setup script
"%INNO_PATH%" "MBAS_Installer_Robust.iss"

if %errorlevel% == 0 (
    echo.
    echo ========================================================================
    echo    BUILD SUCCESSFUL!
    echo ========================================================================
    echo.
    echo Installer created: .\output\MBAS_Setup_v1.2.0_Robust.exe
    echo.
    echo File size:
    dir ".\output\MBAS_Setup_v1.2.0_Robust.exe" | find "MBAS_Setup"
    echo.
    echo This installer can now be:
    echo   - Copied to any Windows PC
    echo   - Shared with users
    echo   - Run without internet connection
    echo   - Installed to C:\MBAS (no admin required)
    echo.
    echo Features:
    echo   [+] Robust process handling
    echo   [+] Automatic database backup on upgrade
    echo   [+] Clean uninstall (no hanging)
    echo   [+] Works without admin rights
    echo   [+] Portable across Windows systems
    echo.
) else (
    echo.
    echo ========================================================================
    echo    BUILD FAILED!
    echo ========================================================================
    echo.
    echo Check the error messages above.
    echo.
    echo Common issues:
    echo   - Missing source files
    echo   - Incorrect paths in .iss file
    echo   - Permission issues
    echo.
)

pause
