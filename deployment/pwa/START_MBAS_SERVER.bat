@echo off
REM ============================================================================
REM MBAS v2.1.0 - Progressive Web App Server
REM Z&T Technologies | State-of-the-Art Business Solutions
REM www.zttechnologies.org
REM ============================================================================

title MBAS Server v2.1.0

echo.
echo ========================================================================
echo  MBAS v2.1.0 - Modern Business Automation System
echo  Progressive Web App Server
echo ========================================================================
echo  Z&T Technologies - State-of-the-Art Business Solutions
echo  Website: www.zttechnologies.org
echo  Email: zttechnologies12@gmail.com
echo ========================================================================
echo.

REM Detect Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python 3.10, 3.11, or 3.12 from python.org
    echo Download: https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% detected
echo.

REM Navigate to backend directory
cd /d "%~dp0..\..\backend"

REM Check if virtual environment exists
if not exist "venv\" (
    echo [SETUP] Creating Python virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo [SETUP] Installing dependencies...
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo [OK] Dependencies installed
echo.

REM Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do set IP=%%a
set IP=%IP:~1%

REM Start server
echo ========================================================================
echo  MBAS Server Starting...
echo ========================================================================
echo.
echo  [LOCAL ACCESS]
echo  Desktop/Laptop:  http://localhost:8000
echo  Same PC:         http://127.0.0.1:8000
echo.
echo  [MOBILE/TABLET ACCESS (on same WiFi)]
echo  URL:             http://%IP%:8000
echo.
echo  Find your IP: Open Command Prompt and type "ipconfig"
echo.
echo ========================================================================
echo  INSTALLATION INSTRUCTIONS (For Mobile/Tablet)
echo ========================================================================
echo  1. Open the URL above in Chrome/Safari on your mobile device
echo  2. Tap "Add to Home Screen" or "Install App"
echo  3. MBAS will install like a native app!
echo  4. Works offline after installation
echo ========================================================================
echo.
echo  Server running... Press Ctrl+C to stop
echo.

REM Start FastAPI server
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000

REM If server stopped
echo.
echo Server stopped.
pause
