@echo off
title Install Backend Dependencies (No Compiler Needed)
color 0A

echo.
echo ============================================================
echo   Installing Backend Dependencies (Pre-Built Only)
echo ============================================================
echo.

cd backend

echo [METHOD 1] Installing with --only-binary (no compilation)...
echo.

pip install --only-binary :all: fastapi==0.104.1 uvicorn==0.24.0 sqlmodel==0.0.14

if errorlevel 1 (
    echo.
    echo [WARN] Method 1 failed, trying Method 2...
    echo.

    echo [METHOD 2] Installing core packages without version pinning...
    pip install fastapi uvicorn sqlmodel

    if errorlevel 1 (
        echo.
        echo [ERROR] Installation failed
        echo.
        echo You need to install Microsoft C++ Build Tools
        echo Or try installing Python 3.11 instead of 3.13
        pause
        exit /b 1
    )
)

echo.
echo [*] Installing additional packages...
pip install python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 python-multipart==0.0.9 apscheduler==3.10.4

echo.
echo [*] Installing data packages with pre-built wheels...
pip install --only-binary :all: pandas numpy scikit-learn

if errorlevel 1 (
    echo [WARN] Failed to install data packages (not critical)
)

echo.
echo [*] Verifying installation...
python -c "import fastapi; import uvicorn; import sqlmodel; print('SUCCESS: Core packages installed')"

if errorlevel 1 (
    echo [ERROR] Verification failed
    pause
    exit /b 1
)

cd ..

echo.
echo ============================================================
echo   SUCCESS! Backend dependencies installed
echo ============================================================
echo.
echo Next: Start backend server
echo   cd backend
echo   python -m uvicorn src.main:app --host 127.0.0.1 --port 8000
echo.
pause
