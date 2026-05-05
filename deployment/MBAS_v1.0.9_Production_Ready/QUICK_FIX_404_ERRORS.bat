@echo off
title MBAS - Quick Fix for 404 Errors
color 0A
setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo    QUICK FIX: Frontend 404 Errors
echo ================================================================================
echo.

REM Try to detect installation path
set "INSTALL_PATH="

if exist "C:\MBAS\backend" (
    set "INSTALL_PATH=C:\MBAS"
    echo [*] Found MBAS at: C:\MBAS
) else if exist "C:\Program Files\MBAS\backend" (
    set "INSTALL_PATH=C:\Program Files\MBAS"
    echo [*] Found MBAS at: C:\Program Files\MBAS
) else (
    echo [!] Could not auto-detect MBAS installation
    echo.
    set /p "INSTALL_PATH=Enter MBAS installation path (e.g., C:\MBAS): "
)

if not exist "%INSTALL_PATH%\backend" (
    echo [FAIL] MBAS backend not found at: %INSTALL_PATH%
    echo        Please enter the correct path.
    pause
    exit /b 1
)

echo [OK] MBAS found at: %INSTALL_PATH%
echo.

REM Stop MBAS if running
echo [Step 1/3] Stopping MBAS...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo [OK] MBAS stopped
echo.

REM Backup old frontend
echo [Step 2/3] Backing up old frontend...
if exist "%INSTALL_PATH%\frontend\dist" (
    if not exist "%INSTALL_PATH%\frontend\dist.backup" (
        move "%INSTALL_PATH%\frontend\dist" "%INSTALL_PATH%\frontend\dist.backup" >nul 2>&1
        echo [OK] Old frontend backed up to: dist.backup
    ) else (
        rmdir /s /q "%INSTALL_PATH%\frontend\dist" >nul 2>&1
        echo [OK] Old frontend removed
    )
)
echo.

REM Copy correct frontend
echo [Step 3/3] Installing correct frontend...
xcopy /E /I /Y "%~dp0frontend\dist" "%INSTALL_PATH%\frontend\dist"
if errorlevel 1 (
    echo [FAIL] Failed to copy frontend!
    pause
    exit /b 1
)
echo [OK] Frontend installed correctly
echo.

REM Verify structure
echo [Verification] Checking structure...
if exist "%INSTALL_PATH%\frontend\dist\assets" (
    echo [OK] Assets folder exists
) else (
    echo [FAIL] Assets folder missing!
    pause
    exit /b 1
)

dir /B "%INSTALL_PATH%\frontend\dist\assets\*.js" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] JavaScript files missing!
) else (
    echo [OK] JavaScript files found
)

dir /B "%INSTALL_PATH%\frontend\dist\assets\*.css" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] CSS files missing!
) else (
    echo [OK] CSS files found
)

echo.
echo ================================================================================
echo    [SUCCESS] Frontend 404 Errors Fixed!
echo ================================================================================
echo.
echo The frontend structure has been corrected.
echo.
echo Next steps:
echo   1. Start MBAS (run START_MBAS_TRAY.bat or desktop icon)
echo   2. Wait 30 seconds for server to start
echo   3. Browser should open automatically
echo   4. You should now see the MBAS interface (no 404 errors)
echo.
echo If you still see 404 errors:
echo   - Check that MBAS is using the correct path
echo   - View server logs in: %INSTALL_PATH%\backend\*.log
echo   - The server should print: "Serving frontend from [path]"
echo.
pause
