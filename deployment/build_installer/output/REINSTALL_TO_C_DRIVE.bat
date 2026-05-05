@echo off
title MBAS - Reinstall to C:\MBAS
color 0E

echo.
echo ========================================================================
echo    MBAS Reinstallation Guide
echo    Moving from Program Files to C:\MBAS
echo ========================================================================
echo.
echo WHY REINSTALL?
echo   - Program Files requires admin permissions for every write operation
echo   - C:\MBAS is much easier to manage
echo   - No permission issues
echo   - Faster and more reliable
echo.
echo WHAT THIS WILL DO:
echo   1. Stop MBAS
echo   2. Uninstall from Program Files
echo   3. Clean up old files
echo   4. Guide you through reinstallation to C:\MBAS
echo.
echo YOUR DATABASE WILL BE PRESERVED:
echo   We'll backup your database before uninstalling
echo.
pause

echo.
echo ========================================================================
echo [Step 1/5] Stopping MBAS...
echo ========================================================================

taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo [OK] MBAS stopped

echo.
echo ========================================================================
echo [Step 2/5] Backing up database...
echo ========================================================================

set OLD_DB=C:\Program Files\MBAS\backend\mbas_database.db
set BACKUP_DIR=%USERPROFILE%\Desktop\MBAS_Backup
set BACKUP_DB=%BACKUP_DIR%\mbas_database.db

if exist "%OLD_DB%" (
    if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

    copy "%OLD_DB%" "%BACKUP_DB%" >nul 2>&1

    if exist "%BACKUP_DB%" (
        echo [OK] Database backed up to: %BACKUP_DB%
        echo.
        echo Your database is safe!
    ) else (
        echo [WARNING] Could not backup database automatically.
        echo.
        echo Please manually copy this file:
        echo   From: %OLD_DB%
        echo   To: %BACKUP_DB%
        echo.
        pause
    )
) else (
    echo [INFO] No database found to backup
)

echo.
echo ========================================================================
echo [Step 3/5] Uninstalling old MBAS...
echo ========================================================================
echo.

REM Try to run uninstaller
if exist "C:\Program Files\MBAS\uninstall\unins000.exe" (
    echo Running uninstaller...
    echo.
    echo IMPORTANT: When uninstaller opens:
    echo   - Click "Yes" to uninstall
    echo   - Close the uninstaller when done
    echo   - Come back to this window
    echo.
    pause

    start "" /wait "C:\Program Files\MBAS\uninstall\unins000.exe"

    timeout /t 3 /nobreak >nul
) else (
    echo Uninstaller not found. Trying manual cleanup...

    REM Manual cleanup
    rd /s /q "C:\Program Files\MBAS" 2>nul

    REM Remove desktop shortcut
    del "%USERPROFILE%\Desktop\MBAS*.lnk" 2>nul

    REM Remove Start Menu folder
    rd /s /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\MBAS" 2>nul
)

echo [OK] Old installation removed

echo.
echo ========================================================================
echo [Step 4/5] Installing MBAS to C:\MBAS...
echo ========================================================================
echo.
echo MANUAL STEPS REQUIRED:
echo.
echo 1. The installer will open shortly
echo 2. Click "Next" through the wizard
echo 3. IMPORTANT: When asked for installation path:
echo    - Change from: C:\Program Files\MBAS
echo    - To: C:\MBAS
echo 4. Check "Create desktop shortcut"
echo 5. Click "Install"
echo 6. Wait for installation to complete
echo 7. Do NOT launch MBAS yet - click "Finish"
echo 8. Come back to this window
echo.
pause

REM Find and run the installer
if exist "%~dp0MBAS_Setup_v1.1.0_Simple.exe" (
    start "" /wait "%~dp0MBAS_Setup_v1.1.0_Simple.exe"
) else if exist "D:\gemini_modern_business_automation_system\deployment\build_installer\output\MBAS_Setup_v1.1.0_Simple.exe" (
    start "" /wait "D:\gemini_modern_business_automation_system\deployment\build_installer\output\MBAS_Setup_v1.1.0_Simple.exe"
) else (
    echo.
    echo [ERROR] Installer not found!
    echo.
    echo Please run MBAS_Setup_v1.1.0_Simple.exe manually:
    echo   Location: D:\gemini_modern_business_automation_system\deployment\build_installer\output\
    echo.
    echo Remember to install to: C:\MBAS
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo [Step 5/5] Restoring database...
echo ========================================================================
echo.

if exist "%BACKUP_DB%" (
    if exist "C:\MBAS\backend" (
        echo Copying database to new location...
        copy "%BACKUP_DB%" "C:\MBAS\backend\mbas_database.db" >nul 2>&1

        if exist "C:\MBAS\backend\mbas_database.db" (
            echo [OK] Database restored!
        ) else (
            echo [WARNING] Could not restore database automatically.
            echo.
            echo Please manually copy:
            echo   From: %BACKUP_DB%
            echo   To: C:\MBAS\backend\mbas_database.db
            echo.
        )
    ) else (
        echo [ERROR] C:\MBAS\backend folder not found!
        echo Installation may not have completed.
        echo.
        echo Your database backup is safe at:
        echo   %BACKUP_DB%
        echo.
        pause
        exit /b 1
    )
) else (
    echo [INFO] No database backup to restore
)

echo.
echo ========================================================================
echo    REINSTALLATION COMPLETE!
echo ========================================================================
echo.
echo MBAS has been reinstalled to: C:\MBAS
echo.
echo Benefits of new location:
echo   [+] No admin permissions needed
echo   [+] Faster file access
echo   [+] No permission errors
echo   [+] Easier to manage
echo.
echo Database status:
if exist "%BACKUP_DB%" (
    echo   [+] Your old database has been restored
    echo   [+] All data preserved
) else (
    echo   [*] Fresh database created
)
echo.
echo ========================================================================
echo    READY TO LAUNCH!
echo ========================================================================
echo.
echo Launch MBAS from:
echo   - Desktop shortcut: "MBAS - Modern Business Automation System"
echo   - Or: C:\MBAS\START_MBAS_TRAY.bat
echo.
echo Wait 30-60 seconds for startup.
echo Browser will open automatically.
echo.
echo Your database backup is kept at:
echo   %BACKUP_DIR%
echo.
choice /C YN /M "Launch MBAS now? (Y/N)"

if errorlevel 2 (
    echo.
    echo OK - Launch MBAS later from the desktop shortcut.
    echo.
    pause
    exit /b 0
)

echo.
echo Launching MBAS...
echo.

cd /d C:\MBAS
start "" "C:\MBAS\START_MBAS_TRAY.bat"

echo.
echo MBAS is starting...
echo Watch for the green tray icon and browser opening.
echo.
pause
