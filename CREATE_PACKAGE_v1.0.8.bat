@echo off
title MBAS v1.0.8 Package Creator
color 0B

echo.
echo ============================================
echo   MBAS v1.0.8 Package Creator
echo ============================================
echo.

REM Create package directory
set PACKAGE_DIR=MBAS_v1.0.8_Production_Ready
if exist "%PACKAGE_DIR%" (
    echo [*] Removing old package directory...
    rmdir /s /q "%PACKAGE_DIR%"
)

echo [*] Creating package directory structure...
mkdir "%PACKAGE_DIR%"
mkdir "%PACKAGE_DIR%\backend"
mkdir "%PACKAGE_DIR%\backend\src"
mkdir "%PACKAGE_DIR%\frontend"
mkdir "%PACKAGE_DIR%\docs"

echo.
echo [*] Copying backend files...
xcopy /E /I /Y backend\src "%PACKAGE_DIR%\backend\src" >nul
xcopy /Y backend\requirements.txt "%PACKAGE_DIR%\backend\" >nul
xcopy /Y backend\watchdog.py "%PACKAGE_DIR%\backend\" >nul

echo [*] Copying frontend built files...
if exist frontend\dist (
    xcopy /E /I /Y frontend\dist "%PACKAGE_DIR%\frontend\dist" >nul
    echo [OK] Frontend dist copied
) else (
    echo [WARN] Frontend dist not found - will copy source
    xcopy /E /I /Y frontend\src "%PACKAGE_DIR%\frontend\src" >nul
    xcopy /Y frontend\package.json "%PACKAGE_DIR%\frontend\" >nul
    xcopy /Y frontend\package-lock.json "%PACKAGE_DIR%\frontend\" >nul
    xcopy /Y frontend\vite.config.ts "%PACKAGE_DIR%\frontend\" >nul
    xcopy /Y frontend\tsconfig.json "%PACKAGE_DIR%\frontend\" >nul
    xcopy /Y frontend\tsconfig.app.json "%PACKAGE_DIR%\frontend\" >nul
    xcopy /Y frontend\tsconfig.node.json "%PACKAGE_DIR%\frontend\" >nul
    xcopy /Y frontend\index.html "%PACKAGE_DIR%\frontend\" >nul
    xcopy /Y frontend\tailwind.config.js "%PACKAGE_DIR%\frontend\" >nul
    xcopy /Y frontend\postcss.config.js "%PACKAGE_DIR%\frontend\" >nul
)

echo [*] Copying startup scripts...
xcopy /Y START_MBAS.bat "%PACKAGE_DIR%\" >nul
xcopy /Y STOP_MBAS.bat "%PACKAGE_DIR%\" >nul
xcopy /Y start-backend.bat "%PACKAGE_DIR%\" >nul
xcopy /Y start-frontend.bat "%PACKAGE_DIR%\" >nul
xcopy /Y AUTO_START_WITH_RECOVERY.bat "%PACKAGE_DIR%\" >nul
xcopy /Y START_WITH_WATCHDOG.bat "%PACKAGE_DIR%\" >nul
xcopy /Y INSTALL_BACKEND_FIXED.bat "%PACKAGE_DIR%\" >nul

echo [*] Copying documentation...
xcopy /Y CHANGELOG_v1.0.8.md "%PACKAGE_DIR%\docs\" >nul
xcopy /Y RELEASE_NOTES_v1.0.8.txt "%PACKAGE_DIR%\" >nul

REM Create quick start guide
echo [*] Creating installation guide...
(
echo ================================================================================
echo    MBAS v1.0.8 - Installation Guide
echo ================================================================================
echo.
echo STEP 1: INSTALL BACKEND DEPENDENCIES
echo    Run: INSTALL_BACKEND_FIXED.bat
echo    Wait for: "Installation complete"
echo.
echo STEP 2: START THE SYSTEM
echo    Option A ^(RECOMMENDED^): AUTO_START_WITH_RECOVERY.bat
echo      - Starts everything with auto-recovery
echo      - Best for production use
echo.
echo    Option B: START_MBAS.bat
echo      - Standard manual start
echo      - No auto-recovery
echo.
echo STEP 3: ACCESS THE SYSTEM
echo    Open browser: http://127.0.0.1:5173
echo    Default login: admin / admin123
echo.
echo STEP 4: VERIFY INSTALLATION
echo    - Dashboard should load
echo    - Check watchdog.log for monitoring events
echo    - Test product search and sales
echo.
echo ================================================================================
echo    TROUBLESHOOTING
echo ================================================================================
echo.
echo If login hangs:
echo    - Wait 30 seconds for timeout
echo    - Click "Retry" button
echo    - Watchdog will auto-restart backend if needed
echo.
echo If system doesn't start:
echo    1. Run CHECK_SYSTEM.bat ^(if available^)
echo    2. Check Python is installed: python --version
echo    3. Check backend logs in command window
echo    4. Read docs\CHANGELOG_v1.0.8.md for details
echo.
echo ================================================================================
echo    MONITORING
echo ================================================================================
echo.
echo Health Check:
echo    http://127.0.0.1:8000/health
echo.
echo Watchdog Log:
echo    Check watchdog.log for auto-recovery events
echo.
echo ================================================================================
) > "%PACKAGE_DIR%\INSTALLATION_GUIDE.txt"

REM Copy license if exists
if exist mbas.license (
    echo [*] Copying license file...
    xcopy /Y mbas.license "%PACKAGE_DIR%\" >nul
)

echo.
echo [*] Creating version info file...
(
echo MBAS Version 1.0.8
echo Build Date: 2026-04-29
echo Package: Production Ready
echo.
echo Features:
echo - Auto-Recovery Watchdog
echo - Smart Login with Timeout
echo - Connection Pool Management
echo - Enhanced Health Monitoring
echo.
echo For details, see RELEASE_NOTES_v1.0.8.txt
) > "%PACKAGE_DIR%\VERSION.txt"

echo.
echo [*] Creating archive...
if exist "%PACKAGE_DIR%.zip" del "%PACKAGE_DIR%.zip"

REM Use PowerShell to create zip
powershell -command "Compress-Archive -Path '%PACKAGE_DIR%' -DestinationPath '%PACKAGE_DIR%.zip' -Force"

if exist "%PACKAGE_DIR%.zip" (
    echo.
    echo ============================================
    echo   Package Created Successfully!
    echo ============================================
    echo.
    echo Package: %PACKAGE_DIR%.zip
    echo Size:
    dir "%PACKAGE_DIR%.zip" | find ".zip"
    echo.
    echo Contents:
    echo   - Backend with watchdog service
    echo   - Frontend application
    echo   - Auto-recovery startup scripts
    echo   - Complete documentation
    echo   - Installation guide
    echo.
    echo [OK] Ready for deployment!
    echo.
) else (
    echo.
    echo [ERROR] Failed to create zip archive
    echo [INFO] Package folder created: %PACKAGE_DIR%
    echo.
)

echo Do you want to open the package folder? ^(Y/N^)
choice /c YN /n /m "Choice: "
if errorlevel 2 goto :end
if errorlevel 1 explorer "%PACKAGE_DIR%"

:end
echo.
pause
