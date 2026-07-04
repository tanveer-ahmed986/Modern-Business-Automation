@echo off
REM ============================================================================
REM  MBAS Professional Launcher (Fallback)
REM  Z&T Technologies - State-of-the-Art Business Solutions
REM  Version 2.5.0 - All runtime data in ProgramData
REM  NOTE: Prefer using START_MBAS.vbs for zero CMD window flash
REM ============================================================================

cd /d "%~dp0"

set "APPDIR=%~dp0"
set "DATADIR=C:\ProgramData\MBAS"
set "VENVDIR=%DATADIR%\venv"
set "LOGDIR=%DATADIR%\logs"
set "LOGFILE=%LOGDIR%\mbas_startup.log"

REM Ensure log directory exists
if not exist "%LOGDIR%" mkdir "%LOGDIR%" 2>nul

echo [%date% %time%] MBAS Startup initiated (BAT launcher) >> "%LOGFILE%"

REM ---- Check 1: Virtual environment ----
if not exist "%VENVDIR%\Scripts\pythonw.exe" (
    if not exist "%VENVDIR%\Scripts\python.exe" (
        echo [%date% %time%] Venv missing - running auto-repair >> "%LOGFILE%"
        if exist "%APPDIR%INSTALL_MBAS.bat" (
            REM Need admin for installation - elevate just the installer
            start "MBAS Setup" /wait cmd /c "title MBAS - Setting up environment... & color 0E & echo. & echo   MBAS is setting up the environment for first use... & echo   This may take 2-5 minutes, please wait... & echo. & call "%APPDIR%INSTALL_MBAS.bat" & echo. & echo   Setup complete! MBAS will start now... & timeout /t 2 /nobreak >nul"
        )
        if not exist "%VENVDIR%\Scripts\python.exe" (
            echo [%date% %time%] Venv creation failed >> "%LOGFILE%"
            powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('MBAS cannot start: Virtual environment not found.`n`nPlease run INSTALL_MBAS.bat as Administrator.`n`nCheck log: %LOGDIR%\install_log.txt', 'MBAS - Setup Error', 'OK', 'Error')"
            exit /b 1
        )
    )
)

REM ---- Check 2: Key files exist ----
if not exist "%APPDIR%scripts\mbas_tray.py" (
    powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('MBAS application files are missing.`n`nPlease reinstall MBAS.', 'MBAS Error', 'OK', 'Error')"
    exit /b 1
)

if not exist "%APPDIR%backend\src\main.py" (
    powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('MBAS backend files are missing.`n`nPlease reinstall MBAS.', 'MBAS Error', 'OK', 'Error')"
    exit /b 1
)

REM ---- Launch tray app silently (no CMD window) ----
echo [%date% %time%] Launching tray app >> "%LOGFILE%"

if exist "%VENVDIR%\Scripts\pythonw.exe" (
    start "" "%VENVDIR%\Scripts\pythonw.exe" "%APPDIR%scripts\mbas_tray.py"
) else (
    start "" "%VENVDIR%\Scripts\python.exe" "%APPDIR%scripts\mbas_tray.py"
)

echo [%date% %time%] Tray app launched >> "%LOGFILE%"
exit /b 0
