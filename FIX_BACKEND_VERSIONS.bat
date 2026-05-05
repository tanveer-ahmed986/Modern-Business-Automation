@echo off
title Fix Backend Version Compatibility
color 0C

echo.
echo ============================================================
echo   Fixing FastAPI + Pydantic Version Compatibility
echo ============================================================
echo.

echo This will install compatible versions of FastAPI and Pydantic
echo.
pause

cd backend

echo [1/3] Uninstalling incompatible packages...
pip uninstall -y fastapi pydantic pydantic-settings pydantic-core

echo.
echo [2/3] Installing compatible versions...
pip install fastapi==0.104.1
pip install pydantic==2.5.3
pip install pydantic-settings==2.1.0

echo.
echo [3/3] Verifying installation...
python -c "import fastapi; import pydantic; print('FastAPI version:', fastapi.__version__); print('Pydantic version:', pydantic.__version__)"

if errorlevel 1 (
    echo [ERROR] Installation failed
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   SUCCESS! Compatible versions installed
echo ============================================================
echo.
echo FastAPI and Pydantic are now compatible
echo.
echo Next step: Start the backend server
echo   cd backend
echo   python -m uvicorn src.main:app --host 127.0.0.1 --port 8000
echo.
pause
