@echo off
REM ============================================================================
REM  MBAS Installation Script
REM  Z&T Technologies - State-of-the-Art Business Solutions
REM  Version 2.5.0 - All writable data in ProgramData\MBAS
REM ============================================================================
REM  IMPORTANT: This script is called by Inno Setup with runhidden flag.
REM  NEVER use 'pause' or any interactive command in this script.
REM ============================================================================

title MBAS Installation - Z^&T Technologies

set "APPDIR=%~dp0"
set "DATADIR=C:\ProgramData\MBAS"
set "VENVDIR=%DATADIR%\venv"
set "DATASUBDIR=%DATADIR%\data"
set "LOGDIR=%DATADIR%\logs"
set "LOGFILE=%LOGDIR%\install_log.txt"

REM ---- Create all ProgramData directories upfront ----
if not exist "%DATADIR%" mkdir "%DATADIR%" 2>nul
if not exist "%DATASUBDIR%" mkdir "%DATASUBDIR%" 2>nul
if not exist "%DATASUBDIR%\config" mkdir "%DATASUBDIR%\config" 2>nul
if not exist "%DATASUBDIR%\backups" mkdir "%DATASUBDIR%\backups" 2>nul
if not exist "%LOGDIR%" mkdir "%LOGDIR%" 2>nul

echo [%date% %time%] MBAS Installation Started > "%LOGFILE%"
echo [INFO] App dir: %APPDIR% >> "%LOGFILE%"
echo [INFO] Data dir: %DATADIR% >> "%LOGFILE%"
echo [INFO] Venv dir: %VENVDIR% >> "%LOGFILE%"

REM Also write a copy of the log to the app dir (readable during install wizard)
echo [%date% %time%] MBAS Installation Started > "%APPDIR%install_log.txt"
echo [INFO] Full log at: %LOGFILE% >> "%APPDIR%install_log.txt"

REM ---- Set permissions on ProgramData\MBAS so non-admin users can write ----
echo [INFO] Setting permissions on data directory... >> "%LOGFILE%"
icacls "%DATADIR%" /grant Users:(OI)(CI)M /T >nul 2>&1
echo [OK] Permissions configured >> "%LOGFILE%"

REM ---- Find the REAL system Python path ----
echo [Step 0/4] Checking Python... >> "%LOGFILE%"

set "SYSTEM_PYTHON="

REM Try 'py' launcher first (most reliable on Windows)
where py >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%i in ('py -3 -c "import sys; print(sys.executable)" 2^>nul') do set "SYSTEM_PYTHON=%%i"
)

REM Fallback: try 'python' from PATH
if not defined SYSTEM_PYTHON (
    where python >nul 2>&1
    if not errorlevel 1 (
        for /f "tokens=*" %%i in ('python -c "import sys; print(sys.executable)" 2^>nul') do set "SYSTEM_PYTHON=%%i"
    )
)

REM Fallback: check common install locations
if not defined SYSTEM_PYTHON (
    for %%P in (
        "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        "C:\Python312\python.exe"
        "C:\Python311\python.exe"
    ) do (
        if exist %%P (
            set "SYSTEM_PYTHON=%%~P"
            goto :PYTHON_FOUND
        )
    )
)

if not defined SYSTEM_PYTHON goto :NO_PYTHON

:PYTHON_FOUND
echo [OK] Python found: %SYSTEM_PYTHON% >> "%LOGFILE%"

REM ---- Verify Python stdlib is intact ----
echo [INFO] Verifying Python installation health... >> "%LOGFILE%"
for %%F in ("%SYSTEM_PYTHON%") do set "PYTHON_DIR=%%~dpF"
if not exist "%PYTHON_DIR%Lib\os.py" (
    echo [ERROR] Python standard library is MISSING or CORRUPTED! >> "%LOGFILE%"
    echo [ERROR] Expected: %PYTHON_DIR%Lib\os.py >> "%LOGFILE%"
    echo [ERROR] Please reinstall Python from https://www.python.org/downloads/ >> "%LOGFILE%"
    echo [ERROR] Choose "Repair" or uninstall and reinstall. >> "%LOGFILE%"
    exit /b 1
)
if not exist "%PYTHON_DIR%Lib\encodings\__init__.py" (
    echo [ERROR] Python 'encodings' module is MISSING! >> "%LOGFILE%"
    echo [ERROR] Please reinstall Python from https://www.python.org/downloads/ >> "%LOGFILE%"
    exit /b 1
)
echo [OK] Python installation verified >> "%LOGFILE%"
"%SYSTEM_PYTHON%" --version >> "%LOGFILE%" 2>&1
goto :CREATE_VENV

:NO_PYTHON
echo [ERROR] Python not found! >> "%LOGFILE%"
echo [%date% %time%] Installation FAILED - Python not found >> "%LOGFILE%"
exit /b 1

REM ---- Create virtual environment in ProgramData (avoids Program Files issues) ----
:CREATE_VENV
echo [Step 1/4] Creating virtual environment... >> "%LOGFILE%"

REM Remove any existing venv
if exist "%VENVDIR%" rmdir /s /q "%VENVDIR%" >> "%LOGFILE%" 2>&1

REM Remove any stale pyvenv.cfg from MBAS app dir
if exist "%APPDIR%pyvenv.cfg" del /f /q "%APPDIR%pyvenv.cfg" >> "%LOGFILE%" 2>&1

REM Get Python's home directory (to run venv creation from there)
for %%F in ("%SYSTEM_PYTHON%") do set "PYTHON_HOME=%%~dpF"

REM Create venv from Python's own directory to avoid prefix confusion
echo [INFO] Creating venv at: %VENVDIR% >> "%LOGFILE%"
echo [INFO] Running from: %PYTHON_HOME% >> "%LOGFILE%"
pushd "%PYTHON_HOME%"
"%SYSTEM_PYTHON%" -m venv "%VENVDIR%" >> "%LOGFILE%" 2>&1
if errorlevel 1 (
    echo [WARN] Standard venv failed, trying --without-pip... >> "%LOGFILE%"
    "%SYSTEM_PYTHON%" -m venv --without-pip --clear "%VENVDIR%" >> "%LOGFILE%" 2>&1
    if errorlevel 1 (
        popd
        goto :VENV_FAILED
    )
    REM Bootstrap pip manually
    echo [INFO] Bootstrapping pip... >> "%LOGFILE%"
    "%VENVDIR%\Scripts\python.exe" -m ensurepip >> "%LOGFILE%" 2>&1
)
popd

REM Verify venv was created
if not exist "%VENVDIR%\Scripts\python.exe" goto :VENV_FAILED

REM Create a pointer file so startup scripts know where the venv is
echo %VENVDIR%> "%APPDIR%venv_path.txt"

echo [OK] Virtual environment created at %VENVDIR% >> "%LOGFILE%"
goto :UPGRADE_PIP

:VENV_FAILED
echo [ERROR] Failed to create virtual environment! >> "%LOGFILE%"
echo [INFO] System Python: %SYSTEM_PYTHON% >> "%LOGFILE%"
echo [INFO] Target venv path: %VENVDIR% >> "%LOGFILE%"
exit /b 1

REM ---- Upgrade pip ----
:UPGRADE_PIP
echo [Step 2/4] Upgrading pip... >> "%LOGFILE%"
"%VENVDIR%\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel --quiet --timeout 60 >> "%LOGFILE%" 2>&1
echo [OK] pip upgrade step done >> "%LOGFILE%"
goto :CHECK_WHEELS

REM ---- Install dependencies ----
:CHECK_WHEELS
echo [Step 3/4] Installing dependencies... >> "%LOGFILE%"
if not exist "%APPDIR%wheels" goto :ONLINE_INSTALL

REM Offline install from bundled wheels
echo [INFO] Found bundled packages, installing offline... >> "%LOGFILE%"
"%VENVDIR%\Scripts\python.exe" -m pip install --no-index --find-links "%APPDIR%wheels" -r "%APPDIR%backend\requirements.txt" --timeout 120 >> "%LOGFILE%" 2>&1
if errorlevel 1 goto :ONLINE_INSTALL
echo [OK] Dependencies installed from bundled packages >> "%LOGFILE%"
goto :INIT_DB

:ONLINE_INSTALL
echo [INFO] Trying online install... >> "%LOGFILE%"
"%VENVDIR%\Scripts\python.exe" -m pip install -r "%APPDIR%backend\requirements.txt" --timeout 120 --retries 3 --no-input >> "%LOGFILE%" 2>&1
if errorlevel 1 goto :ONLINE_RETRY
echo [OK] Dependencies installed online >> "%LOGFILE%"
goto :INIT_DB

:ONLINE_RETRY
echo [WARN] First attempt failed, retrying... >> "%LOGFILE%"
"%VENVDIR%\Scripts\python.exe" -m pip install -r "%APPDIR%backend\requirements.txt" --default-timeout=180 --retries 5 --no-input >> "%LOGFILE%" 2>&1
if errorlevel 1 goto :DEPS_FAILED
echo [OK] Dependencies installed on retry >> "%LOGFILE%"
goto :INIT_DB

:DEPS_FAILED
echo [ERROR] Failed to install dependencies! >> "%LOGFILE%"
echo [%date% %time%] Installation FAILED - pip install error >> "%LOGFILE%"
exit /b 1

REM ---- Initialize database ----
:INIT_DB
echo [Step 4/4] Initializing database... >> "%LOGFILE%"
pushd "%APPDIR%backend"
"%VENVDIR%\Scripts\python.exe" -c "from src.scripts.init_db import bootstrap; bootstrap()" >> "%LOGFILE%" 2>&1
if errorlevel 1 echo [WARN] Database init had issues, will retry on first run >> "%LOGFILE%"
popd
echo [OK] Database step done >> "%LOGFILE%"

echo [INFO] Database location: %DATASUBDIR%\mbas_database.db >> "%LOGFILE%"
echo [INFO] Log files location: %LOGDIR% >> "%LOGFILE%"
echo [%date% %time%] Installation COMPLETED successfully >> "%LOGFILE%"

REM Update the app-dir copy too
echo [%date% %time%] Installation COMPLETED successfully >> "%APPDIR%install_log.txt"
echo [INFO] Full log at: %LOGFILE% >> "%APPDIR%install_log.txt"

REM ---- EXIT CLEANLY - NO PAUSE ----
exit /b 0
