@echo off
REM ============================================================================
REM  MBAS Quick Fix - Hide CMD Window
REM  Z&T Technologies - State-of-the-Art Business Solutions
REM
REM  This script updates an existing MBAS installation to fix the visible
REM  CMD window issue without requiring a full reinstall.
REM ============================================================================

title MBAS Quick Fix - Hide CMD Window
color 0E

echo.
echo ================================================================================
echo   MBAS Quick Fix - Hide CMD Window
echo   Z^&T Technologies - State-of-the-Art Business Solutions
echo ================================================================================
echo.
echo This will update your MBAS installation to run the server completely hidden.
echo.
echo What this fixes:
echo   - Removes the visible CMD window when MBAS starts
echo   - Server runs silently in the background
echo   - More professional user experience
echo.
echo IMPORTANT: This requires MBAS to be stopped.
echo.
pause

REM Check for common installation paths
set "MBAS_PATH="

if exist "C:\Program Files\MBAS\scripts\mbas_tray.py" (
    set "MBAS_PATH=C:\Program Files\MBAS"
) else if exist "C:\Program Files (x86)\MBAS\scripts\mbas_tray.py" (
    set "MBAS_PATH=C:\Program Files (x86)\MBAS"
) else if exist "%LOCALAPPDATA%\MBAS\scripts\mbas_tray.py" (
    set "MBAS_PATH=%LOCALAPPDATA%\MBAS"
)

if "%MBAS_PATH%"=="" (
    echo.
    echo [ERROR] MBAS installation not found!
    echo.
    echo Checked locations:
    echo   - C:\Program Files\MBAS
    echo   - C:\Program Files (x86)\MBAS
    echo   - %LOCALAPPDATA%\MBAS
    echo.
    echo Please specify the installation path manually.
    echo.
    pause
    exit /b 1
)

echo.
echo Found MBAS installation at:
echo %MBAS_PATH%
echo.

REM Stop MBAS if running
echo Stopping MBAS...
taskkill /F /IM pythonw.exe /T >nul 2>&1
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

REM Backup original file
if exist "%MBAS_PATH%\scripts\mbas_tray.py" (
    echo Creating backup...
    copy /Y "%MBAS_PATH%\scripts\mbas_tray.py" "%MBAS_PATH%\scripts\mbas_tray.py.backup" >nul 2>&1
    echo Backup created: mbas_tray.py.backup
    echo.
)

REM Copy the fixed file
echo Applying fix...
if not exist "scripts\mbas_tray.py" (
    echo.
    echo [ERROR] Fixed script not found!
    echo Please run this from the build_installer directory.
    echo.
    pause
    exit /b 1
)

copy /Y "scripts\mbas_tray.py" "%MBAS_PATH%\scripts\mbas_tray.py" >nul

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to copy file!
    echo This may require Administrator privileges.
    echo.
    echo Please run this script as Administrator:
    echo   1. Right-click on this batch file
    echo   2. Select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo   Fix Applied Successfully!
echo ================================================================================
echo.
echo The server will now run completely hidden in the background.
echo No CMD window will appear when MBAS starts.
echo.
echo You can now:
echo   1. Start MBAS normally (from desktop or Start menu)
echo   2. Verify that no CMD window appears
echo   3. Check system tray for MBAS icon
echo.
echo Note: If you still see a CMD window, try:
echo   - Restart Windows
echo   - Reinstall using the v2.0.6 installer
echo.
pause
