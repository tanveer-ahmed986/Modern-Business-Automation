@echo off
echo.
echo ============================================================
echo   Quick System Check
echo ============================================================
echo.

echo Checking Python...
python --version
echo.

echo Checking Node.js...
node --version
echo.

echo Checking current directory...
cd
echo.

echo Checking backend folder...
dir backend 2>nul
echo.

echo Checking frontend folder...
dir frontend 2>nul
echo.

echo Checking frontend\node_modules...
if exist "frontend\node_modules\" (
    echo [OK] node_modules exists
) else (
    echo [ERROR] node_modules NOT FOUND!
    echo.
    echo You need to run:
    echo   cd frontend
    echo   npm install --legacy-peer-deps
)
echo.

echo ============================================================
echo.
echo Press any key to continue...
pause >nul
