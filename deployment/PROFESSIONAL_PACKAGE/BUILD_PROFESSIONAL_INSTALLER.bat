@echo off
title Building Professional MBAS Installer - Z&T Technologies
color 0B
setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo    MBAS Professional Installer Builder
echo    A Product of Z^&T Technologies
echo ================================================================================
echo.
echo This will create a professional Windows installer (.exe) with:
echo   - Embedded Python runtime (no Python installation needed)
echo   - Professional system tray mode (no CMD windows)
echo   - Z^&T Technologies branding
echo   - Auto-update capability
echo   - Clean uninstall support
echo.
echo Requirements:
echo   - Inno Setup 6 installed
echo   - Internet connection (first time only)
echo   - 500MB free disk space
echo.
pause

cd /d "%~dp0"

REM ============================================================================
REM STEP 1: Check Prerequisites
REM ============================================================================
echo.
echo [Step 1/8] Checking prerequisites...
echo.

set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%INNO_PATH%" (
    echo [FAIL] Inno Setup 6 not found!
    echo.
    echo Please install from: https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 1
)
echo [OK] Inno Setup found

REM Check if Node.js is available (for frontend build)
where npm >nul 2>&1
if errorlevel 1 (
    echo [WARN] Node.js not found - will use pre-built frontend
    set "SKIP_FRONTEND_BUILD=1"
) else (
    echo [OK] Node.js found
    set "SKIP_FRONTEND_BUILD=0"
)

echo.

REM ============================================================================
REM STEP 2: Build Frontend (if needed)
REM ============================================================================
if "%SKIP_FRONTEND_BUILD%"=="0" (
    echo [Step 2/8] Building production frontend...
    echo.

    cd ..\..\frontend

    echo [*] Installing frontend dependencies...
    call npm install --silent

    echo [*] Building production bundle...
    call npm run build

    if errorlevel 1 (
        echo [FAIL] Frontend build failed!
        pause
        exit /b 1
    )

    cd ..\deployment\PROFESSIONAL_PACKAGE
    echo [OK] Frontend built successfully
) else (
    echo [Step 2/8] Skipping frontend build (using existing)
)
echo.

REM ============================================================================
REM STEP 3: Prepare Package Directory
REM ============================================================================
echo [Step 3/8] Preparing package structure...
echo.

if exist "package" rmdir /s /q "package"
mkdir "package"
mkdir "package\backend"
mkdir "package\frontend"
mkdir "package\scripts"
mkdir "package\docs"

echo [OK] Directory structure created
echo.

REM ============================================================================
REM STEP 4: Copy Application Files
REM ============================================================================
echo [Step 4/8] Copying application files...
echo.

REM Copy backend
xcopy /E /I /Y "..\..\backend" "package\backend" /EXCLUDE:exclude.txt >nul 2>&1
echo [*] Backend copied

REM Copy frontend
xcopy /E /I /Y "..\..\frontend\dist" "package\frontend\dist" >nul 2>&1
echo [*] Frontend copied

REM Copy scripts
xcopy /E /I /Y "..\MBAS_v1.0.9_Production_Ready\scripts" "package\scripts" >nul 2>&1
echo [*] Scripts copied

echo [OK] Application files ready
echo.

REM ============================================================================
REM STEP 5: Copy Branded Files
REM ============================================================================
echo [Step 5/8] Adding Z^&T Technologies branding...
echo.

copy /Y "branding\*.*" "package\" >nul 2>&1
copy /Y "docs\*.*" "package\docs\" >nul 2>&1

echo [OK] Branding applied
echo.

REM ============================================================================
REM STEP 6: Download Embedded Python (if needed)
REM ============================================================================
echo [Step 6/8] Preparing embedded Python runtime...
echo.

if not exist "python-embed" (
    echo [*] Downloading Python 3.11.9 embedded distribution...
    echo     This is a one-time download (25MB, may take 2-5 minutes)
    echo.

    powershell -Command "& { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip' -OutFile 'python-embed.zip' }"

    if errorlevel 1 (
        echo [FAIL] Failed to download Python!
        echo Please download manually from: https://www.python.org/downloads/
        pause
        exit /b 1
    )

    echo [*] Extracting Python runtime...
    powershell -Command "Expand-Archive -Path 'python-embed.zip' -DestinationPath 'python-embed' -Force"
    del python-embed.zip

    echo [OK] Python runtime ready
) else (
    echo [OK] Using existing Python runtime
)
echo.

REM ============================================================================
REM STEP 7: Build Installer
REM ============================================================================
echo [Step 7/8] Building Windows installer...
echo.

"%INNO_PATH%" "MBAS_Professional_Installer.iss"

if errorlevel 1 (
    echo [FAIL] Installer build failed!
    pause
    exit /b 1
)

echo [OK] Installer built successfully
echo.

REM ============================================================================
REM STEP 8: Create Distribution Package
REM ============================================================================
echo [Step 8/8] Creating distribution package...
echo.

if not exist "Output" mkdir "Output"

REM Get version from installer
set "VERSION=2.0.0"
set "INSTALLER_NAME=MBAS_Professional_Setup_v%VERSION%_ZT_Technologies.exe"

if exist "Output\MBAS_Setup.exe" (
    move /Y "Output\MBAS_Setup.exe" "Output\%INSTALLER_NAME%" >nul 2>&1
)

REM Copy documentation
copy /Y "docs\*.*" "Output\" >nul 2>&1

REM Create checksums
certutil -hashfile "Output\%INSTALLER_NAME%" SHA256 > "Output\SHA256_CHECKSUM.txt"

echo [OK] Distribution package ready
echo.

REM ============================================================================
REM COMPLETE
REM ============================================================================
echo ================================================================================
echo    [SUCCESS] Professional Installer Created!
echo    A Product of Z^&T Technologies
echo ================================================================================
echo.
echo Created files:
dir "Output\*.exe" /B
echo.
echo File size:
dir "Output\*.exe" | findstr ".exe"
echo.
echo Location: %CD%\Output\
echo.
echo Next steps:
echo   1. Test the installer on this machine
echo   2. Test on a clean Windows VM (no Python/Node.js)
echo   3. Distribute to end users
echo.
echo Installation features:
echo   ✓ One-click installation (no dependencies needed)
echo   ✓ Professional system tray mode
echo   ✓ Auto-start with Windows (optional)
echo   ✓ Clean uninstall support
echo   ✓ Z^&T Technologies branding throughout
echo.
pause
