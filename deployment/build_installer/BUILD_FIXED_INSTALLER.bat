@echo off
title Build MBAS Fixed Installer (No Taskkill)
color 0B

echo.
echo ========================================================================
echo    Building MBAS Fixed Installer v1.2.1
echo    (PowerShell-only, no taskkill dependency)
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
echo    Building Fixed Installer...
echo ========================================================================
echo.
echo This installer uses PowerShell instead of taskkill.exe
echo Perfect for systems with corrupted taskkill or strict security.
echo.
echo This may take 2-5 minutes depending on your system.
echo.

REM Compile the Inno Setup script
"%INNO_PATH%" "MBAS_Installer_NoTaskkill.iss"

if %errorlevel% == 0 (
    echo.
    echo ========================================================================
    echo    BUILD SUCCESSFUL!
    echo ========================================================================
    echo.
    echo Installer created: .\output\MBAS_Setup_v1.2.1_NoTaskkill.exe
    echo.
    echo File size:
    dir ".\output\MBAS_Setup_v1.2.1_NoTaskkill.exe" | find "MBAS_Setup"
    echo.
    echo This installer:
    echo   [+] Uses PowerShell instead of taskkill.exe
    echo   [+] Fixes error 0xc0000142 (DLL initialization failure)
    echo   [+] Works on systems with corrupted taskkill.exe
    echo   [+] More reliable on locked-down corporate systems
    echo   [+] Includes all previous fixes (process handling, backup, etc.)
    echo.
    echo You can now use this installer instead of the original one.
    echo.
) else (
    echo.
    echo ========================================================================
    echo    BUILD FAILED!
    echo ========================================================================
    echo.
    echo Check the error messages above.
    echo.
)

pause
