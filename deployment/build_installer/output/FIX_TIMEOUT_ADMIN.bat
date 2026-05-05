@echo off
REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires Administrator privileges.
    echo Requesting elevation...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

title MBAS - Fix Timeout (Administrator)
color 0B

echo.
echo ========================================================================
echo    MBAS Timeout Fix - Running as Administrator
echo ========================================================================
echo.

set TRAY_FILE=C:\Program Files\MBAS\scripts\mbas_tray.py
set BACKUP_FILE=C:\Program Files\MBAS\scripts\mbas_tray.py.backup

echo [Step 1/5] Checking file exists...
if not exist "%TRAY_FILE%" (
    echo [ERROR] File not found: %TRAY_FILE%
    pause
    exit /b 1
)
echo [OK] File found

echo.
echo [Step 2/5] Creating backup...
copy "%TRAY_FILE%" "%BACKUP_FILE%" >nul 2>&1
echo [OK] Backup created

echo.
echo [Step 3/5] Updating timeout from 15 to 60 seconds...

REM Create a temporary VBS script to do the replacement
echo Set objFS = CreateObject("Scripting.FileSystemObject") > %TEMP%\replace.vbs
echo Set objFile = objFS.OpenTextFile("%TRAY_FILE%", 1) >> %TEMP%\replace.vbs
echo content = objFile.ReadAll >> %TEMP%\replace.vbs
echo objFile.Close >> %TEMP%\replace.vbs
echo content = Replace(content, "max_retries = 15", "max_retries = 60") >> %TEMP%\replace.vbs
echo content = Replace(content, "within 15 seconds", "within 60 seconds") >> %TEMP%\replace.vbs
echo Set objFile = objFS.OpenTextFile("%TRAY_FILE%", 2) >> %TEMP%\replace.vbs
echo objFile.Write content >> %TEMP%\replace.vbs
echo objFile.Close >> %TEMP%\replace.vbs

cscript //nologo %TEMP%\replace.vbs
del %TEMP%\replace.vbs

echo [OK] File updated

echo.
echo [Step 4/5] Verifying change...
findstr /C:"max_retries = 60" "%TRAY_FILE%" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Update failed! Restoring backup...
    copy "%BACKUP_FILE%" "%TRAY_FILE%" >nul 2>&1
    pause
    exit /b 1
)
echo [OK] Verified: Timeout is now 60 seconds

echo.
echo [Step 5/5] Stopping any running MBAS...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo [OK] Processes stopped

echo.
echo ========================================================================
echo    SUCCESS! Timeout increased to 60 seconds
echo ========================================================================
echo.
echo Next steps:
echo   1. Launch MBAS from desktop shortcut
echo   2. Wait up to 60 seconds for startup
echo   3. Browser should open automatically
echo.
echo The timeout has been increased from 15 to 60 seconds.
echo This gives MBAS enough time to initialize all components.
echo.
echo Press any key to close this window...
pause >nul
