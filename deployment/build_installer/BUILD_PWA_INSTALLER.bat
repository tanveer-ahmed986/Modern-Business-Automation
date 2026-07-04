@echo off
REM ============================================================================
REM MBAS v2.1.0 PWA - Installer Build Script
REM Creates .exe installer and .zip package for distribution
REM ============================================================================

echo.
echo ========================================
echo  MBAS v2.1.0 PWA - Installer Builder
echo ========================================
echo.

REM Check if Inno Setup is installed
set INNO_COMPILER="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %INNO_COMPILER% (
    echo Warning: Inno Setup 6 not found at default location
    echo Looking for alternative locations...

    set INNO_COMPILER="C:\Program Files\Inno Setup 6\ISCC.exe"
    if not exist %INNO_COMPILER% (
        echo.
        echo ERROR: Inno Setup not found!
        echo.
        echo Please install Inno Setup 6 from:
        echo https://jrsoftware.org/isdl.php
        echo.
        echo Or build manually:
        echo 1. Open MBAS_v2.1.0_PWA_Installer.iss in Inno Setup
        echo 2. Click Build -^> Compile
        echo.
        pause
        exit /b 1
    )
)

echo Found Inno Setup compiler: %INNO_COMPILER%
echo.

REM Make sure we're in the right directory
cd /d "%~dp0"

REM Create output directory
if not exist "output" mkdir output

REM Clean old builds
echo Cleaning previous builds...
del /q "output\MBAS_v2.1.0_PWA_Beta_Setup.exe" 2>nul
del /q "output\MBAS_v2.1.0_PWA_Beta_Package.zip" 2>nul

REM Compile the installer
echo.
echo Compiling installer...
echo.
%INNO_COMPILER% "MBAS_v2.1.0_PWA_Installer.iss"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Installer compilation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Installer built successfully!
echo ========================================
echo.
echo File: output\MBAS_v2.1.0_PWA_Beta_Setup.exe
echo.

REM Create portable zip package
echo Creating portable ZIP package...
echo.

REM Create temp directory for packaging
set TEMP_PKG=output\temp_package
if exist "%TEMP_PKG%" rmdir /s /q "%TEMP_PKG%"
mkdir "%TEMP_PKG%"
mkdir "%TEMP_PKG%\MBAS_v2.1.0_PWA"

REM Copy files to package
echo Copying backend...
xcopy /E /I /Q /Y "..\..\backend" "%TEMP_PKG%\MBAS_v2.1.0_PWA\backend" /EXCLUDE:exclude_list.txt >nul

echo Copying frontend...
xcopy /E /I /Q /Y "..\..\frontend\dist" "%TEMP_PKG%\MBAS_v2.1.0_PWA\frontend\dist" >nul

echo Copying scripts...
xcopy /E /I /Q /Y "INSTALL_PWA.bat" "%TEMP_PKG%\MBAS_v2.1.0_PWA\" >nul
xcopy /E /I /Q /Y "START_MBAS_PWA.bat" "%TEMP_PKG%\MBAS_v2.1.0_PWA\" >nul
xcopy /E /I /Q /Y "STOP_MBAS.bat" "%TEMP_PKG%\MBAS_v2.1.0_PWA\" >nul

echo Copying license...
xcopy /E /I /Q /Y "beta_license.json" "%TEMP_PKG%\MBAS_v2.1.0_PWA\mbas.license" >nul

echo Copying documentation...
xcopy /E /I /Q /Y "PWA_QUICK_START.txt" "%TEMP_PKG%\MBAS_v2.1.0_PWA\" >nul
xcopy /E /I /Q /Y "MOBILE_TESTING_GUIDE.txt" "%TEMP_PKG%\MBAS_v2.1.0_PWA\" >nul

echo Copying icon...
xcopy /E /I /Q /Y "..\..\mbas_icon.ico" "%TEMP_PKG%\MBAS_v2.1.0_PWA\" >nul

REM Create README for portable version
echo Creating README...
(
echo MBAS v2.1.0 PWA - Portable Edition
echo =====================================
echo.
echo This is a portable version of MBAS that doesn't require installation.
echo.
echo Quick Start:
echo 1. Run INSTALL_PWA.bat to install Python dependencies
echo 2. Run START_MBAS_PWA.bat to start the server
echo 3. Open browser to http://localhost:8000
echo 4. Login with admin/admin123
echo.
echo For mobile testing, see MOBILE_TESTING_GUIDE.txt
echo For more details, see PWA_QUICK_START.txt
echo.
echo Beta License: STANDARD tier, perpetual
echo Replace mbas.license with production license after testing.
) > "%TEMP_PKG%\MBAS_v2.1.0_PWA\README.txt"

REM Create ZIP using PowerShell
echo Compressing to ZIP...
powershell -Command "Compress-Archive -Path '%TEMP_PKG%\MBAS_v2.1.0_PWA' -DestinationPath 'output\MBAS_v2.1.0_PWA_Beta_Package.zip' -Force"

REM Clean up temp directory
rmdir /s /q "%TEMP_PKG%"

echo.
echo ========================================
echo  Build Complete!
echo ========================================
echo.
echo Created files:
echo.
echo 1. EXE Installer (recommended):
echo    output\MBAS_v2.1.0_PWA_Beta_Setup.exe
echo    - Full Windows installer
echo    - Installs to Program Files
echo    - Creates Start Menu shortcuts
echo    - Includes uninstaller
echo.
echo 2. Portable ZIP Package:
echo    output\MBAS_v2.1.0_PWA_Beta_Package.zip
echo    - Extract and run anywhere
echo    - No installation required
echo    - Includes all files and docs
echo.
echo Distribution:
echo  - Send .exe for easy installation
echo  - Send .zip for portable use
echo  - Both include beta license and documentation
echo.
pause
