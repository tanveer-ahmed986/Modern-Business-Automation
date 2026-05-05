@echo off
title MBAS - Modern Business Automation System
color 0A

echo.
echo ================================================================
echo        MBAS - Modern Business Automation System v1.0.0
echo ================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo         Please run INSTALL.bat first.
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [!] Dependencies not installed. Running installer...
    echo.
    call "%~dp0INSTALL.bat"
    if errorlevel 1 (
        echo [ERROR] Installation failed. Cannot start MBAS.
        pause
        exit /b 1
    )
)

echo [OK] Starting MBAS Server...
echo.
echo    Access MBAS at: http://localhost:8000
echo.
echo    Default Login:
echo       Username: admin
echo       Password: admin123
echo.
echo    Press Ctrl+C to stop the server.
echo    DO NOT close this window while using MBAS.
echo.
echo ================================================================
echo.

REM Wait 2 seconds then open browser
start "" /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8000"

REM Start the backend server (which also serves the frontend)
cd /d "%~dp0backend"
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000

echo.
echo MBAS has stopped.
pause
