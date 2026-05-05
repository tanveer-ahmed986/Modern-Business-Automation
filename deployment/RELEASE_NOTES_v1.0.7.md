# MBAS v1.0.7 - Release Notes

## 🔒 Enhanced Security, Background Service & Currency Fix Release

**Release Date:** April 27, 2026
**Version:** 1.0.7 Standard Edition
**Package:** MBAS_v1.0.7_Standard_20260427_DevOps.zip
**Status:** Production Ready ✅

---

## 🌟 What's New in v1.0.7

### 🐛 Bug Fixes

#### ✅ Currency Display Fix
- **Fixed hardcoded currency symbols** in Purchases and Suppliers sections
- Currency now **dynamically updates** based on Settings configuration
- Supports all currencies: USD ($), EUR (€), GBP (£), PKR (Rs.), INR (₹)
- **Affected sections:**
  - Purchase page (product prices, cart totals, grand total)
  - Supplier ledger (balance display)
- Now consistent with Billing, Dashboard, and Inventory sections

### Major Security Enhancements

#### ✅ Auto-Logout Security Feature
- **Automatic session clearing** when browser closes
- **No persistent sessions** across browser restarts
- **sessionStorage** instead of localStorage for enhanced security
- Users **must login every time** they open the browser
- Prevents unauthorized access if computer is left unattended

#### ✅ Enhanced Token Security
- JWT token expiry reduced from 8 hours to **2 hours**
- Automatic token refresh on activity
- Secure session management
- Better protection against session hijacking

### Background Service Mode

#### ✅ System Tray Integration
- **No visible CMD window** when running
- **System tray icon** for easy control
- Right-click menu with options:
  - Open MBAS (launches browser)
  - Start Server
  - Stop Server
  - Show Status
  - Exit

#### ✅ Silent Operation
- Server runs completely in background
- Uses `pythonw.exe` for hidden execution
- Process management via `psutil`
- Auto-detect if server is already running

### Technical Improvements

#### ✅ Frontend Changes
- `sessionStorage` for authentication tokens
- Auto-clear credentials on browser/tab close
- Updated all API interceptors
- Session expiry handling improved

#### ✅ Backend Changes
- JWT expiry time optimized for security
- Better session validation
- Enhanced error messages

---

## 📋 Complete Feature List

### Core Features (Unchanged)
- ✅ Point of Sale (POS) / Billing
- ✅ Inventory Management
- ✅ Customer Management
- ✅ Supplier Management
- ✅ Purchase Orders
- ✅ Dashboard Analytics
- ✅ Sales Reports
- ✅ User Management (RBAC)
- ✅ Settings & Configuration
- ✅ Database Backup/Restore

### Standard Tier Features (Unchanged)
- ✅ All Basic features
- ✅ Advanced Reports & Analytics
- ✅ Profit & Loss Reports
- ✅ Sales by Category
- ✅ Payment Method Analysis
- ✅ Top Products Analysis

### NEW Security Features (v1.0.7)
- ✅ Auto-logout on browser close
- ✅ Session-based authentication
- ✅ 2-hour token expiry
- ✅ No persistent sessions

### NEW User Experience (v1.0.7)
- ✅ Background service mode
- ✅ System tray integration
- ✅ Silent server operation
- ✅ Easy server control

---

## 🔧 System Requirements

### Minimum Requirements
- **OS:** Windows 10/11 (64-bit)
- **Python:** 3.11 or 3.12 (NOT 3.13)
- **RAM:** 4 GB minimum (8 GB recommended)
- **Disk:** 500 MB free space
- **Internet:** Required for initial installation only

### Recommended Setup
- **OS:** Windows 11 Pro
- **Python:** 3.12.4
- **RAM:** 8 GB
- **Disk:** 1 GB free space (for database growth)
- **Display:** 1920x1080 or higher

---

## 📦 Installation Guide

### New Installation

1. **Extract Package:**
   ```
   Extract: MBAS_v1.0.7_Standard_20260427_DevOps.zip
   To: C:\MBAS (or any location)
   ```

2. **Run Installer:**
   ```
   Double-click: INSTALL.bat
   Wait: 2-4 minutes
   ```

3. **Verify Installation:**
   ```
   Run: HEALTH_CHECK.bat
   All checks should pass ✓
   ```

4. **Start MBAS (Background Mode - Recommended):**
   ```
   Double-click: START_MBAS_TRAY.bat

   - Server runs in background (no CMD window)
   - System tray icon appears
   - Right-click icon to control server
   - Click "Open MBAS" to launch browser
   ```

5. **Start MBAS (Standard Mode - Alternative):**
   ```
   Double-click: START_MBAS.bat

   - CMD window remains visible
   - Shows server logs
   - Close window to stop server
   ```

6. **First Login:**
   ```
   URL: http://localhost:8000
   Username: admin
   Password: admin123

   ⚠️ IMPORTANT: Change password immediately!
   ```

7. **Security Note:**
   ```
   - You MUST login every time you open the browser
   - Session is cleared when you close the browser
   - This is intentional for security
   - Token expires after 2 hours of inactivity
   ```

---

## 🔄 Upgrading from v1.0.6

### Important Notes
- v1.0.7 includes **breaking security changes**
- Previous localStorage sessions will be **automatically cleared**
- Users will need to **login again** after upgrade

### Upgrade Steps

**IMPORTANT: Backup First!**

```batch
# 1. Backup database
Copy: [Old MBAS]\backend\mbas_database.db
To: Desktop\mbas_backup.db

# 2. Backup license
Copy: [Old MBAS]\mbas.license
To: Desktop\mbas.license.backup
```

**Method 1: Fresh Install (Recommended)**

1. Extract v1.0.7 to new folder
2. Run INSTALL.bat
3. Stop MBAS
4. Copy old database to new folder:
   ```
   Copy: Desktop\mbas_backup.db
   To: [New MBAS]\backend\mbas_database.db
   ```
5. Copy license:
   ```
   Copy: Desktop\mbas.license.backup
   To: [New MBAS]\mbas.license
   ```
6. Start MBAS (use START_MBAS_TRAY.bat for background mode)

**Method 2: In-Place Update**

1. Stop old MBAS
2. Backup database and license (see above)
3. Replace these folders:
   - `frontend\dist\` (entire folder)
   - `backend\src\` (entire folder)
4. Add new files:
   - `scripts\mbas_tray.py`
   - `START_MBAS_TRAY.bat`
5. Start MBAS

---

## 🎯 Key Changes in v1.0.7

### Security Changes

**Before v1.0.7:**
- Token stored in localStorage ❌
- Session persists after browser close ❌
- 8-hour token expiry ⚠️
- Must manually logout 🤷

**After v1.0.7:**
- Token stored in sessionStorage ✅
- Session cleared on browser close ✅
- 2-hour token expiry ✅
- Auto-logout built-in 🎉

### User Experience Changes

**Before v1.0.7:**
- CMD window always visible ❌
- No background mode ❌
- Manual start/stop only 😐

**After v1.0.7:**
- Background service mode ✅
- System tray integration ✅
- Easy server control ✅
- Choose CMD or silent mode ⚡

---

## 🎓 Usage Guide

### Background Mode (Recommended)

**Starting MBAS:**
1. Double-click `START_MBAS_TRAY.bat`
2. Wait 3 seconds for server to start
3. System tray icon appears (bottom-right, near clock)
4. Green icon = Running, Red icon = Stopped

**Using MBAS:**
1. Right-click tray icon
2. Click "Open MBAS"
3. Browser opens to login page
4. Login with credentials
5. Use MBAS normally

**Stopping MBAS:**
1. Close browser (auto-logout activated)
2. Right-click tray icon
3. Click "Exit"
4. Server stops gracefully

### Standard Mode (Alternative)

**Starting MBAS:**
1. Double-click `START_MBAS.bat`
2. CMD window appears with server logs
3. Browser opens automatically

**Stopping MBAS:**
1. Press Ctrl+C in CMD window
2. Or close the CMD window

---

## 📝 What's Included in Package

### Files & Folders
```
MBAS_Package_V2/
├── INSTALL.bat              # Virtual environment installer
├── START_MBAS.bat           # Start server (standard mode)
├── START_MBAS_TRAY.bat      # Start server (background mode) ⭐ NEW
├── STOP_MBAS.bat            # Stop server
├── HEALTH_CHECK.bat         # Installation validator
├── README.txt               # Quick start guide
├── DEPLOYMENT_GUIDE.txt     # IT admin guide
├── mbas.license             # Standard tier license
├── mbas_icon.ico            # Desktop icon
├── create_shortcut.vbs      # Shortcut creator
│
├── backend/
│   ├── src/                 # FastAPI application
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Auth, DB, features (UPDATED)
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   ├── scripts/        # DB init & migration
│   │   └── embedded/       # Public key
│   │
│   ├── requirements.txt     # Production dependencies
│   ├── requirements-lock.txt # Locked versions
│   └── requirements-premium.txt # Optional ML
│
├── frontend/dist/           # Pre-built React app (UPDATED) ⭐
├── scripts/                 # System tray app ⭐ NEW
│   ├── mbas_tray.py        # Tray application
│   └── START_MBAS_TRAY.bat # Tray launcher
└── venv/                    # Created during install
```

---

## 🔒 Security Features

### Authentication
- ✅ **sessionStorage** for tokens (auto-clear on browser close)
- ✅ **2-hour JWT expiry** for enhanced security
- ✅ **Bcrypt password hashing** (cost factor 12)
- ✅ **Auto-logout** on browser close
- ✅ **No persistent sessions**

### Network Security
- ✅ **Local only** (127.0.0.1 only)
- ✅ **No external connections** after install
- ✅ **CORS restricted** to localhost
- ✅ **No telemetry** or data transmission

### Data Security
- ✅ **SQLite database** with file permissions
- ✅ **Input validation** on all forms
- ✅ **RBAC** (Role-based access control)
- ✅ **Transaction integrity** for financial operations

---

## 🐛 Known Issues & Solutions

### Issue: "Must login every time"
**This is not a bug** - This is the new security feature in v1.0.7!
- Sessions intentionally cleared on browser close
- Prevents unauthorized access
- Industry best practice for sensitive business data

### Issue: "Session expired after 2 hours"
**This is intentional** - Enhanced security feature
- Protects against session hijacking
- Simply login again to continue
- Active use extends session automatically

### Issue: System tray icon not visible
**Solution:**
1. Check Windows taskbar settings
2. Make sure "Show hidden icons" is enabled
3. Look for green/red circle with "M"
4. Try clicking the up arrow (^) in taskbar

### Issue: Python 3.13 Compatibility
**Error:** bcrypt compatibility issues
**Solution:** Use Python 3.11 or 3.12 only

### Issue: Port 8000 In Use
**Error:** Address already in use
**Solution:**
- Right-click tray icon → Exit
- Or run STOP_MBAS.bat

---

## 📊 Version History

### v1.0.7 (April 27, 2026) - Current
- ✅ Auto-logout security (sessionStorage)
- ✅ 2-hour token expiry
- ✅ Background service mode
- ✅ System tray integration
- ✅ Silent server operation

### v1.0.6 (April 27, 2026)
- ✅ Complete currency synchronization (all pages)
- ✅ Reports page currency fix (13 locations)
- ✅ Dashboard backend currency fix

### v1.0.5 (April 27, 2026)
- ✅ Dashboard metrics card currency (backend)

### v1.0.4 (April 27, 2026)
- ✅ Frontend currency sync (Inventory, Dashboard)

### v1.0.3 (April 27, 2026)
- ✅ Settings save fix (field names)
- ✅ Database migration script

### v1.0.2 (April 27, 2026)
- ✅ Billing Decimal type fix
- ✅ Pydantic v2 compatibility

### v1.0.1 (April 27, 2026)
- ✅ Virtual environment isolation
- ✅ Dependency locking
- ✅ Health check tool

### v1.0.0 (April 25, 2026)
- Initial release

---

## 🎓 Testing Checklist

### After Installation

**1. Health Check:**
- [ ] Run HEALTH_CHECK.bat
- [ ] All 10 checks pass ✓

**2. Background Mode Test:**
- [ ] Run START_MBAS_TRAY.bat
- [ ] No CMD window appears ✓
- [ ] System tray icon visible ✓
- [ ] Icon is green (server running) ✓
- [ ] Right-click shows menu ✓

**3. Login Test:**
- [ ] Click "Open MBAS" from tray menu
- [ ] Browser opens to login page ✓
- [ ] Login with admin/admin123 ✓
- [ ] Dashboard loads successfully ✓

**4. Auto-Logout Test:**
- [ ] Use MBAS normally
- [ ] Close browser completely
- [ ] Open browser again
- [ ] Redirected to login page ✓ (Expected behavior)
- [ ] Must login again ✓ (Security feature working)

**5. Token Expiry Test:**
- [ ] Login to MBAS
- [ ] Wait 2+ hours (or modify backend for testing)
- [ ] Try to perform action
- [ ] Session expires, redirected to login ✓

**6. Core Features:**
- [ ] Create product ✓
- [ ] Create sale ✓
- [ ] Generate invoice ✓
- [ ] View reports ✓
- [ ] Backup database ✓

**7. Tray Icon Control:**
- [ ] Right-click tray icon → Stop Server
- [ ] Icon turns red ✓
- [ ] Right-click tray icon → Start Server
- [ ] Icon turns green ✓
- [ ] Right-click tray icon → Exit
- [ ] Icon disappears ✓

---

## 📞 Support & Documentation

### Included Documentation
1. **README.txt** - Quick start for end users
2. **DEPLOYMENT_GUIDE.txt** - IT deployment guide
3. **RELEASE_NOTES_v1.0.7.md** - This document

### Troubleshooting
1. Run HEALTH_CHECK.bat first
2. Check console for error messages
3. Review system tray icon status
4. Refer to DEPLOYMENT_GUIDE.txt

### New Features Documentation
- **Background Service:** Use START_MBAS_TRAY.bat instead of START_MBAS.bat
- **Auto-Logout:** Intentional security feature, not a bug
- **Session Security:** 2-hour expiry, auto-refresh on activity

---

## 🎯 Target Users

### Perfect For:
- ✅ Retail shops (Pharmacy, Electronics, Grocery)
- ✅ Small businesses (10-100 transactions/day)
- ✅ **Security-conscious businesses** (NEW)
- ✅ **Shared computer environments** (NEW)
- ✅ Offline-first requirements
- ✅ Single location operations
- ✅ Windows-based POS systems

### Especially Good For v1.0.7:
- ✅ **Multi-user computer setups** (auto-logout prevents unauthorized access)
- ✅ **High-security requirements** (session-based auth)
- ✅ **Retail counters** (background mode = cleaner workspace)
- ✅ **Pharmacies** (regulatory compliance for session security)

### Not Suitable For:
- ❌ Multi-location chains (use cloud version)
- ❌ High-volume e-commerce (use cloud version)
- ❌ Linux/Mac deployment (use Docker version)

---

## 📈 Performance Metrics

### Typical Performance (Unchanged)
- **Installation Time:** 2-4 minutes
- **Startup Time:** 2-3 seconds
- **Database Size:** ~50 MB per 10,000 sales
- **Memory Usage:** ~150 MB RAM
- **Response Time:** <100ms for most operations

### Background Mode Performance
- **Startup Time:** 2-3 seconds (same as standard)
- **Memory Usage:** ~150 MB RAM (same as standard)
- **CPU Usage:** <1% when idle
- **System Tray:** ~5 MB RAM overhead

---

## 🔐 License Information

### Standard Tier Includes:
- ✅ All Basic features
- ✅ Advanced reports
- ✅ Profit & Loss reports
- ✅ Sales analytics
- ✅ Payment method analysis
- ✅ Category performance
- ✅ Top products tracking
- ✅ Tax reports
- ✅ Customer analytics
- ✅ **Enhanced security features** (NEW)
- ✅ **Background service mode** (NEW)
- ✅ Lifetime updates (within tier)

### License File
- **Location:** `mbas.license`
- **Type:** Perpetual (Standard)
- **Signature:** RSA-4096 cryptographic
- **Validation:** On every startup

---

## 🚀 Quick Start Summary

```batch
# 1. Extract
Unzip to: C:\MBAS

# 2. Install
Run: INSTALL.bat (2-4 minutes)

# 3. Verify
Run: HEALTH_CHECK.bat (all pass ✓)

# 4. Start (Background Mode - Recommended)
Run: START_MBAS_TRAY.bat
Look for system tray icon (bottom-right)

# 5. Open MBAS
Right-click tray icon → "Open MBAS"

# 6. Login
URL: http://localhost:8000
User: admin
Pass: admin123

# 7. Setup
- Change password
- Settings → Configure currency, tax
- Add products
- Create first sale

# 8. Security Note
- Must login every time browser opens
- Session clears when browser closes
- This is intentional for security!
```

---

## ✨ Conclusion

**MBAS v1.0.7 is the most secure and user-friendly version yet!**

### Key Achievements:
- ✅ Enhanced security with auto-logout
- ✅ Background service mode for cleaner operation
- ✅ System tray integration for easy control
- ✅ 2-hour token expiry for better protection
- ✅ All previous features and fixes included
- ✅ Production-ready for security-conscious businesses

### Ready For:
- ✅ **High-security environments** (NEW)
- ✅ **Shared computer setups** (NEW)
- ✅ Production deployment
- ✅ Customer distribution
- ✅ Enterprise use
- ✅ Daily operations

### Perfect For Businesses That:
- ✅ Need strong session security
- ✅ Have multiple users on same computer
- ✅ Want cleaner workspace (background mode)
- ✅ Require regulatory compliance (auto-logout)
- ✅ Value data privacy and security

**Thank you for using MBAS!** 🎉

---

*Release Date: April 27, 2026*
*Package: MBAS_v1.0.7_Standard_20260427_DevOps.zip*
*Build: Production*
*Status: Stable ✅*
*Security: Enhanced 🔒*
