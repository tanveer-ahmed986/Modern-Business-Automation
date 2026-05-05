"""
Create isolated virtual environment installer for MBAS deployment.
Follows DevOps best practices for reproducible, portable installations.
"""

import os
import sys
import subprocess
from pathlib import Path


def create_venv_install_bat():
    """Generate INSTALL.bat with virtual environment isolation"""

    install_script = r'''@echo off
title MBAS - Installation
color 0A
setlocal enabledelayedexpansion

echo.
echo ================================================================
echo    MBAS - Modern Business Automation System
echo    Installation with Virtual Environment Isolation
echo ================================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.11 or 3.12:
    echo    1. Download from: https://www.python.org/downloads/
    echo    2. Run the installer
    echo    3. IMPORTANT: Check "Add Python to PATH"
    echo    4. Restart this script after installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

REM Check Python version (3.11 or 3.12 ONLY - 3.13 has compatibility issues)
python -c "import sys; v=sys.version_info; exit(0 if (v.major==3 and 11<=v.minor<=12) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Incompatible Python version detected!
    echo.
    echo MBAS requires Python 3.11 or 3.12 for maximum compatibility.
    echo Python 3.13+ has known issues with bcrypt and other packages.
    echo.
    echo Please install Python 3.11 or 3.12 from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo [OK] Python version compatible
echo.

REM Remove old virtual environment if exists
if exist "%~dp0venv" (
    echo [*] Removing old virtual environment...
    rmdir /s /q "%~dp0venv"
)

echo [Step 1/5] Creating isolated virtual environment...
python -m venv "%~dp0venv"
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment!
    echo.
    pause
    exit /b 1
)
echo [OK] Virtual environment created
echo.

echo [Step 2/5] Activating virtual environment...
call "%~dp0venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

echo [Step 3/5] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel --quiet
if errorlevel 1 (
    echo [WARN] Failed to upgrade pip, continuing anyway...
)
echo [OK] Package managers upgraded
echo.

echo [Step 4/5] Installing dependencies (this may take 2-4 minutes)...
echo.
echo     [*] Installing core packages...
python -m pip install --no-cache-dir -r "%~dp0backend\requirements.txt"
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies!
    echo.
    echo Common fixes:
    echo   1. Check your internet connection
    echo   2. Make sure you're using Python 3.11 or 3.12
    echo   3. Try running as Administrator
    echo   4. Disable antivirus temporarily
    echo.
    pause
    exit /b 1
)
echo [OK] All dependencies installed
echo.

echo [Step 5/5] Initializing database and creating shortcuts...
cd /d "%~dp0backend"
python -c "from src.scripts.init_db import bootstrap; bootstrap()"
if errorlevel 1 (
    echo [WARN] Database initialization had issues.
    echo        The database will be created on first start.
)
cd /d "%~dp0"

REM Create desktop shortcut
if exist "%~dp0mbas_icon.ico" (
    cscript //nologo "%~dp0create_shortcut.vbs" "%~dp0START_MBAS.bat" "MBAS" "%~dp0mbas_icon.ico" >nul 2>&1
) else (
    cscript //nologo "%~dp0create_shortcut.vbs" "%~dp0START_MBAS.bat" "MBAS" >nul 2>&1
)
if not errorlevel 1 (
    echo [OK] Desktop shortcut created
)

echo.
echo ================================================================
echo    [SUCCESS] Installation Complete!
echo ================================================================
echo.
echo MBAS is now installed in an isolated virtual environment.
echo This prevents conflicts with other Python packages on your system.
echo.
echo Next steps:
echo    1. Double-click the "MBAS" icon on your desktop
echo       (or run START_MBAS.bat in this folder)
echo    2. Browser will open to: http://localhost:8000
echo    3. Login: admin / admin123
echo    4. IMPORTANT: Change the password immediately!
echo.
echo Technical details:
echo    - Virtual environment: %~dp0venv
echo    - Backend: %~dp0backend
echo    - Database: %~dp0backend\mbas_database.db
echo.
pause
'''

    return install_script


def create_venv_start_bat():
    """Generate START_MBAS.bat that uses virtual environment"""

    start_script = r'''@echo off
title MBAS Server
color 0B

REM Check if virtual environment exists
if not exist "%~dp0venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run INSTALL.bat first to set up MBAS.
    echo.
    pause
    exit /b 1
)

echo [OK] Starting MBAS Server...
echo.

REM Activate virtual environment
call "%~dp0venv\Scripts\activate.bat"

REM Change to backend directory
cd /d "%~dp0backend"

REM Start FastAPI server
echo Starting backend server...
echo Server will be available at: http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the server.
echo.

REM Wait 2 seconds then open browser
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:8000"

REM Start uvicorn
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000

REM If we get here, server stopped
echo.
echo [*] Server stopped.
pause
'''

    return start_script


def create_venv_stop_bat():
    """Generate STOP_MBAS.bat to stop the server"""

    stop_script = r'''@echo off
title MBAS - Stop Server
color 0C

echo.
echo ================================================================
echo    MBAS - Stopping Server
echo ================================================================
echo.

REM Kill any Python processes running uvicorn
taskkill /F /FI "WINDOWTITLE eq MBAS Server" >nul 2>&1
taskkill /F /IM python.exe /FI "IMAGENAME eq python.exe" /FI "MEMUSAGE gt 50000" >nul 2>&1

echo [OK] All MBAS server processes stopped.
echo.
echo You can now:
echo    - Close this window
echo    - Run START_MBAS.bat to restart the server
echo    - Run INSTALL.bat to reinstall
echo.
pause
'''

    return stop_script


def create_requirements_lock():
    """Generate requirements-lock.txt with exact versions for reproducibility"""

    requirements_lock = '''# MBAS Production Dependencies - Locked Versions
# Generated for Python 3.11/3.12 compatibility
# DO NOT MODIFY - Use requirements.txt for development

# Core Framework
fastapi==0.115.5
pydantic==2.10.3
pydantic-core==2.27.2
pydantic-settings==2.7.0
uvicorn[standard]==0.34.0

# Database
sqlmodel==0.0.22
sqlalchemy==2.0.36

# Authentication & Security
python-jose[cryptography]==3.3.0
cryptography==44.0.0
passlib==1.7.4
bcrypt==3.2.2
python-multipart==0.0.20

# Utilities
apscheduler==3.10.4
typing-extensions==4.12.2

# Uvicorn Standard Dependencies
httptools==0.6.4
uvloop==0.21.0; sys_platform != 'win32'
watchfiles==1.0.3
websockets==14.1
'''

    return requirements_lock


def create_health_check_script():
    """Generate health check script to verify installation"""

    health_check = r'''@echo off
title MBAS - Health Check
color 0E

echo.
echo ================================================================
echo    MBAS - Installation Health Check
echo ================================================================
echo.

REM Check virtual environment
if not exist "%~dp0venv" (
    echo [X] Virtual environment NOT found
    echo     Run INSTALL.bat first
    goto :FAILED
) else (
    echo [OK] Virtual environment exists
)

REM Activate venv and check Python
call "%~dp0venv\Scripts\activate.bat" >nul 2>&1
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python NOT accessible in venv
    goto :FAILED
) else (
    echo [OK] Python accessible:
    python --version
)

REM Check key packages
echo.
echo [*] Checking installed packages...
python -c "import fastapi; print(f'[OK] FastAPI {fastapi.__version__}')"
if errorlevel 1 goto :FAILED

python -c "import uvicorn; print(f'[OK] Uvicorn {uvicorn.__version__}')"
if errorlevel 1 goto :FAILED

python -c "import sqlmodel; print('[OK] SQLModel installed')"
if errorlevel 1 goto :FAILED

python -c "import pydantic; print(f'[OK] Pydantic {pydantic.__version__}')"
if errorlevel 1 goto :FAILED

REM Check backend files
echo.
if exist "%~dp0backend\src\main.py" (
    echo [OK] Backend source files found
) else (
    echo [X] Backend files NOT found
    goto :FAILED
)

REM Check frontend
if exist "%~dp0frontend\dist\index.html" (
    echo [OK] Frontend build found
) else (
    echo [X] Frontend NOT found
    goto :FAILED
)

REM Check database
if exist "%~dp0backend\mbas_database.db" (
    echo [OK] Database exists
) else (
    echo [!] Database NOT found (will be created on first start)
)

REM Check port availability
netstat -an | findstr ":8000" >nul 2>&1
if not errorlevel 1 (
    echo [!] Port 8000 is IN USE
    echo     Run STOP_MBAS.bat if server is running
) else (
    echo [OK] Port 8000 available
)

echo.
echo ================================================================
echo    [SUCCESS] Health Check Passed!
echo ================================================================
echo.
echo Your MBAS installation is ready to use.
echo.
echo To start MBAS:
echo    1. Run START_MBAS.bat (or double-click desktop icon)
echo    2. Wait for "Uvicorn running..." message
echo    3. Browser will open automatically
echo    4. Login: admin / admin123
echo.
pause
exit /b 0

:FAILED
echo.
echo ================================================================
echo    [FAILED] Health Check Failed
echo ================================================================
echo.
echo Please run INSTALL.bat to fix the installation.
echo.
pause
exit /b 1
'''

    return health_check


if __name__ == "__main__":
    print("Creating virtual environment installer scripts...")

    root = Path(__file__).resolve().parent.parent
    output_dir = root / "deployment" / "venv_scripts"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create scripts
    scripts = {
        "INSTALL_VENV.bat": create_venv_install_bat(),
        "START_VENV.bat": create_venv_start_bat(),
        "STOP_VENV.bat": create_venv_stop_bat(),
        "HEALTH_CHECK.bat": create_health_check_script(),
    }

    for filename, content in scripts.items():
        filepath = output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[+] Created: {filepath}")

    # Create requirements-lock.txt
    lock_file = root / "backend" / "requirements-lock.txt"
    with open(lock_file, 'w', encoding='utf-8') as f:
        f.write(create_requirements_lock())
    print(f"[+] Created: {lock_file}")

    print("\n[SUCCESS] Virtual environment installer created!")
    print("\nFiles created:")
    print("  - deployment/venv_scripts/INSTALL_VENV.bat")
    print("  - deployment/venv_scripts/START_VENV.bat")
    print("  - deployment/venv_scripts/STOP_VENV.bat")
    print("  - deployment/venv_scripts/HEALTH_CHECK.bat")
    print("  - backend/requirements-lock.txt")
