================================================================
   MBAS - Modern Business Automation System v1.0.7
   Basic Edition - DevOps-Grade Deployment
================================================================

WHAT'S NEW IN v1.0.7:
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
  1. Extract this ZIP file to any location (e.g., C:\MBAS)
  2. Double-click INSTALL.bat
  3. Wait for installation to complete (2-4 minutes)
  4. Double-click "MBAS" icon on desktop (or START_MBAS.bat)
  5. Login: admin / admin123
  6. CHANGE PASSWORD IMMEDIATELY!

INSTALLATION DETAILS:
--------------------
  INSTALL.bat creates an isolated Python virtual environment.
  This prevents conflicts with other Python software on your computer.
  All dependencies are installed in: [MBAS]\venv\

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
  Package built: 2026-04-27 15:52:20
  Package type: DevOps-Grade with Virtual Environment Isolation
================================================================
