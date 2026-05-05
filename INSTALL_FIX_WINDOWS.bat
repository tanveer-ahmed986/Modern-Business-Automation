@echo off
title MBAS - Fix Windows Installation (No Compiler Needed)
color 0A

echo.
echo ================================================================
echo   MBAS - Windows Installation Fix
echo   Installing pre-built packages (no compiler needed)
echo ================================================================
echo.

REM Upgrade pip first
echo [Step 1/3] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip
    pause
    exit /b 1
)

REM Install packages that don't need compilation
echo.
echo [Step 2/3] Installing backend dependencies (pre-built)...
cd backend

REM Install packages one by one with pre-built wheels
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install sqlmodel==0.0.14
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-multipart==0.0.6
pip install email-validator==2.1.0
pip install apscheduler==3.10.4

REM Install data science packages with pre-built wheels
echo.
echo Installing data science packages...
pip install pandas==2.1.3
pip install numpy==1.26.2
pip install scikit-learn==1.3.2

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo.
    echo Trying alternative method...
    pip install --only-binary :all: pandas numpy scikit-learn
)

echo.
echo [Step 3/3] Verifying installation...
python -c "import pandas; import numpy; import sklearn; print('Success! All packages installed.')"

if errorlevel 1 (
    echo [ERROR] Verification failed
    pause
    exit /b 1
)

cd ..

REM Install frontend dependencies
echo.
echo [Step 4/5] Installing frontend dependencies...
cd frontend

echo Installing Node.js packages (this may take 2-3 minutes)...
echo Using --legacy-peer-deps to handle React version conflicts...
call npm install --legacy-peer-deps

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install frontend dependencies
    echo [i] Trying with --force flag...
    call npm install --force
    if errorlevel 1 (
        echo [ERROR] Frontend installation failed
        cd ..
        pause
        exit /b 1
    )
)

cd ..

echo.
echo [Step 5/5] Initializing database...
cd backend
python src\scripts\init_db.py
if errorlevel 1 (
    echo [WARN] Database initialization failed (will be created on first run)
)
cd ..

echo.
echo ================================================================
echo   SUCCESS! All dependencies installed successfully
echo ================================================================
echo.
echo Next steps:
echo   1. Run: START_MBAS.bat
echo   2. Browser will open automatically
echo   3. Login: admin / admin123
echo.
pause
