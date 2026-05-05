@echo off
title MBAS with Auto-Recovery Watchdog
color 0B

echo.
echo ============================================
echo   MBAS System with Auto-Recovery
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Install requests if not already installed
echo [*] Checking dependencies...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [*] Installing requests library...
    python -m pip install requests
)

echo [OK] Dependencies ready
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
