@echo off
title MBAS - Fix Frontend 404 Errors
color 0E

echo.
echo ================================================================================
echo    FIX FRONTEND 404 ERRORS
echo ================================================================================
echo.
echo Problem: Server starts but shows 404 errors for JavaScript and CSS files
echo.
echo   GET /assets/index-*.js HTTP/1.1" 404 Not Found
echo   GET /assets/index-*.css HTTP/1.1" 404 Not Found
echo.
echo This happens because the frontend files are in the wrong folder.
echo.
echo This fix takes 5 seconds.
echo.
pause

REM Check if frontend dist exists
if not exist "%~dp0frontend\dist" (
    echo [FAIL] Frontend dist folder not found!
    echo        Expected: %~dp0frontend\dist
    pause
    exit /b 1
)

REM Check if assets folder exists with files
if not exist "%~dp0frontend\dist\assets\index-*.js" (
    echo [FAIL] Frontend assets missing!
    echo.
    echo The frontend hasn't been built correctly.
    echo Please rebuild the frontend:
    echo   cd frontend
    echo   npm install
    echo   npm run build
    echo.
    pause
    exit /b 1
)

echo [OK] Frontend structure is correct!
echo.
echo The frontend files are in the right location.
echo The 404 errors should not occur with this package.
echo.
echo If you're still seeing 404 errors after installation:
echo   1. The installation might have copied old files
echo   2. You need to reinstall MBAS
echo   3. Or manually copy the frontend folder
echo.
echo Folder structure (correct):
tree /F "%~dp0frontend\dist" /A
echo.
echo ================================================================================
echo    TROUBLESHOOTING 404 ERRORS
echo ================================================================================
echo.
echo If MBAS is already installed and showing 404 errors:
echo.
echo Option 1: Reinstall MBAS
echo   - Uninstall current version
echo   - Install the updated installer (after rebuilding)
echo.
echo Option 2: Manual fix
echo   1. Stop MBAS (run STOP_MBAS.bat or close tray icon)
echo   2. Navigate to where MBAS is installed (probably C:\MBAS)
echo   3. Delete C:\MBAS\frontend\dist folder
echo   4. Copy this folder: %~dp0frontend\dist
echo   5. To: C:\MBAS\frontend\dist
echo   6. Restart MBAS
echo.
echo Option 3: Quick copy (if installed at C:\MBAS)
echo   Run the command below to automatically copy:
echo.
echo   xcopy /E /I /Y "%~dp0frontend\dist" "C:\MBAS\frontend\dist"
echo.
pause
