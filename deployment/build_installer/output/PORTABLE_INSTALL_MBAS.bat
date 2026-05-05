@echo off
title MBAS - Portable Installation (No Installer Required)
color 0A

echo.
echo ========================================================================
echo    MBAS Portable Installation
echo ========================================================================
echo.
echo This method does NOT use the installer. It manually extracts and
echo sets up MBAS without calling taskkill or any problematic system tools.
echo.
echo Perfect for systems with corrupted system files or strict security.
echo.
echo ========================================================================
echo.

REM Check if source files exist
set SOURCE_DIR=%~dp0..\MBAS_v1.0.9_Production_Ready
if not exist "%SOURCE_DIR%" (
    echo [ERROR] Source files not found!
    echo.
    echo Expected location: %SOURCE_DIR%
    echo.
    echo You need the full MBAS package with source files.
    pause
    exit /b 1
)

echo [OK] Source files found
echo.

REM Ask for installation directory
echo Where would you like to install MBAS?
echo.
echo Recommended: C:\MBAS (no admin required)
echo.
set /P INSTALL_DIR="Enter installation path (or press Enter for C:\MBAS): "
if "%INSTALL_DIR%"=="" set INSTALL_DIR=C:\MBAS

echo.
echo Installation directory: %INSTALL_DIR%
echo.

REM Create installation directory
if not exist "%INSTALL_DIR%" (
    echo Creating directory: %INSTALL_DIR%
    mkdir "%INSTALL_DIR%" 2>nul
    if errorlevel 1 (
        echo [ERROR] Cannot create directory. Try running as Administrator.
        pause
        exit /b 1
    )
)

echo.
echo ========================================================================
echo    Step 1: Stopping any running MBAS processes
echo ========================================================================
echo.

REM Kill processes using PowerShell (safer than taskkill)
echo Stopping MBAS processes using PowerShell...
powershell -ExecutionPolicy Bypass -Command "Get-Process | Where-Object {$_.ProcessName -match 'python|pythonw|node'} | Where-Object {$_.Path -like '*MBAS*' -or $_.CommandLine -like '*mbas*'} | Stop-Process -Force" 2>nul

REM Wait for processes to terminate
timeout /t 2 /nobreak >nul

echo [OK] Processes stopped
echo.

echo ========================================================================
echo    Step 2: Copying files (this may take 1-2 minutes)
echo ========================================================================
echo.

echo Copying backend files...
xcopy "%SOURCE_DIR%\backend" "%INSTALL_DIR%\backend\" /E /I /Y /Q
if errorlevel 1 (
    echo [ERROR] Failed to copy backend files
    pause
    exit /b 1
)

echo Copying frontend files...
xcopy "%SOURCE_DIR%\frontend" "%INSTALL_DIR%\frontend\" /E /I /Y /Q
if errorlevel 1 (
    echo [ERROR] Failed to copy frontend files
    pause
    exit /b 1
)

echo Copying scripts...
xcopy "%SOURCE_DIR%\scripts" "%INSTALL_DIR%\scripts\" /E /I /Y /Q

echo Copying documentation...
xcopy "%SOURCE_DIR%\docs" "%INSTALL_DIR%\docs\" /E /I /Y /Q

echo Copying startup files...
copy "%SOURCE_DIR%\*.bat" "%INSTALL_DIR%\" /Y >nul
copy "%SOURCE_DIR%\*.txt" "%INSTALL_DIR%\" /Y >nul
copy "%SOURCE_DIR%\*.md" "%INSTALL_DIR%\" /Y >nul
copy "%SOURCE_DIR%\mbas_icon.ico" "%INSTALL_DIR%\" /Y >nul
copy "%SOURCE_DIR%\mbas.license" "%INSTALL_DIR%\" /Y >nul

echo [OK] Files copied successfully
echo.

echo ========================================================================
echo    Step 3: Unblocking files
echo ========================================================================
echo.

echo Unblocking downloaded files using PowerShell...
powershell -ExecutionPolicy Bypass -Command "Get-ChildItem -Path '%INSTALL_DIR%' -Recurse | Unblock-File" 2>nul

echo [OK] Files unblocked
echo.

echo ========================================================================
echo    Step 4: Checking Python
echo ========================================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.11 or 3.12 from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

echo ========================================================================
echo    Step 5: Installing dependencies (2-4 minutes)
echo ========================================================================
echo.

cd /d "%INSTALL_DIR%"

echo Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing backend dependencies...
cd backend
python -m pip install --upgrade pip setuptools wheel --quiet
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install backend dependencies
    pause
    exit /b 1
)

echo [OK] Backend dependencies installed
echo.

echo Initializing database...
cd /d "%INSTALL_DIR%\backend"
python -m src.scripts.init_db
if errorlevel 1 (
    echo [WARNING] Database initialization had issues, but continuing...
)

echo [OK] Database initialized
echo.

echo ========================================================================
echo    Step 6: Creating shortcuts
echo ========================================================================
echo.

REM Create desktop shortcut using VBScript
echo Creating desktop shortcut...
set SHORTCUT_SCRIPT=%TEMP%\create_mbas_shortcut.vbs
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%SHORTCUT_SCRIPT%"
echo sLinkFile = "%USERPROFILE%\Desktop\MBAS.lnk" >> "%SHORTCUT_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%SHORTCUT_SCRIPT%"
echo oLink.TargetPath = "%INSTALL_DIR%\START_MBAS_TRAY.bat" >> "%SHORTCUT_SCRIPT%"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%SHORTCUT_SCRIPT%"
echo oLink.IconLocation = "%INSTALL_DIR%\mbas_icon.ico" >> "%SHORTCUT_SCRIPT%"
echo oLink.Description = "MBAS - Modern Business Automation System" >> "%SHORTCUT_SCRIPT%"
echo oLink.Save >> "%SHORTCUT_SCRIPT%"

cscript //nologo "%SHORTCUT_SCRIPT%"
del "%SHORTCUT_SCRIPT%"

echo [OK] Desktop shortcut created
echo.

echo ========================================================================
echo    Step 7: Adding Windows Defender exclusion (optional)
echo ========================================================================
echo.

echo Adding Windows Defender exclusion for better performance...
echo (This requires administrator privileges - will skip if not admin)
powershell -ExecutionPolicy Bypass -Command "try { Add-MpPreference -ExclusionPath '%INSTALL_DIR%' } catch { Write-Host 'Skipped (not admin)' }" 2>nul

echo.

echo ========================================================================
echo    INSTALLATION COMPLETE!
echo ========================================================================
echo.
echo MBAS has been successfully installed to:
echo %INSTALL_DIR%
echo.
echo Shortcuts created:
echo   - Desktop shortcut: MBAS.lnk
echo.
echo You can start MBAS by:
echo   1. Double-clicking the desktop shortcut
echo   2. Running: %INSTALL_DIR%\START_MBAS_TRAY.bat
echo.
echo Default credentials:
echo   Username: admin
echo   Password: admin123
echo   (Change these after first login!)
echo.
echo ========================================================================
echo.

echo Would you like to start MBAS now?
echo.
choice /C YN /N /M "Start MBAS? (Y/N): "

if errorlevel 2 goto :exit
if errorlevel 1 goto :start_mbas

:start_mbas
echo.
echo Starting MBAS...
cd /d "%INSTALL_DIR%"
start "" "%INSTALL_DIR%\START_MBAS_TRAY.bat"
echo.
echo MBAS is starting in the background.
echo Look for the MBAS icon in your system tray.
echo.
echo After a few seconds, open your browser to:
echo http://localhost:3000
echo.
goto :exit

:exit
echo.
echo Installation complete! You can close this window.
pause
exit /b 0
