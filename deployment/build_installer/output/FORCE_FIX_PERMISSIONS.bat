@echo off
REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo This script MUST run as Administrator!
    echo Requesting elevation...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

title MBAS - FORCE Fix Permissions
color 0C

echo.
echo ========================================================================
echo    MBAS AGGRESSIVE PERMISSION FIX
echo    Takes full ownership and grants all permissions
echo ========================================================================
echo.

set MBAS_DIR=C:\Program Files\MBAS

echo [*] Target folder: %MBAS_DIR%
echo.
pause

echo.
echo [Step 1/6] Taking ownership of MBAS folder...
echo This may take 1-2 minutes...
echo.

takeown /F "%MBAS_DIR%" /R /D Y

if errorlevel 1 (
    echo [ERROR] Failed to take ownership!
    pause
    exit /b 1
)

echo [OK] Ownership taken

echo.
echo [Step 2/6] Granting Administrators full control...
echo.

icacls "%MBAS_DIR%" /grant Administrators:(OI)(CI)F /T /C /Q

echo [OK] Administrators granted full control

echo.
echo [Step 3/6] Granting current user full control...
echo.

for /f "tokens=*" %%a in ('whoami') do set USERNAME=%%a
echo Current user: %USERNAME%

icacls "%MBAS_DIR%" /grant "%USERNAME%:(OI)(CI)F" /T /C /Q

echo [OK] User granted full control

echo.
echo [Step 4/6] Granting Users group full control...
echo.

icacls "%MBAS_DIR%" /grant Users:(OI)(CI)F /T /C /Q

echo [OK] Users group granted full control

echo.
echo [Step 5/6] Removing inheritance and keeping existing permissions...
echo.

icacls "%MBAS_DIR%" /inheritance:d /T /C /Q

echo [OK] Inheritance disabled

echo.
echo [Step 6/6] Testing write access...
echo.

REM Try multiple write tests
echo.
echo Test 1: Writing to MBAS root...
echo test > "%MBAS_DIR%\test1.txt" 2>nul
if errorlevel 1 (
    echo [ERROR] Cannot write to root folder
    goto :failed
) else (
    del "%MBAS_DIR%\test1.txt" 2>nul
    echo [OK] Root folder writable
)

echo.
echo Test 2: Writing to backend folder...
echo test > "%MBAS_DIR%\backend\test2.txt" 2>nul
if errorlevel 1 (
    echo [ERROR] Cannot write to backend folder
    goto :failed
) else (
    del "%MBAS_DIR%\backend\test2.txt" 2>nul
    echo [OK] Backend folder writable
)

echo.
echo Test 3: Creating config directory...
if not exist "%MBAS_DIR%\backend\config" (
    mkdir "%MBAS_DIR%\backend\config" 2>nul
    if errorlevel 1 (
        echo [ERROR] Cannot create config directory
        goto :failed
    ) else (
        echo [OK] Config directory created
    )
) else (
    echo [OK] Config directory exists
)

echo.
echo Test 4: Writing to config directory...
echo test > "%MBAS_DIR%\backend\config\test3.txt" 2>nul
if errorlevel 1 (
    echo [ERROR] Cannot write to config folder
    goto :failed
) else (
    del "%MBAS_DIR%\backend\config\test3.txt" 2>nul
    echo [OK] Config folder writable
)

echo.
echo ========================================================================
echo    SUCCESS! ALL PERMISSIONS FIXED!
echo ========================================================================
echo.
echo All write access tests passed!
echo MBAS can now create config files, logs, and databases.
echo.
echo The "Access is denied" error should be completely resolved.
echo.
goto :success

:failed
echo.
echo ========================================================================
echo    PERMISSIONS STILL NOT WORKING
echo ========================================================================
echo.
echo The folder may be protected by:
echo   - Antivirus software
echo   - Windows Defender
echo   - Corporate Group Policy
echo   - Encrypted file system
echo.
echo ALTERNATIVE SOLUTION:
echo   Uninstall MBAS and reinstall to a different location:
echo   - Recommended: C:\MBAS (easier to manage)
echo   - NOT Program Files (requires admin for every write)
echo.
echo Would you like to:
echo   [1] Try disabling antivirus and run this script again
echo   [2] Uninstall and reinstall to C:\MBAS
echo   [3] Exit and investigate manually
echo.
choice /C 123 /N /M "Choose option (1, 2, or 3): "

if errorlevel 3 exit /b 1
if errorlevel 2 goto :reinstall
if errorlevel 1 (
    echo.
    echo Please disable Windows Defender / Antivirus and run this script again.
    pause
    exit /b 1
)

:reinstall
echo.
echo To reinstall to C:\MBAS:
echo   1. Go to Start Menu ^> MBAS ^> Uninstall MBAS
echo   2. Run MBAS_Setup_v1.1.0_Simple.exe
echo   3. When asked for installation path, enter: C:\MBAS
echo   4. Complete installation
echo.
echo The C:\MBAS location does NOT require admin permissions!
echo.
pause
exit /b 0

:success
echo.
echo ========================================================================
echo    NEXT STEPS
echo ========================================================================
echo.
echo 1. Close this window
echo 2. Launch MBAS from desktop shortcut
echo 3. Wait 30-60 seconds for startup
echo 4. Browser should open automatically
echo 5. Login: admin / admin123
echo.
echo Press any key to close...
pause >nul
