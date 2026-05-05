@echo off
title Test Frontend Server
color 0B

echo.
echo ============================================================
echo   Testing MBAS Frontend Server
echo ============================================================
echo.

cd frontend

echo Checking if node_modules exists...
if exist "node_modules\" (
    echo [OK] node_modules folder found
) else (
    echo [ERROR] node_modules NOT found
    echo.
    echo Installing dependencies now...
    call npm install --legacy-peer-deps
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting Vite dev server on http://localhost:5173
echo.
echo Watch for errors:
echo - If you see "EADDRINUSE" = Port 5173 already in use
echo - If you see "Local: http://localhost:5173" = Frontend is working!
echo.
echo After it starts, open browser to: http://localhost:5173
echo.
echo Press Ctrl+C to stop
echo.

call npm run dev

pause
