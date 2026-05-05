@echo off
title MBAS v1.0.9 Package Creator
color 0B

echo.
echo ============================================
echo   MBAS v1.0.9 Package Creator
echo ============================================
echo.

REM Create package directory
set PACKAGE_DIR=deployment\MBAS_v1.0.9_Production_Ready
if exist "%PACKAGE_DIR%" (
    echo [*] Package directory already exists
    echo [*] Use this script to rebuild the zip only
) else (
    echo [ERROR] Package directory not found: %PACKAGE_DIR%
    echo [INFO] Please ensure the package directory exists first
    pause
    exit /b 1
)

echo.
echo [*] Verifying critical files...

REM Check for INSTALL.bat
if not exist "%PACKAGE_DIR%\INSTALL.bat" (
    echo [WARN] INSTALL.bat not found - copying from MBAS_Package_V2...
    if exist "deployment\MBAS_Package_V2\INSTALL.bat" (
        xcopy /Y "deployment\MBAS_Package_V2\INSTALL.bat" "%PACKAGE_DIR%\" >nul
        echo [OK] INSTALL.bat copied
    ) else (
        echo [ERROR] Source file not found: deployment\MBAS_Package_V2\INSTALL.bat
    )
)

REM Check for create_shortcut.vbs
if not exist "%PACKAGE_DIR%\create_shortcut.vbs" (
    echo [WARN] create_shortcut.vbs not found - copying...
    if exist "deployment\MBAS_Package_V2\create_shortcut.vbs" (
        xcopy /Y "deployment\MBAS_Package_V2\create_shortcut.vbs" "%PACKAGE_DIR%\" >nul
        echo [OK] create_shortcut.vbs copied
    )
)

REM Check for mbas_icon.ico
if not exist "%PACKAGE_DIR%\mbas_icon.ico" (
    echo [WARN] mbas_icon.ico not found - copying...
    if exist "deployment\MBAS_Package_V2\mbas_icon.ico" (
        xcopy /Y "deployment\MBAS_Package_V2\mbas_icon.ico" "%PACKAGE_DIR%\" >nul
        echo [OK] mbas_icon.ico copied
    )
)

REM Check for HEALTH_CHECK.bat
if not exist "%PACKAGE_DIR%\HEALTH_CHECK.bat" (
    echo [WARN] HEALTH_CHECK.bat not found - copying...
    if exist "deployment\MBAS_Package_V2\HEALTH_CHECK.bat" (
        xcopy /Y "deployment\MBAS_Package_V2\HEALTH_CHECK.bat" "%PACKAGE_DIR%\" >nul
        echo [OK] HEALTH_CHECK.bat copied
    )
)

REM Check for START_MBAS_TRAY.bat
if not exist "%PACKAGE_DIR%\START_MBAS_TRAY.bat" (
    echo [ERROR] START_MBAS_TRAY.bat not found!
) else (
    echo [OK] START_MBAS_TRAY.bat exists
)

REM Check for mbas_tray.py
if not exist "%PACKAGE_DIR%\scripts\mbas_tray.py" (
    echo [ERROR] scripts\mbas_tray.py not found!
) else (
    echo [OK] scripts\mbas_tray.py exists
)

echo.
echo [*] File verification complete
echo.
echo [*] Creating archive...

cd deployment
if exist "MBAS_v1.0.9_Production_Ready.zip" (
    echo [*] Removing old zip file...
    del "MBAS_v1.0.9_Production_Ready.zip"
)

REM Use PowerShell to create zip
powershell -command "Compress-Archive -Path 'MBAS_v1.0.9_Production_Ready' -DestinationPath 'MBAS_v1.0.9_Production_Ready.zip' -Force"

cd ..

if exist "deployment\MBAS_v1.0.9_Production_Ready.zip" (
    echo.
    echo ============================================
    echo   Package Created Successfully!
    echo ============================================
    echo.
    echo Package: deployment\MBAS_v1.0.9_Production_Ready.zip
    echo.

    REM Get file size
    for %%A in ("deployment\MBAS_v1.0.9_Production_Ready.zip") do echo Size: %%~zA bytes

    echo.
    echo Critical files included:
    echo   [X] INSTALL.bat - Main installation script
    echo   [X] START_MBAS_TRAY.bat - System tray launcher
    echo   [X] scripts\mbas_tray.py - Tray application
    echo   [X] create_shortcut.vbs - Desktop shortcut creator
    echo   [X] mbas_icon.ico - Application icon
    echo   [X] HEALTH_CHECK.bat - System health checker
    echo   [X] Backend source code
    echo   [X] Frontend dist files
    echo   [X] Documentation
    echo.
    echo [OK] Ready for deployment!
    echo.
) else (
    echo.
    echo [ERROR] Failed to create zip archive
    echo [INFO] Package folder exists at: %PACKAGE_DIR%
    echo.
)

echo Do you want to open the deployment folder? (Y/N)
choice /c YN /n /m "Choice: "
if errorlevel 2 goto :end
if errorlevel 1 explorer "deployment"

:end
echo.
pause
