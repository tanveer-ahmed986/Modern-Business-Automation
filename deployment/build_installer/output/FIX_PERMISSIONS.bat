@echo off
REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires Administrator privileges.
    echo Requesting elevation...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

title MBAS - Fix Folder Permissions
color 0B

echo.
echo ========================================================================
echo    MBAS Permissions Fix - Solves "Access is denied" Error
echo ========================================================================
echo.
echo This script will grant full write permissions to the MBAS folder.
echo This allows MBAS to create config files and databases.
echo.
pause

set MBAS_DIR=C:\Program Files\MBAS

echo.
echo [Step 1/4] Checking MBAS installation...
if not exist "%MBAS_DIR%" (
    echo [ERROR] MBAS not found at: %MBAS_DIR%
    pause
    exit /b 1
)
echo [OK] MBAS found

echo.
echo [Step 2/4] Granting full permissions to current user...
echo This may take 30-60 seconds...

REM Get current username
for /f "tokens=*" %%a in ('whoami') do set USERNAME=%%a

REM Grant full control to the current user
icacls "%MBAS_DIR%" /grant "%USERNAME%:(OI)(CI)F" /T /C /Q

if errorlevel 1 (
    echo [ERROR] Failed to set permissions!
    pause
    exit /b 1
)

echo [OK] Permissions granted

echo.
echo [Step 3/4] Creating required directories...

REM Create config directory if it doesn't exist
if not exist "%MBAS_DIR%\backend\config" (
    mkdir "%MBAS_DIR%\backend\config"
    echo [OK] Created config directory
) else (
    echo [OK] Config directory already exists
)

REM Create logs directory if it doesn't exist
if not exist "%MBAS_DIR%\backend\logs" (
    mkdir "%MBAS_DIR%\backend\logs"
    echo [OK] Created logs directory
) else (
    echo [OK] Logs directory already exists
)

echo.
echo [Step 4/4] Verifying write access...

REM Test if we can write to the directory
echo test > "%MBAS_DIR%\test_write.txt" 2>nul
if errorlevel 1 (
    echo [ERROR] Still cannot write to MBAS folder!
    echo Please check Windows permissions manually.
    pause
    exit /b 1
)
del "%MBAS_DIR%\test_write.txt" 2>nul
echo [OK] Write access verified

echo.
echo ========================================================================
echo    SUCCESS! Permissions Fixed
echo ========================================================================
echo.
echo The MBAS folder now has full write permissions.
echo The "Access is denied" error should be resolved.
echo.
echo Next steps:
echo   1. Close this window
echo   2. Launch MBAS from desktop shortcut
echo   3. Wait 30-60 seconds for startup
echo   4. Browser should open automatically
echo.
echo Press any key to close...
pause >nul
