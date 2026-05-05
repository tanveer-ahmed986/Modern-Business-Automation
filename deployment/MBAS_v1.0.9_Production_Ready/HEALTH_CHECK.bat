@echo off
title MBAS - Health Check
color 0E

echo.
echo ================================================================
echo    MBAS - Installation Health Check
echo ================================================================
echo.

REM Check virtual environment
if not exist "%~dp0venv" (
    echo [X] Virtual environment NOT found
    echo     Run INSTALL.bat first
    goto :FAILED
) else (
    echo [OK] Virtual environment exists
)

REM Activate venv and check Python
call "%~dp0venv\Scripts\activate.bat" >nul 2>&1
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python NOT accessible in venv
    goto :FAILED
) else (
    echo [OK] Python accessible:
    python --version
)

REM Check key packages
echo.
echo [*] Checking installed packages...
python -c "import fastapi; print(f'[OK] FastAPI {fastapi.__version__}')"
if errorlevel 1 goto :FAILED

python -c "import uvicorn; print(f'[OK] Uvicorn {uvicorn.__version__}')"
if errorlevel 1 goto :FAILED

python -c "import sqlmodel; print('[OK] SQLModel installed')"
if errorlevel 1 goto :FAILED

python -c "import pydantic; print(f'[OK] Pydantic {pydantic.__version__}')"
if errorlevel 1 goto :FAILED

REM Check backend files
echo.
if exist "%~dp0backend\src\main.py" (
    echo [OK] Backend source files found
) else (
    echo [X] Backend files NOT found
    goto :FAILED
)

REM Check frontend
if exist "%~dp0frontend\dist\index.html" (
    echo [OK] Frontend build found
) else (
    echo [X] Frontend NOT found
    goto :FAILED
)

REM Check database
if exist "%~dp0backend\mbas_database.db" (
    echo [OK] Database exists
) else (
    echo [!] Database NOT found (will be created on first start)
)

REM Check port availability
netstat -an | findstr ":8000" >nul 2>&1
if not errorlevel 1 (
    echo [!] Port 8000 is IN USE
    echo     Run STOP_MBAS.bat if server is running
) else (
    echo [OK] Port 8000 available
)

echo.
echo ================================================================
echo    [SUCCESS] Health Check Passed!
echo ================================================================
echo.
echo Your MBAS installation is ready to use.
echo.
echo To start MBAS:
echo    1. Run START_MBAS.bat (or double-click desktop icon)
echo    2. Wait for "Uvicorn running..." message
echo    3. Browser will open automatically
echo    4. Login: admin / admin123
echo.
pause
exit /b 0

:FAILED
echo.
echo ================================================================
echo    [FAILED] Health Check Failed
echo ================================================================
echo.
echo Please run INSTALL.bat to fix the installation.
echo.
pause
exit /b 1
