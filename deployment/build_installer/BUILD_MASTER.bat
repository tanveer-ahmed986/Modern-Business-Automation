@echo off
title MBAS Professional Installer Builder
color 0B

:MENU
cls
echo.
echo ========================================================================
echo    MBAS Professional Installer Builder
echo    Version 1.2.0
echo ========================================================================
echo.
echo Current Status:
if exist ".\output\MBAS_Setup_v1.2.0_Robust.exe" (
    echo   [X] Robust Installer Built
) else (
    echo   [ ] Robust Installer Not Built
)
if exist ".\output\MBAS_v1.2.0_Portable.zip" (
    echo   [X] Portable Package Built
) else (
    echo   [ ] Portable Package Not Built
)
echo.
echo ========================================================================
echo    MAIN MENU
echo ========================================================================
echo.
echo   [1] Build Robust Installer (.exe) - RECOMMENDED FOR DISTRIBUTION
echo   [2] Build Portable Package (.zip) - NO INSTALLATION REQUIRED
echo   [3] Build Both
echo.
echo   [4] Force Uninstall MBAS (Fix Hanging Uninstaller)
echo   [5] Test Built Installer
echo   [6] Open Output Folder
echo.
echo   [7] View Documentation
echo   [8] System Check
echo.
echo   [0] Exit
echo.
echo ========================================================================
echo.
set /p choice="Enter your choice (0-8): "

if "%choice%"=="1" goto BUILD_INSTALLER
if "%choice%"=="2" goto BUILD_PORTABLE
if "%choice%"=="3" goto BUILD_BOTH
if "%choice%"=="4" goto FORCE_UNINSTALL
if "%choice%"=="5" goto TEST_INSTALLER
if "%choice%"=="6" goto OPEN_OUTPUT
if "%choice%"=="7" goto VIEW_DOCS
if "%choice%"=="8" goto SYSTEM_CHECK
if "%choice%"=="0" goto EXIT

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto MENU

:BUILD_INSTALLER
cls
echo.
echo ========================================================================
echo    Building Robust Installer
echo ========================================================================
echo.
call BUILD_ROBUST_INSTALLER.bat
pause
goto MENU

:BUILD_PORTABLE
cls
echo.
echo ========================================================================
echo    Building Portable Package
echo ========================================================================
echo.
call CREATE_PORTABLE_PACKAGE.bat
pause
goto MENU

:BUILD_BOTH
cls
echo.
echo ========================================================================
echo    Building Both Installer and Portable Package
echo ========================================================================
echo.
echo [Step 1/2] Building Robust Installer...
echo.
call BUILD_ROBUST_INSTALLER.bat

echo.
echo.
echo [Step 2/2] Building Portable Package...
echo.
call CREATE_PORTABLE_PACKAGE.bat

echo.
echo ========================================================================
echo    BOTH PACKAGES BUILT SUCCESSFULLY!
echo ========================================================================
echo.
echo Created:
if exist ".\output\MBAS_Setup_v1.2.0_Robust.exe" (
    echo   [X] .\output\MBAS_Setup_v1.2.0_Robust.exe
)
if exist ".\output\MBAS_v1.2.0_Portable.zip" (
    echo   [X] .\output\MBAS_v1.2.0_Portable.zip
)
echo.
pause
goto MENU

:FORCE_UNINSTALL
cls
echo.
echo ========================================================================
echo    Force Uninstall MBAS (Fix Hanging Uninstaller)
echo ========================================================================
echo.
echo This will forcefully remove MBAS from your system.
echo Use this if the normal uninstaller is stuck.
echo.
echo Your database will be backed up before removal.
echo.
set /p confirm="Are you sure? (Y/N): "
if /i not "%confirm%"=="Y" goto MENU

call FORCE_UNINSTALL.bat
pause
goto MENU

:TEST_INSTALLER
cls
echo.
echo ========================================================================
echo    Test Built Installer
echo ========================================================================
echo.

if not exist ".\output\MBAS_Setup_v1.2.0_Robust.exe" (
    echo [ERROR] Installer not found!
    echo.
    echo Please build the installer first (Option 1 or 3).
    echo.
    pause
    goto MENU
)

echo Found: .\output\MBAS_Setup_v1.2.0_Robust.exe
echo.
echo File Information:
dir ".\output\MBAS_Setup_v1.2.0_Robust.exe" | find "MBAS_Setup"
echo.
echo WARNING: This will run the installer on THIS computer.
echo          Recommended to test on a separate VM or test machine.
echo.
set /p runtest="Run installer now? (Y/N): "
if /i not "%runtest%"=="Y" goto MENU

echo.
echo Launching installer...
start "" ".\output\MBAS_Setup_v1.2.0_Robust.exe"
echo.
echo Installer launched in a new window.
echo.
pause
goto MENU

:OPEN_OUTPUT
cls
echo.
echo ========================================================================
echo    Opening Output Folder
echo ========================================================================
echo.
if not exist ".\output" (
    echo Output folder does not exist yet.
    echo Build an installer first.
    echo.
    pause
    goto MENU
)

start "" ".\output"
echo.
echo Output folder opened in Windows Explorer.
echo.
pause
goto MENU

:VIEW_DOCS
cls
echo.
echo ========================================================================
echo    Documentation
echo ========================================================================
echo.
echo Available documentation:
echo.
if exist "INSTALLER_SOLUTION_GUIDE.md" (
    echo   [X] INSTALLER_SOLUTION_GUIDE.md - Complete guide
)
if exist "FORCE_UNINSTALL.bat" (
    echo   [X] FORCE_UNINSTALL.bat - Emergency uninstaller
)
if exist "MBAS_Installer_Robust.iss" (
    echo   [X] MBAS_Installer_Robust.iss - Installer source code
)
echo.
echo.
set /p opendoc="Open INSTALLER_SOLUTION_GUIDE.md? (Y/N): "
if /i "%opendoc%"=="Y" (
    if exist "INSTALLER_SOLUTION_GUIDE.md" (
        start "" "INSTALLER_SOLUTION_GUIDE.md"
    ) else (
        echo File not found!
    )
)
echo.
pause
goto MENU

:SYSTEM_CHECK
cls
echo.
echo ========================================================================
echo    System Check
echo ========================================================================
echo.
echo Checking system requirements for building installers...
echo.

REM Check Inno Setup
echo [1/4] Checking for Inno Setup...
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo   [OK] Inno Setup 6 found
) else (
    echo   [X] Inno Setup 6 NOT FOUND
    echo       Download from: https://jrsoftware.org/isdl.php
)

REM Check 7-Zip
echo.
echo [2/4] Checking for 7-Zip...
where 7z >nul 2>&1
if %errorlevel%==0 (
    echo   [OK] 7-Zip found
) else (
    echo   [!] 7-Zip not found (optional - PowerShell will be used instead)
    echo       Download from: https://www.7-zip.org/
)

REM Check Source Files
echo.
echo [3/4] Checking source files...
if exist "..\MBAS_v1.0.9_Production_Ready" (
    echo   [OK] Source files found
    echo       Location: ..\MBAS_v1.0.9_Production_Ready
) else (
    echo   [X] Source files NOT FOUND
    echo       Expected: ..\MBAS_v1.0.9_Production_Ready
)

REM Check PowerShell
echo.
echo [4/4] Checking PowerShell...
where powershell >nul 2>&1
if %errorlevel%==0 (
    echo   [OK] PowerShell found
) else (
    echo   [X] PowerShell NOT FOUND (required)
)

echo.
echo ========================================================================
echo    System Check Complete
echo ========================================================================
echo.

REM Summary
set ready=1
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set ready=0
if not exist "..\MBAS_v1.0.9_Production_Ready" set ready=0

if %ready%==1 (
    echo Status: [READY] You can build installers
) else (
    echo Status: [NOT READY] Please install missing components
    echo.
    echo Action Items:
    if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
        echo   - Install Inno Setup 6
    )
    if not exist "..\MBAS_v1.0.9_Production_Ready" (
        echo   - Ensure source files are in correct location
    )
)

echo.
pause
goto MENU

:EXIT
cls
echo.
echo ========================================================================
echo    Exiting MBAS Installer Builder
echo ========================================================================
echo.
echo Thank you for using MBAS Professional Installer Builder!
echo.
echo For help, see: INSTALLER_SOLUTION_GUIDE.md
echo.
timeout /t 2 >nul
exit /b 0
