@echo off
title Fix NPM Dependency Error
color 0C

echo.
echo ============================================================
echo   Fixing NPM Dependency Conflict
echo ============================================================
echo.

echo [*] This will fix the React version conflict error
echo [*] Location: frontend folder
echo.

cd frontend

echo [1/2] Removing old node_modules...
if exist "node_modules\" (
    rmdir /s /q node_modules
    echo [OK] Removed old node_modules
) else (
    echo [i] No node_modules found (skipping)
)

echo.
echo [2/2] Installing dependencies with --legacy-peer-deps...
echo [i] This may take 2-3 minutes...
echo.

call npm install --legacy-peer-deps

if errorlevel 1 (
    echo.
    echo [ERROR] Installation with --legacy-peer-deps failed
    echo [i] Trying with --force flag...
    echo.
    call npm install --force
    if errorlevel 1 (
        echo.
        echo [ERROR] Installation completely failed
        echo.
        echo Possible solutions:
        echo   1. Make sure Node.js is installed (https://nodejs.org/)
        echo   2. Delete package-lock.json and try again
        echo   3. Run: npm cache clean --force
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ============================================================
echo   SUCCESS! Dependencies installed
echo ============================================================
echo.
echo You can now run START_MBAS.bat
echo.
pause
