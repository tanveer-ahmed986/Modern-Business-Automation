@echo off
title MBAS - Stop Server
color 0C

echo.
echo ================================================================
echo        Stopping MBAS Server...
echo ================================================================
echo.

REM Find and kill the MBAS uvicorn process on port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Stopping process %%a on port 8000...
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo [OK] MBAS Server stopped.
echo.
pause
