@echo off
title MBAS - Starting with Debug Logging
color 0E

REM Navigate to script directory
cd /d "%~dp0"

REM Create log file with timestamp
set LOG_FILE=%~dp0mbas_startup_debug.log
echo ======================================== > "%LOG_FILE%"
echo MBAS Startup Debug Log >> "%LOG_FILE%"
echo Started: %date% %time% >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo [DEBUG] Starting MBAS with detailed logging...
echo [DEBUG] Log file: %LOG_FILE%
echo.

REM Log current directory
echo [CHECK 1/10] Current Directory >> "%LOG_FILE%"
cd >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Check Python installation
echo [CHECK 2/10] Checking Python... >> "%LOG_FILE%"
python --version >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! >> "%LOG_FILE%"
    echo [ERROR] Python not found! Please install Python 3.11 or 3.12.
    echo Error details saved to: %LOG_FILE%
    notepad "%LOG_FILE%"
    pause
    exit /b 1
)
echo [OK] Python found >> "%LOG_FILE%"
echo.

REM Check if venv exists
echo [CHECK 3/10] Checking Virtual Environment >> "%LOG_FILE%"
if exist "%~dp0venv\Scripts\python.exe" (
    echo [OK] Virtual environment found >> "%LOG_FILE%"
) else (
    echo [ERROR] Virtual environment not found! >> "%LOG_FILE%"
    echo [ERROR] Please run INSTALL.bat first >> "%LOG_FILE%"
    echo.
    echo [ERROR] Virtual environment not found!
    echo Please run INSTALL.bat first to set up MBAS.
    echo.
    echo Error details saved to: %LOG_FILE%
    notepad "%LOG_FILE%"
    pause
    exit /b 1
)
echo. >> "%LOG_FILE%"

REM Activate virtual environment
echo [CHECK 4/10] Activating Virtual Environment >> "%LOG_FILE%"
call "%~dp0venv\Scripts\activate.bat" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to activate venv >> "%LOG_FILE%"
    echo [ERROR] Failed to activate virtual environment!
    echo Error details saved to: %LOG_FILE%
    notepad "%LOG_FILE%"
    pause
    exit /b 1
)
echo [OK] Virtual environment activated >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Check database exists
echo [CHECK 5/10] Checking Database >> "%LOG_FILE%"
if exist "%~dp0backend\mbas_database.db" (
    echo [OK] Database found >> "%LOG_FILE%"
) else (
    echo [WARN] Database not found, will be created >> "%LOG_FILE%"
    echo [*] Initializing database... >> "%LOG_FILE%"

    cd backend
    python -c "from pathlib import Path; import sys; sys.path.insert(0, 'src'); from scripts.init_db import bootstrap; bootstrap()" >> "%LOG_FILE%" 2>&1
    if errorlevel 1 (
        echo [ERROR] Database initialization failed >> "%LOG_FILE%"
        echo [ERROR] Failed to initialize database!
        echo Error details saved to: %LOG_FILE%
        cd ..
        notepad "%LOG_FILE%"
        pause
        exit /b 1
    )
    cd ..
    echo [OK] Database initialized >> "%LOG_FILE%"
)
echo. >> "%LOG_FILE%"

REM Check required Python packages
echo [CHECK 6/10] Verifying Python Packages >> "%LOG_FILE%"
python -c "import fastapi, uvicorn, sqlalchemy, pystray" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] Required packages missing >> "%LOG_FILE%"
    echo [*] Attempting to install missing packages... >> "%LOG_FILE%"

    python -m pip install pystray Pillow psutil requests --quiet >> "%LOG_FILE%" 2>&1

    python -c "import fastapi, uvicorn, sqlalchemy, pystray" >> "%LOG_FILE%" 2>&1
    if errorlevel 1 (
        echo [ERROR] Package installation failed >> "%LOG_FILE%"
        echo [ERROR] Required packages are missing!
        echo Please run INSTALL.bat to install dependencies.
        echo Error details saved to: %LOG_FILE%
        notepad "%LOG_FILE%"
        pause
        exit /b 1
    )
)
echo [OK] All required packages found >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Check port 8000 availability
echo [CHECK 7/10] Checking Port 8000 >> "%LOG_FILE%"
netstat -ano | findstr ":8000" >> "%LOG_FILE%" 2>&1
if not errorlevel 1 (
    echo [WARN] Port 8000 is already in use >> "%LOG_FILE%"
    echo [WARN] Attempting to free port 8000... >> "%LOG_FILE%"

    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
        echo [*] Killing process %%a >> "%LOG_FILE%"
        taskkill /F /PID %%a >> "%LOG_FILE%" 2>&1
    )

    timeout /t 2 /nobreak >nul
)
echo [OK] Port 8000 available >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Check system tray script exists
echo [CHECK 8/10] Checking Tray Script >> "%LOG_FILE%"
if exist "%~dp0scripts\mbas_tray.py" (
    echo [OK] Tray script found >> "%LOG_FILE%"
) else (
    echo [ERROR] Tray script not found at: %~dp0scripts\mbas_tray.py >> "%LOG_FILE%"
    echo [ERROR] System tray script missing!
    echo Error details saved to: %LOG_FILE%
    notepad "%LOG_FILE%"
    pause
    exit /b 1
)
echo. >> "%LOG_FILE%"

REM Check backend main.py exists
echo [CHECK 9/10] Checking Backend Main >> "%LOG_FILE%"
if exist "%~dp0backend\src\main.py" (
    echo [OK] Backend main.py found >> "%LOG_FILE%"
) else (
    echo [ERROR] Backend main.py not found >> "%LOG_FILE%"
    echo [ERROR] Backend application file missing!
    echo Error details saved to: %LOG_FILE%
    notepad "%LOG_FILE%"
    pause
    exit /b 1
)
echo. >> "%LOG_FILE%"

REM Log system information
echo [CHECK 10/10] System Information >> "%LOG_FILE%"
echo Python Version: >> "%LOG_FILE%"
python --version >> "%LOG_FILE%" 2>&1
echo. >> "%LOG_FILE%"
echo Python Path: >> "%LOG_FILE%"
where python >> "%LOG_FILE%" 2>&1
echo. >> "%LOG_FILE%"
echo Working Directory: >> "%LOG_FILE%"
cd >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"
echo Environment Variables: >> "%LOG_FILE%"
echo PATH=%PATH% >> "%LOG_FILE%"
echo VIRTUAL_ENV=%VIRTUAL_ENV% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo ======================================== >> "%LOG_FILE%"
echo All checks passed! Starting MBAS... >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo.
echo [OK] All checks passed!
echo [*] Starting MBAS system tray...
echo.

REM Start system tray with full error logging
cd scripts
python mbas_tray.py >> "%LOG_FILE%" 2>&1

REM If we get here, the tray script exited
echo. >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"
echo MBAS Exited >> "%LOG_FILE%"
echo Time: %date% %time% >> "%LOG_FILE%"
echo Exit Code: %errorlevel% >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"

if errorlevel 1 (
    echo.
    echo [ERROR] MBAS exited with an error!
    echo.
    echo Opening debug log...
    notepad "%LOG_FILE%"
) else (
    echo.
    echo MBAS stopped normally.
)

pause
