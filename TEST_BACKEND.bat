@echo off
title Test Backend Server
color 0A

echo.
echo ============================================================
echo   Testing MBAS Backend Server
echo ============================================================
echo.

cd backend

echo Starting FastAPI backend on http://localhost:8000
echo.
echo Watch for errors:
echo - If you see "ModuleNotFoundError" = Dependencies not installed
echo - If you see "Uvicorn running" = Backend is working!
echo.
echo Press Ctrl+C to stop
echo.

python -m uvicorn src.main:app --host 127.0.0.1 --port 8000

pause
