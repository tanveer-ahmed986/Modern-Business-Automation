@echo off
title MBAS - Force Uninstall (Emergency)
color 0C

echo.
echo ========================================================================
echo    MBAS EMERGENCY UNINSTALLER
echo    Use this if the normal uninstaller is stuck
echo ========================================================================
echo.
echo WARNING: This will forcefully remove MBAS from your system.
echo.
echo This will:
echo   [1] Kill all MBAS processes (Python, Node.js)
echo   [2] Kill the stuck uninstaller
echo   [3] Remove all MBAS files and folders
echo   [4] Clean up shortcuts and registry entries
echo.
echo Your database will be backed up to Desktop before removal.
echo.
pause

echo.
echo ========================================================================
echo [Step 1/6] Backing up your database...
echo ========================================================================

set BACKUP_DIR=%USERPROFILE%\Desktop\MBAS_Backup_Emergency
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Try to find and backup database from any location
if exist "C:\Program Files\MBAS\backend\mbas_database.db" (
    copy "C:\Program Files\MBAS\backend\mbas_database.db" "%BACKUP_DIR%\mbas_database.db" >nul 2>&1
    echo [OK] Database backed up from Program Files
)

if exist "C:\MBAS\backend\mbas_database.db" (
    copy "C:\MBAS\backend\mbas_database.db" "%BACKUP_DIR%\mbas_database_c.db" >nul 2>&1
    echo [OK] Database backed up from C:\MBAS
)

echo [OK] Backup complete: %BACKUP_DIR%

echo.
echo ========================================================================
echo [Step 2/6] Killing stuck uninstaller...
echo ========================================================================

REM Kill any stuck Inno Setup uninstallers
taskkill /F /IM unins000.exe /T >nul 2>&1
taskkill /F /IM unins001.exe /T >nul 2>&1
taskkill /F /IM uninst.exe /T >nul 2>&1

timeout /t 2 /nobreak >nul
echo [OK] Uninstaller processes terminated

echo.
echo ========================================================================
echo [Step 3/6] Stopping all MBAS processes...
echo ========================================================================

REM Kill Python processes
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1

REM Kill Node.js processes
taskkill /F /IM node.exe /T >nul 2>&1

REM Kill anything using MBAS ports
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" 2^>nul') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000" 2^>nul') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173" 2^>nul') do taskkill /F /PID %%a >nul 2>&1

timeout /t 3 /nobreak >nul
echo [OK] All processes stopped

echo.
echo ========================================================================
echo [Step 4/6] Removing file locks...
echo ========================================================================

REM Use handle.exe if available (SysInternals tool), otherwise skip
where handle.exe >nul 2>&1
if %errorlevel% == 0 (
    echo Found handle.exe - releasing file locks...
    handle.exe -c "C:\Program Files\MBAS" -y -nobanner >nul 2>&1
    handle.exe -c "C:\MBAS" -y -nobanner >nul 2>&1
) else (
    echo [INFO] handle.exe not found - skipping advanced lock removal
    echo       (This is OK - proceeding with standard removal)
)

echo [OK] Lock removal attempt complete

echo.
echo ========================================================================
echo [Step 5/6] Removing MBAS files...
echo ========================================================================

REM Remove from Program Files
if exist "C:\Program Files\MBAS" (
    echo Removing: C:\Program Files\MBAS
    rd /s /q "C:\Program Files\MBAS" 2>nul

    REM If still exists, try again with more force
    if exist "C:\Program Files\MBAS" (
        echo Retrying with elevated permissions...
        powershell -Command "Remove-Item -Path 'C:\Program Files\MBAS' -Recurse -Force -ErrorAction SilentlyContinue" >nul 2>&1
    )

    if exist "C:\Program Files\MBAS" (
        echo [WARNING] Some files could not be removed (may be system-protected)
        echo          You can manually delete: C:\Program Files\MBAS
    ) else (
        echo [OK] Removed from Program Files
    )
)

REM Remove from C:\MBAS
if exist "C:\MBAS" (
    echo Removing: C:\MBAS
    rd /s /q "C:\MBAS" 2>nul

    if exist "C:\MBAS" (
        powershell -Command "Remove-Item -Path 'C:\MBAS' -Recurse -Force -ErrorAction SilentlyContinue" >nul 2>&1
    )

    if not exist "C:\MBAS" (
        echo [OK] Removed from C:\MBAS
    )
)

echo.
echo ========================================================================
echo [Step 6/6] Cleaning up shortcuts and registry...
echo ========================================================================

REM Remove desktop shortcuts
del "%USERPROFILE%\Desktop\MBAS*.lnk" 2>nul
del "%PUBLIC%\Desktop\MBAS*.lnk" 2>nul

REM Remove Start Menu items
rd /s /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\MBAS" 2>nul
rd /s /q "%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\MBAS" 2>nul

REM Remove startup items
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\MBAS*" 2>nul

REM Clean up registry (uninstall entry)
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\{8D4F7A2B-1C3E-4F9A-B2D1-6E8F9A3B4C5D}_is1" /f >nul 2>&1
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\{8D4F7A2B-1C3E-4F9A-B2D1-6E8F9A3B4C5D}_is1" /f >nul 2>&1
reg delete "HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\{8D4F7A2B-1C3E-4F9A-B2D1-6E8F9A3B4C5D}_is1" /f >nul 2>&1

echo [OK] Shortcuts and registry cleaned

echo.
echo ========================================================================
echo    UNINSTALL COMPLETE!
echo ========================================================================
echo.
echo MBAS has been removed from your system.
echo.
echo Your database has been backed up to:
echo   %BACKUP_DIR%
echo.
echo Files removed:
if not exist "C:\Program Files\MBAS" (
    echo   [X] C:\Program Files\MBAS
) else (
    echo   [!] C:\Program Files\MBAS - SOME FILES REMAIN
)

if not exist "C:\MBAS" (
    echo   [X] C:\MBAS
) else (
    echo   [!] C:\MBAS - SOME FILES REMAIN
)

echo   [X] Desktop shortcuts
echo   [X] Start Menu entries
echo   [X] Registry entries
echo.
echo You can now:
echo   - Reinstall MBAS if desired
echo   - Restore your database from: %BACKUP_DIR%
echo.
pause
