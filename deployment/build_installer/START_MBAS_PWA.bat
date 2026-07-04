@echo off
REM ============================================================================
REM MBAS v2.1.0 PWA - Startup Script
REM Starts the FastAPI backend server (serves both API and PWA frontend)
REM ============================================================================

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if already running
tasklist /FI "WINDOWTITLE eq MBAS v2.1.0 PWA Server" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo MBAS is already running!
    echo Open: http://localhost:8000
    pause
    exit /b 0
)

echo.
echo ================================================
echo  MBAS v2.1.0 PWA - Progressive Web App Edition
echo ================================================
echo.
echo Starting server...
echo.
echo Access MBAS at: http://localhost:8000
echo.
echo For mobile access:
echo   1. Find your IP: ipconfig
echo   2. On mobile: http://YOUR-IP:8000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Set data directory to local
set MBAS_DATA_DIR=%SCRIPT_DIR%data

REM Create data directory if it doesn't exist
if not exist "%MBAS_DATA_DIR%" mkdir "%MBAS_DATA_DIR%"

REM Start the server
title MBAS v2.1.0 PWA Server
cd backend
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000

REM If we get here, server stopped
echo.
echo Server stopped.
pause
