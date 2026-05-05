@echo off
title Stop MBAS
color 0C

echo.
echo ============================================================
echo   Stopping MBAS - All Services
echo ============================================================
echo.

echo [*] Stopping Backend Server (Python)...
taskkill /F /IM python.exe >nul 2>&1
if errorlevel 1 (
    echo [i] No backend processes found
) else (
    echo [OK] Backend stopped
)

echo.
echo [*] Stopping Frontend Server (Node.js)...
taskkill /F /IM node.exe >nul 2>&1
if errorlevel 1 (
    echo [i] No frontend processes found
) else (
    echo [OK] Frontend stopped
)

echo.
echo ============================================================
echo   All MBAS services stopped
echo ============================================================
echo.
pause
