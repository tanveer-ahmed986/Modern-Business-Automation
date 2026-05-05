@echo off
title MBAS Frontend Server
color 0B

echo.
echo ============================================
echo   MBAS Frontend Server Starting...
echo ============================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed!
    echo.
    echo Please install Node.js 18 or higher
    echo Download from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo [OK] Node.js found
echo.

REM Navigate to frontend directory
cd frontend

REM Check if node_modules exists
if not exist "node_modules\" (
    echo [*] Installing frontend dependencies...
    echo     This may take a few minutes on first run...
    echo     Using --legacy-peer-deps to handle React version conflicts...
    echo.
    call npm install --legacy-peer-deps
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install frontend dependencies
        echo [i] Trying with --force flag...
        call npm install --force
        if errorlevel 1 (
            echo [ERROR] Installation failed completely
            pause
            exit /b 1
        )
    )
    echo.
    echo [OK] Dependencies installed successfully
    echo.
)

REM Start frontend dev server
echo [*] Starting Vite dev server on http://localhost:5173
echo.
echo [i] Keep this window open while using MBAS
echo [i] Press Ctrl+C to stop the frontend
echo.

npm run dev

pause
