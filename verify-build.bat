@echo off
REM ============================================
REM  MBAS Build Verification Script
REM  Verifies the build output and installer
REM ============================================

echo.
echo ============================================
echo   MBAS Build Verification
echo ============================================
echo.

set ERROR_COUNT=0

REM Check backend binary
echo [1/6] Checking backend binary...
if exist backend\build\mbas-backend.exe (
    echo [OK] Backend binary exists
    for %%f in (backend\build\mbas-backend.exe) do echo       Size: %%~zf bytes
) else (
    echo [FAIL] Backend binary not found
    set /a ERROR_COUNT+=1
)
echo.

REM Check frontend build
echo [2/6] Checking frontend build...
if exist frontend\dist\index.html (
    echo [OK] Frontend built
    dir /s /b frontend\dist\*.js | find /c ".js" > temp_count.txt
    set /p JS_COUNT=<temp_count.txt
    del temp_count.txt
    echo       JS files: !JS_COUNT!
) else (
    echo [FAIL] Frontend build not found
    set /a ERROR_COUNT+=1
)
echo.

REM Check Tauri binaries directory
echo [3/6] Checking Tauri binaries...
if exist tauri-app\src-tauri\binaries\mbas-backend.exe (
    echo [OK] Backend copied to Tauri binaries
) else (
    echo [FAIL] Backend not found in Tauri binaries
    set /a ERROR_COUNT+=1
)
echo.

REM Check Tauri build output
echo [4/6] Checking Tauri build output...
if exist tauri-app\src-tauri\target\release\bundle\msi (
    echo [OK] Tauri MSI bundle directory exists
    dir /b tauri-app\src-tauri\target\release\bundle\msi\*.msi 2>nul
    if %errorlevel% equ 0 (
        echo [OK] MSI installer found:
        for %%f in (tauri-app\src-tauri\target\release\bundle\msi\*.msi) do (
            echo       - %%~nxf
            echo         Size: %%~zf bytes (%%~zf / 1048576 = approx. %%~zf MB)
        )
    ) else (
        echo [FAIL] No MSI installer found
        set /a ERROR_COUNT+=1
    )
) else (
    echo [FAIL] Tauri MSI bundle directory not found
    set /a ERROR_COUNT+=1
)
echo.

REM Check license file
echo [5/6] Checking license file...
if exist mbas.license (
    echo [OK] License file exists
) else (
    echo [WARNING] No license file in root (customers will need one)
)
echo.

REM Check test license
echo [6/6] Checking test license...
if exist tools\test-store-premium.mbas-license (
    echo [OK] Test license exists for testing
) else (
    echo [WARNING] No test license found
)
echo.

REM Summary
echo ============================================
if %ERROR_COUNT% equ 0 (
    echo   VERIFICATION PASSED!
    echo ============================================
    echo.
    echo All build artifacts are present and valid.
    echo.
    echo Deployment checklist:
    echo   [x] Backend compiled
    echo   [x] Frontend built
    echo   [x] Tauri installer created
    echo   [ ] Test installer on clean Windows machine
    echo   [ ] Create customer license files
    echo   [ ] Package installer + license for distribution
    echo.
) else (
    echo   VERIFICATION FAILED!
    echo ============================================
    echo.
    echo Errors found: %ERROR_COUNT%
    echo Please review the output above and rebuild.
    echo.
)

pause
