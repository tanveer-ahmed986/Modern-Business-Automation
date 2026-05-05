@echo off
title MBAS Server
color 0B

REM Check if virtual environment exists
if not exist "%~dp0venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run INSTALL.bat first to set up MBAS.
    echo.
    pause
    exit /b 1
)

echo [OK] Starting MBAS Server...
echo.

REM Activate virtual environment
call "%~dp0venv\Scripts\activate.bat"

REM Change to backend directory
cd /d "%~dp0backend"

REM Start FastAPI server
echo Starting backend server...
echo Server will be available at: http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the server.
echo.

REM Wait 2 seconds then open browser
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:8000"

REM Start uvicorn
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000

REM If we get here, server stopped
echo.
echo [*] Server stopped.
pause
