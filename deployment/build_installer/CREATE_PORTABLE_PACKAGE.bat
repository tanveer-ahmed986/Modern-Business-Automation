@echo off
title Create MBAS Portable Package
color 0B

echo.
echo ========================================================================
echo    Creating MBAS Portable Package (No Installation Required)
echo ========================================================================
echo.
echo This creates a ZIP package that can run from any folder
echo No installation needed - just extract and run!
echo.

REM Check if 7-Zip is available
where 7z >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] 7-Zip not found in PATH
    echo           Using PowerShell compression (slower)
    echo.
    set USE_POWERSHELL=1
) else (
    echo [OK] Found 7-Zip
    set USE_POWERSHELL=0
)

REM Check source
if not exist "..\MBAS_v1.0.9_Production_Ready" (
    echo [ERROR] Source files not found: ..\MBAS_v1.0.9_Production_Ready
    pause
    exit /b 1
)

REM Create output directory
if not exist ".\output" mkdir ".\output"

REM Set package name
set PACKAGE_NAME=MBAS_v1.2.0_Portable
set OUTPUT_ZIP=.\output\%PACKAGE_NAME%.zip
set TEMP_DIR=.\output\%PACKAGE_NAME%

echo.
echo ========================================================================
echo    Preparing portable package...
echo ========================================================================
echo.

REM Clean temp directory
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

echo [1/5] Copying application files...
xcopy /E /I /Y "..\MBAS_v1.0.9_Production_Ready\backend" "%TEMP_DIR%\backend\" >nul
xcopy /E /I /Y "..\MBAS_v1.0.9_Production_Ready\frontend" "%TEMP_DIR%\frontend\" >nul
xcopy /E /I /Y "..\MBAS_v1.0.9_Production_Ready\scripts" "%TEMP_DIR%\scripts\" >nul
xcopy /E /I /Y "..\MBAS_v1.0.9_Production_Ready\docs" "%TEMP_DIR%\docs\" >nul

echo [2/5] Copying startup scripts...
copy "..\MBAS_v1.0.9_Production_Ready\*.bat" "%TEMP_DIR%\" >nul
copy "..\MBAS_v1.0.9_Production_Ready\*.txt" "%TEMP_DIR%\" >nul
copy "..\MBAS_v1.0.9_Production_Ready\*.md" "%TEMP_DIR%\" >nul
copy "..\MBAS_v1.0.9_Production_Ready\mbas_icon.ico" "%TEMP_DIR%\" >nul
copy "..\MBAS_v1.0.9_Production_Ready\mbas.license" "%TEMP_DIR%\" >nul

echo [3/5] Creating portable launcher...

REM Create portable launcher
(
echo @echo off
echo title MBAS Portable - First Run Setup
echo color 0E
echo.
echo ========================================================================
echo    MBAS Portable Edition - First Run
echo ========================================================================
echo.
echo This portable version can run from any folder without installation!
echo.
echo Requirements:
echo   - Python 3.11 or 3.12 installed on your system
echo   - Internet connection for first-time dependency installation
echo.
echo Current location: %%CD%%
echo.
echo First run will:
echo   1. Create virtual environment
echo   2. Install Python dependencies
echo   3. Install frontend dependencies
echo   4. Initialize database
echo.
echo This takes 2-4 minutes on first run only.
echo.
pause
echo.
echo Starting installation...
echo.
call INSTALL.bat
echo.
echo ========================================================================
echo    Setup Complete! Starting MBAS...
echo ========================================================================
echo.
call START_MBAS_TRAY.bat
) > "%TEMP_DIR%\PORTABLE_FIRST_RUN.bat"

REM Create quick start readme
(
echo ========================================================================
echo    MBAS PORTABLE EDITION - QUICK START
echo ========================================================================
echo.
echo FIRST TIME SETUP:
echo   1. Extract this ZIP to any folder (e.g., D:\MBAS_Portable)
echo   2. Make sure Python 3.11 or 3.12 is installed
echo   3. Run: PORTABLE_FIRST_RUN.bat
echo   4. Wait 2-4 minutes for first-time setup
echo   5. Browser will open automatically
echo.
echo SUBSEQUENT RUNS:
echo   - Just run: START_MBAS_TRAY.bat
echo   - Or use the desktop shortcut created during first run
echo.
echo MOVING TO ANOTHER PC:
echo   1. Copy the entire extracted folder to new PC
echo   2. Run PORTABLE_FIRST_RUN.bat again on the new PC
echo   3. Your database moves with the folder!
echo.
echo SYSTEM REQUIREMENTS:
echo   - Windows 10/11 (64-bit)
echo   - Python 3.11 or 3.12
echo   - 2GB free disk space
echo   - 4GB RAM minimum
echo.
echo ADVANTAGES OF PORTABLE:
echo   - No installation required
echo   - Run from USB drive or network folder
echo   - Easy to backup (just copy the folder^)
echo   - Multiple versions can coexist
echo   - No registry entries
echo   - No admin rights needed
echo.
echo SUPPORT:
echo   - See README_FIRST.txt for detailed documentation
echo   - See START_HERE_IF_PROBLEMS.txt for troubleshooting
echo.
echo ========================================================================
) > "%TEMP_DIR%\PORTABLE_README.txt"

echo [4/5] Compressing package...

REM Delete old package if exists
if exist "%OUTPUT_ZIP%" del "%OUTPUT_ZIP%"

if %USE_POWERSHELL%==1 (
    echo Using PowerShell compression...
    powershell -Command "Compress-Archive -Path '%TEMP_DIR%' -DestinationPath '%OUTPUT_ZIP%' -CompressionLevel Optimal"
) else (
    echo Using 7-Zip compression...
    7z a -tzip "%OUTPUT_ZIP%" ".\output\%PACKAGE_NAME%\*" -mx=9 >nul
)

echo [5/5] Cleaning up temporary files...
rd /s /q "%TEMP_DIR%"

echo.
echo ========================================================================
echo    PORTABLE PACKAGE CREATED!
echo ========================================================================
echo.
echo Package: %OUTPUT_ZIP%
echo.

if exist "%OUTPUT_ZIP%" (
    echo File size:
    dir "%OUTPUT_ZIP%" | find ".zip"
    echo.
    echo This portable package:
    echo   [+] Can run from any folder
    echo   [+] No installation required
    echo   [+] Works on any Windows PC
    echo   [+] Database travels with the folder
    echo   [+] No admin rights needed
    echo   [+] Can run from USB drive
    echo.
    echo Distribution:
    echo   1. Share this ZIP file with users
    echo   2. Users extract to any folder
    echo   3. Users run PORTABLE_FIRST_RUN.bat
    echo   4. Done!
    echo.
) else (
    echo [ERROR] Package creation failed!
    echo.
)

pause
