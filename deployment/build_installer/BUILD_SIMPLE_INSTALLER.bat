@echo off
title Building MBAS Simple Installer
color 0B
setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo    MBAS Simple Installer Builder v1.1.0
echo    Creates Windows installer (requires Python on target system)
echo ========================================================================
echo.

cd /d "%~dp0"

REM Step 1: Check prerequisites
echo [Step 1/4] Checking prerequisites...
echo.

REM Check if Inno Setup is installed
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo [ERROR] Inno Setup 6 not found!
    echo.
    echo Please install Inno Setup 6 from: https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 1
)
echo [OK] Inno Setup 6 found
echo.

REM Step 2: Verify package structure
echo [Step 2/4] Verifying package structure...
echo.

if not exist "..\MBAS_v1.0.9_Production_Ready\backend" (
    echo [ERROR] Backend folder not found!
    echo.
    echo Expected: ..\MBAS_v1.0.9_Production_Ready\backend
    echo.
    pause
    exit /b 1
)

if not exist "..\MBAS_v1.0.9_Production_Ready\frontend" (
    echo [ERROR] Frontend folder not found!
    echo.
    echo Expected: ..\MBAS_v1.0.9_Production_Ready\frontend
    echo.
    pause
    exit /b 1
)

if not exist "..\MBAS_v1.0.9_Production_Ready\mbas_icon.ico" (
    echo [ERROR] Icon file not found!
    echo.
    echo Expected: ..\MBAS_v1.0.9_Production_Ready\mbas_icon.ico
    echo.
    pause
    exit /b 1
)

if not exist "..\MBAS_v1.0.9_Production_Ready\docs\LICENSE.txt" (
    echo [ERROR] LICENSE.txt not found!
    echo.
    echo Expected: ..\MBAS_v1.0.9_Production_Ready\docs\LICENSE.txt
    echo.
    pause
    exit /b 1
)

echo [OK] All required files found
echo.

REM Step 3: Create output directory
echo [Step 3/4] Preparing output directory...
echo.

if not exist "output" mkdir output

echo [OK] Output directory ready
echo.

REM Step 4: Compile installer with Inno Setup
echo [Step 4/4] Compiling installer...
echo.
echo This will take 1-2 minutes depending on compression...
echo.

"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" MBAS_Installer_Simple.iss

if errorlevel 1 (
    echo.
    echo ========================================================================
    echo [ERROR] Installer compilation failed!
    echo ========================================================================
    echo.
    echo Please check:
    echo   1. All files referenced in MBAS_Installer_Simple.iss exist
    echo   2. Inno Setup is properly installed
    echo   3. No syntax errors in the .iss file
    echo.
    echo To see detailed errors:
    echo   1. Open: "C:\Program Files (x86)\Inno Setup 6\Compil32.exe"
    echo   2. File ^> Open: MBAS_Installer_Simple.iss
    echo   3. Build ^> Compile
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo    SUCCESS! Installer created successfully!
echo ========================================================================
echo.

if exist "output\MBAS_Setup_v1.1.0_Simple.exe" (
    for %%A in ("output\MBAS_Setup_v1.1.0_Simple.exe") do (
        set size=%%~zA
        set /a sizeMB=!size! / 1048576
    )

    echo Installer location:
    echo   %~dp0output\MBAS_Setup_v1.1.0_Simple.exe
    echo.
    echo File size: !sizeMB! MB
    echo.
    echo ========================================================================
    echo This installer includes:
    echo ========================================================================
    echo   [+] All MBAS application files
    echo   [+] Backend and frontend code
    echo   [+] All startup and troubleshooting scripts
    echo   [+] Complete documentation
    echo   [+] Desktop and Start Menu shortcuts
    echo   [+] Automatic file unblocking
    echo   [+] Windows Defender exclusion
    echo   [+] Professional uninstaller
    echo.
    echo ========================================================================
    echo Installation requirements on target PC:
    echo ========================================================================
    echo   [!] Windows 10 or 11 (64-bit)
    echo   [!] Python 3.11 or 3.12 installed
    echo   [!] Python added to PATH
    echo   [!] Internet connection (for dependencies)
    echo   [!] ~500 MB free disk space
    echo.
    echo ========================================================================
    echo What the installer does:
    echo ========================================================================
    echo   1. Copies all MBAS files to Program Files\MBAS
    echo   2. Unblocks downloaded files (fixes Smart App Control)
    echo   3. Adds Windows Defender exclusion
    echo   4. Runs INSTALL.bat (creates venv, installs dependencies)
    echo   5. Creates desktop and Start Menu shortcuts
    echo   6. Optionally starts MBAS after installation
    echo.
    echo ========================================================================
    echo TESTING CHECKLIST:
    echo ========================================================================
    echo.
    echo Before distributing to clients, test on a clean Windows PC:
    echo.
    echo   [ ] Install Python 3.11 or 3.12
    echo   [ ] Run MBAS_Setup_v1.1.0_Simple.exe
    echo   [ ] Follow installation wizard
    echo   [ ] Wait for dependency installation
    echo   [ ] Verify MBAS starts successfully
    echo   [ ] Test login (admin / admin123)
    echo   [ ] Verify all features work
    echo   [ ] Test uninstaller
    echo.
    echo ========================================================================
    echo NEXT STEPS:
    echo ========================================================================
    echo.
    echo 1. TEST on a clean Windows VM:
    echo    - Verify installer works correctly
    echo    - Check all features
    echo    - Test performance
    echo.
    echo 2. DISTRIBUTE to clients:
    echo    - Share: MBAS_Setup_v1.1.0_Simple.exe
    echo    - Provide: Python installation instructions
    echo    - Include: Quick start guide
    echo.
    echo 3. CLIENT INSTRUCTIONS:
    echo    a. Install Python 3.11 or 3.12 from python.org
    echo    b. Check "Add Python to PATH" during installation
    echo    c. Restart computer
    echo    d. Run MBAS_Setup_v1.1.0_Simple.exe
    echo    e. Follow wizard (takes 5-10 minutes)
    echo    f. Launch MBAS from desktop icon
    echo.
    echo ========================================================================

    REM Open output folder
    echo Opening output folder...
    echo.
    start "" explorer "output"

) else (
    echo [ERROR] Installer file not found!
    echo.
    echo Expected: output\MBAS_Setup_v1.1.0_Simple.exe
    echo.
    pause
    exit /b 1
)

echo.
echo Press any key to exit...
pause >nul
