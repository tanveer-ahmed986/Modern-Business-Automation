================================================================================
    MBAS v1.0.9 - Modern Business Automation System
    Professional System Tray Edition with License Management
================================================================================

Thank you for choosing MBAS - the complete business automation solution!

This package includes everything you need to run a professional inventory,
sales, and business management system.

================================================================================
  📦 PACKAGE CONTENTS
================================================================================

✅ MBAS Core Application
   - Backend API (FastAPI + Python)
   - Frontend Dashboard (React + TypeScript)
   - SQLite Database (embedded)

✅ System Tray Application (NEW!)
   - Background operation mode
   - Professional user experience
   - No visible CMD windows

✅ License Management System (NEW!)
   - Secure license validation
   - Package tier enforcement
   - Anti-piracy protection

✅ Auto-Recovery Features
   - Watchdog monitoring
   - Automatic restart on hang
   - Health checking

✅ Documentation
   - Release notes
   - Upgrade guide
   - User manual
   - Installation guide

================================================================================
  🚀 QUICK START (FIRST-TIME USERS)
================================================================================

Step 1: Install Backend
  → Double-click: INSTALL.bat
  → Wait for "Installation complete"
  → This creates Python virtual environment

Step 2: Start MBAS
  → Double-click: START_MBAS_TRAY.bat
  → System tray icon appears (🟢 green)
  → Browser opens automatically

Step 3: Login
  → Default credentials:
     Username: admin
     Password: admin123
  → IMPORTANT: Change password after first login!

Step 4: Start Using
  → Dashboard shows business overview
  → Add products, customers, suppliers
  → Create sales and purchases
  → Generate reports

Done! You're ready to manage your business.

================================================================================
  🎯 STARTUP OPTIONS
================================================================================

For End Users (RECOMMENDED):
  📌 START_MBAS_TRAY.bat
     • Professional system tray mode
     • Runs completely hidden
     • Auto-opens browser
     • Perfect for daily use

For Administrators:
  📌 AUTO_START_WITH_RECOVERY.bat
     • Visible windows with monitoring
     • Auto-recovery on crashes
     • Good for troubleshooting

For Developers:
  📌 START_MBAS.bat
     • Standard visible windows
     • Manual control
     • Good for development

To Stop:
  📌 STOP_MBAS.bat
     OR Right-click tray icon > Exit

================================================================================
  🎨 SYSTEM TRAY GUIDE
================================================================================

Finding the Tray Icon:
  • Look in Windows system tray (bottom-right)
  • Small circular icon
  • May be in hidden icons (click ^)

Icon Colors:
  🟢 Green Circle = Server Running (ready to use)
  🔴 Red Circle = Server Stopped
  ⚪ Gray Circle = Server Starting (please wait)

Using the Tray Menu:
  • Double-click icon → Opens MBAS in browser
  • Right-click icon → Shows menu:
    - Open MBAS (open in browser)
    - Start Server (if stopped)
    - Stop Server (stop backend)
    - Status (check if running)
    - Exit (close everything)

Notifications:
  • Shows when server starts/stops
  • Displays errors if startup fails
  • Status updates as needed

================================================================================
  📋 SYSTEM REQUIREMENTS
================================================================================

Operating System:
  ✅ Windows 10 (64-bit)
  ✅ Windows 11 (64-bit)
  ❌ Windows 7/8 (not supported)

Software Prerequisites:
  ✅ Python 3.11 or higher
     → Download: https://python.org
     → Check: Open CMD, type "python --version"

  ⚠️  Node.js (only for development)
     → Not needed for running the application
     → Only needed if modifying frontend code

Hardware:
  • CPU: Any modern processor (Intel/AMD)
  • RAM: 4GB minimum, 8GB recommended
  • Storage: 500MB free space
  • Display: 1366x768 minimum resolution

Network:
  • Ports 8000 and 5173 must be available
  • No internet required (runs offline)
  • Firewall may need to allow Python

================================================================================
  🔐 LICENSE INFORMATION
================================================================================

License File: mbas.license
  • Located in package root folder
  • Required for system operation
  • Validates on startup

License Types:

  📦 BASIC Package
     • Core inventory management
     • Sales and billing
     • Supplier management
     • Basic reports
     • Single user
     Price: ₹15,000 / $200

  📦 STANDARD Package
     • All Basic features
     • Multi-user support
     • Advanced reports
     • Custom categories
     • Export to Excel/PDF
     Price: ₹30,000 / $400

  📦 PREMIUM Package
     • All Standard features
     • AI-powered forecasting
     • Advanced analytics
     • API access
     • Priority support
     Price: ₹50,000 / $700

Checking Your License:
  1. Login to MBAS
  2. Go to Settings > System
  3. View license tier and expiry date

Renewing License:
  • Contact your vendor before expiry
  • Replace mbas.license file
  • Restart MBAS
  • New license activates automatically

================================================================================
  📂 FOLDER STRUCTURE
================================================================================

MBAS_v1.0.9_Production_Ready/
├── START_MBAS_TRAY.bat          ← START HERE (recommended)
├── AUTO_START_WITH_RECOVERY.bat ← Alternative startup
├── START_MBAS.bat               ← Standard startup
├── STOP_MBAS.bat                ← Stop system
├── INSTALL_BACKEND_FIXED.bat    ← One-time installation
├── mbas.license                 ← License file
├── README_v1.0.9.txt            ← This file
├── RELEASE_NOTES_v1.0.9.txt     ← What's new
├── UPGRADE_GUIDE_v1.0.9.txt     ← Upgrade instructions
│
├── scripts/                     ← System tray application
│   └── mbas_tray.py
│
├── backend/                     ← Backend API server
│   ├── src/                     ← Source code
│   ├── mbas_database.db         ← Your data (backup this!)
│   ├── requirements.txt         ← Python dependencies
│   └── watchdog.py              ← Auto-recovery service
│
├── frontend/                    ← Frontend dashboard
│   ├── dist/                    ← Production build
│   └── src/                     ← Source code
│
└── docs/                        ← Documentation
    ├── USER_MANUAL.pdf
    └── INSTALLATION_GUIDE.txt

================================================================================
  ⚙️ INSTALLATION STEPS (DETAILED)
================================================================================

If you haven't installed yet, follow these steps carefully:

1. Extract Package
   ─────────────────
   • Right-click MBAS_v1.0.9_Production_Ready.zip
   • Choose "Extract All"
   • Destination: C:\MBAS or D:\MBAS (your choice)
   • Click Extract
   • Open extracted folder

2. Install Python (if not already installed)
   ──────────────────────────────────────────
   • Go to https://python.org
   • Download Python 3.11 or higher
   • Run installer
   • ✅ CHECK "Add Python to PATH"
   • Click "Install Now"
   • Wait for completion

3. Run Backend Installation
   ─────────────────────────
   • In MBAS folder, find: INSTALL_BACKEND_FIXED.bat
   • Right-click → Run as Administrator
   • Wait for completion (may take 5-10 minutes)
   • Message: "Installation complete"

4. Verify Installation
   ────────────────────
   • Check for: venv/ folder (virtual environment)
   • Check for: backend/mbas_database.db (database)
   • Check for: mbas.license (license file)

5. First Run
   ─────────
   • Double-click: START_MBAS_TRAY.bat
   • Wait for system tray icon (🟢 green)
   • Browser opens automatically to login page
   • Login: admin / admin123

6. Change Default Password
   ────────────────────────
   • After login, go to Settings
   • Click "Change Password"
   • Enter new password
   • Save changes
   • IMPORTANT: Remember your new password!

================================================================================
  🔧 TROUBLESHOOTING
================================================================================

Problem: Python not found
────────────────────────
Symptom: "python is not recognized" error
Solution:
  1. Install Python from python.org
  2. During install, CHECK "Add Python to PATH"
  3. Restart computer
  4. Run INSTALL_BACKEND_FIXED.bat again

Problem: System tray icon doesn't appear
────────────────────────────────────────
Symptom: No MBAS icon in system tray
Solution:
  1. Check hidden icons (click ^ in tray)
  2. Wait 10 seconds (may be starting)
  3. Try AUTO_START_WITH_RECOVERY.bat instead
  4. Check if Python is installed

Problem: Browser doesn't open
────────────────────────────
Symptom: Tray icon shows but no browser
Solution:
  1. Wait 10 seconds (auto-open may be delayed)
  2. Manually open: http://127.0.0.1:5173
  3. Check if icon is green (server running)

Problem: "Port already in use"
─────────────────────────────
Symptom: Server won't start, port error
Solution:
  1. Run STOP_MBAS.bat
  2. Open Task Manager (Ctrl+Shift+Esc)
  3. End any "python.exe" or "node.exe" processes
  4. Wait 10 seconds
  5. Run START_MBAS_TRAY.bat again

Problem: Login fails with correct password
──────────────────────────────────────────
Symptom: "Invalid credentials" but password is correct
Solution:
  1. Check Caps Lock is OFF
  2. Try default: admin / admin123
  3. Check backend is running (green icon)
  4. Check browser console for errors (F12)

Problem: Database error on startup
──────────────────────────────────
Symptom: Error about database locked or corrupted
Solution:
  1. Stop MBAS completely
  2. Delete: backend/mbas_database.db-journal
  3. Restart system
  4. If persists, restore database from backup

Problem: License errors
──────────────────────
Symptom: "License not found" or "Invalid license"
Solution:
  1. Verify mbas.license exists in root folder
  2. Check file is not empty (should be ~1KB)
  3. Contact vendor for valid license
  4. Copy license file to package root
  5. Restart MBAS

================================================================================
  💾 BACKUP AND DATA PROTECTION
================================================================================

What to Backup:
  📁 backend/mbas_database.db (YOUR DATA - CRITICAL!)
  📁 mbas.license (your license)
  📁 backend/config/* (if you have custom configs)

Backup Schedule:
  • Daily: If actively using
  • Weekly: For normal use
  • Before updates: Always!
  • Before system changes: Recommended

How to Backup:
  1. Stop MBAS (STOP_MBAS.bat or tray menu)
  2. Navigate to backend/ folder
  3. Copy mbas_database.db
  4. Paste to safe location
  5. Rename: mbas_database_backup_YYYYMMDD.db
  6. Store in multiple locations:
     - External USB drive
     - Network drive
     - Cloud storage (encrypted)

How to Restore:
  1. Stop MBAS
  2. Delete corrupted mbas_database.db
  3. Copy backup file
  4. Rename to: mbas_database.db
  5. Restart MBAS

Automated Backup (Advanced):
  • Use Windows Task Scheduler
  • Schedule daily copy of database
  • To network location or cloud
  • Retention: Keep last 30 days

================================================================================
  👥 USER MANAGEMENT
================================================================================

Default Account:
  Username: admin
  Password: admin123
  Role: Administrator (full access)

Creating New Users:
  1. Login as admin
  2. Go to Settings > Users
  3. Click "Add New User"
  4. Fill details:
     - Username
     - Password
     - Full Name
     - Role (Admin/Manager/Sales User)
  5. Save

User Roles:

  🔑 Administrator
     • Full system access
     • Can manage users
     • Can change settings
     • Can view all reports
     • Can delete data

  📊 Manager
     • Can view all data
     • Can create sales/purchases
     • Can generate reports
     • Cannot delete critical data
     • Cannot manage users

  🛒 Sales User
     • Can create sales
     • Can view products
     • Can view customers
     • Cannot access purchases
     • Cannot view reports

Best Practices:
  • Each person has their own account
  • Use strong passwords (8+ characters)
  • Disable accounts for departed staff
  • Review user access monthly
  • Never share admin password

================================================================================
  📊 KEY FEATURES
================================================================================

✅ Inventory Management
   • Product catalog with categories
   • Stock tracking (in/out/balance)
   • Low stock alerts
   • Barcode support
   • Product images

✅ Sales & Billing
   • Quick sale interface
   • Invoice generation
   • Payment tracking
   • Tax calculations
   • Discount management
   • Print/Email invoices

✅ Purchase Management
   • Purchase orders
   • Supplier management
   • Bill tracking
   • Payment terms
   • Purchase history

✅ Supplier Ledger
   • Outstanding balances
   • Payment history
   • Credit terms
   • Contact management

✅ Reports & Analytics
   • Sales reports (daily/monthly/yearly)
   • Stock reports
   • Profit/loss analysis
   • Top products
   • Customer analysis
   • Export to Excel/PDF

✅ Advanced Features (Premium)
   • AI-powered demand forecasting
   • Advanced analytics dashboard
   • Custom report builder
   • API access
   • Multi-location support

================================================================================
  🌐 ACCESSING MBAS
================================================================================

Local Access (Same Computer):
  URL: http://127.0.0.1:5173
  OR:  http://localhost:5173

Network Access (Other Computers on LAN):
  1. Find your computer's IP:
     • Open CMD
     • Type: ipconfig
     • Note "IPv4 Address" (e.g., 192.168.1.100)

  2. Configure Windows Firewall:
     • Allow Python through firewall
     • Allow ports 8000 and 5173

  3. On other computers:
     • Open browser
     • Go to: http://YOUR_IP:5173
     • Example: http://192.168.1.100:5173

Mobile Access (Same WiFi):
  • Connect phone/tablet to same WiFi
  • Open browser on mobile
  • Go to: http://YOUR_IP:5173
  • Login normally

Security Note:
  • For LAN access only (not internet)
  • Use strong passwords
  • Consider VPN for remote access
  • Regular security updates

================================================================================
  📞 SUPPORT AND HELP
================================================================================

Self-Help Resources:
  📄 USER_MANUAL.pdf - Complete user guide
  📄 RELEASE_NOTES_v1.0.9.txt - What's new
  📄 UPGRADE_GUIDE_v1.0.9.txt - Upgrade instructions
  📄 This README file

Common Questions:
  Q: Is internet required?
  A: No, MBAS works completely offline.

  Q: Can multiple users access simultaneously?
  A: Yes, on the same network (LAN access).

  Q: What about my data security?
  A: Data stored locally, encrypted at rest.

  Q: Can I customize the system?
  A: Premium license includes API access.

  Q: What about backups?
  A: Manual backup recommended (see Backup section).

  Q: Is there mobile app?
  A: Access via mobile browser (responsive design).

Technical Support:
  📧 Email: support@mbas.example.com
  📱 Phone: +91-XXXX-XXXXXX
  💬 WhatsApp: +91-XXXX-XXXXXX

  Support Hours:
  Monday-Friday: 9:00 AM - 6:00 PM
  Saturday: 9:00 AM - 2:00 PM
  Sunday: Closed

Response Time:
  • Email: Within 24 hours
  • Phone: Immediate (during hours)
  • Critical issues: Priority handling

Remote Assistance:
  • TeamViewer or AnyDesk
  • By appointment
  • For licensed customers

================================================================================
  🎓 TRAINING AND ONBOARDING
================================================================================

Getting Started (1-2 hours):
  1. Watch introduction video
  2. Follow USER_MANUAL.pdf
  3. Create sample products
  4. Create test sale
  5. Generate sample report

Training Materials:
  📹 Video Tutorials (if available)
     • System overview (10 min)
     • Creating products (15 min)
     • Making sales (20 min)
     • Reports and analytics (15 min)

  📖 Documentation
     • User manual (comprehensive)
     • Quick reference cards
     • FAQ document

  👨‍🏫 Live Training (optional)
     • On-site training available
     • Remote training via video call
     • Customized to your business
     • Contact vendor for pricing

Sample Data:
  • System includes sample products
  • Practice with test data first
  • Delete samples when ready
  • Start fresh for production

Best Practices:
  • Train all users before go-live
  • Designate a "super user" internally
  • Review processes weekly initially
  • Gather feedback from users

================================================================================
  🔄 UPDATES AND MAINTENANCE
================================================================================

Checking for Updates:
  • Check with vendor quarterly
  • Subscribe to update notifications
  • Test updates in development first

Installing Updates:
  1. Backup database
  2. Download new version
  3. Follow UPGRADE_GUIDE
  4. Verify functionality
  5. Train users on changes

Update Policy:
  • Minor updates: Free for 1 year
  • Major updates: May require upgrade fee
  • Security patches: Always free
  • Bug fixes: Always free

System Maintenance:
  Weekly:
    • Backup database
    • Check disk space
    • Review error logs

  Monthly:
    • Review user accounts
    • Archive old data (if needed)
    • Update documentation

  Quarterly:
    • Check for software updates
    • Review security settings
    • Performance optimization

================================================================================
  📈 BUSINESS BENEFITS
================================================================================

Save Time:
  • Faster billing (seconds vs minutes)
  • Automated stock tracking
  • Quick report generation
  • Less manual paperwork

Save Money:
  • Reduce inventory errors
  • Prevent stockouts
  • Optimize purchasing
  • Better supplier negotiation

Grow Business:
  • Professional invoices
  • Better customer service
  • Data-driven decisions
  • Identify top products

Reduce Errors:
  • Automated calculations
  • Duplicate detection
  • Validation checks
  • Audit trails

Better Control:
  • Real-time inventory visibility
  • Financial tracking
  • User access control
  • Complete audit history

================================================================================
  ⚖️ LEGAL AND COMPLIANCE
================================================================================

Software License:
  • Proprietary software
  • Licensed, not sold
  • One license per installation
  • Transferable with vendor approval

Data Privacy:
  • Your data stays on your computer
  • No cloud storage without consent
  • GDPR-compliant (if applicable)
  • You own your data

Warranty:
  • Software provided "as is"
  • No guarantee of fitness
  • Support as per license tier
  • Backups are your responsibility

Compliance:
  • GST-ready invoicing
  • Tax calculation support
  • Audit trail maintenance
  • Regulatory reporting (India)

Copyright:
  © 2026 MBAS Development Team
  All rights reserved.

================================================================================
  🎉 THANK YOU
================================================================================

Thank you for choosing MBAS!

We're committed to helping your business succeed with reliable,
professional business automation software.

If you have questions, suggestions, or need assistance, please
don't hesitate to contact us.

Happy Business Management! 🚀

================================================================================
  VERSION INFORMATION
================================================================================

Version: 1.0.9
Release Date: April 30, 2026
Package: MBAS_v1.0.9_Production_Ready
Based on: MBAS v1.0.8 (Auto-Recovery Update)

New in v1.0.9:
  ✅ System tray integration
  ✅ License management system
  ✅ Professional background operation
  ✅ Auto-browser opening
  ✅ Package tier enforcement

All v1.0.8 features retained:
  ✅ Auto-recovery watchdog
  ✅ Health monitoring
  ✅ Connection pooling
  ✅ Enhanced reliability

For detailed changelog, see RELEASE_NOTES_v1.0.9.txt

================================================================================
  END OF README
================================================================================
