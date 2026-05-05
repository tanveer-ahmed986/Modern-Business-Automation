@echo off
title MBAS Diagnostics
color 0E

echo.
echo ============================================================
echo   MBAS - System Diagnostics
echo ============================================================
echo.

REM Check Python
echo [CHECK 1/6] Python Installation
python --version 2>nul
if errorlevel 1 (
    echo [ERROR] Python NOT installed
    echo Please install Python from https://www.python.org/downloads/
) else (
    echo [OK] Python installed
)
echo.

REM Check Node.js
echo [CHECK 2/6] Node.js Installation
node --version 2>nul
if errorlevel 1 (
    echo [ERROR] Node.js NOT installed
    echo Please install Node.js from https://nodejs.org/
) else (
    echo [OK] Node.js installed
)
echo.

REM Check backend folder
echo [CHECK 3/6] Backend Files
if exist "backend\src\main.py" (
    echo [OK] Backend files present
) else (
    echo [ERROR] Backend files missing
    echo Missing: backend\src\main.py
)
echo.

REM Check frontend folder
echo [CHECK 4/6] Frontend Files
if exist "frontend\package.json" (
    echo [OK] Frontend files present
) else (
    echo [ERROR] Frontend files missing
    echo Missing: frontend\package.json
)
echo.

REM Check frontend dependencies
echo [CHECK 5/6] Frontend Dependencies
if exist "frontend\node_modules\" (
    echo [OK] Frontend node_modules exists
) else (
    echo [ERROR] Frontend dependencies NOT installed
    echo Run: cd frontend ^&^& npm install --legacy-peer-deps
)
echo.

REM Check backend dependencies
echo [CHECK 6/6] Backend Dependencies
cd backend
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [ERROR] Backend dependencies NOT installed
    echo Run: cd backend ^&^& pip install -r requirements.txt
) else (
    echo [OK] Backend dependencies installed
)
cd ..
echo.

echo ============================================================
echo   Testing Servers (Manual Check)
echo ============================================================
echo.
echo Let's test each server separately to see what's wrong.
echo.
pause

REM Test Backend
echo.
echo ============================================================
echo   TEST 1: Starting Backend Server
echo ============================================================
echo.
echo Starting backend on http://localhost:8000
echo Watch for errors below...
echo.
cd backend
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000
cd ..
