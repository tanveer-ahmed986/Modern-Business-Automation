@echo off
title Building MBAS Launchers - Z&T Technologies
color 0B

echo.
echo ================================================================================
echo    Building MBAS Professional Launchers
echo    Z^&T Technologies - www.zttechnologies.org
echo ================================================================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [*] Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [FAIL] Failed to install PyInstaller!
        pause
        exit /b 1
    )
)

echo [Step 1/2] Building main launcher (MBAS.exe)...
pyinstaller --onefile --windowed ^
    --icon=..\branding\mbas_icon.ico ^
    --name=MBAS ^
    --version-file=version_info.txt ^
    mbas_launcher.py

if errorlevel 1 (
    echo [FAIL] Failed to build MBAS.exe
    pause
    exit /b 1
)

echo [Step 2/2] Building tray launcher (MBAS_Tray.exe)...
pyinstaller --onefile --windowed ^
    --icon=..\branding\mbas_icon.ico ^
    --name=MBAS_Tray ^
    --version-file=version_info.txt ^
    mbas_tray_launcher.py

if errorlevel 1 (
    echo [FAIL] Failed to build MBAS_Tray.exe
    pause
    exit /b 1
)

REM Clean up build files
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

echo.
echo ================================================================================
echo    [SUCCESS] Launchers Built!
echo ================================================================================
echo.
echo Created files:
dir dist\*.exe /B
echo.
echo File sizes:
dir dist\*.exe | findstr ".exe"
echo.
pause
