@echo off
REM ============================================================================
REM  MBAS - Bundle Python Wheels for Offline Installation
REM  Z&T Technologies
REM  Run this ONCE on a machine with internet to download all dependencies.
REM  The wheels/ folder will be included in the installer for offline installs.
REM ============================================================================

title MBAS - Bundle Dependencies for Offline Install
color 0B

echo.
echo ================================================================================
echo    MBAS Dependency Bundler - Z^&T Technologies
echo ================================================================================
echo.
echo This will download all Python packages needed by MBAS into a wheels/ folder.
echo The installer will use these packages for offline installation on client machines.
echo.

cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.11 or 3.12 first.
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

REM Create wheels directory
if exist "%~dp0wheels" (
    echo Cleaning old wheels...
    rmdir /s /q "%~dp0wheels"
)
mkdir "%~dp0wheels"

REM Download all wheels
echo [Step 1/2] Downloading packages...
echo.
python -m pip download -r "..\..\backend\requirements.txt" -d "%~dp0wheels" --python-version 3.12 --platform win_amd64 --only-binary=:all:
if errorlevel 1 (
    echo.
    echo [WARN] Some binary wheels not available, downloading source packages too...
    python -m pip download -r "..\..\backend\requirements.txt" -d "%~dp0wheels"
)

REM Also download pip, setuptools, wheel themselves
echo.
echo [Step 2/2] Downloading pip/setuptools/wheel...
python -m pip download pip setuptools wheel -d "%~dp0wheels" --python-version 3.12 --platform win_amd64 --only-binary=:all:
if errorlevel 1 (
    python -m pip download pip setuptools wheel -d "%~dp0wheels"
)

echo.
echo ================================================================================
echo    [SUCCESS] Wheels bundled successfully!
echo ================================================================================
echo.
echo Location: %~dp0wheels\
echo.
echo Files bundled:
dir /b "%~dp0wheels\*.whl" 2>nul | find /c ".whl"
echo wheel files
dir /b "%~dp0wheels\*.tar.gz" 2>nul | find /c ".tar.gz"
echo source packages
echo.
echo The installer will now include these for offline installation.
echo.
pause
