@echo off
title MBAS - Fix Frontend Structure
color 0B

echo.
echo ================================================================================
echo    FIXING FRONTEND FOLDER STRUCTURE
echo ================================================================================
echo.
echo Problem: Frontend assets in wrong location
echo   Current:  frontend/dist/*.js and *.css
echo   Expected: frontend/dist/assets/*.js and *.css
echo.
echo This will:
echo   1. Copy correctly built frontend from development folder
echo   2. Update deployment package structure
echo   3. Ready for installer rebuild
echo.
pause

cd /d "%~dp0"

REM Step 1: Copy correctly built frontend from development
echo [Step 1/3] Copying correctly built frontend...
echo.

REM Remove old frontend dist
if exist "MBAS_v1.0.9_Production_Ready\frontend\dist" (
    echo Removing old frontend...
    rmdir /s /q "MBAS_v1.0.9_Production_Ready\frontend\dist"
)

REM Copy new frontend dist with correct structure
echo Copying new frontend with correct structure...
xcopy /E /I /Y "..\frontend\dist" "MBAS_v1.0.9_Production_Ready\frontend\dist"

if errorlevel 1 (
    echo [FAIL] Failed to copy frontend!
    pause
    exit /b 1
)

echo [OK] Frontend copied
echo.

REM Step 2: Verify structure
echo [Step 2/3] Verifying folder structure...
echo.

if not exist "MBAS_v1.0.9_Production_Ready\frontend\dist\assets" (
    echo [FAIL] Assets folder still missing!
    echo.
    echo Manual steps needed:
    echo   1. cd frontend
    echo   2. npm run build
    echo   3. Then re-run this script
    pause
    exit /b 1
)

if not exist "MBAS_v1.0.9_Production_Ready\frontend\dist\assets\index-CE4PNPuu.js" (
    echo [WARN] JavaScript file not found - might have different hash
    echo        This is OK if other .js files exist
)

echo [OK] Folder structure correct
echo.

REM Step 3: Show structure
echo [Step 3/3] Current structure:
echo.
tree /F "MBAS_v1.0.9_Production_Ready\frontend\dist" /A
echo.

echo ================================================================================
echo    [SUCCESS] Frontend Structure Fixed!
echo ================================================================================
echo.
echo Next steps:
echo   1. Run: build_installer\REBUILD_INSTALLER_WITH_FIXES.bat
echo   2. This will create updated installer with correct frontend
echo.
echo For currently installed MBAS:
echo   1. Navigate to C:\MBAS\frontend\
echo   2. Delete the dist folder
echo   3. Copy the fixed dist from deployment package
echo.
pause
