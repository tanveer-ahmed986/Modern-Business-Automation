@echo off
REM ============================================================================
REM MBAS v2.1.0 PWA - Installation Script
REM Installs dependencies and initializes database
REM ============================================================================

echo.
echo ========================================
echo  MBAS v2.1.0 PWA - Installation
echo ========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check Python
echo [1/3] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.10, 3.11, or 3.12
    echo Download from: https://www.python.org/
    timeout /t 10
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found: Python %PYTHON_VERSION%

REM Install dependencies
echo.
echo [2/3] Installing Python dependencies...
cd backend
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    timeout /t 10
    exit /b 1
)
cd ..
echo Dependencies installed successfully

REM Initialize database
echo.
echo [3/3] Database will be initialized on first run
echo.
echo Default credentials:
echo   Username: admin
echo   Password: admin123
echo.

echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo Next steps:
echo  1. Double-click START_MBAS_PWA.bat
echo  2. Open browser to http://localhost:8000
echo  3. Login with admin/admin123
echo.
echo For mobile testing, see MOBILE_TESTING_GUIDE.txt
echo.
timeout /t 5
