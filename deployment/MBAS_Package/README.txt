================================================================
   MBAS - Modern Business Automation System v1.0.0
   Basic Edition
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
  Database:  backend\mbas_database.db
  Backups:   backend\backups\
  Config:    backend\config\

  To backup: Copy this entire MBAS folder to USB drive.
  To restore: Replace the folder on the new computer.
  To move: Copy folder to new computer, run INSTALL.bat, then START_MBAS.bat.

FEATURES (Basic Edition):
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
