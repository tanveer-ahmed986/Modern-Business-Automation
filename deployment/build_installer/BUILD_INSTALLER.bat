@echo off
title Building MBAS Installer
color 0B
setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo    MBAS Installer Builder v1.1.0
echo    Creates self-contained Windows installer with embedded Python
echo ========================================================================
echo.

cd /d "%~dp0"

REM Step 1: Check prerequisites
echo [Step 1/7] Checking prerequisites...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.11 or 3.12.
    pause
    exit /b 1
)
echo [OK] Python found:
python --version
echo.

REM Check if Inno Setup is installed
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo [WARN] Inno Setup 6 not found at default location.
    echo.
    echo Please install Inno Setup 6 from: https://jrsoftware.org/isdl.php
    echo.
    echo After installation, run this script again.
    echo.
    pause
    exit /b 1
)
echo [OK] Inno Setup found
echo.

REM Step 2: Download embedded Python if not exists
echo [Step 2/7] Preparing embedded Python runtime...
echo.

set PYTHON_EMBED_URL=https://www.python.org/ftp/python/3.12.1/python-3.12.1-embed-amd64.zip
set PYTHON_EMBED_DIR=python-3.12.1-embed-amd64

if not exist "%PYTHON_EMBED_DIR%" (
    echo [*] Downloading Python 3.12.1 embedded runtime...

    REM Use PowerShell to download
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_EMBED_URL%' -OutFile 'python-embed.zip'}"

    if errorlevel 1 (
        echo [ERROR] Failed to download Python runtime!
        echo.
        echo Please manually download from:
        echo %PYTHON_EMBED_URL%
        echo.
        echo And extract to: %PYTHON_EMBED_DIR%
        echo.
        pause
        exit /b 1
    )

    echo [*] Extracting Python runtime...
    powershell -Command "Expand-Archive -Path 'python-embed.zip' -DestinationPath '%PYTHON_EMBED_DIR%' -Force"
    del python-embed.zip

    echo [*] Configuring embedded Python for pip...
    REM Enable site-packages in python312._pth
    echo python312.zip > "%PYTHON_EMBED_DIR%\python312._pth"
    echo . >> "%PYTHON_EMBED_DIR%\python312._pth"
    echo Lib\site-packages >> "%PYTHON_EMBED_DIR%\python312._pth"
    echo import site >> "%PYTHON_EMBED_DIR%\python312._pth"

    REM Download get-pip.py
    powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%PYTHON_EMBED_DIR%\get-pip.py'"

    REM Install pip
    "%PYTHON_EMBED_DIR%\python.exe" "%PYTHON_EMBED_DIR%\get-pip.py"

    echo [OK] Embedded Python configured
) else (
    echo [OK] Embedded Python already exists
)
echo.

REM Step 3: Create pre-built virtual environment
echo [Step 3/7] Creating pre-built virtual environment with all dependencies...
echo.

if exist "venv_prebuilt" (
    echo [*] Removing old pre-built venv...
    rmdir /s /q venv_prebuilt
)

echo [*] Creating fresh virtual environment...
python -m venv venv_prebuilt
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment!
    pause
    exit /b 1
)

echo [*] Activating venv...
call venv_prebuilt\Scripts\activate.bat

echo [*] Upgrading pip...
python -m pip install --upgrade pip setuptools wheel --quiet

echo [*] Installing MBAS dependencies (this will take 2-5 minutes)...
echo.

REM Install backend dependencies
if exist "..\MBAS_v1.0.9_Production_Ready\backend\requirements-lock.txt" (
    python -m pip install -r "..\MBAS_v1.0.9_Production_Ready\backend\requirements-lock.txt"
) else if exist "..\MBAS_v1.0.9_Production_Ready\backend\requirements.txt" (
    python -m pip install -r "..\MBAS_v1.0.9_Production_Ready\backend\requirements.txt"
) else (
    echo [ERROR] requirements.txt not found!
    pause
    exit /b 1
)

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)

REM Install system tray dependencies
echo [*] Installing system tray dependencies...
python -m pip install pystray Pillow psutil requests --quiet

echo [*] Installing watchdog dependencies...
python -m pip install watchdog --quiet

echo [OK] All dependencies installed
echo.

call deactivate

REM Step 4: Verify package structure
echo [Step 4/7] Verifying package structure...
echo.

if not exist "..\MBAS_v1.0.9_Production_Ready\backend" (
    echo [ERROR] Backend folder not found!
    pause
    exit /b 1
)

if not exist "..\MBAS_v1.0.9_Production_Ready\frontend" (
    echo [ERROR] Frontend folder not found!
    pause
    exit /b 1
)

if not exist "..\MBAS_v1.0.9_Production_Ready\mbas_icon.ico" (
    echo [ERROR] Icon file not found!
    pause
    exit /b 1
)

echo [OK] Package structure verified
echo.

REM Step 5: Create output directory
echo [Step 5/7] Preparing output directory...
echo.

if not exist "output" mkdir output

REM Step 6: Compile installer with Inno Setup
echo [Step 6/7] Compiling installer (this may take 1-2 minutes)...
echo.

"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /Q MBAS_Installer.iss

if errorlevel 1 (
    echo.
    echo [ERROR] Installer compilation failed!
    echo.
    echo Please check:
    echo   1. All files referenced in MBAS_Installer.iss exist
    echo   2. Inno Setup is properly installed
    echo   3. No syntax errors in the .iss file
    echo.
    pause
    exit /b 1
)

echo [OK] Installer compiled successfully!
echo.

REM Step 7: Verify installer
echo [Step 7/7] Verifying installer...
echo.

if exist "output\MBAS_Setup_v1.1.0.exe" (
    echo ========================================================================
    echo    SUCCESS! Installer created successfully!
    echo ========================================================================
    echo.
    echo Installer location: %~dp0output\MBAS_Setup_v1.1.0.exe
    echo File size:
    dir "output\MBAS_Setup_v1.1.0.exe" | findstr MBAS_Setup
    echo.
    echo This installer includes:
    echo   - Embedded Python 3.12.1 runtime (no Python installation required)
    echo   - All backend dependencies pre-installed
    echo   - MBAS application files
    echo   - Database auto-initialization
    echo   - Desktop and Start Menu shortcuts
    echo   - Windows Defender exclusion (optional)
    echo   - Complete uninstaller
    echo.
    echo The installer can be distributed to any Windows 10/11 PC.
    echo No additional software installation required!
    echo.
    echo Next steps:
    echo   1. Test the installer on a clean Windows VM
    echo   2. Verify all features work correctly
    echo   3. Distribute to clients
    echo.

    REM Open output folder
    explorer "output"

) else (
    echo [ERROR] Installer file not found!
    echo.
    echo Expected: output\MBAS_Setup_v1.1.0.exe
    echo.
    pause
    exit /b 1
)

echo.
echo Press any key to exit...
pause >nul
