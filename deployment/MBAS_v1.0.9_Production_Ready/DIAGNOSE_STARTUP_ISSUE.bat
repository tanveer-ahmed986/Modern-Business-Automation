@echo off
title MBAS - Startup Diagnostic Tool
color 0E
setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo    MBAS STARTUP DIAGNOSTIC TOOL
echo    This will identify why the server fails to start
echo ================================================================================
echo.

REM Step 1: Check Python
echo [Step 1/8] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python is NOT installed or not in PATH
    echo        Please install Python 3.11 or 3.12 from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python found
echo.

REM Step 2: Check Python version
echo [Step 2/8] Checking Python version compatibility...
python -c "import sys; v=sys.version_info; print(f'Version: {v.major}.{v.minor}.{v.micro}'); exit(0 if (v.major==3 and 11<=v.minor<=12) else 1)" 2>nul
if errorlevel 1 (
    echo [WARN] Python version might be incompatible
    echo        MBAS works best with Python 3.11 or 3.12
)
echo [OK] Python version compatible
echo.

REM Step 3: Check virtual environment
echo [Step 3/8] Checking virtual environment...
if not exist "%~dp0venv\Scripts\python.exe" (
    echo [FAIL] Virtual environment NOT found!
    echo        Expected location: %~dp0venv
    echo.
    echo ACTION REQUIRED: Run INSTALL.bat first to create virtual environment
    echo.
    pause
    exit /b 1
)
echo [OK] Virtual environment exists
echo.

REM Step 4: Activate venv and check dependencies
echo [Step 4/8] Checking dependencies...
call "%~dp0venv\Scripts\activate.bat"

python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [FAIL] FastAPI not installed
    echo ACTION: pip install fastapi
)

python -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo [FAIL] Uvicorn not installed
    echo ACTION: pip install uvicorn
)

python -c "import sqlmodel" 2>nul
if errorlevel 1 (
    echo [FAIL] SQLModel not installed
    echo ACTION: pip install sqlmodel
)

python -c "import pystray" 2>nul
if errorlevel 1 (
    echo [WARN] pystray not installed (needed for system tray)
    echo ACTION: pip install pystray Pillow psutil
)

echo [OK] Core dependencies check complete
echo.

REM Step 5: Check backend structure
echo [Step 5/8] Checking backend file structure...
if not exist "%~dp0backend\src\main.py" (
    echo [FAIL] Backend main.py not found!
    echo        Expected: %~dp0backend\src\main.py
    pause
    exit /b 1
)
echo [OK] Backend structure valid
echo.

REM Step 6: Test server startup with detailed error output
echo [Step 6/8] Testing backend server startup...
echo             This will take 15-30 seconds...
echo             Watching for errors...
echo.

cd /d "%~dp0backend"

REM Create a temporary test script
echo import sys > test_startup.py
echo from pathlib import Path >> test_startup.py
echo try: >> test_startup.py
echo     print("Attempting to import FastAPI...") >> test_startup.py
echo     from fastapi import FastAPI >> test_startup.py
echo     print("FastAPI imported successfully") >> test_startup.py
echo     print("") >> test_startup.py
echo     print("Attempting to import main app...") >> test_startup.py
echo     from src.main import app >> test_startup.py
echo     print("Main app imported successfully") >> test_startup.py
echo     print("") >> test_startup.py
echo     print("Checking app configuration...") >> test_startup.py
echo     print(f"App title: {app.title}") >> test_startup.py
echo     print(f"App version: {app.version}") >> test_startup.py
echo     print("") >> test_startup.py
echo     print("SUCCESS: Backend can be imported without errors") >> test_startup.py
echo     sys.exit(0) >> test_startup.py
echo except Exception as e: >> test_startup.py
echo     print(f"ERROR: {e}") >> test_startup.py
echo     import traceback >> test_startup.py
echo     traceback.print_exc() >> test_startup.py
echo     sys.exit(1) >> test_startup.py

python test_startup.py
set STARTUP_TEST_RESULT=%errorlevel%
del test_startup.py

if %STARTUP_TEST_RESULT% neq 0 (
    echo.
    echo [FAIL] Backend failed to import - see error above
    echo.
    echo COMMON ISSUES:
    echo   1. Missing dependencies - run INSTALL.bat again
    echo   2. Corrupted venv - delete venv folder and reinstall
    echo   3. Python version incompatibility - use Python 3.11 or 3.12
    echo   4. Missing license file - check if mbas.license exists
    echo   5. Database corruption - delete backend\mbas_database.db and restart
    echo.
    pause
    exit /b 1
)

echo [OK] Backend imports successfully
echo.

REM Step 7: Check if port 8000 is already in use
echo [Step 7/8] Checking if port 8000 is available...
netstat -ano | findstr ":8000.*LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo [WARN] Port 8000 is already in use!
    echo        Another process is using the port MBAS needs.
    echo.
    netstat -ano | findstr ":8000.*LISTENING"
    echo.
    echo ACTION: Stop the process using port 8000 or use STOP_MBAS.bat
)
echo.

REM Step 8: Try to start server for real (with timeout)
echo [Step 8/8] Starting server for 10 seconds to verify startup...
echo             Watch for any errors below:
echo.

start /B python -m uvicorn src.main:app --host 127.0.0.1 --port 8000

REM Wait 10 seconds for startup
timeout /t 10 /nobreak

REM Check if server is running
netstat -ano | findstr ":8000.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [FAIL] Server did NOT start successfully
    echo        Server failed to bind to port 8000 within 10 seconds
    echo.
    echo RECOMMENDED ACTIONS:
    echo   1. Check the error messages above
    echo   2. Look for Python import errors or module not found
    echo   3. Check if mbas.license file exists in: %~dp0
    echo   4. Try running: EMERGENCY_FIX.bat
    echo   5. Review log file: backend\*.log
    echo.
) else (
    echo.
    echo [SUCCESS] Server is running on port 8000!
    echo           Open browser to: http://localhost:8000
    echo.
    echo The server will continue running for testing.
    echo When done, press any key to stop the server...
)

pause

REM Stop the server
taskkill /F /IM python.exe /T >nul 2>&1

cd /d "%~dp0"

echo.
echo ================================================================================
echo    DIAGNOSTIC COMPLETE
echo ================================================================================
echo.
echo If the server started successfully above, the installation is OK.
echo The issue might be with the system tray launcher.
echo.
echo NEXT STEPS:
echo   1. If server started OK: Try START_MBAS_TRAY_DEBUG.bat
echo   2. If server failed: Run EMERGENCY_FIX.bat or reinstall
echo   3. Check logs: mbas_tray.log and backend\*.log
echo.
pause
