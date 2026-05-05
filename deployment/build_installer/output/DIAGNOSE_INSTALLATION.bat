@echo off
title MBAS Installation Diagnostics
color 0E

echo.
echo ========================================================================
echo    MBAS Installation Diagnostics
echo    Checking what went wrong with the installation
echo ========================================================================
echo.

set INSTALL_PATH=C:\Program Files\MBAS
set LOG_FILE=%TEMP%\mbas_diagnostic_report.txt

echo Creating diagnostic report...
echo. > "%LOG_FILE%"
echo MBAS Installation Diagnostic Report >> "%LOG_FILE%"
echo Generated: %date% %time% >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Check 1: Installation path exists
echo [1/10] Checking installation path...
if exist "%INSTALL_PATH%" (
    echo [OK] Installation found at: %INSTALL_PATH% >> "%LOG_FILE%"
    echo [OK] Installation found
) else (
    echo [ERROR] Installation not found at: %INSTALL_PATH% >> "%LOG_FILE%"
    echo [ERROR] Installation path not found!
    echo.
    echo MBAS is not installed at the expected location.
    echo Please run MBAS_Setup_v1.1.0_Simple.exe first.
    pause
    exit /b 1
)

REM Check 2: Virtual environment
echo [2/10] Checking virtual environment...
if exist "%INSTALL_PATH%\venv\Scripts\python.exe" (
    echo [OK] Virtual environment exists >> "%LOG_FILE%"

    REM Get venv size
    for /f "tokens=3" %%a in ('dir "%INSTALL_PATH%\venv" /s /-c ^| findstr "File(s)"') do set VENV_SIZE=%%a
    echo     Size: %VENV_SIZE% bytes >> "%LOG_FILE%"
    echo [OK] Virtual environment found
) else (
    echo [ERROR] Virtual environment not found >> "%LOG_FILE%"
    echo [ERROR] Virtual environment missing!
    echo.
    echo The installation may not have completed properly.
    goto :show_fix
)

REM Check 3: Python packages
echo [3/10] Checking Python packages...
cd /d "%INSTALL_PATH%"
call venv\Scripts\activate.bat

python -c "import sys; print('Python:', sys.version)" >> "%LOG_FILE%" 2>&1
echo. >> "%LOG_FILE%"
echo Checking packages: >> "%LOG_FILE%"

python -c "import fastapi" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] fastapi not installed >> "%LOG_FILE%"
    echo [ERROR] FastAPI missing
    goto :show_fix
) else (
    echo [OK] fastapi installed >> "%LOG_FILE%"
)

python -c "import uvicorn" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] uvicorn not installed >> "%LOG_FILE%"
    echo [ERROR] Uvicorn missing
    goto :show_fix
) else (
    echo [OK] uvicorn installed >> "%LOG_FILE%"
)

python -c "import sqlalchemy" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] sqlalchemy not installed >> "%LOG_FILE%"
    echo [ERROR] SQLAlchemy missing
    goto :show_fix
) else (
    echo [OK] sqlalchemy installed >> "%LOG_FILE%"
)

python -c "import pystray" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] pystray not installed >> "%LOG_FILE%"
    echo [ERROR] Pystray missing
    goto :show_fix
) else (
    echo [OK] pystray installed >> "%LOG_FILE%"
)

echo [OK] All required packages present

REM Check 4: Database
echo [4/10] Checking database...
if exist "%INSTALL_PATH%\backend\mbas_database.db" (
    for %%A in ("%INSTALL_PATH%\backend\mbas_database.db") do set DB_SIZE=%%~zA
    echo [OK] Database exists (size: %DB_SIZE% bytes) >> "%LOG_FILE%"
    echo [OK] Database found
) else (
    echo [ERROR] Database not found >> "%LOG_FILE%"
    echo [ERROR] Database missing
    goto :show_fix
)

REM Check 5: Backend files
echo [5/10] Checking backend files...
if exist "%INSTALL_PATH%\backend\src\main.py" (
    echo [OK] Backend main.py exists >> "%LOG_FILE%"
    echo [OK] Backend files present
) else (
    echo [ERROR] Backend main.py not found >> "%LOG_FILE%"
    echo [ERROR] Backend files missing
    goto :show_fix
)

REM Check 6: Frontend files
echo [6/10] Checking frontend files...
if exist "%INSTALL_PATH%\frontend\dist\index.html" (
    echo [OK] Frontend build exists >> "%LOG_FILE%"
    echo [OK] Frontend files present
) else (
    echo [ERROR] Frontend build not found >> "%LOG_FILE%"
    echo [ERROR] Frontend files missing
    goto :show_fix
)

REM Check 7: Port availability
echo [7/10] Checking port 8000...
netstat -ano | findstr ":8000" >> "%LOG_FILE%" 2>&1
if not errorlevel 1 (
    echo [WARNING] Port 8000 is in use >> "%LOG_FILE%"
    echo [WARNING] Port 8000 is already in use!
    echo.
    echo This is likely the problem!
    goto :show_fix
) else (
    echo [OK] Port 8000 is available >> "%LOG_FILE%"
    echo [OK] Port 8000 available
)

REM Check 8: System tray script
echo [8/10] Checking system tray...
if exist "%INSTALL_PATH%\scripts\mbas_tray.py" (
    echo [OK] System tray script exists >> "%LOG_FILE%"
    echo [OK] Tray script present
) else (
    echo [ERROR] Tray script not found >> "%LOG_FILE%"
    echo [ERROR] Tray script missing
    goto :show_fix
)

REM Check 9: Try starting backend manually
echo [9/10] Testing backend startup...
echo. >> "%LOG_FILE%"
echo Testing backend startup: >> "%LOG_FILE%"

cd backend
start /B python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 > "%TEMP%\mbas_backend_test.log" 2>&1

echo Waiting 10 seconds for backend to start...
timeout /t 10 /nobreak >nul

REM Check if backend is running
curl http://127.0.0.1:8000/api/health > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Backend failed to start >> "%LOG_FILE%"
    echo [ERROR] Backend startup failed!
    echo.
    echo Checking backend log...
    type "%TEMP%\mbas_backend_test.log" >> "%LOG_FILE%"

    REM Kill the test backend
    taskkill /F /IM python.exe >nul 2>&1

    goto :show_fix
) else (
    echo [OK] Backend started successfully >> "%LOG_FILE%"
    echo [OK] Backend can start

    REM Kill the test backend
    taskkill /F /IM python.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
)

REM Check 10: System info
echo [10/10] Collecting system info...
echo. >> "%LOG_FILE%"
echo System Information: >> "%LOG_FILE%"
echo Windows Version: >> "%LOG_FILE%"
ver >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"
echo Python Version: >> "%LOG_FILE%"
python --version >> "%LOG_FILE%" 2>&1
echo. >> "%LOG_FILE%"

echo.
echo ========================================================================
echo    Diagnostics Complete!
echo ========================================================================
echo.
echo Opening diagnostic report...
notepad "%LOG_FILE%"

echo.
echo Based on the diagnostics, what would you like to do?
echo.
echo [1] Run EMERGENCY_FIX to reinstall everything
echo [2] Manually start MBAS with debug logging
echo [3] Exit and review the report
echo.
choice /C 123 /N /M "Choose option (1, 2, or 3): "

if errorlevel 3 exit /b 0
if errorlevel 2 goto :debug_start
if errorlevel 1 goto :emergency_fix

:show_fix
echo.
echo ========================================================================
echo    PROBLEM DETECTED!
echo ========================================================================
echo.
echo Opening diagnostic report...
notepad "%LOG_FILE%"
echo.
echo RECOMMENDED SOLUTIONS:
echo.
echo OPTION 1 (Recommended): EMERGENCY FIX
echo   This will reinstall everything automatically.
echo   1. Go to: %INSTALL_PATH%
echo   2. Right-click: EMERGENCY_FIX.bat
echo   3. Run as administrator
echo   4. Wait 5-10 minutes
echo.
echo OPTION 2: Manual Start with Debug
echo   See detailed error messages.
echo   1. Go to: %INSTALL_PATH%
echo   2. Run: START_MBAS_TRAY_DEBUG.bat
echo   3. Review the log file
echo.
echo OPTION 3: Complete Reinstall
echo   Uninstall and install again.
echo   1. Start Menu ^> MBAS ^> Uninstall MBAS
echo   2. Run: MBAS_Setup_v1.1.0_Simple.exe again
echo.
echo What would you like to do now?
echo [1] Run EMERGENCY_FIX automatically
echo [2] Start with debug logging
echo [3] Exit
echo.
choice /C 123 /N /M "Choose option (1, 2, or 3): "

if errorlevel 3 exit /b 1
if errorlevel 2 goto :debug_start
if errorlevel 1 goto :emergency_fix

:emergency_fix
echo.
echo Starting EMERGENCY_FIX...
cd /d "%INSTALL_PATH%"
call EMERGENCY_FIX.bat
exit /b 0

:debug_start
echo.
echo Starting MBAS with debug logging...
cd /d "%INSTALL_PATH%"
call START_MBAS_TRAY_DEBUG.bat
exit /b 0
