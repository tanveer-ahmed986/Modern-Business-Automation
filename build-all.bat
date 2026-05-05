@echo off
REM ============================================
REM  MBAS Production Build Pipeline
REM  Builds: Backend (Nuitka) + Frontend (Vite) + Tauri Installer
REM ============================================

setlocal EnableDelayedExpansion

echo.
echo ============================================
echo   MBAS Production Build Pipeline
echo ============================================
echo.

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM Check for Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

echo [OK] Prerequisites check passed
echo.

REM Step 1: Install Python dependencies
echo ============================================
echo [1/6] Installing backend dependencies...
echo ============================================
cd backend
if exist requirements.txt (
    pip install -r requirements.txt -q
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Python dependencies
        cd ..
        pause
        exit /b 1
    )
    echo [OK] Backend dependencies installed
) else (
    echo [WARNING] requirements.txt not found
)
cd ..
echo.

REM Step 2: Run backend tests (optional but recommended)
echo ============================================
echo [2/6] Running backend tests...
echo ============================================
cd backend
if exist pytest.ini (
    echo Running pytest...
    pytest --tb=short -q
    if %errorlevel% neq 0 (
        echo [WARNING] Some tests failed. Continue anyway? (Y/N)
        set /p continue=
        if /i not "!continue!"=="Y" (
            cd ..
            pause
            exit /b 1
        )
    ) else (
        echo [OK] All backend tests passed
    )
) else (
    echo [SKIP] pytest not configured
)
cd ..
echo.

REM Step 3: Compile backend with Nuitka
echo ============================================
echo [3/6] Compiling backend with Nuitka...
echo ============================================
echo This may take 5-15 minutes...
cd backend
python scripts/build.py
if %errorlevel% neq 0 (
    echo [ERROR] Nuitka compilation failed
    cd ..
    pause
    exit /b 1
)
cd ..
echo.

REM Step 4: Copy backend binary to Tauri
echo ============================================
echo [4/6] Copying backend to Tauri binaries...
echo ============================================
if not exist tauri-app\src-tauri\binaries (
    mkdir tauri-app\src-tauri\binaries
)

if exist backend\build\mbas-backend.exe (
    copy /Y backend\build\mbas-backend.exe tauri-app\src-tauri\binaries\
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to copy backend binary
        pause
        exit /b 1
    )
    echo [OK] Backend binary copied to Tauri
) else (
    echo [ERROR] Backend executable not found at backend\build\mbas-backend.exe
    pause
    exit /b 1
)
echo.

REM Step 5: Build frontend
echo ============================================
echo [5/6] Building React frontend...
echo ============================================
cd frontend
if exist package.json (
    echo Installing frontend dependencies...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install frontend dependencies
        cd ..
        pause
        exit /b 1
    )

    echo Building frontend...
    call npm run build
    if %errorlevel% neq 0 (
        echo [ERROR] Frontend build failed
        cd ..
        pause
        exit /b 1
    )
    echo [OK] Frontend built successfully
) else (
    echo [ERROR] package.json not found in frontend/
    cd ..
    pause
    exit /b 1
)
cd ..
echo.

REM Step 6: Build Tauri desktop installer
echo ============================================
echo [6/6] Building Tauri MSI installer...
echo ============================================
cd tauri-app
if exist package.json (
    echo Installing Tauri dependencies...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Tauri dependencies
        cd ..
        pause
        exit /b 1
    )

    echo Building Tauri application...
    call npm run tauri build
    if %errorlevel% neq 0 (
        echo [ERROR] Tauri build failed
        cd ..
        pause
        exit /b 1
    )
    echo [OK] Tauri installer built successfully
) else (
    echo [ERROR] package.json not found in tauri-app/
    cd ..
    pause
    exit /b 1
)
cd ..
echo.

REM Success message
echo.
echo ============================================
echo   BUILD SUCCESSFUL!
echo ============================================
echo.
echo Installer location:
echo   tauri-app\src-tauri\target\release\bundle\msi\
echo.
echo Files generated:
for %%f in (tauri-app\src-tauri\target\release\bundle\msi\*.msi) do (
    echo   - %%~nxf (%%~zf bytes)
)
echo.
echo Next steps:
echo   1. Test installer on a clean Windows machine
echo   2. Create license file with: cd tools ^&^& python license_generator.py
echo   3. Distribute installer + license file to customers
echo.

pause
exit /b 0
