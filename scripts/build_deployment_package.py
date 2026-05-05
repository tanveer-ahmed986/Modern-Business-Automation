"""
Build Deployment Package for MBAS
Creates a customer-ready zip file with pre-built frontend and all dependencies.
The resulting package only requires Python to be installed on the client machine.
"""

import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path
from datetime import datetime


class DeploymentBuilder:
    def __init__(self, tier="Basic"):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.deploy_dir = self.root_dir / "deployment"
        self.package_dir = self.deploy_dir / "MBAS_Package"
        self.version = "1.0.0"
        self.tier = tier

    def clean(self):
        """Remove old deployment files"""
        print("[*] Cleaning old deployment files...")
        if self.deploy_dir.exists():
            shutil.rmtree(self.deploy_dir)
        self.deploy_dir.mkdir(parents=True)
        self.package_dir.mkdir(parents=True)
        print("[+] Clean complete")

    def build_frontend(self):
        """Build React frontend to static files"""
        print("[*] Building frontend...")

        frontend_dir = self.root_dir / "frontend"
        if not frontend_dir.exists():
            print("[ERROR] Frontend directory not found!")
            return False

        # Install dependencies if needed
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print("    Installing npm dependencies...")
            result = subprocess.run(
                ["npm", "install", "--legacy-peer-deps"],
                cwd=str(frontend_dir),
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"[WARN] npm install failed: {result.stderr}")
                print("    Trying with --force...")
                result = subprocess.run(
                    ["npm", "install", "--force"],
                    cwd=str(frontend_dir),
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"[ERROR] npm install failed: {result.stderr}")
                    return False

        # Build production bundle
        print("    Running vite build...")
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=str(frontend_dir),
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"[WARN] Frontend build failed: {result.stderr}")
            print("    Trying TypeScript-skip build...")
            # Try building with skipLibCheck
            result = subprocess.run(
                ["npx", "vite", "build"],
                cwd=str(frontend_dir),
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"[ERROR] Frontend build failed completely: {result.stderr}")
                return False

        dist_dir = frontend_dir / "dist"
        if not dist_dir.exists() or not (dist_dir / "index.html").exists():
            print("[ERROR] Frontend build produced no output!")
            return False

        print("[+] Frontend built successfully")
        return True

    def copy_backend(self):
        """Copy backend Python files (excluding __pycache__, tests, dev files)"""
        print("[*] Copying backend files...")

        backend_src = self.root_dir / "backend"
        backend_dst = self.package_dir / "backend"

        # Copy source code
        if (backend_src / "src").exists():
            shutil.copytree(
                backend_src / "src",
                backend_dst / "src",
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(
                    '__pycache__', '*.pyc', '*.pyo',
                    'tests', 'test_*', '*_test.py',
                    '.pytest_cache'
                )
            )

        # Copy requirements.txt (production only - strip test deps)
        req_file = backend_src / "requirements.txt"
        if req_file.exists():
            with open(req_file, 'r') as f:
                lines = f.readlines()

            prod_lines = []
            skip_section = False
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("# Testing") or stripped.startswith("# Dev"):
                    skip_section = True
                    continue
                if skip_section and (stripped == "" or stripped.startswith("#")):
                    continue
                if skip_section and not stripped.startswith("#") and stripped:
                    if any(pkg in stripped.lower() for pkg in ['pytest', 'httpx', 'coverage']):
                        continue
                    skip_section = False
                if not skip_section and stripped and not stripped.startswith('#'):
                    # Skip commented-out packages
                    if not stripped.startswith('# '):
                        prod_lines.append(line)

            with open(backend_dst / "requirements.txt", 'w') as f:
                f.writelines(prod_lines)
        else:
            # Fallback requirements (Basic tier - no ML packages)
            with open(backend_dst / "requirements.txt", 'w') as f:
                f.write("""fastapi>=0.104.1,<1.0
pydantic>=2.5.3,<3.0
uvicorn[standard]>=0.24.0,<1.0
sqlmodel>=0.0.14,<1.0
pydantic-settings>=2.1.0,<3.0
python-jose[cryptography]>=3.3.0,<4.0
passlib>=1.7.4,<2.0
bcrypt>=3.2.0,<4.0
python-multipart>=0.0.9,<1.0
apscheduler>=3.10.4,<4.0
""")

        # Copy optional Premium requirements (ML/AI packages)
        req_premium = backend_src / "requirements-premium.txt"
        if req_premium.exists():
            shutil.copy2(req_premium, backend_dst / "requirements-premium.txt")

        # Create necessary directories
        (backend_dst / "database").mkdir(parents=True, exist_ok=True)
        (backend_dst / "backups").mkdir(parents=True, exist_ok=True)
        (backend_dst / "config").mkdir(parents=True, exist_ok=True)

        print("[+] Backend files copied")

    def copy_frontend_dist(self):
        """Copy pre-built frontend files"""
        print("[*] Copying frontend build...")

        dist_src = self.root_dir / "frontend" / "dist"
        dist_dst = self.package_dir / "frontend" / "dist"

        if dist_src.exists():
            shutil.copytree(dist_src, dist_dst, dirs_exist_ok=True)
            print("[+] Frontend build copied")
        else:
            print("[WARN] Frontend dist not found - frontend will not be served from backend")

    def copy_license_file(self):
        """Copy license file and public key"""
        print("[*] Copying license files...")

        # Copy the license template
        license_src = self.root_dir / "mbas.license"
        if license_src.exists():
            shutil.copy2(license_src, self.package_dir / "mbas.license")
            print("[+] License file copied")
        else:
            # Create a template license (will run in Basic/demo mode)
            print("    No license file found, creating template...")

        # Ensure public key is in the package
        pubkey_src = self.root_dir / "backend" / "src" / "embedded" / "public_key.pem"
        pubkey_dst = self.package_dir / "backend" / "src" / "embedded" / "public_key.pem"
        if pubkey_src.exists():
            pubkey_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(pubkey_src, pubkey_dst)
            print("[+] Public key copied")
        else:
            print("[WARN] Public key not found")

        # Copy icon file for desktop shortcut
        icon_src = self.root_dir / "tauri-app" / "src-tauri" / "icons" / "icon.ico"
        if icon_src.exists():
            shutil.copy2(icon_src, self.package_dir / "mbas_icon.ico")
            print("[+] Icon file copied")
        else:
            print("[WARN] Icon file not found")

        # Copy VBS shortcut creator
        vbs_src = self.root_dir / "scripts" / "create_shortcut.vbs"
        if vbs_src.exists():
            shutil.copy2(vbs_src, self.package_dir / "create_shortcut.vbs")
            print("[+] Shortcut creator copied")

        # Copy diagnostic tool
        diag_src = self.root_dir / "scripts" / "DIAGNOSE.bat"
        if diag_src.exists():
            shutil.copy2(diag_src, self.package_dir / "DIAGNOSE.bat")
            print("[+] Diagnostic tool copied")

        print("[+] License files handled")

    def create_startup_scripts(self):
        """Create installation and startup scripts"""
        print("[*] Creating startup scripts...")

        # --- INSTALL.bat ---
        install_script = r"""@echo off
title MBAS - Install Dependencies
color 0A

echo.
echo ================================================================
echo    MBAS - Modern Business Automation System
echo    Dependency Installation
echo ================================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.11 or higher:
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

REM Check Python version (3.11 or 3.12 recommended)
python -c "import sys; exit(0 if sys.version_info >= (3, 11) and sys.version_info < (3, 13) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [WARN] Python 3.13+ detected. We recommend Python 3.11 or 3.12 for best compatibility.
    echo        If installation fails, please install Python 3.11 or 3.12.
    echo.
    timeout /t 3 /nobreak >nul
)
echo.

echo [Step 1/4] Upgrading pip and setuptools...
python -m pip install --upgrade pip setuptools wheel --quiet
echo [OK] pip upgraded
echo.

echo [Step 2/4] Installing dependencies...
echo            This may take 1-3 minutes...
echo.
python -m pip install -r "%~dp0backend\requirements.txt" --only-binary :all: 2>nul
if errorlevel 1 (
    echo     Retrying with source builds allowed for small packages...
    python -m pip install -r "%~dp0backend\requirements.txt"
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install dependencies.
        echo         Please check your internet connection and try again.
        echo.
        pause
        exit /b 1
    )
)
echo [OK] All dependencies installed
echo.

echo [Step 3/4] Initializing database...
cd /d "%~dp0backend"
python -c "from src.scripts.init_db import bootstrap; bootstrap()"

if errorlevel 1 (
    echo [WARN] Database initialization had issues.
    echo        The database will be created automatically on first start.
)

cd /d "%~dp0"

echo.
echo [Step 4/4] Creating desktop shortcut...
if exist "%~dp0mbas_icon.ico" (
    cscript //nologo "%~dp0create_shortcut.vbs" "%~dp0START_MBAS.bat" "MBAS" "%~dp0mbas_icon.ico" >nul 2>&1
) else (
    cscript //nologo "%~dp0create_shortcut.vbs" "%~dp0START_MBAS.bat" "MBAS" >nul 2>&1
)
if errorlevel 1 (
    echo [WARN] Could not create desktop shortcut.
    echo        You can manually create a shortcut to START_MBAS.bat
) else (
    echo [OK] Desktop shortcut created!
)

echo.
echo ================================================================
echo    [OK] Installation Complete!
echo ================================================================
echo.
echo Next steps:
echo    1. Double-click the "MBAS" icon on your desktop
echo       (or double-click START_MBAS.bat in this folder)
echo    2. Your browser will open to: http://localhost:8000
echo    3. Login with: admin / admin123
echo    4. IMPORTANT: Change the admin password immediately!
echo.
pause
"""

        # --- START_MBAS.bat ---
        start_script = r"""@echo off
title MBAS - Modern Business Automation System
color 0A

echo.
echo ================================================================
echo        MBAS - Modern Business Automation System v1.0.0
echo ================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo         Please run INSTALL.bat first.
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [!] Dependencies not installed. Running installer...
    echo.
    call "%~dp0INSTALL.bat"
    if errorlevel 1 (
        echo [ERROR] Installation failed. Cannot start MBAS.
        pause
        exit /b 1
    )
)

echo [OK] Starting MBAS Server...
echo.
echo    Access MBAS at: http://localhost:8000
echo.
echo    Default Login:
echo       Username: admin
echo       Password: admin123
echo.
echo    Press Ctrl+C to stop the server.
echo    DO NOT close this window while using MBAS.
echo.
echo ================================================================
echo.

REM Wait 2 seconds then open browser
start "" /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8000"

REM Start the backend server (which also serves the frontend)
cd /d "%~dp0backend"
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000

echo.
echo MBAS has stopped.
pause
"""

        # --- STOP_MBAS.bat ---
        stop_script = r"""@echo off
title MBAS - Stop Server
color 0C

echo.
echo ================================================================
echo        Stopping MBAS Server...
echo ================================================================
echo.

REM Find and kill the MBAS uvicorn process on port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Stopping process %%a on port 8000...
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo [OK] MBAS Server stopped.
echo.
pause
"""

        # Write scripts
        with open(self.package_dir / "INSTALL.bat", 'w', newline='\r\n') as f:
            f.write(install_script)

        with open(self.package_dir / "START_MBAS.bat", 'w', newline='\r\n') as f:
            f.write(start_script)

        with open(self.package_dir / "STOP_MBAS.bat", 'w', newline='\r\n') as f:
            f.write(stop_script)

        print("[+] Startup scripts created")

    def create_readme(self):
        """Create README.txt for the deployment package"""
        print("[*] Creating README...")

        readme = f"""================================================================
   MBAS - Modern Business Automation System v{self.version}
   {self.tier} Edition
================================================================

SYSTEM REQUIREMENTS:
-------------------
  Operating System: Windows 10/11 (64-bit)
  RAM: Minimum 4 GB (8 GB recommended)
  Disk Space: 500 MB free space
  Internet: Required ONLY for first-time installation
            After setup, works 100% OFFLINE

INSTALLATION (First Time Only):
-------------------------------
  1. Install Python 3.11 or higher:
     -> Download from: https://www.python.org/downloads/
     -> Run installer
     -> CHECK "Add Python to PATH" (VERY IMPORTANT!)
     -> Complete installation

  2. Run the MBAS installer:
     -> Double-click: INSTALL.bat
     -> Wait for all dependencies to install (2-5 minutes)
     -> Done!

DAILY USAGE:
-----------
  Start: Double-click START_MBAS.bat
  Stop:  Close the server window, or double-click STOP_MBAS.bat
  Access: http://localhost:8000 (opens automatically)

FIRST LOGIN:
-----------
  Username: admin
  Password: admin123
  IMPORTANT: Change password immediately after first login!

YOUR DATA:
---------
  Database:  backend\\mbas_database.db
  Backups:   backend\\backups\\
  Config:    backend\\config\\

  To backup: Copy this entire MBAS folder to USB drive.
  To restore: Replace the folder on the new computer.
  To move: Copy folder to new computer, run INSTALL.bat, then START_MBAS.bat.

FEATURES ({self.tier} Edition):
---------------------------------
  [OK] Dashboard with real-time business metrics
  [OK] Inventory management (products, stock, categories)
  [OK] Point of Sale / Billing system
  [OK] Invoice generation (Thermal + A4 formats)
  [OK] Customer management
  [OK] Supplier management
  [OK] Purchase order management
  [OK] Sales reports and analytics
  [OK] User management (Admin, Manager, Sales roles)
  [OK] Data backup and restore

TROUBLESHOOTING:
---------------
  Problem: "Python is not installed" error
  Fix:     Install Python from python.org, check "Add to PATH"

  Problem: "Port 8000 already in use"
  Fix:     Run STOP_MBAS.bat, then try START_MBAS.bat again

  Problem: Application won't start after installation
  Fix:     Run INSTALL.bat again to reinstall dependencies

  Problem: Forgot admin password
  Fix:     Contact your system administrator or vendor

  Problem: Moving to a new computer
  Fix:     Copy entire MBAS folder, install Python, run INSTALL.bat

SUPPORT:
--------
  Email: support@yourdomain.com
  Phone: +92-XXX-XXXXXXX

================================================================
  Thank you for choosing MBAS!
  Your trusted offline business automation solution.
================================================================
"""

        with open(self.package_dir / "README.txt", 'w', encoding='utf-8') as f:
            f.write(readme)

        print("[+] README created")

    def create_zip(self):
        """Create the final zip package"""
        print("[*] Creating zip package...")

        timestamp = datetime.now().strftime("%Y%m%d")
        zip_name = f"MBAS_v{self.version}_{self.tier}_{timestamp}.zip"
        zip_path = self.deploy_dir / zip_name

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            for root, dirs, files in os.walk(self.package_dir):
                # Skip __pycache__ directories
                dirs[:] = [d for d in dirs if d != '__pycache__']
                for file in files:
                    if file.endswith(('.pyc', '.pyo')):
                        continue
                    file_path = Path(root) / file
                    arcname = Path("MBAS_Package") / file_path.relative_to(self.package_dir)
                    zipf.write(file_path, arcname)

        file_size = zip_path.stat().st_size / (1024 * 1024)
        print(f"[+] Package created: {zip_name}")
        print(f"    Size: {file_size:.1f} MB")
        print(f"    Location: {zip_path}")

        return zip_path

    def build(self):
        """Build complete deployment package"""
        print("\n" + "=" * 60)
        print(f"  MBAS Deployment Package Builder")
        print(f"  Version: {self.version} | Tier: {self.tier}")
        print("=" * 60 + "\n")

        try:
            self.clean()

            # Build frontend first (needs node_modules from source tree)
            frontend_built = self.build_frontend()
            if not frontend_built:
                print("\n[WARN] Frontend build failed!")
                print("       The package will include frontend source files instead.")
                print("       Client will need Node.js installed.\n")

            self.copy_backend()

            if frontend_built:
                self.copy_frontend_dist()
            else:
                # Fallback: copy frontend source
                print("[*] Copying frontend source as fallback...")
                frontend_src = self.root_dir / "frontend"
                frontend_dst = self.package_dir / "frontend"
                shutil.copytree(
                    frontend_src, frontend_dst,
                    dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(
                        'node_modules', 'dist', '.vite',
                        'coverage', '*.log', '.env.local'
                    )
                )

            self.copy_license_file()
            self.create_startup_scripts()
            self.create_readme()
            zip_path = self.create_zip()

            print("\n" + "=" * 60)
            print("  [OK] BUILD SUCCESSFUL!")
            print("=" * 60)
            print(f"\n  Package: {zip_path}")
            print(f"\n  Customer Installation Steps:")
            print(f"    1. Extract the zip file")
            print(f"    2. Install Python 3.11+ (python.org)")
            print(f"    3. Double-click INSTALL.bat")
            print(f"    4. Double-click START_MBAS.bat")
            print(f"    5. Login: admin / admin123")
            print("\n" + "=" * 60 + "\n")

            return True

        except Exception as e:
            print(f"\n[ERROR] BUILD FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    tier = sys.argv[1] if len(sys.argv) > 1 else "Basic"
    builder = DeploymentBuilder(tier=tier)
    success = builder.build()
    sys.exit(0 if success else 1)
