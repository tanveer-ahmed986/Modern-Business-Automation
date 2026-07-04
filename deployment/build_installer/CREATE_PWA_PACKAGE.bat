@echo off
REM ============================================================================
REM MBAS v2.1.0 PWA - Package Creator (No Inno Setup Required)
REM Creates a portable ZIP package for beta testing
REM ============================================================================

echo.
echo ==========================================
echo  MBAS v2.1.0 PWA - Package Creator
echo ==========================================
echo.

cd /d "%~dp0"

REM Create output directory
if not exist "output" mkdir output

REM Clean old packages
echo Cleaning previous packages...
del /q "output\MBAS_v2.1.0_PWA_Beta_Package.zip" 2>nul
if exist "output\MBAS_v2.1.0_PWA" rmdir /s /q "output\MBAS_v2.1.0_PWA"

REM Create package directory
echo.
echo Creating package structure...
mkdir "output\MBAS_v2.1.0_PWA"

REM Copy backend (exclude development files)
echo [1/7] Copying backend files...
robocopy "..\..\backend" "output\MBAS_v2.1.0_PWA\backend" /E /NFL /NDL /NJH /NJS /XD __pycache__ .pytest_cache tests data backups /XF *.db *.db-shm *.db-wal *.log *.pyc *.pyo secret.key >nul

REM Copy frontend dist
echo [2/7] Copying frontend PWA...
robocopy "..\..\frontend\dist" "output\MBAS_v2.1.0_PWA\frontend\dist" /E /NFL /NDL /NJH /NJS >nul

REM Copy scripts
echo [3/7] Copying launcher scripts...
copy /Y "INSTALL_PWA.bat" "output\MBAS_v2.1.0_PWA\INSTALL_PWA.bat" >nul
copy /Y "START_MBAS_PWA.bat" "output\MBAS_v2.1.0_PWA\START_MBAS.bat" >nul
copy /Y "STOP_MBAS.bat" "output\MBAS_v2.1.0_PWA\STOP_MBAS.bat" >nul

REM Copy license
echo [4/7] Copying beta license...
copy /Y "beta_license.json" "output\MBAS_v2.1.0_PWA\mbas.license" >nul

REM Copy documentation
echo [5/7] Copying documentation...
copy /Y "PWA_QUICK_START.txt" "output\MBAS_v2.1.0_PWA\README.txt" >nul
copy /Y "MOBILE_TESTING_GUIDE.txt" "output\MBAS_v2.1.0_PWA\MOBILE_TESTING_GUIDE.txt" >nul

REM Copy icon if exists
echo [6/7] Copying icon...
if exist "..\..\mbas_icon.ico" copy /Y "..\..\mbas_icon.ico" "output\MBAS_v2.1.0_PWA\mbas_icon.ico" >nul

REM Create ZIP
echo [7/7] Creating ZIP archive...
powershell -Command "Compress-Archive -Path 'output\MBAS_v2.1.0_PWA\*' -DestinationPath 'output\MBAS_v2.1.0_PWA_Beta_Package.zip' -CompressionLevel Optimal -Force"

if %errorlevel% equ 0 (
    REM Calculate size
    for %%A in ("output\MBAS_v2.1.0_PWA_Beta_Package.zip") do set SIZE=%%~zA
    set /a SIZE_MB=SIZE/1048576

    echo.
    echo ==========================================
    echo  Package Created Successfully!
    echo ==========================================
    echo.
    echo File: output\MBAS_v2.1.0_PWA_Beta_Package.zip
    echo Size: ~%SIZE_MB% MB
    echo.
    echo Package Contents:
    echo  ✓ Backend (FastAPI server)
    echo  ✓ Frontend (PWA build)
    echo  ✓ Beta License (STANDARD, perpetual)
    echo  ✓ Installation script
    echo  ✓ Startup scripts
    echo  ✓ Documentation
    echo.
    echo To use:
    echo  1. Send ZIP file to beta testers
    echo  2. Extract to any folder
    echo  3. Run INSTALL_PWA.bat
    echo  4. Run START_MBAS.bat
    echo.
    echo Beta testers should:
    echo  - Test on different Windows versions (7/10/11)
    echo  - Test on mobile devices (see MOBILE_TESTING_GUIDE.txt)
    echo  - Report any issues or feedback
    echo.

    REM Keep unzipped folder for quick testing
    echo Note: Unzipped folder kept at:
    echo       output\MBAS_v2.1.0_PWA\
    echo       (for quick local testing)
    echo.
) else (
    echo.
    echo ERROR: Failed to create ZIP package!
    echo.
)

pause
