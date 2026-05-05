@echo off
title MBAS - Stop Services
color 0C

echo.
echo ============================================================
echo        Stopping MBAS Services...
echo ============================================================
echo.

REM Kill Python processes (backend)
echo [1/2] Stopping Backend Server...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
if errorlevel 1 (
    echo [i] No backend processes found
) else (
    echo [OK] Backend stopped
)

REM Kill Node.js processes (frontend)
echo [2/2] Stopping Frontend Server...
taskkill /F /IM node.exe /T >nul 2>&1
if errorlevel 1 (
    echo [i] No frontend processes found
) else (
    echo [OK] Frontend stopped
)

echo.
echo ============================================================
echo    MBAS Stopped Successfully
echo ============================================================
echo.
pause
