@echo off
REM ============================================
REM  MBAS Quick Build (Development)
REM  Skips tests, uses faster compilation
REM ============================================

echo.
echo ============================================
echo   MBAS Quick Build (Development)
echo ============================================
echo.

REM Build frontend only
echo [1/2] Building frontend...
cd frontend
call npm run build
if %errorlevel% neq 0 (
    echo [ERROR] Frontend build failed
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] Frontend built
echo.

REM Build Tauri (assumes backend binary already exists or using dev mode)
echo [2/2] Building Tauri (dev mode)...
cd tauri-app
call npm run tauri build -- --debug
if %errorlevel% neq 0 (
    echo [ERROR] Tauri build failed
    cd ..
    pause
    exit /b 1
)
cd ..
echo.

echo ============================================
echo   QUICK BUILD COMPLETE!
echo ============================================
echo.
echo Debug installer location:
echo   tauri-app\src-tauri\target\debug\bundle\
echo.

pause
