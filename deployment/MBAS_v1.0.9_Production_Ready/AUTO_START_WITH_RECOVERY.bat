@echo off
title MBAS Auto-Start with Recovery
color 0E

echo.
echo ============================================
echo   MBAS Complete System with Auto-Recovery
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
call "%~dp0venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)

echo [OK] Virtual environment activated
echo.

echo [*] Starting backend watchdog in background...
start "MBAS Watchdog" /MIN cmd /c "cd /d "%~dp0" && call venv\Scripts\activate.bat && cd backend && python watchdog.py"

timeout /t 5 /nobreak >nul

echo [*] Starting frontend...
start "MBAS Frontend" cmd /c "cd frontend && npm run dev"

echo.
echo ============================================
echo   MBAS System Started with Auto-Recovery
echo ============================================
echo.
echo [OK] Backend: http://127.0.0.1:8000 (with watchdog)
echo [OK] Frontend: http://127.0.0.1:5173
echo.
echo [i] The watchdog will automatically restart
echo [i] the backend if it becomes unresponsive
echo.
echo [i] Check watchdog.log for recovery events
echo.
echo Press any key to stop all services...
pause >nul

echo.
echo [*] Stopping all services...
taskkill /FI "WINDOWTITLE eq MBAS*" /F >nul 2>&1
echo [OK] All services stopped
echo.
pause
