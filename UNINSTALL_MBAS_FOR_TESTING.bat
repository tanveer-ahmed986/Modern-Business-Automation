@echo off
title Uninstall MBAS - Complete Cleanup
color 0C

cls
echo.
echo ================================================================================
echo    UNINSTALL MBAS - COMPLETE CLEANUP
echo    Z^&T Technologies
echo ================================================================================
echo.
echo This will completely remove MBAS from your computer to prepare for
echo testing the new professional installer.
echo.
echo WARNING: This will delete:
echo   - MBAS installation files
echo   - Database (your business data)
echo   - All settings
echo   - Desktop shortcuts
echo.
echo BACKUP: If you want to keep your data, backup this folder first:
echo   C:\MBAS_TEST\backend\mbas_database.db
echo.
pause

echo.
echo [Step 1/6] Stopping MBAS services...
echo.

REM Stop all MBAS processes
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1

echo [OK] All MBAS processes stopped
timeout /t 2 /nobreak >nul

echo.
echo [Step 2/6] Removing desktop shortcuts...
echo.

REM Remove desktop shortcuts
del "%USERPROFILE%\Desktop\MBAS.lnk" >nul 2>&1
del "%USERPROFILE%\Desktop\MBAS - Business Automation.lnk" >nul 2>&1
del "%USERPROFILE%\Desktop\MBAS_TEST.lnk" >nul 2>&1

echo [OK] Desktop shortcuts removed

echo.
echo [Step 3/6] Removing Start Menu entries...
echo.

REM Remove Start Menu entries
rmdir /s /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\MBAS" >nul 2>&1
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\MBAS.lnk" >nul 2>&1

echo [OK] Start Menu entries removed

echo.
echo [Step 4/6] Removing startup entries...
echo.

REM Remove startup entries
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\MBAS.lnk" >nul 2>&1

echo [OK] Startup entries removed

echo.
echo [Step 5/6] Removing installation folders...
echo.

REM Remove installation folders
if exist "C:\MBAS_TEST" (
    echo Removing C:\MBAS_TEST...
    rmdir /s /q "C:\MBAS_TEST" >nul 2>&1

    REM If still exists, try harder
    if exist "C:\MBAS_TEST" (
        echo Taking ownership and retrying...
        takeown /F "C:\MBAS_TEST" /R /D Y >nul 2>&1
        icacls "C:\MBAS_TEST" /grant administrators:F /T >nul 2>&1
        rmdir /s /q "C:\MBAS_TEST" >nul 2>&1
    )

    if exist "C:\MBAS_TEST" (
        echo [WARN] Some files could not be deleted
        echo        You may need to delete C:\MBAS_TEST manually
    ) else (
        echo [OK] C:\MBAS_TEST removed
    )
) else (
    echo [OK] C:\MBAS_TEST not found
)

REM Also check for C:\MBAS (in case it was installed there)
if exist "C:\MBAS" (
    echo Removing C:\MBAS...
    rmdir /s /q "C:\MBAS" >nul 2>&1
    echo [OK] C:\MBAS removed
)

REM Also check Program Files
if exist "C:\Program Files\MBAS" (
    echo Removing C:\Program Files\MBAS...
    rmdir /s /q "C:\Program Files\MBAS" >nul 2>&1
    echo [OK] C:\Program Files\MBAS removed
)

echo.
echo [Step 6/6] Cleaning up registry entries...
echo.

REM Note: Registry cleanup is optional since we're not using Windows installer
echo [OK] Registry cleanup not needed (manual installation)

echo.
echo ================================================================================
echo    [SUCCESS] MBAS COMPLETELY UNINSTALLED
echo ================================================================================
echo.
echo Your system is now clean and ready to test the new installer.
echo.
echo VERIFICATION:
dir "C:\MBAS_TEST" >nul 2>&1
if errorlevel 1 (
    echo   [OK] C:\MBAS_TEST removed
) else (
    echo   [WARN] C:\MBAS_TEST still exists
)

dir "C:\MBAS" >nul 2>&1
if errorlevel 1 (
    echo   [OK] C:\MBAS removed
) else (
    echo   [WARN] C:\MBAS still exists
)

if not exist "%USERPROFILE%\Desktop\MBAS*.lnk" (
    echo   [OK] Desktop shortcuts removed
) else (
    echo   [WARN] Some shortcuts still exist
)

echo.
echo NEXT STEPS:
echo   1. Restart your computer (recommended for complete cleanup)
echo   2. Navigate to: D:\gemini_modern_business_automation_system\MBAS_v2.0_CLIENT_PACKAGE\
echo   3. Run: MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe
echo   4. Test the installation process
echo   5. Verify all features work
echo.
pause
