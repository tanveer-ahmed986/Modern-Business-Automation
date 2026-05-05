@echo off
title MBAS - Complete Uninstall Tool
color 0C
setlocal enabledelayedexpansion

echo.
echo ================================================================
echo    MBAS Complete Uninstall and Cleanup Tool
echo ================================================================
echo.
echo This will remove ALL MBAS installations from your system:
echo   - F:\MBAS_v1.0.9_Production_Ready
echo   - C:\MBAS
echo   - Desktop shortcuts
echo   - Running processes
echo   - Locked files
echo.
echo WARNING: This will DELETE all MBAS files and data!
echo.
pause

REM Check for admin rights
net session >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Administrator rights required!
    echo.
    echo Right-click this file and select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo    STEP 1: Stopping MBAS Services
echo ================================================================
echo.

echo [1/6] Killing all Python processes...
taskkill /F /IM python.exe >nul 2>&1
if errorlevel 1 (
    echo [INFO] No python.exe processes found
) else (
    echo [OK] python.exe processes terminated
)

taskkill /F /IM pythonw.exe >nul 2>&1
if errorlevel 1 (
    echo [INFO] No pythonw.exe processes found
) else (
    echo [OK] pythonw.exe processes terminated
)

echo.
echo [2/6] Checking for processes using port 8000...
netstat -ano | findstr ":8000.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo [OK] Port 8000 is free
) else (
    echo [WARN] Port 8000 is in use, killing processes...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000.*LISTENING"') do (
        echo Killing PID: %%a
        taskkill /F /PID %%a >nul 2>&1
    )
    echo [OK] Port 8000 freed
)

echo.
echo [3/6] Waiting for processes to fully terminate...
timeout /t 3 /nobreak >nul
echo [OK] Wait complete

echo.
echo ================================================================
echo    STEP 2: Removing F: Drive Installation
echo ================================================================
echo.

if exist "F:\MBAS_v1.0.9_Production_Ready" (
    echo [*] Found MBAS at F:\MBAS_v1.0.9_Production_Ready
    echo [*] Taking ownership and removing...

    REM Take ownership
    takeown /f "F:\MBAS_v1.0.9_Production_Ready" /r /d y >nul 2>&1

    REM Grant permissions
    icacls "F:\MBAS_v1.0.9_Production_Ready" /grant "%username%":F /t /c /q >nul 2>&1

    REM Delete
    rd /s /q "F:\MBAS_v1.0.9_Production_Ready" >nul 2>&1

    if exist "F:\MBAS_v1.0.9_Production_Ready" (
        echo [WARN] Some files remain, trying robocopy method...
        mkdir "%temp%\empty_dir" 2>nul
        robocopy "%temp%\empty_dir" "F:\MBAS_v1.0.9_Production_Ready" /purge /mt:8 >nul 2>&1
        rd /s /q "F:\MBAS_v1.0.9_Production_Ready" >nul 2>&1
        rd /s /q "%temp%\empty_dir" >nul 2>&1
    )

    if exist "F:\MBAS_v1.0.9_Production_Ready" (
        echo [ERROR] Could not remove F: installation completely
        echo [INFO] Some files may be locked - restart and try again
    ) else (
        echo [OK] F: drive installation removed
    )
) else (
    echo [INFO] No installation found at F:\MBAS_v1.0.9_Production_Ready
)

REM Also check for nested folder
if exist "F:\MBAS_v1.0.9_Production_Ready\MBAS_v1.0.9_Production_Ready" (
    echo [*] Found nested folder, removing...
    takeown /f "F:\MBAS_v1.0.9_Production_Ready\MBAS_v1.0.9_Production_Ready" /r /d y >nul 2>&1
    rd /s /q "F:\MBAS_v1.0.9_Production_Ready\MBAS_v1.0.9_Production_Ready" >nul 2>&1
)

echo.
echo ================================================================
echo    STEP 3: Removing C: Drive Installation
echo ================================================================
echo.

if exist "C:\MBAS" (
    echo [*] Found MBAS at C:\MBAS
    echo [*] Taking ownership and removing...

    REM Take ownership
    takeown /f "C:\MBAS" /r /d y >nul 2>&1

    REM Grant permissions
    icacls "C:\MBAS" /grant "%username%":F /t /c /q >nul 2>&1

    REM Delete
    rd /s /q "C:\MBAS" >nul 2>&1

    if exist "C:\MBAS" (
        echo [WARN] Some files remain, trying robocopy method...
        mkdir "%temp%\empty_dir" 2>nul
        robocopy "%temp%\empty_dir" "C:\MBAS" /purge /mt:8 >nul 2>&1
        rd /s /q "C:\MBAS" >nul 2>&1
        rd /s /q "%temp%\empty_dir" >nul 2>&1
    )

    if exist "C:\MBAS" (
        echo [ERROR] Could not remove C: installation completely
        echo [INFO] Some files may be locked - restart and try again
    ) else (
        echo [OK] C: drive installation removed
    )
) else (
    echo [INFO] No installation found at C:\MBAS
)

echo.
echo ================================================================
echo    STEP 4: Removing Desktop Shortcuts
echo ================================================================
echo.

set DESKTOP=%USERPROFILE%\Desktop

if exist "%DESKTOP%\MBAS.lnk" (
    del /f /q "%DESKTOP%\MBAS.lnk" >nul 2>&1
    echo [OK] Removed desktop shortcut: MBAS.lnk
) else (
    echo [INFO] No MBAS.lnk found on desktop
)

REM Check for other possible shortcut names
if exist "%DESKTOP%\MBAS Server.lnk" (
    del /f /q "%DESKTOP%\MBAS Server.lnk" >nul 2>&1
    echo [OK] Removed desktop shortcut: MBAS Server.lnk
)

if exist "%DESKTOP%\Modern Business Automation System.lnk" (
    del /f /q "%DESKTOP%\Modern Business Automation System.lnk" >nul 2>&1
    echo [OK] Removed desktop shortcut: Modern Business Automation System.lnk
)

echo.
echo ================================================================
echo    STEP 5: Cleaning Temporary Files
echo ================================================================
echo.

echo [*] Removing temp files...

REM Clean temp directories
if exist "%temp%\mbas*" (
    rd /s /q "%temp%\mbas*" >nul 2>&1
    echo [OK] Removed MBAS temp files
)

if exist "%LOCALAPPDATA%\MBAS" (
    rd /s /q "%LOCALAPPDATA%\MBAS" >nul 2>&1
    echo [OK] Removed MBAS local app data
)

REM Clean pip cache for MBAS-related packages
if exist "%LOCALAPPDATA%\pip\Cache" (
    echo [*] Cleaning pip cache...
    REM Don't delete entire cache, just note it
    echo [INFO] Pip cache remains (shared with other Python apps)
)

echo.
echo ================================================================
echo    STEP 6: Final Verification
echo ================================================================
echo.

set ERRORS=0

echo [4/6] Checking F: drive...
if exist "F:\MBAS_v1.0.9_Production_Ready" (
    echo [X] F:\MBAS_v1.0.9_Production_Ready still exists
    set /a ERRORS+=1
) else (
    echo [OK] F: drive clean
)

echo.
echo [5/6] Checking C: drive...
if exist "C:\MBAS" (
    echo [X] C:\MBAS still exists
    set /a ERRORS+=1
) else (
    echo [OK] C: drive clean
)

echo.
echo [6/6] Checking desktop shortcuts...
if exist "%DESKTOP%\MBAS.lnk" (
    echo [X] Desktop shortcut still exists
    set /a ERRORS+=1
) else (
    echo [OK] Desktop clean
)

echo.
echo ================================================================

if %ERRORS% GTR 0 (
    echo    [WARNING] Uninstall completed with %ERRORS% errors
    echo ================================================================
    echo.
    echo Some files could not be removed.
    echo.
    echo NEXT STEPS:
    echo   1. Restart your computer
    echo   2. Run this script again
    echo   3. Manually delete remaining folders
    echo.
) else (
    echo    [SUCCESS] Complete Uninstall Successful!
    echo ================================================================
    echo.
    echo All MBAS installations have been removed from:
    echo   - F: drive
    echo   - C: drive
    echo   - Desktop shortcuts
    echo   - Running processes
    echo.
    echo Your system is now clean and ready for a fresh installation.
    echo.
    echo NEXT STEPS FOR FRESH INSTALL:
    echo   1. Extract MBAS_v1.0.9_Production_Ready.zip to C:\MBAS
    echo   2. Navigate to C:\MBAS in File Explorer
    echo   3. Right-click INSTALL.bat
    echo   4. Select "Run as Administrator"
    echo   5. Wait for completion
    echo.
)

echo ================================================================
echo.

REM Create uninstall log
echo MBAS Uninstall Log > mbas_uninstall_log.txt
echo Date: %date% %time% >> mbas_uninstall_log.txt
echo Errors: %ERRORS% >> mbas_uninstall_log.txt
echo. >> mbas_uninstall_log.txt
echo Removed: >> mbas_uninstall_log.txt
if not exist "F:\MBAS_v1.0.9_Production_Ready" echo   - F:\MBAS_v1.0.9_Production_Ready >> mbas_uninstall_log.txt
if not exist "C:\MBAS" echo   - C:\MBAS >> mbas_uninstall_log.txt
if not exist "%DESKTOP%\MBAS.lnk" echo   - Desktop shortcut >> mbas_uninstall_log.txt
echo. >> mbas_uninstall_log.txt

echo Log file created: mbas_uninstall_log.txt
echo.

pause
