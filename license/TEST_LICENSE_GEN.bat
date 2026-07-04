@echo off
setlocal enabledelayedexpansion
title MBAS License Generator - Quick Test
color 0A

echo.
echo ================================================================
echo   MBAS LICENSE GENERATOR - QUICK TEST
echo ================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)
echo [OK] Python found:
python --version
echo.

REM Get script directory
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%
echo [DEBUG] Script directory: %SCRIPT_DIR%
echo.

REM Change to project root
cd /d "%SCRIPT_DIR%\.."
echo [DEBUG] Current directory: %CD%
echo.

REM Check if sign_license.py exists
if exist "tools\sign_license.py" (
    echo [OK] sign_license.py found
) else (
    echo [ERROR] sign_license.py NOT found!
    echo Looking in: %CD%\tools\sign_license.py
    pause
    exit /b 1
)
echo.

REM Check if private key exists
if exist "tools\keys\private_key.pem" (
    echo [OK] Private key found
) else (
    echo [ERROR] Private key NOT found!
    echo Looking in: %CD%\tools\keys\private_key.pem
    pause
    exit /b 1
)
echo.

REM Generate test license
echo ============================================
echo   GENERATING TEST LICENSE...
echo ============================================
echo.
echo Business: Test Pharmacy
echo Tier: Standard
echo Type: Perpetual
echo.

set CMD=python tools\sign_license.py --licensee "Test Pharmacy" --tier standard --type perpetual --output license\test.license

echo [DEBUG] Command: !CMD!
echo.

!CMD!

if errorlevel 1 (
    echo.
    echo [ERROR] License generation FAILED!
    echo.
    echo Troubleshooting:
    echo 1. Check if cryptography module is installed:
    echo    pip install cryptography
    echo.
    echo 2. Check Python version (need 3.11+):
    echo    python --version
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   SUCCESS!
echo ============================================
echo.

if exist "license\test.license" (
    echo [OK] Test license created: license\test.license
    echo.
    echo License contents:
    type "license\test.license"
    echo.
) else (
    echo [ERROR] License file not found!
    echo Expected: license\test.license
    echo.
)

echo.
pause
