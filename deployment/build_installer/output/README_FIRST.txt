================================================================================
MBAS v2.1.0 PWA - PROFESSIONAL EDITION
BETA DISTRIBUTION PACKAGE
================================================================================

           Modern Business Automation System
        A Product of Z&T Technologies
        https://www.zttechnologies.org

================================================================================
QUICK START
================================================================================

1. Install Python 3.10+ from: https://www.python.org/
   (Make sure to check "Add Python to PATH" during installation!)

2. Run: MBAS_v2.1.0_PWA_Beta_Setup.exe

3. Follow installation wizard (all automated, no CMD windows!)

4. Login with:
   Username: admin
   Password: admin123

5. Start managing your business!

================================================================================
PACKAGE CONTENTS
================================================================================

✓ MBAS_v2.1.0_PWA_Beta_Setup.exe (2.3 MB)
  Professional Windows installer with silent installation

✓ BETA_TESTING_INSTRUCTIONS.txt
  Comprehensive guide for beta testers

✓ CHECKSUM.txt
  SHA256 checksum for installer verification

✓ WHATS_NEW_v2.1.0.txt
  List of new features and improvements

✓ README_FIRST.txt (this file)
  Quick start guide

================================================================================
WHAT IS MBAS?
================================================================================

MBAS (Modern Business Automation System) is an offline-first business
management solution designed for small to medium businesses.

KEY FEATURES:
✓ Inventory Management - Track products, categories, stock levels
✓ Point of Sale - Fast billing with receipt printing
✓ Customer Management - Track customer purchases and payments
✓ Supplier Management - Purchase orders and payment tracking
✓ Reports & Analytics - Sales, inventory, and financial reports
✓ Multi-User Support - Admin, Manager, and Sales User roles
✓ Automatic Backups - Daily backups with restore capability
✓ Offline Capable - Works without internet connection
✓ Mobile Friendly - Access via WiFi on phones/tablets

================================================================================
NEW IN v2.1.0 PWA
================================================================================

✓ CRITICAL FIX: Server startup bug fixed (was preventing system from starting)
✓ Progressive Web App (PWA) architecture
✓ Service Worker for offline functionality
✓ Mobile-optimized responsive UI
✓ Silent installation (no black CMD windows!)
✓ Professional launcher with error handling
✓ Port conflict detection and resolution
✓ Performance optimizations for low-spec hardware
✓ Windows 7 compatibility (Python 3.10+)
✓ Enhanced security with bcrypt password hashing

================================================================================
SYSTEM REQUIREMENTS
================================================================================

MINIMUM:
- Windows 7 SP1 or newer
- Python 3.10, 3.11, or 3.12
- 2GB RAM
- 100MB free disk space
- Chrome 90+, Edge 90+, or Firefox 90+

RECOMMENDED:
- Windows 10/11
- Python 3.12
- 4GB+ RAM
- SSD storage
- Chrome or Edge (latest)

MOBILE (Optional):
- Android 5.0+ with Chrome browser
- WiFi connection to PC running MBAS

================================================================================
INSTALLATION STEPS
================================================================================

STEP 1: Install Python (if not already installed)
----------------------------------------------
Download from: https://www.python.org/downloads/

IMPORTANT: Check "Add Python to PATH" during installation!

Verify installation:
Open Command Prompt and type: python --version
Should show: Python 3.10.x, 3.11.x, or 3.12.x

STEP 2: Run MBAS Installer
----------------------------------------------
Double-click: MBAS_v2.1.0_PWA_Beta_Setup.exe

Follow the wizard:
1. Click "Next"
2. Accept license
3. Choose install location (default: C:\Program Files\MBAS)
4. Select shortcuts
5. Click "Install"
6. Wait for installation (1-2 minutes)
7. Check "Launch MBAS now"
8. Click "Finish"

NO BLACK CMD WINDOWS WILL APPEAR!

STEP 3: First Launch
----------------------------------------------
- Silent launcher starts server (5-7 seconds)
- Browser opens automatically to http://localhost:8000
- Success dialog shows login credentials

STEP 4: Login
----------------------------------------------
Username: admin
Password: admin123

Change password in Settings after first login!

================================================================================
TESTING GUIDE
================================================================================

For comprehensive testing instructions, see:
BETA_TESTING_INSTRUCTIONS.txt

Quick testing checklist:
□ Dashboard loads correctly
□ Add products to inventory
□ Create a sale transaction
□ Add customers and suppliers
□ Generate a report
□ Test on mobile device (optional)
□ Test offline functionality (disconnect internet, refresh)
□ Test performance with 50+ products

================================================================================
TROUBLESHOOTING
================================================================================

PROBLEM: Installer shows "Python not installed"
SOLUTION: Install Python from python.org, make sure to check "Add to PATH"

PROBLEM: Server won't start
SOLUTION: Check if port 8000 is already in use. Close any existing MBAS instances.

PROBLEM: Browser doesn't open automatically
SOLUTION: Manually open browser and go to: http://localhost:8000

PROBLEM: Can't access from mobile device
SOLUTION: Make sure mobile is on same WiFi as PC. Find PC's IP with "ipconfig" command.

PROBLEM: "Cannot connect to server" error
SOLUTION: Server may still be starting. Wait 10 seconds and refresh.

PROBLEM: Performance is slow
SOLUTION: Close other applications, try with fewer than 100 products initially.

For more help, contact: support@zttechnologies.org

================================================================================
UNINSTALLING
================================================================================

If you need to uninstall:
1. Control Panel → Programs → Uninstall a program
2. Find "MBAS - Business Automation System v2.1.0"
3. Click "Uninstall"
4. Your data is kept in C:\Program Files\MBAS\data\
   (delete manually if you want to remove all data)

================================================================================
FILE VERIFICATION
================================================================================

Installer: MBAS_v2.1.0_PWA_Beta_Setup.exe
Size: 2.3 MB
SHA256: See CHECKSUM.txt

To verify integrity:
certutil -hashfile MBAS_v2.1.0_PWA_Beta_Setup.exe SHA256

Compare output with CHECKSUM.txt

================================================================================
BETA TESTING FEEDBACK
================================================================================

We value your feedback! Please report:

✓ Bugs or errors
✓ Performance issues
✓ UI/UX suggestions
✓ Missing features
✓ Mobile experience

Send feedback to: support@zttechnologies.org
Subject: MBAS v2.1.0 Beta Feedback

Include:
- Your Windows version
- Python version (python --version)
- Description of issue/suggestion
- Screenshots (if applicable)

================================================================================
LICENSE & SUPPORT
================================================================================

LICENSE:
This is a BETA version for testing purposes only.
License validation is BYPASSED in beta mode.
Production version will require a valid license.

For production licensing:
Email: sales@zttechnologies.org
Website: https://www.zttechnologies.org/mbas

SUPPORT:
Email: support@zttechnologies.org
Response time: 24-48 hours

================================================================================
ABOUT Z&T TECHNOLOGIES
================================================================================

Z&T Technologies specializes in state-of-the-art business automation
solutions for small and medium enterprises.

Our Mission:
Making professional business management software accessible and
affordable for businesses of all sizes.

Our Products:
- MBAS (Modern Business Automation System)
- Custom ERP solutions
- Inventory management systems
- Point of sale solutions

Contact:
Email: info@zttechnologies.org
Web: https://www.zttechnologies.org

================================================================================
VERSION INFORMATION
================================================================================

Product: MBAS (Modern Business Automation System)
Version: 2.1.0 PWA Professional Edition
Release Date: June 22, 2026
Release Type: Beta
Build: PWA-2026.06.22

Previous Versions:
- v2.0.5: Desktop-only, Python 3.12 required
- v2.0.4: Windows 10/11 only
- v2.0.3: Initial production release

Changelog:
See WHATS_NEW_v2.1.0.txt for detailed changes

================================================================================

Built with: FastAPI + React + Vite + SQLite + PWA Technology
Tested on: Windows 7/10/11 | Python 3.10/3.11/3.12

Z&T Technologies - State-of-the-Art Business Solutions

================================================================================
