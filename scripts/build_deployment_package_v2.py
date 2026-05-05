"""
Enhanced Deployment Package Builder for MBAS v2.0
Follows DevOps best practices with virtual environment isolation.
Creates production-ready, reproducible, portable deployment packages.
"""

import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path
from datetime import datetime


class DeploymentBuilderV2:
    def __init__(self, tier="Basic"):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.deploy_dir = self.root_dir / "deployment"
        self.package_dir = self.deploy_dir / "MBAS_Package_V2"
        self.version = "1.0.7"
        self.tier = tier
        self.date_str = datetime.now().strftime("%Y%m%d")

    def clean(self):
        """Remove old deployment files"""
        print("[*] Cleaning old deployment files...")
        if self.package_dir.exists():
            shutil.rmtree(self.package_dir)
        self.package_dir.mkdir(parents=True)
        print("[+] Clean complete")

    def build_frontend(self):
        """Build React frontend to static files"""
        print("[*] Building frontend...")

        frontend_dir = self.root_dir / "frontend"
        if not frontend_dir.exists():
            print("[ERROR] Frontend directory not found!")
            return False

        # Check if dist already exists and is recent
        dist_dir = frontend_dir / "dist"
        if dist_dir.exists() and (dist_dir / "index.html").exists():
            print("[+] Using existing frontend build")
            return True

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
                print(f"[WARN] npm install failed, trying with --force...")
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
            print(f"[ERROR] Frontend build failed: {result.stderr}")
            return False

        if not (dist_dir / "index.html").exists():
            print("[ERROR] Frontend build produced no output!")
            return False

        print("[+] Frontend built successfully")
        return True

    def copy_backend(self):
        """Copy backend Python files"""
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
                    '.pytest_cache', '*.db', '*.db-*'
                )
            )

        # Copy requirements.txt (filter test dependencies)
        self.copy_requirements(backend_src, backend_dst)

        # Create necessary directories
        (backend_dst / "database").mkdir(parents=True, exist_ok=True)
        (backend_dst / "backups").mkdir(parents=True, exist_ok=True)
        (backend_dst / "config").mkdir(parents=True, exist_ok=True)

        print("[+] Backend files copied")

    def copy_requirements(self, backend_src, backend_dst):
        """Copy and filter requirements files"""

        # Copy main requirements (production only)
        req_file = backend_src / "requirements.txt"
        if req_file.exists():
            with open(req_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            prod_lines = []
            skip_test_section = False

            for line in lines:
                stripped = line.strip()

                # Skip testing section
                if "# Testing" in stripped or "# Dev" in stripped:
                    skip_test_section = True
                    continue

                # Skip test packages
                if any(pkg in stripped.lower() for pkg in ['pytest', 'httpx', 'coverage']):
                    continue

                # Keep non-empty, non-test lines
                if stripped and not stripped.startswith('# Testing'):
                    if skip_test_section and stripped.startswith('#'):
                        skip_test_section = False
                    if not skip_test_section:
                        prod_lines.append(line)

            with open(backend_dst / "requirements.txt", 'w', encoding='utf-8') as f:
                f.writelines(prod_lines)

        # Copy requirements-lock.txt if exists (for reproducibility)
        lock_file = backend_src / "requirements-lock.txt"
        if lock_file.exists():
            shutil.copy2(lock_file, backend_dst / "requirements-lock.txt")
            print("    [+] Copied requirements-lock.txt for reproducible installs")

        # Copy optional Premium requirements
        req_premium = backend_src / "requirements-premium.txt"
        if req_premium.exists():
            shutil.copy2(req_premium, backend_dst / "requirements-premium.txt")

    def copy_frontend_dist(self):
        """Copy pre-built frontend files"""
        print("[*] Copying frontend build...")

        dist_src = self.root_dir / "frontend" / "dist"
        dist_dst = self.package_dir / "frontend" / "dist"

        if dist_src.exists():
            shutil.copytree(dist_src, dist_dst, dirs_exist_ok=True)
            print("[+] Frontend build copied")
        else:
            print("[ERROR] Frontend dist not found! Build frontend first.")
            return False
        return True

    def copy_assets(self):
        """Copy license, icons, and support files"""
        print("[*] Copying assets...")

        # License file
        license_src = self.root_dir / "mbas.license"
        if license_src.exists():
            shutil.copy2(license_src, self.package_dir / "mbas.license")

        # Public key for license validation
        pubkey_src = self.root_dir / "backend" / "src" / "embedded" / "public_key.pem"
        if pubkey_src.exists():
            pubkey_dst = self.package_dir / "backend" / "src" / "embedded" / "public_key.pem"
            pubkey_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(pubkey_src, pubkey_dst)

        # Desktop icon
        icon_src = self.root_dir / "tauri-app" / "src-tauri" / "icons" / "icon.ico"
        if icon_src.exists():
            shutil.copy2(icon_src, self.package_dir / "mbas_icon.ico")

        # VBScript shortcut creator
        vbs_src = self.root_dir / "scripts" / "create_shortcut.vbs"
        if vbs_src.exists():
            shutil.copy2(vbs_src, self.package_dir / "create_shortcut.vbs")

        print("[+] Assets copied")

    def copy_venv_scripts(self):
        """Copy virtual environment installation scripts"""
        print("[*] Copying virtual environment installer...")

        venv_scripts_dir = self.root_dir / "deployment" / "venv_scripts"
        if not venv_scripts_dir.exists():
            print("[ERROR] Virtual environment scripts not found!")
            print("        Run: python scripts/create_venv_installer.py")
            return False

        # Copy INSTALL_VENV.bat as INSTALL.bat (primary installer)
        install_venv = venv_scripts_dir / "INSTALL_VENV.bat"
        if install_venv.exists():
            shutil.copy2(install_venv, self.package_dir / "INSTALL.bat")

        # Copy START_VENV.bat as START_MBAS.bat
        start_venv = venv_scripts_dir / "START_VENV.bat"
        if start_venv.exists():
            shutil.copy2(start_venv, self.package_dir / "START_MBAS.bat")

        # Copy STOP_VENV.bat as STOP_MBAS.bat
        stop_venv = venv_scripts_dir / "STOP_VENV.bat"
        if stop_venv.exists():
            shutil.copy2(stop_venv, self.package_dir / "STOP_MBAS.bat")

        # Copy HEALTH_CHECK.bat
        health_check = venv_scripts_dir / "HEALTH_CHECK.bat"
        if health_check.exists():
            shutil.copy2(health_check, self.package_dir / "HEALTH_CHECK.bat")

        print("[+] Virtual environment installer copied")
        return True

    def copy_tray_app(self):
        """Copy system tray application files"""
        print("[*] Copying system tray application...")

        scripts_src = self.root_dir / "scripts"
        scripts_dst = self.package_dir / "scripts"
        scripts_dst.mkdir(parents=True, exist_ok=True)

        # Copy tray application files
        tray_py = scripts_src / "mbas_tray.py"
        if tray_py.exists():
            shutil.copy2(tray_py, scripts_dst / "mbas_tray.py")
            print("    [+] Copied mbas_tray.py")

        tray_bat = scripts_src / "START_MBAS_TRAY.bat"
        if tray_bat.exists():
            shutil.copy2(tray_bat, scripts_dst / "START_MBAS_TRAY.bat")
            print("    [+] Copied START_MBAS_TRAY.bat")

        # Also copy to root for easy access
        if tray_bat.exists():
            shutil.copy2(tray_bat, self.package_dir / "START_MBAS_TRAY.bat")
            print("    [+] Copied START_MBAS_TRAY.bat to package root")

        print("[+] System tray application copied")
        return True

    def create_readme(self):
        """Create comprehensive README"""
        print("[*] Creating README...")

        readme = f"""================================================================
   MBAS - Modern Business Automation System v{self.version}
   {self.tier} Edition - DevOps-Grade Deployment
================================================================

WHAT'S NEW IN v{self.version}:
---------------------------
  ✓ Background Service Mode (No visible CMD window!)
  ✓ System Tray Integration (Start/Stop from taskbar)
  ✓ Auto-Logout Security (Session cleared when browser closes)
  ✓ Enhanced Session Security (2-hour token expiry)
  ✓ Virtual Environment Isolation (No global package conflicts!)
  ✓ Reproducible Installations (Locked dependencies)
  ✓ Python 3.11/3.12 Validation (Prevents 3.13 compatibility issues)
  ✓ Health Check Tool (Verify installation integrity)

SYSTEM REQUIREMENTS:
-------------------
  Operating System: Windows 10/11 (64-bit)
  Python: 3.11 or 3.12 ONLY (NOT 3.13 - compatibility issues)
  RAM: Minimum 4 GB (8 GB recommended)
  Disk Space: 500 MB free space
  Internet: Required ONLY for first-time installation
            After setup, works 100% OFFLINE

QUICK START (Recommended):
-------------------------
  1. Extract this ZIP file to any location (e.g., C:\\MBAS)
  2. Double-click INSTALL.bat
  3. Wait for installation to complete (2-4 minutes)
  4. Double-click "MBAS" icon on desktop (or START_MBAS.bat)
  5. Login: admin / admin123
  6. CHANGE PASSWORD IMMEDIATELY!

INSTALLATION DETAILS:
--------------------
  INSTALL.bat creates an isolated Python virtual environment.
  This prevents conflicts with other Python software on your computer.
  All dependencies are installed in: [MBAS]\\venv\\

  If installation fails:
  - Make sure you have Python 3.11 or 3.12
  - Check your internet connection
  - Run as Administrator
  - Run HEALTH_CHECK.bat to diagnose issues

VERIFICATION:
------------
  After installation, run HEALTH_CHECK.bat to verify:
  ✓ Virtual environment created
  ✓ Python accessible
  ✓ All packages installed
  ✓ Backend files present
  ✓ Frontend build present
  ✓ Port 8000 available
  ✓ Database ready

STARTING MBAS:
-------------
  Method 1 (RECOMMENDED): Background Mode with System Tray
    - Double-click START_MBAS_TRAY.bat
    - MBAS runs in background (no CMD window)
    - System tray icon appears in taskbar (bottom-right)
    - Right-click icon to Open MBAS, Start/Stop Server, or Exit

  Method 2: Standard Mode (CMD window visible)
    - Double-click "MBAS" desktop icon
    - Or double-click START_MBAS.bat in this folder
    - CMD window remains visible while server runs

  Browser will open automatically to: http://localhost:8000

STOPPING MBAS:
-------------
  Background Mode:
    - Right-click system tray icon → Exit

  Standard Mode:
    - Press Ctrl+C in the MBAS window
    - Or run STOP_MBAS.bat
    - Or close the MBAS command window

SECURITY FEATURES:
-----------------
  ✓ Auto-logout when browser closes (sessionStorage)
  ✓ 2-hour token expiry for enhanced security
  ✓ Must login every time browser opens
  ✓ No persistent sessions across browser restarts

TROUBLESHOOTING:
---------------
  Problem: "Python not found"
  Solution: Install Python 3.11 or 3.12 from python.org
           Make sure to check "Add Python to PATH" during install

  Problem: "Port 8000 already in use"
  Solution: Run STOP_MBAS.bat first, or change port in backend

  Problem: "Page loading failed"
  Solution: 1. Run HEALTH_CHECK.bat
           2. Check if backend is running (should see Uvicorn logs)
           3. Try http://127.0.0.1:8000 instead

  Problem: "Virtual environment not found"
  Solution: Re-run INSTALL.bat

  Problem: "Dependencies failed to install"
  Solution: 1. Verify Python 3.11 or 3.12 (NOT 3.13)
           2. Check internet connection
           3. Try running as Administrator
           4. Temporarily disable antivirus

TECHNICAL ARCHITECTURE:
----------------------
  Frontend: React 18 + TypeScript + Vite (Pre-built)
  Backend: FastAPI + Python + SQLModel ORM
  Database: SQLite with FTS5 full-text search
  Server: Uvicorn ASGI server
  Isolation: Python virtual environment (venv)

FILE STRUCTURE:
--------------
  MBAS_Package_V2/
  ├── INSTALL.bat           # Installer (creates venv)
  ├── START_MBAS.bat        # Start server (standard mode)
  ├── START_MBAS_TRAY.bat   # Start server (background mode with tray icon)
  ├── STOP_MBAS.bat         # Stop server
  ├── HEALTH_CHECK.bat      # Verify installation
  ├── mbas.license          # License file
  ├── mbas_icon.ico         # Desktop icon
  ├── backend/              # FastAPI backend
  │   ├── src/             # Source code
  │   ├── requirements.txt # Production dependencies
  │   └── requirements-lock.txt  # Locked versions
  ├── frontend/dist/        # Pre-built React app
  ├── scripts/              # System tray application
  │   ├── mbas_tray.py     # System tray app
  │   └── START_MBAS_TRAY.bat  # Tray launcher
  └── venv/                # Python virtual environment (created during install)

SUPPORT:
-------
  For technical support, documentation, or feature requests,
  contact your software vendor.

================================================================
  Package built: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
  Package type: DevOps-Grade with Virtual Environment Isolation
================================================================
"""

        with open(self.package_dir / "README.txt", 'w', encoding='utf-8') as f:
            f.write(readme)

        print("[+] README created")

    def create_deployment_guide(self):
        """Create detailed deployment guide for IT administrators"""
        print("[*] Creating deployment guide...")

        guide = f"""================================================================
   MBAS v{self.version} - IT Administrator Deployment Guide
================================================================

OVERVIEW:
--------
This guide provides detailed deployment instructions for IT
administrators deploying MBAS in enterprise environments.

DEPLOYMENT ARCHITECTURE:
-----------------------
MBAS uses a virtual environment-based deployment model:
  - Isolated Python environment (no global package pollution)
  - Reproducible installations via locked dependencies
  - Portable deployment (can be moved to different locations)
  - Single-user desktop application (not multi-tenant)

PRE-DEPLOYMENT CHECKLIST:
------------------------
[ ] Python 3.11.x or 3.12.x installed on target systems
[ ] Python added to system PATH
[ ] 500 MB free disk space available
[ ] Internet connection (for initial dependency download only)
[ ] User has write permissions to installation directory
[ ] Port 8000 available (or configure custom port)
[ ] No existing Python 3.13+ (causes bcrypt compatibility issues)

INSTALLATION METHODS:
--------------------
1. INTERACTIVE INSTALLATION (Recommended for single deployments):
   - User double-clicks INSTALL.bat
   - Follows on-screen prompts
   - Desktop shortcut created automatically

2. SILENT INSTALLATION (For mass deployment via GPO/SCCM):
   Create deployment script:

   @echo off
   cd /d "%~dp0"
   python -m venv venv
   call venv\\Scripts\\activate.bat
   python -m pip install --no-cache-dir -r backend\\requirements.txt
   cd backend
   python -c "from src.scripts.init_db import bootstrap; bootstrap()"

   Deploy via Group Policy or SCCM task sequence.

3. NETWORK SHARE DEPLOYMENT:
   - Install MBAS to network share (\\\\server\\MBAS)
   - Users run START_MBAS.bat from network
   - Each user gets own database in %APPDATA%\\MBAS\\

SECURITY CONSIDERATIONS:
-----------------------
  ✓ All traffic is local (127.0.0.1 only)
  ✓ No external network connections after installation
  ✓ SQLite database with file-level permissions
  ✓ bcrypt password hashing (cost factor 12)
  ✓ JWT tokens for session management
  ✓ CORS restricted to localhost
  ✓ No telemetry or external data transmission

POST-INSTALLATION VERIFICATION:
------------------------------
1. Run HEALTH_CHECK.bat on each deployed system
2. Verify all checks pass
3. Test login with admin/admin123
4. Force password change on first login
5. Create user accounts as needed
6. Configure backup settings

BACKUP STRATEGY:
---------------
Database Location: [INSTALL_DIR]\\backend\\mbas_database.db

Recommended backup approach:
  1. Stop MBAS (STOP_MBAS.bat)
  2. Copy mbas_database.db to backup location
  3. Restart MBAS (START_MBAS.bat)

Automated backups can be configured in Settings > Backup.

UPGRADE PROCEDURE:
-----------------
To upgrade to a new version:
  1. STOP_MBAS.bat
  2. Backup mbas_database.db
  3. Copy mbas.license to safe location
  4. Extract new version to different folder
  5. Copy old mbas_database.db to new backend folder
  6. Copy mbas.license to new folder
  7. Run INSTALL.bat in new folder
  8. Verify with HEALTH_CHECK.bat
  9. START_MBAS.bat

FIREWALL CONFIGURATION:
----------------------
MBAS only listens on 127.0.0.1:8000 (localhost).
No inbound firewall rules needed.

For remote access (NOT RECOMMENDED without SSL):
  - Modify backend\\src\\main.py: Change --host to 0.0.0.0
  - Add firewall rule allowing port 8000
  - IMPORTANT: Use reverse proxy with SSL in production

TROUBLESHOOTING:
---------------
Issue: Virtual environment creation fails
Fix: Verify Python installation, check disk space, run as admin

Issue: Dependencies fail to install
Fix: Check internet, verify Python 3.11/3.12, disable antivirus temp

Issue: Database locked errors
Fix: Ensure only one instance running, check file permissions

Issue: Port 8000 in use
Fix: Run STOP_MBAS.bat, check for other services on port 8000

PERFORMANCE TUNING:
------------------
For optimal performance:
  - Install on SSD if possible
  - Ensure 8 GB RAM for databases >10,000 records
  - Consider uvicorn workers for multi-core systems:
    Modify START_MBAS.bat: --workers 2

LICENSE MANAGEMENT:
------------------
License file: mbas.license
  - Must be in same directory as INSTALL.bat
  - Validated on each startup
  - Tier determines available features:
    * Basic: Core POS and inventory
    * Standard: + Reports and analytics
    * Premium: + AI forecasting and advanced features

To deploy new license:
  1. STOP_MBAS.bat
  2. Replace mbas.license
  3. START_MBAS.bat
  4. Verify tier in Settings > System Info

TECHNICAL SUPPORT:
-----------------
For enterprise support, escalate to software vendor with:
  - HEALTH_CHECK.bat output
  - Python version (python --version)
  - Windows version
  - Error messages from console
  - Steps to reproduce issue

================================================================
   Deployment Package Built: {datetime.now().strftime("%Y-%m-%d")}
================================================================
"""

        with open(self.package_dir / "DEPLOYMENT_GUIDE.txt", 'w', encoding='utf-8') as f:
            f.write(guide)

        print("[+] Deployment guide created")

    def create_zip(self):
        """Create deployment ZIP file"""
        print("[*] Creating deployment ZIP...")

        zip_name = f"MBAS_v{self.version}_{self.tier}_{self.date_str}_DevOps.zip"
        zip_path = self.deploy_dir / zip_name

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.package_dir):
                # Skip venv directory if it exists
                if 'venv' in dirs:
                    dirs.remove('venv')
                if '__pycache__' in dirs:
                    dirs.remove('__pycache__')

                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(self.package_dir.parent)
                    zipf.write(file_path, arcname)

        print(f"[+] ZIP created: {zip_path}")
        print(f"    Size: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")
        return zip_path

    def build_all(self):
        """Execute complete build process"""
        print("="*70)
        print(f"   MBAS v{self.version} DevOps-Grade Deployment Builder")
        print("="*70)
        print(f"Tier: {self.tier}")
        print(f"Date: {self.date_str}")
        print(f"Output: {self.package_dir}")
        print("="*70)
        print()

        steps = [
            ("Cleaning old files", self.clean),
            ("Building frontend", self.build_frontend),
            ("Copying backend", self.copy_backend),
            ("Copying frontend dist", self.copy_frontend_dist),
            ("Copying assets", self.copy_assets),
            ("Copying virtual environment installer", self.copy_venv_scripts),
            ("Copying system tray application", self.copy_tray_app),
            ("Creating README", self.create_readme),
            ("Creating deployment guide", self.create_deployment_guide),
            ("Creating ZIP package", self.create_zip),
        ]

        for step_name, step_func in steps:
            print(f"\n{'='*70}")
            print(f"STEP: {step_name}")
            print(f"{'='*70}")
            result = step_func()
            if result is False:
                print(f"\n[ERROR] Build failed at: {step_name}")
                return False

        print("\n" + "="*70)
        print("   BUILD COMPLETE!")
        print("="*70)
        print("\nDeployment package created successfully!")
        print(f"\nLocation: {self.deploy_dir}")
        print(f"\nNext steps:")
        print("  1. Test the package on a clean Windows system")
        print("  2. Run HEALTH_CHECK.bat after installation")
        print("  3. Verify all features work correctly")
        print("  4. Distribute to customers")
        print()

        return True


if __name__ == "__main__":
    tier = sys.argv[1] if len(sys.argv) > 1 else "Basic"

    if tier not in ["Basic", "Standard", "Premium"]:
        print(f"Error: Invalid tier '{tier}'")
        print("Usage: python build_deployment_package_v2.py [Basic|Standard|Premium]")
        sys.exit(1)

    builder = DeploymentBuilderV2(tier=tier)
    success = builder.build_all()
    sys.exit(0 if success else 1)
