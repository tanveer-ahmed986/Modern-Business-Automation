@echo off
:: ============================================================================
::  MBAS License Generator - Interactive
::  Z&T Technologies - State-of-the-Art Business Solutions
::
::  Generates RSA-4096 signed license files for MBAS customers.
::  Supports: Trial (custom days), Subscription (6mo/1yr), Perpetual
:: ============================================================================

title MBAS License Generator - Z^&T Technologies
color 0A

echo.
echo ================================================================
echo   MBAS LICENSE GENERATOR
echo   Z^&T Technologies - State-of-the-Art Business Solutions
echo   RSA-4096 Cryptographically Signed Licenses
echo ================================================================
echo.

:: ---- Check Python ----
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is NOT installed or not in PATH!
    echo.
    echo Please install Python 3.11 or 3.12 from:
    echo   https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

:: Show Python version
for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] %PYVER% detected
echo.

:: ---- Ensure cryptography package ----
python -c "import cryptography" >nul 2>&1
if errorlevel 1 (
    echo [!] Required package 'cryptography' not found. Installing...
    echo.
    python -m pip install cryptography >nul 2>&1
    if errorlevel 1 (
        echo [!] pip failed, trying ensurepip first...
        python -m ensurepip --upgrade >nul 2>&1
        python -m pip install cryptography >nul 2>&1
        if errorlevel 1 (
            echo [ERROR] Could not install 'cryptography' package.
            echo.
            echo Please install it manually:
            echo   python -m pip install cryptography
            echo.
            pause
            exit /b 1
        )
    )
    echo [OK] 'cryptography' package installed successfully.
    echo.
) else (
    echo [OK] 'cryptography' package found
    echo.
)

:: ---- Check RSA keys exist ----
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "PROJECT_ROOT=%SCRIPT_DIR%\.."
set "KEYS_DIR=%PROJECT_ROOT%\tools\keys"

if not exist "%KEYS_DIR%\private_key.pem" (
    echo [!] RSA private key not found at: %KEYS_DIR%\private_key.pem
    echo [*] Generating new RSA-4096 key pair...
    echo.
    python "%SCRIPT_DIR%\mbas_license_generator.py" --generate-keys
    if errorlevel 1 (
        echo [ERROR] Key generation failed!
        pause
        exit /b 1
    )
    echo.
) else (
    echo [OK] RSA-4096 private key found
    echo.
)

:: ---- Run the interactive generator ----
echo Starting interactive license generator...
echo.

python "%SCRIPT_DIR%\mbas_license_generator.py"

if errorlevel 1 (
    echo.
    echo [ERROR] License generation encountered an error.
    echo.
    echo Troubleshooting:
    echo   1. Check Python version: python --version  (need 3.11+)
    echo   2. Reinstall cryptography: python -m pip install --force-reinstall cryptography
    echo   3. Check that tools\keys\private_key.pem exists
    echo.
)

echo.
pause
