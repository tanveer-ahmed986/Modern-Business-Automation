@echo off
REM ============================================================================
REM  MBAS v2.0.7 - Build and Installation Guide
REM  Z&T Technologies
REM ============================================================================

title Building MBAS v2.0.7 Installer
color 0B

echo.
echo ================================================================================
echo   MBAS v2.0.7 - Build and Install
echo   Z^&T Technologies - State-of-the-Art Business Solutions
echo ================================================================================
echo.
echo This script will:
echo   1. Build the new v2.0.7 installer with all fixes
echo   2. Guide you through uninstalling the old version
echo   3. Help you install the new version
echo.
pause

REM ============================
REM Step 1: Build Installer
REM ============================
echo.
echo [Step 1/3] Building v2.0.7 Installer...
echo.

cd deployment\build_installer

if not exist "..\..\frontend\dist\index.html" (
    echo.
    echo [ERROR] Frontend not built!
    echo Please run: cd frontend ^&^& npm run build
    echo.
    pause
    exit /b 1
)

"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "MBAS_Installer_Professional_ZT_v2.0.7.iss"

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Build Complete! ✅
echo ========================================
echo.
echo Installer location:
echo   %CD%\output\MBAS_Professional_Setup_v2.0.7_ZT_Technologies.exe
echo.

REM ============================
REM Step 2: Uninstall Old Version
REM ============================
echo.
echo [Step 2/3] Uninstalling Old Version...
echo.
echo IMPORTANT: Your data will be PRESERVED!
echo   - Database location: C:\ProgramData\MBAS\data\mbas_database.db
echo   - This file will NOT be deleted
echo.
echo Please:
echo   1. Close this window after reading
echo   2. Go to: Settings -^> Apps -^> MBAS
echo   3. Click "Uninstall"
echo   4. Wait for uninstall to complete
echo   5. Come back and run the installer
echo.
pause

REM ============================
REM Step 3: Install New Version
REM ============================
echo.
echo [Step 3/3] Ready to Install v2.0.7
echo.
echo The installer is located at:
echo   %CD%\output\MBAS_Professional_Setup_v2.0.7_ZT_Technologies.exe
echo.
echo Would you like to launch it now?
echo.
pause

start "" "%CD%\output\MBAS_Professional_Setup_v2.0.7_ZT_Technologies.exe"

echo.
echo ========================================
echo   Installer Launched! ✅
echo ========================================
echo.
echo After installation completes:
echo   1. MBAS will start automatically
echo   2. Login: admin / admin123
echo   3. Go to Products -^> Add Product
echo   4. Verify categories appear in dropdown
echo   5. Verify no CMD windows flash
echo.
echo If you see any issues, check:
echo   C:\ProgramData\MBAS\logs\mbas_tray.log
echo.
pause
