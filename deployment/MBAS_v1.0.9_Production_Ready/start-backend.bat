@echo off
title MBAS Backend Server
color 0A

echo.
echo ============================================
echo   MBAS Backend Server Starting...
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.11 or higher
    echo Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Navigate to backend directory
cd backend

REM Start backend server
echo [*] Starting FastAPI backend on http://localhost:8000
echo.
echo [i] Keep this window open while using MBAS
echo [i] Press Ctrl+C to stop the backend
echo.

python -m uvicorn src.main:app --host 127.0.0.1 --port 8000

pause
