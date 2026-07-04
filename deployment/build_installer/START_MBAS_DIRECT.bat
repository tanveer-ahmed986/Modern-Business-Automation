@echo off
REM ============================================================================
REM  MBAS Direct Mode Launcher
REM  Z&T Technologies - State-of-the-Art Business Solutions
REM  Version 2.5.0 - Venv and data in ProgramData
REM ============================================================================

REM Admin elevation removed - not needed for localhost:8000
REM Firewall rule is added during installation

title MBAS Server - Z^&T Technologies
color 0A

set "APPDIR=%~dp0"
set "DATADIR=C:\ProgramData\MBAS"
set "VENVDIR=%DATADIR%\venv"

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

REM Check virtual environment
if not exist "%VENVDIR%\Scripts\python.exe" (
    echo.
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run INSTALL_MBAS.bat as Administrator first.
    echo Expected at: %VENVDIR%
    echo.
    pause
    exit /b 1
)

REM Verify key packages are available
"%VENVDIR%\Scripts\python.exe" -c "import uvicorn, fastapi" 2>nul
if errorlevel 1 (
    echo.
    echo [ERROR] Required Python packages not installed!
    echo.
    echo Please run INSTALL_MBAS.bat as Administrator to fix this.
    echo.
    pause
    exit /b 1
)

REM Change to backend directory
cd "%APPDIR%backend"

REM Open browser after 5 seconds
start "" /b cmd /c "timeout /t 5 /nobreak >nul && start http://localhost:8000"

REM Start server (port 8000 serves both API and frontend)
echo Starting uvicorn server...
echo.
"%VENVDIR%\Scripts\python.exe" -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --workers 1 --timeout-keep-alive 30

echo.
echo ================================================================================
echo MBAS Server stopped.
echo.
echo If the server crashed, check the error messages above.
echo Common issues:
echo   - Port 8000 already in use (close other MBAS instances)
echo   - Missing packages (run INSTALL_MBAS.bat)
echo.
echo Data location: %DATADIR%\data\
echo Logs location: %DATADIR%\logs\
echo ================================================================================
pause
