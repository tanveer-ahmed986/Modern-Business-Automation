@echo off
title MBAS System Check
color 0E

echo Running system diagnostics...
echo Results will be saved to: diagnostic_report.txt
echo.

REM Save all output to file
(
echo ============================================================
echo   MBAS System Diagnostic Report
echo   Generated: %date% %time%
echo ============================================================
echo.

echo [CHECK 1/8] Current Directory
cd
echo.

echo [CHECK 2/8] Python Installation
python --version 2>&1
if errorlevel 1 (
    echo ERROR: Python NOT installed
) else (
    echo SUCCESS: Python is installed
)
echo.

echo [CHECK 3/8] Node.js Installation
node --version 2>&1
if errorlevel 1 (
    echo ERROR: Node.js NOT installed
) else (
    echo SUCCESS: Node.js is installed
)
echo.

echo [CHECK 4/8] npm Installation
npm --version 2>&1
if errorlevel 1 (
    echo ERROR: npm NOT installed
) else (
    echo SUCCESS: npm is installed
)
echo.

echo [CHECK 5/8] Backend Files
if exist "backend\src\main.py" (
    echo SUCCESS: backend\src\main.py found
) else (
    echo ERROR: backend\src\main.py NOT FOUND
)
if exist "backend\requirements.txt" (
    echo SUCCESS: backend\requirements.txt found
) else (
    echo ERROR: backend\requirements.txt NOT FOUND
)
echo.

echo [CHECK 6/8] Frontend Files
if exist "frontend\package.json" (
    echo SUCCESS: frontend\package.json found
) else (
    echo ERROR: frontend\package.json NOT FOUND
)
if exist "frontend\src\App.tsx" (
    echo SUCCESS: frontend\src\App.tsx found
) else (
    echo ERROR: frontend\src\App.tsx NOT FOUND
)
echo.

echo [CHECK 7/8] Frontend Dependencies
if exist "frontend\node_modules\" (
    echo SUCCESS: frontend\node_modules exists
    dir frontend\node_modules | find "Directory of"
) else (
    echo ERROR: frontend\node_modules NOT FOUND
    echo SOLUTION: Run "cd frontend && npm install --legacy-peer-deps"
)
echo.

echo [CHECK 8/8] Backend Dependencies Check
cd backend 2>&1
python -c "import fastapi; print('SUCCESS: FastAPI installed')" 2>&1
if errorlevel 1 (
    echo ERROR: FastAPI NOT installed
    echo SOLUTION: Run "cd backend && pip install -r requirements.txt"
)
python -c "import uvicorn; print('SUCCESS: Uvicorn installed')" 2>&1
if errorlevel 1 (
    echo ERROR: Uvicorn NOT installed
)
cd .. 2>&1
echo.

echo ============================================================
echo   DIAGNOSTIC SUMMARY
echo ============================================================
echo.
echo If you see any "ERROR" messages above, those need to be fixed.
echo.
echo Common fixes:
echo - Python not installed: https://www.python.org/downloads/
echo - Node.js not installed: https://nodejs.org/
echo - node_modules missing: cd frontend ^&^& npm install --legacy-peer-deps
echo - Backend deps missing: cd backend ^&^& pip install -r requirements.txt
echo.
echo ============================================================

) > diagnostic_report.txt

REM Display the report
type diagnostic_report.txt

echo.
echo.
echo Report saved to: diagnostic_report.txt
echo.
echo Press any key to close...
pause >nul
