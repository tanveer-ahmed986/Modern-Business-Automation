@echo off
title MBAS - Automatic Setup and Start
color 0A

echo.
echo ============================================================
echo   MBAS - Automatic Setup and Start
echo   This will set up everything automatically
echo ============================================================
echo.

REM Step 1: Kill any existing processes
echo [1/7] Stopping any existing MBAS processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul
echo [OK] Old processes stopped
echo.

REM Step 2: Check Python and Node.js
echo [2/7] Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Python and Node.js found
echo.

REM Step 3: Install/verify backend dependencies
echo [3/7] Checking backend dependencies...
cd backend
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [*] Installing backend dependencies...
    pip install -q fastapi uvicorn sqlmodel python-jose[cryptography] passlib[bcrypt] python-multipart apscheduler >nul 2>&1
    if errorlevel 1 (
        echo [WARN] Some packages may not have installed, but continuing...
    )
)
cd ..
echo [OK] Backend dependencies ready
echo.

REM Step 4: Check if database exists
echo [4/7] Checking database...
if not exist "backend\database\mbas_database.db" (
    echo [*] Database not found, creating...
    cd backend
    python -c "from sqlmodel import SQLModel, create_engine; from pathlib import Path; Path('database').mkdir(exist_ok=True); engine = create_engine('sqlite:///database/mbas_database.db'); SQLModel.metadata.create_all(engine); print('[OK] Database created')" 2>nul

    REM Create admin user
    python -c "from sqlmodel import Session, create_engine, select; from passlib.context import CryptContext; from src.models.core import User, Settings, UserRole; engine = create_engine('sqlite:///database/mbas_database.db'); pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto'); session = Session(engine); stmt = select(User).where(User.username == 'admin'); admin = session.exec(stmt).first(); print('[OK] Admin user exists') if admin else None; session.add(User(username='admin', full_name='System Administrator', hashed_password=pwd_context.hash('admin123'), role=UserRole.ADMIN, is_active=True)) if not admin else None; session.add(Settings(id=1, company_name='My Business', currency='USD', tax_rate=0.0, feature_flags={})) if not admin else None; session.commit() if not admin else None; print('[OK] Admin user created: admin/admin123') if not admin else None" 2>nul
    cd ..
)
echo [OK] Database ready
echo.

REM Step 5: Check frontend dependencies
echo [5/7] Checking frontend dependencies...
if not exist "frontend\node_modules\" (
    echo [*] Installing frontend dependencies (this may take 2-3 minutes)...
    cd frontend
    call npm install --legacy-peer-deps >nul 2>&1
    cd ..
)
echo [OK] Frontend dependencies ready
echo.

REM Step 6: Start backend
echo [6/7] Starting Backend Server...
cd backend
start "MBAS Backend" cmd /k "python -m uvicorn src.main:app --host 127.0.0.1 --port 8000"
cd ..
timeout /t 3 /nobreak >nul
echo [OK] Backend starting on port 8000
echo.

REM Step 7: Start frontend
echo [7/7] Starting Frontend Server...
cd frontend
start "MBAS Frontend" cmd /k "npm run dev"
cd ..
timeout /t 5 /nobreak >nul
echo [OK] Frontend starting on port 5173
echo.

REM Wait for servers to start
echo.
echo ============================================================
echo   Waiting for servers to start (15 seconds)...
echo ============================================================
timeout /t 15 /nobreak >nul

REM Open browser
echo.
echo [*] Opening MBAS in browser...
start http://localhost:5173

echo.
echo ============================================================
echo   MBAS is now running!
echo ============================================================
echo.
echo Two windows have opened:
echo   [1] MBAS Backend  - Keep this open (port 8000)
echo   [2] MBAS Frontend - Keep this open (port 5173)
echo.
echo Browser opened to: http://localhost:5173
echo.
echo Login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo To stop MBAS:
echo   - Close the Backend window (press Ctrl+C, then Y)
echo   - Close the Frontend window (press Ctrl+C, then Y)
echo   - Or run: taskkill /F /IM python.exe /IM node.exe
echo.
echo ============================================================
echo.
echo You can close THIS window now.
echo The Backend and Frontend windows must stay open.
echo.
pause
