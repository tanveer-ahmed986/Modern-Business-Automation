@echo off
REM ============================================================================
REM  MBAS Installation Script
REM  Z&T Technologies - State-of-the-Art Business Solutions
REM  Version 2.0.2 - Fixed: no pause, timeouts, offline support
REM ============================================================================
REM  IMPORTANT: This script is called by Inno Setup with runhidden flag.
REM  NEVER use 'pause' or any interactive command in this script.
REM ============================================================================

title MBAS Installation - Z&T Technologies

set "APPDIR=%~dp0"
set "LOGFILE=%APPDIR%install_log.txt"

echo [%date% %time%] MBAS Installation Started > "%LOGFILE%"

REM ---- Check Python ----
echo [Step 0/4] Checking Python... >> "%LOGFILE%"
python --version >> "%LOGFILE%" 2>&1
if errorlevel 1 goto :NO_PYTHON
echo [OK] Python found >> "%LOGFILE%"
goto :CREATE_VENV

:NO_PYTHON
echo [ERROR] Python not found! >> "%LOGFILE%"
echo [%date% %time%] Installation FAILED - Python not found >> "%LOGFILE%"
exit /b 1

REM ---- Create virtual environment ----
:CREATE_VENV
echo [Step 1/4] Creating virtual environment... >> "%LOGFILE%"
if exist "%APPDIR%venv" rmdir /s /q "%APPDIR%venv" >> "%LOGFILE%" 2>&1
python -m venv "%APPDIR%venv" >> "%LOGFILE%" 2>&1
if errorlevel 1 goto :VENV_FAILED
call "%APPDIR%venv\Scripts\activate.bat" >> "%LOGFILE%" 2>&1
echo [OK] Virtual environment created >> "%LOGFILE%"
goto :UPGRADE_PIP

:VENV_FAILED
echo [ERROR] Failed to create virtual environment! >> "%LOGFILE%"
exit /b 1

REM ---- Upgrade pip ----
:UPGRADE_PIP
echo [Step 2/4] Upgrading pip... >> "%LOGFILE%"
python -m pip install --upgrade pip setuptools wheel --quiet --timeout 60 >> "%LOGFILE%" 2>&1
echo [OK] pip upgrade step done >> "%LOGFILE%"
goto :CHECK_WHEELS

REM ---- Install dependencies ----
:CHECK_WHEELS
echo [Step 3/4] Installing dependencies... >> "%LOGFILE%"
if not exist "%APPDIR%wheels" goto :ONLINE_INSTALL

REM Offline install from bundled wheels
echo [INFO] Found bundled packages, installing offline... >> "%LOGFILE%"
python -m pip install --no-index --find-links "%APPDIR%wheels" -r "%APPDIR%backend\requirements.txt" --timeout 120 >> "%LOGFILE%" 2>&1
if errorlevel 1 goto :ONLINE_INSTALL
echo [OK] Dependencies installed from bundled packages >> "%LOGFILE%"
goto :INIT_DB

:ONLINE_INSTALL
echo [INFO] Trying online install... >> "%LOGFILE%"
python -m pip install -r "%APPDIR%backend\requirements.txt" --timeout 120 --retries 3 --no-input >> "%LOGFILE%" 2>&1
if errorlevel 1 goto :ONLINE_RETRY
echo [OK] Dependencies installed online >> "%LOGFILE%"
goto :INIT_DB

:ONLINE_RETRY
echo [WARN] First attempt failed, retrying... >> "%LOGFILE%"
python -m pip install -r "%APPDIR%backend\requirements.txt" --default-timeout=180 --retries 5 --no-input >> "%LOGFILE%" 2>&1
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
python -c "from src.scripts.init_db import bootstrap; bootstrap()" >> "%LOGFILE%" 2>&1
if errorlevel 1 echo [WARN] Database init had issues, will retry on first run >> "%LOGFILE%"
popd
echo [OK] Database step done >> "%LOGFILE%"

echo [%date% %time%] Installation COMPLETED successfully >> "%LOGFILE%"

REM ---- EXIT CLEANLY - NO PAUSE ----
exit /b 0
