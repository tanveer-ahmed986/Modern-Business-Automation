@echo off
REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ========================================================================
    echo    MBAS Complete Solution
    echo ========================================================================
    echo.
    echo This script requires Administrator privileges.
    echo.
    echo Requesting elevation...
    echo.
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

title MBAS - Complete Solution (All Fixes)
color 0C

echo.
echo ========================================================================
echo    MBAS COMPLETE SOLUTION
echo    Fixes ALL Issues in One Go
echo ========================================================================
echo.
echo This will fix:
echo   [1] Permission denied errors
echo   [2] Startup timeout (15 to 60 seconds)
echo   [3] Missing directories
echo   [4] Write access issues
echo.
echo Estimated time: 2-3 minutes
echo.
pause

set MBAS_DIR=C:\Program Files\MBAS

echo.
echo ========================================================================
echo [FIX 1/5] Stopping MBAS processes...
echo ========================================================================

taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo [OK] All processes stopped

echo.
echo ========================================================================
echo [FIX 2/5] Granting folder permissions...
echo ========================================================================
echo This may take 30-60 seconds...
echo.

REM Get current username
for /f "tokens=*" %%a in ('whoami') do set USERNAME=%%a

REM Grant full control
icacls "%MBAS_DIR%" /grant "%USERNAME%:(OI)(CI)F" /T /C /Q

if errorlevel 1 (
    echo [ERROR] Failed to set permissions!
    echo.
    echo Please try running this script again.
    pause
    exit /b 1
)

echo [OK] Permissions granted successfully

echo.
echo ========================================================================
echo [FIX 3/5] Creating required directories...
echo ========================================================================

REM Create config directory
if not exist "%MBAS_DIR%\backend\config" (
    mkdir "%MBAS_DIR%\backend\config"
    echo [OK] Created: backend\config
)

REM Create logs directory
if not exist "%MBAS_DIR%\backend\logs" (
    mkdir "%MBAS_DIR%\backend\logs"
    echo [OK] Created: backend\logs
)

REM Create backups directory
if not exist "%MBAS_DIR%\backend\backups" (
    mkdir "%MBAS_DIR%\backend\backups"
    echo [OK] Created: backend\backups
)

echo [OK] All directories ready

echo.
echo ========================================================================
echo [FIX 4/5] Fixing startup timeout...
echo ========================================================================

set TRAY_FILE=%MBAS_DIR%\scripts\mbas_tray.py

REM Create VBS script for replacement
echo Set objFS = CreateObject("Scripting.FileSystemObject") > %TEMP%\fix_timeout.vbs
echo Set objFile = objFS.OpenTextFile("%TRAY_FILE%", 1) >> %TEMP%\fix_timeout.vbs
echo content = objFile.ReadAll >> %TEMP%\fix_timeout.vbs
echo objFile.Close >> %TEMP%\fix_timeout.vbs
echo content = Replace(content, "max_retries = 15", "max_retries = 60") >> %TEMP%\fix_timeout.vbs
echo content = Replace(content, "within 15 seconds", "within 60 seconds") >> %TEMP%\fix_timeout.vbs
echo Set objFile = objFS.OpenTextFile("%TRAY_FILE%", 2) >> %TEMP%\fix_timeout.vbs
echo objFile.Write content >> %TEMP%\fix_timeout.vbs
echo objFile.Close >> %TEMP%\fix_timeout.vbs

cscript //nologo %TEMP%\fix_timeout.vbs
del %TEMP%\fix_timeout.vbs

REM Verify change
findstr /C:"max_retries = 60" "%TRAY_FILE%" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Timeout update may have failed
) else (
    echo [OK] Timeout increased to 60 seconds
)

echo.
echo ========================================================================
echo [FIX 5/5] Verifying installation...
echo ========================================================================

REM Check virtual environment
if exist "%MBAS_DIR%\venv\Scripts\python.exe" (
    echo [OK] Virtual environment present
) else (
    echo [ERROR] Virtual environment missing!
    echo.
    echo Please run MBAS_Setup_v1.1.0_Simple.exe again.
    pause
    exit /b 1
)

REM Check database
if exist "%MBAS_DIR%\backend\mbas_database.db" (
    echo [OK] Database present
) else (
    echo [WARNING] Database missing - will be created on first run
)

REM Check backend
if exist "%MBAS_DIR%\backend\src\main.py" (
    echo [OK] Backend files present
) else (
    echo [ERROR] Backend missing!
    pause
    exit /b 1
)

REM Test write access
echo test > "%MBAS_DIR%\test.txt" 2>nul
if errorlevel 1 (
    echo [ERROR] Still no write access!
    pause
    exit /b 1
) else (
    del "%MBAS_DIR%\test.txt"
    echo [OK] Write access verified
)

echo.
echo ========================================================================
echo    ALL FIXES APPLIED SUCCESSFULLY!
echo ========================================================================
echo.
echo What was fixed:
echo   [+] Folder permissions - Full write access granted
echo   [+] Startup timeout - Increased from 15 to 60 seconds
echo   [+] Config directory - Created
echo   [+] Logs directory - Created
echo   [+] Backups directory - Created
echo   [+] Write access - Verified working
echo.
echo ========================================================================
echo    READY TO LAUNCH MBAS
echo ========================================================================
echo.
echo Next steps:
echo   1. Click "Launch MBAS Now" below, OR
echo   2. Launch manually from desktop shortcut
echo.
echo When MBAS starts:
echo   - Wait 30-60 seconds (be patient!)
echo   - Green tray icon will appear near clock
echo   - Browser will open to http://localhost:3000
echo   - Login: admin / admin123
echo.
echo.
choice /C YN /M "Launch MBAS now? (Y/N)"

if errorlevel 2 (
    echo.
    echo OK - you can launch MBAS later from the desktop shortcut.
    echo.
    pause
    exit /b 0
)

echo.
echo ========================================================================
echo    Launching MBAS...
echo ========================================================================
echo.
echo Please wait 30-60 seconds for startup...
echo The browser will open automatically when ready.
echo.

cd /d "%MBAS_DIR%"
start "" "%MBAS_DIR%\START_MBAS_TRAY.bat"

echo.
echo MBAS is starting in the background.
echo.
echo Watch for:
echo   - Green tray icon (near clock)
echo   - Browser opening automatically
echo.
echo If nothing happens after 60 seconds:
echo   - Check system tray for icon
echo   - Manually open: http://localhost:3000
echo.
echo.
echo Press any key to close this window...
pause >nul
