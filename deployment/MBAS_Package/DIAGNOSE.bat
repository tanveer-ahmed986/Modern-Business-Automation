@echo off
title MBAS - Diagnostic Tool
color 0E

echo.
echo ================================================================
echo   MBAS - DIAGNOSTIC TOOL
echo ================================================================
echo.
echo This will check your MBAS installation and identify issues.
echo.
pause
cls

echo.
echo ================================================================
echo   CHECKING YOUR MBAS INSTALLATION...
echo ================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python NOT installed
    echo.
    echo Please install Python 3.11+ from python.org
    echo.
    goto FAILED
) else (
    echo [OK] Python found:
    python --version
)

REM Check FastAPI
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [X] FastAPI NOT installed
    echo.
    echo Fix: Run INSTALL.bat
    echo.
    goto FAILED
) else (
    echo [OK] FastAPI installed
)

REM Check files
if exist "backend\src\main.py" (
    echo [OK] main.py found
) else (
    echo [X] main.py NOT found - package corrupted!
    goto FAILED
)

if exist "frontend\dist\index.html" (
    echo [OK] Frontend found
) else (
    echo [X] Frontend NOT found - package corrupted!
    goto FAILED
)

REM Check port
netstat -an | findstr ":8000" >nul 2>&1
if not errorlevel 1 (
    echo [!] Port 8000 already in use
    echo.
    echo Fix: Run STOP_MBAS.bat
    echo.
) else (
    echo [OK] Port 8000 available
)

echo.
echo ================================================================
echo   ALL CHECKS PASSED!
echo ================================================================
echo.
echo Your installation looks good.
echo.
echo To start MBAS:
echo   1. Double-click START_MBAS.bat
echo   2. Wait for "Uvicorn running..." message
echo   3. Browser should open automatically
echo   4. Login: admin / admin123
echo.
echo If page still doesn't load:
echo   1. Check browser console (Press F12)
echo   2. Try: http://localhost:8000/health
echo   3. See: PAGE_LOADING_FIX.md for detailed help
echo.
pause
exit /b 0

:FAILED
echo.
echo ================================================================
echo   DIAGNOSTIC FAILED
echo ================================================================
echo.
echo Please fix the issues above.
echo.
pause
exit /b 1
