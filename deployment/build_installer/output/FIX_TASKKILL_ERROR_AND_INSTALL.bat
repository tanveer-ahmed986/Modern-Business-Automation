@echo off
title MBAS - Fix Taskkill Error and Install
color 0B

echo.
echo ========================================================================
echo    MBAS Installation - Taskkill Error Fix
echo ========================================================================
echo.
echo Problem Detected: taskkill.exe is corrupted on your system
echo Error Code: 0xc0000142 (DLL initialization failure)
echo.
echo This script will:
echo   1. Test if taskkill works on your system
echo   2. Run Windows System File Checker to repair it
echo   3. Install MBAS using PowerShell instead of taskkill
echo.
echo ========================================================================
echo.

pause

REM Test taskkill
echo [1/3] Testing taskkill.exe...
taskkill /? >nul 2>&1
if errorlevel 1 (
    echo [ERROR] taskkill.exe is not working properly!
    echo Error code: 0xc0000142 indicates corrupted system files.
    echo.
) else (
    echo [OK] taskkill.exe is working.
    echo.
)

REM Run System File Checker
echo [2/3] Running Windows System File Checker...
echo.
echo This will repair corrupted system files including taskkill.exe
echo You need Administrator privileges for this step.
echo.
echo Press any key to run SFC scan (requires admin), or
echo Press Ctrl+C to skip this step
pause

echo.
echo Running: sfc /scannow
echo This may take 5-15 minutes...
echo.

sfc /scannow

echo.
echo SFC scan complete!
echo.
echo Check the results above. If corruption was found and fixed,
echo taskkill.exe should now work properly.
echo.

REM Test taskkill again
echo Testing taskkill.exe again...
taskkill /? >nul 2>&1
if errorlevel 1 (
    echo [WARNING] taskkill.exe still not working.
    echo We will use PowerShell-based installation instead.
    echo.
) else (
    echo [OK] taskkill.exe is now working!
    echo.
)

echo [3/3] Installing MBAS...
echo.
echo Choose installation method:
echo.
echo [1] Use portable installation (NO installer, manual setup)
echo [2] Try installer again (if taskkill is fixed)
echo [3] Exit
echo.
choice /C 123 /N /M "Choose option (1, 2, or 3): "

if errorlevel 3 exit /b 0
if errorlevel 2 goto :try_installer
if errorlevel 1 goto :portable_install

:try_installer
echo.
echo Launching installer...
start "" "%~dp0MBAS_Setup_v1.2.0_Robust.exe"
echo.
echo If the installer hangs again, close it and choose portable installation.
pause
exit /b 0

:portable_install
echo.
echo ========================================================================
echo    PORTABLE INSTALLATION
echo ========================================================================
echo.
echo This will extract MBAS files manually without using the installer.
echo.
call "%~dp0PORTABLE_INSTALL_MBAS.bat"
exit /b 0
