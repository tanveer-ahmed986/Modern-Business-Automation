@echo off
title MBAS with Auto-Recovery Watchdog
color 0B

echo.
echo ============================================
echo   MBAS System with Auto-Recovery
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "%~dp0venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run INSTALL.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

echo [OK] Virtual environment found
echo.

REM Activate virtual environment
echo [*] Activating virtual environment...
call "%~dp0venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)

echo [OK] Virtual environment activated
echo.

echo ============================================
echo   Starting MBAS with Watchdog Protection
echo ============================================
echo.
echo [i] The watchdog will monitor the backend
echo [i] and automatically restart it if it
echo [i] becomes unresponsive.
echo.
echo [i] Logs are saved to: watchdog.log
echo.
echo [i] Press Ctrl+C to stop the watchdog
echo.
echo ============================================
echo.

REM Navigate to backend directory and start watchdog
cd backend
python watchdog.py

pause
