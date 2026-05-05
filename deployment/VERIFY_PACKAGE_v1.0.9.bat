@echo off
title MBAS v1.0.9 Package Verification
color 0A

echo.
echo ========================================================
echo   MBAS v1.0.9 - Package Verification
echo ========================================================
echo.

set PKG=MBAS_v1.0.9_Production_Ready
set ALL_OK=1

echo Checking package contents...
echo.

REM Check directory exists
if not exist "%PKG%" (
    echo [ERROR] Package directory not found: %PKG%
    set ALL_OK=0
    goto :end
)

echo Package directory: %PKG%
echo.
echo Critical Files:
echo --------------------------------------------------------

REM Check INSTALL.bat
if exist "%PKG%\INSTALL.bat" (
    echo [OK] INSTALL.bat
) else (
    echo [MISSING] INSTALL.bat ^^^!^^^!^^^!
    set ALL_OK=0
)

REM Check START_MBAS_TRAY.bat
if exist "%PKG%\START_MBAS_TRAY.bat" (
    echo [OK] START_MBAS_TRAY.bat
) else (
    echo [MISSING] START_MBAS_TRAY.bat ^^^!^^^!^^^!
    set ALL_OK=0
)

REM Check create_shortcut.vbs
if exist "%PKG%\create_shortcut.vbs" (
    echo [OK] create_shortcut.vbs
) else (
    echo [MISSING] create_shortcut.vbs ^^^!^^^!^^^!
    set ALL_OK=0
)

REM Check mbas_icon.ico
if exist "%PKG%\mbas_icon.ico" (
    echo [OK] mbas_icon.ico
) else (
    echo [MISSING] mbas_icon.ico ^^^!^^^!^^^!
    set ALL_OK=0
)

REM Check HEALTH_CHECK.bat
if exist "%PKG%\HEALTH_CHECK.bat" (
    echo [OK] HEALTH_CHECK.bat
) else (
    echo [MISSING] HEALTH_CHECK.bat ^^^!^^^!^^^!
    set ALL_OK=0
)

REM Check scripts/mbas_tray.py
if exist "%PKG%\scripts\mbas_tray.py" (
    echo [OK] scripts\mbas_tray.py
) else (
    echo [MISSING] scripts\mbas_tray.py ^^^!^^^!^^^!
    set ALL_OK=0
)

REM Check backend files
if exist "%PKG%\backend\src\main.py" (
    echo [OK] backend\src\main.py
) else (
    echo [MISSING] backend\src\main.py ^^^!^^^!^^^!
    set ALL_OK=0
)

REM Check backend requirements
if exist "%PKG%\backend\requirements.txt" (
    echo [OK] backend\requirements.txt
) else (
    echo [MISSING] backend\requirements.txt ^^^!^^^!^^^!
    set ALL_OK=0
)

REM Check frontend dist
if exist "%PKG%\frontend\dist\index.html" (
    echo [OK] frontend\dist\index.html
) else (
    echo [MISSING] frontend\dist\index.html ^^^!^^^!^^^!
    set ALL_OK=0
)

REM Check README
if exist "%PKG%\README_v1.0.9.txt" (
    echo [OK] README_v1.0.9.txt
) else (
    echo [MISSING] README_v1.0.9.txt ^^^!^^^!^^^!
    set ALL_OK=0
)

echo.
echo Supporting Files:
echo --------------------------------------------------------

if exist "%PKG%\START_MBAS.bat" echo [OK] START_MBAS.bat
if exist "%PKG%\STOP_MBAS.bat" echo [OK] STOP_MBAS.bat
if exist "%PKG%\AUTO_START_WITH_RECOVERY.bat" echo [OK] AUTO_START_WITH_RECOVERY.bat
if exist "%PKG%\mbas.license" echo [OK] mbas.license
if exist "%PKG%\RELEASE_NOTES_v1.0.9.txt" echo [OK] RELEASE_NOTES_v1.0.9.txt
if exist "%PKG%\UPGRADE_GUIDE_v1.0.9.txt" echo [OK] UPGRADE_GUIDE_v1.0.9.txt

echo.
echo --------------------------------------------------------

REM Check README content for correct installation file
findstr /C:"INSTALL.bat" "%PKG%\README_v1.0.9.txt" >nul 2>&1
if errorlevel 1 (
    echo [WARN] README may not reference INSTALL.bat correctly
    set ALL_OK=0
) else (
    echo [OK] README references INSTALL.bat
)

echo.
echo Zip Package:
echo --------------------------------------------------------

if exist "%PKG%.zip" (
    echo [OK] %PKG%.zip exists
    for %%A in ("%PKG%.zip") do echo     Size: %%~zA bytes ^(%%~zAk KB^)
) else (
    echo [MISSING] %PKG%.zip
    echo [INFO] Run CREATE_PACKAGE_v1.0.9.bat to create it
    set ALL_OK=0
)

:end
echo.
echo ========================================================

if %ALL_OK%==1 (
    echo   [SUCCESS] Package verification PASSED
    echo   All critical files are present and correct.
    echo   Package is ready for deployment!
) else (
    echo   [FAILED] Package verification FAILED
    echo   Some critical files are missing.
    echo   Please run CREATE_PACKAGE_v1.0.9.bat to fix.
)

echo ========================================================
echo.
pause
