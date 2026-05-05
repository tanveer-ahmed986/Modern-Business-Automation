@echo off
title MBAS - Emergency Diagnostic Tool
color 0E
setlocal enabledelayedexpansion

echo ================================================================
echo    MBAS Emergency Diagnostic Tool
echo ================================================================
echo.
echo This will identify why MBAS won't install or start.
echo.
pause

REM Create log file
set LOG_FILE=mbas_diagnostic_log.txt
echo MBAS Diagnostic Report > %LOG_FILE%
echo Date: %date% %time% >> %LOG_FILE%
echo ============================================ >> %LOG_FILE%
echo. >> %LOG_FILE%

echo.
echo [CHECK 1/10] Python Installation...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python is NOT installed or not in PATH
    echo [FAIL] Python is NOT installed or not in PATH >> %LOG_FILE%
    echo.
    echo SOLUTION: Install Python 3.11 or 3.12 from python.org
    echo           Make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
) else (
    python --version
    echo [PASS] Python found >> %LOG_FILE%
    python --version >> %LOG_FILE%
    echo.
)

echo.
echo [CHECK 2/10] Python Version...
echo.

python -c "import sys; print(f'Python {sys.version}')"
python -c "import sys; print(f'Python {sys.version}')" >> %LOG_FILE%
echo.

echo.
echo [CHECK 3/10] Running as Administrator...
echo.

net session >nul 2>&1
if errorlevel 1 (
    echo [FAIL] NOT running as Administrator!
    echo [FAIL] NOT running as Administrator! >> %LOG_FILE%
    echo.
    echo CRITICAL: You MUST run this as Administrator!
    echo.
    echo How to run as Administrator:
    echo   1. Close this window
    echo   2. Right-click this file
    echo   3. Select "Run as Administrator"
    echo.
    pause
    exit /b 1
) else (
    echo [PASS] Running as Administrator
    echo [PASS] Running as Administrator >> %LOG_FILE%
    echo.
)

echo.
echo [CHECK 4/10] Current Directory...
echo.

echo Current Directory: %CD%
echo Current Directory: %CD% >> %LOG_FILE%
echo.

if exist "INSTALL.bat" (
    echo [PASS] INSTALL.bat found in current directory
    echo [PASS] INSTALL.bat found >> %LOG_FILE%
) else (
    echo [FAIL] INSTALL.bat NOT found!
    echo [FAIL] INSTALL.bat NOT found! >> %LOG_FILE%
    echo.
    echo Please run this from the MBAS installation folder
    echo.
    pause
    exit /b 1
)
echo.

echo.
echo [CHECK 5/10] Existing venv folder...
echo.

if exist "venv" (
    echo [WARN] Old venv folder exists!
    echo [WARN] Old venv folder exists! >> %LOG_FILE%
    echo.
    echo Attempting to remove...

    REM Kill Python processes first
    taskkill /F /IM python.exe >nul 2>&1
    taskkill /F /IM pythonw.exe >nul 2>&1
    timeout /t 2 /nobreak >nul

    REM Try to remove
    rmdir /s /q venv 2>nul

    if exist "venv" (
        echo [FAIL] Cannot remove venv folder - files are locked!
        echo [FAIL] Cannot remove venv folder >> %LOG_FILE%
        echo.
        echo Trying advanced removal...

        REM Take ownership
        takeown /f venv /r /d y >nul 2>&1
        icacls venv /grant %username%:F /t >nul 2>&1
        rmdir /s /q venv >nul 2>&1

        if exist "venv" (
            echo [CRITICAL] Still cannot remove venv!
            echo [CRITICAL] Still cannot remove venv! >> %LOG_FILE%
            echo.
            echo POSSIBLE CAUSES:
            echo   1. Antivirus is blocking
            echo   2. Files are open in another program
            echo   3. System permissions issue
            echo.
            echo SOLUTIONS:
            echo   1. Disable antivirus temporarily
            echo   2. Restart computer
            echo   3. Manually delete venv folder
            echo.
            pause
        ) else (
            echo [PASS] venv removed successfully (advanced method)
            echo [PASS] venv removed (advanced) >> %LOG_FILE%
        )
    ) else (
        echo [PASS] venv removed successfully
        echo [PASS] venv removed >> %LOG_FILE%
    )
    echo.
) else (
    echo [PASS] No old venv folder
    echo [PASS] No old venv folder >> %LOG_FILE%
    echo.
)

echo.
echo [CHECK 6/10] Write Permissions...
echo.

echo test > test_permissions.tmp 2>nul
if exist "test_permissions.tmp" (
    del test_permissions.tmp
    echo [PASS] Write permissions OK
    echo [PASS] Write permissions OK >> %LOG_FILE%
    echo.
) else (
    echo [FAIL] No write permissions!
    echo [FAIL] No write permissions! >> %LOG_FILE%
    echo.
    echo SOLUTION: Run as Administrator
    echo.
    pause
    exit /b 1
)

echo.
echo [CHECK 7/10] Python venv Module...
echo.

python -m venv --help >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python venv module not available!
    echo [FAIL] Python venv module missing >> %LOG_FILE%
    echo.
    echo SOLUTION: Reinstall Python with all components
    echo.
    pause
    exit /b 1
) else (
    echo [PASS] Python venv module available
    echo [PASS] Python venv module available >> %LOG_FILE%
    echo.
)

echo.
echo [CHECK 8/10] Antivirus Detection...
echo.

REM Check if Windows Defender is running
sc query WinDefend | find "RUNNING" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Windows Defender not running
    echo [INFO] Windows Defender not running >> %LOG_FILE%
) else (
    echo [WARN] Windows Defender is active
    echo [WARN] Windows Defender is active >> %LOG_FILE%
    echo.
    echo Windows Defender may block venv creation.
    echo Consider temporarily disabling it.
    echo.
)

echo.
echo [CHECK 9/10] Port 8000 Availability...
echo.

netstat -ano | findstr ":8000.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo [PASS] Port 8000 is available
    echo [PASS] Port 8000 available >> %LOG_FILE%
    echo.
) else (
    echo [WARN] Port 8000 is in use!
    echo [WARN] Port 8000 is in use! >> %LOG_FILE%
    echo.
    echo Finding process...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000.*LISTENING"') do (
        echo Process ID: %%a
        echo Process ID: %%a >> %LOG_FILE%
        tasklist /FI "PID eq %%a"
        tasklist /FI "PID eq %%a" >> %LOG_FILE%
    )
    echo.
    echo Kill this process before installing
    echo.
)

echo.
echo [CHECK 10/10] Testing venv Creation...
echo.

echo Creating test virtual environment...
python -m venv test_venv 2>test_venv_error.log

if exist "test_venv\Scripts\python.exe" (
    echo [PASS] Test venv created successfully!
    echo [PASS] Test venv created successfully! >> %LOG_FILE%
    echo.
    echo Cleaning up test venv...
    rmdir /s /q test_venv
    echo.
) else (
    echo [FAIL] Cannot create virtual environment!
    echo [FAIL] Cannot create virtual environment! >> %LOG_FILE%
    echo.
    echo Error details:
    type test_venv_error.log
    type test_venv_error.log >> %LOG_FILE%
    echo.
    echo CRITICAL ISSUE: Python cannot create virtual environments
    echo.
    echo POSSIBLE CAUSES:
    echo   1. Antivirus blocking
    echo   2. Corrupted Python installation
    echo   3. Insufficient disk space
    echo   4. System-level restrictions
    echo.
    echo SOLUTIONS:
    echo   1. Disable antivirus completely (not just real-time)
    echo   2. Reinstall Python
    echo   3. Check disk space (need 500MB free)
    echo   4. Try installing Python in a different location
    echo.
    pause
)

if exist "test_venv_error.log" del test_venv_error.log

echo.
echo ================================================================
echo    DIAGNOSTIC COMPLETE
echo ================================================================
echo.
echo Log file created: %LOG_FILE%
echo.

REM Count passes and fails
set PASS_COUNT=0
set FAIL_COUNT=0

findstr /C:"[PASS]" %LOG_FILE% >nul 2>&1
if not errorlevel 1 (
    for /f %%i in ('findstr /C:"[PASS]" %LOG_FILE% ^| find /c "[PASS]"') do set PASS_COUNT=%%i
)

findstr /C:"[FAIL]" %LOG_FILE% >nul 2>&1
if not errorlevel 1 (
    for /f %%i in ('findstr /C:"[FAIL]" %LOG_FILE% ^| find /c "[FAIL]"') do set FAIL_COUNT=%%i
)

echo SUMMARY:
echo   Passed: %PASS_COUNT% checks
echo   Failed: %FAIL_COUNT% checks
echo.

if %FAIL_COUNT% GTR 0 (
    echo [ACTION REQUIRED] Fix the failed checks above
    echo.
    echo Most common issues:
    echo   1. Not running as Administrator
    echo   2. Antivirus blocking (Windows Defender)
    echo   3. Old venv folder can't be deleted
    echo.
    echo RECOMMENDED NEXT STEPS:
    echo   1. Disable Windows Defender temporarily
    echo   2. Restart computer
    echo   3. Run INSTALL.bat as Administrator
    echo.
) else (
    echo [SUCCESS] All checks passed!
    echo.
    echo You should be able to install now.
    echo.
    echo Next step:
    echo   Right-click INSTALL.bat
    echo   Select "Run as Administrator"
    echo.
)

echo.
echo Full diagnostic log: %LOG_FILE%
echo.
pause

REM Open log file
notepad %LOG_FILE%
