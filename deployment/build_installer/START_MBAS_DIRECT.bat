@echo off
REM ============================================================================
REM  MBAS Direct Mode Launcher
REM  Z&T Technologies - State-of-the-Art Business Solutions
REM  Starts the backend server directly with console output visible.
REM  Requires admin to write database in Program Files.
REM ============================================================================

REM Request admin elevation if not already admin
net session >nul 2>&1
if errorlevel 1 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

title MBAS Server - Z&T Technologies
color 0A

cls
echo.
echo ================================================================================
echo    MBAS - Modern Business Automation System
echo    Z^&T Technologies - State-of-the-Art Business Solutions
echo    www.zttechnologies.org
echo ================================================================================
echo.
echo Server starting...
echo.
echo Access MBAS at: http://localhost:8000
echo Default Login: admin / admin123
echo.
echo IMPORTANT: Change password after first login!
echo.
echo Press Ctrl+C to stop the server.
echo DO NOT close this window while using MBAS.
echo ================================================================================
echo.

cd /d "%~dp0"

REM Activate virtual environment
if exist "%~dp0venv\Scripts\activate.bat" (
    call "%~dp0venv\Scripts\activate.bat"
) else (
    echo [ERROR] Virtual environment not found!
    echo Please run INSTALL_MBAS.bat first.
    pause
    exit /b 1
)

REM Change to backend directory
cd "%~dp0backend"

REM Open browser after 5 seconds
start "" /b cmd /c "timeout /t 5 /nobreak >nul && start http://localhost:8000"

REM Start server (port 8000 serves both API and frontend)
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000

echo.
echo MBAS Server stopped.
pause
