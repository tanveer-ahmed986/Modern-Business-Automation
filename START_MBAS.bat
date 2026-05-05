@echo off
title MBAS - Quick Start
color 0A

echo.
echo ============================================================
echo   MBAS - Starting System
echo ============================================================
echo.

REM Kill old processes
echo [1/4] Stopping old processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul
echo       Done!
echo.

REM Check if we're in the right directory
echo [2/4] Checking location...
if not exist "backend\" (
    echo.
    echo [ERROR] backend folder not found!
    echo.
    echo Please run this from the MBAS_Package folder
    echo Current location: %CD%
    echo.
    pause
    exit /b 1
)
if not exist "frontend\" (
    echo.
    echo [ERROR] frontend folder not found!
    echo.
    echo Please run this from the MBAS_Package folder
    echo.
    pause
    exit /b 1
)
echo       Done!
echo.

REM Start backend
echo [3/4] Starting Backend...
cd backend
start "MBAS Backend - Keep Open" cmd /k "echo Starting backend... && python -m uvicorn src.main:app --host 127.0.0.1 --port 8000"
cd ..
timeout /t 3 /nobreak >nul
echo       Backend window opened
echo.

REM Start frontend
echo [4/4] Starting Frontend...
cd frontend
start "MBAS Frontend - Keep Open" cmd /k "echo Starting frontend... && npm run dev"
cd ..
timeout /t 5 /nobreak >nul
echo       Frontend window opened
echo.

echo ============================================================
echo   Waiting for servers to start...
echo ============================================================
echo.
echo   This will take about 10-15 seconds
echo.
timeout /t 10 /nobreak

echo.
echo [*] Opening browser...
start http://localhost:5173

echo.
echo ============================================================
echo   MBAS Started!
echo ============================================================
echo.
echo Two windows are open:
echo   [1] MBAS Backend - Keep Open
echo   [2] MBAS Frontend - Keep Open
echo.
echo Browser opened to: http://localhost:5173
echo.
echo Login:
echo   Username: admin
echo   Password: admin123
echo.
echo IMPORTANT: Keep both Backend and Frontend windows open!
echo.
echo To stop MBAS:
echo   Close both windows or run STOP_ALL.bat
echo.
echo ============================================================
echo.
pause
