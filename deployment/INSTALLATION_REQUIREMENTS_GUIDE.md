# MBAS Installation Requirements & Setup Guide

**Version**: 1.0.7
**Last Updated**: April 28, 2026
**Target Audience**: IT Administrators, System Installers, Technical Support

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Pre-Installation Checklist](#pre-installation-checklist)
3. [Required Software](#required-software)
4. [Installation Steps](#installation-steps)
5. [First-Time Setup](#first-time-setup)
6. [Verification & Testing](#verification--testing)
7. [Troubleshooting](#troubleshooting)
8. [Uninstallation](#uninstallation)

---

## 🖥️ System Requirements

### Minimum Requirements

| Component | Specification |
|-----------|---------------|
| **Operating System** | Windows 10 (64-bit) or later |
| **Processor** | Intel Core i3 or AMD Ryzen 3 (2.0 GHz+) |
| **RAM** | 4 GB |
| **Storage** | 2 GB available disk space |
| **Display** | 1366 x 768 resolution |
| **Network** | Not required (offline-first system) |

### Recommended Requirements

| Component | Specification |
|-----------|---------------|
| **Operating System** | Windows 11 (64-bit) |
| **Processor** | Intel Core i5 or AMD Ryzen 5 (2.5 GHz+) |
| **RAM** | 8 GB or more |
| **Storage** | 5 GB SSD storage |
| **Display** | 1920 x 1080 resolution or higher |
| **Network** | Internet connection for initial setup only |

### Database Capacity

- **SQLite Database**: Supports 100,000+ records
- **Concurrent Users**: Up to 5 simultaneous connections
- **Transaction Volume**: 500+ invoices per day

---

## ✅ Pre-Installation Checklist

Before installing MBAS, verify the following:

### Software Prerequisites

- [ ] **Python 3.11 or 3.12** installed (see [Required Software](#required-software))
- [ ] **SQLite3** included with Python (verify with `sqlite3 --version`)
- [ ] **Microsoft Visual C++ Redistributable** (2015-2022) installed
- [ ] **Windows PowerShell 5.1** or later (included in Windows 10/11)
- [ ] **Modern Web Browser** (Chrome, Edge, Firefox - latest version)

### System Configuration

- [ ] **Administrator privileges** available for installation
- [ ] **User Account Control (UAC)** enabled
- [ ] **Windows Defender** or antivirus exceptions configured (if needed)
- [ ] **Firewall** configured to allow localhost connections
- [ ] **Disk space** verified (minimum 2 GB free)

### Network Requirements

- [ ] **Internet connection** for initial dependency installation (one-time)
- [ ] **Localhost access** not blocked by security software
- [ ] **Ports 8000 and 5173** available (or custom ports configured)

### Business Readiness

- [ ] **Business information** ready (name, address, tax ID, currency)
- [ ] **Logo image** prepared (PNG/JPG, recommended 200x200px)
- [ ] **User accounts** planned (Admin, Manager, Sales roles)
- [ ] **Product list** prepared for import (optional)

---

## 🛠️ Required Software

### 1. Python Installation

**Version Required**: Python 3.11.x or 3.12.x

#### Download Python

1. Visit: https://www.python.org/downloads/
2. Download **Python 3.12.x** (latest stable release)
3. Choose **Windows installer (64-bit)**

#### Installation Steps

1. Run the Python installer
2. ✅ **IMPORTANT**: Check "Add Python to PATH"
3. ✅ Check "Install pip"
4. Click "Install Now"
5. Wait for installation to complete
6. Click "Close"

#### Verify Installation

Open Command Prompt and run:

```cmd
python --version
```

Expected output:
```
Python 3.12.x
```

Check pip installation:

```cmd
pip --version
```

Expected output:
```
pip 24.x.x from ... (python 3.12)
```

### 2. SQLite3 (Included with Python)

SQLite3 is automatically included with Python. Verify installation:

```cmd
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

Expected output:
```
3.45.x
```

### 3. Microsoft Visual C++ Redistributable

**Required for**: Python cryptography packages

#### Download & Install

1. Visit: https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist
2. Download: **vc_redist.x64.exe** (64-bit version)
3. Run installer
4. Accept license and click "Install"
5. Restart computer if prompted

### 4. Web Browser

**Supported Browsers**:
- Google Chrome (recommended)
- Microsoft Edge
- Mozilla Firefox

**Minimum Version**: Any version from 2024 or later

---

## 📦 Installation Steps

### Method 1: Production Installation (Recommended)

This method uses the pre-packaged deployment ZIP file.

#### Step 1: Extract Package

1. Download `MBAS_v1.0.7_Basic_20260427_DevOps.zip`
2. Right-click → "Extract All..."
3. Choose installation directory (e.g., `C:\MBAS` or `D:\MBAS`)
4. Click "Extract"

**Recommended Paths**:
- `C:\MBAS` (system-wide installation)
- `D:\MBAS` (separate drive installation)
- `F:\Applications\MBAS` (network drive - ensure fast access)

❌ **Avoid Paths With**:
- Spaces (e.g., "C:\Program Files\MBAS")
- Special characters (e.g., "C:\Apps&Tools\MBAS")
- Non-English characters
- Very long paths (> 100 characters)

#### Step 2: Run Installer

1. Navigate to extracted folder
2. Double-click **`INSTALL.bat`**
3. Wait for installation (2-5 minutes)

**What Happens During Installation**:
- Creates Python virtual environment (`venv/`)
- Downloads and installs dependencies
- Initializes SQLite database
- Creates desktop shortcut "MBAS"
- Configures system tray launcher

#### Step 3: Wait for Completion

Installation progress:

```
[1/5] Creating virtual environment...
[2/5] Installing backend dependencies...
[3/5] Installing system tray components...
[4/5] Initializing database...
[5/5] Creating desktop shortcut...

Installation complete! ✅
```

**Total Time**: 2-5 minutes (depends on internet speed)

### Method 2: Development Installation

For developers or custom installations.

#### Step 1: Clone or Extract Source Code

```cmd
cd D:\
git clone https://github.com/your-repo/mbas.git
cd mbas
```

Or extract source ZIP to desired location.

#### Step 2: Create Virtual Environment

```cmd
python -m venv venv
venv\Scripts\activate
```

#### Step 3: Install Backend Dependencies

```cmd
cd backend
pip install -r requirements-lock.txt
```

#### Step 4: Install Frontend Dependencies

```cmd
cd ..\frontend
npm install
```

#### Step 5: Initialize Database

```cmd
cd ..\backend
python src\scripts\init_db.py
```

#### Step 6: Create Admin User

```cmd
python -c "from backend.src.scripts.init_db import create_default_admin; create_default_admin()"
```

---

## 🚀 First-Time Setup

### Launch MBAS

#### Method 1: Desktop Shortcut (Recommended)

1. Double-click **"MBAS"** icon on desktop
2. Wait 3-5 seconds (first-time dependency setup)
3. System tray icon appears (green checkmark)
4. Browser opens automatically to http://localhost:8000

**First Launch Behavior**:
- First click: 3-5 second delay (one-time system tray setup)
- Subsequent launches: Instant (< 1 second)

#### Method 2: Manual Launcher

1. Navigate to MBAS installation folder
2. Double-click **`START_MBAS_TRAY.bat`**
3. Same behavior as desktop shortcut

#### Method 3: Standard Mode (Visible Console)

1. Double-click **`START_MBAS.bat`**
2. Two console windows will appear (backend + frontend)
3. Browser opens automatically
4. Console windows remain visible (useful for debugging)

### Login

Default administrator credentials:

```
Username: admin
Password: admin123
```

⚠️ **Security Warning**: Change the default password immediately after first login!

### Initial Configuration

After first login, configure:

1. **Business Settings** (Settings → Business Info)
   - Business name
   - Address and contact details
   - Tax ID / Registration number
   - Currency (USD, EUR, INR, etc.)
   - Timezone

2. **Upload Business Logo** (Settings → Branding)
   - File formats: PNG, JPG
   - Recommended size: 200x200 pixels
   - Maximum file size: 2 MB

3. **Create User Accounts** (Settings → Users)
   - Create Manager accounts
   - Create Sales User accounts
   - Assign appropriate roles

4. **Configure Invoice Settings** (Settings → Invoice)
   - Invoice prefix (default: INV)
   - Tax rates (GST, VAT, Sales Tax)
   - Payment terms
   - Invoice footer text

5. **Add Initial Product Data** (Inventory → Products)
   - Import products from CSV (optional)
   - Or manually add products

---

## ✅ Verification & Testing

### Health Check

Run the automated health check:

1. Navigate to MBAS installation folder
2. Double-click **`HEALTH_CHECK.bat`**
3. Review output:

```
MBAS System Health Check
========================

✅ Python Installation: OK (3.12.x)
✅ Virtual Environment: OK
✅ Backend Dependencies: OK
✅ Database: OK (mbas.db - 2.1 MB)
✅ Frontend Build: OK
✅ System Tray Dependencies: OK

Status: All systems operational ✅
```

### Manual Verification

#### 1. Backend API Test

Open browser and navigate to:

```
http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.7"
}
```

#### 2. API Documentation

Access interactive API docs:

```
http://localhost:8000/docs
```

You should see the FastAPI Swagger UI with all endpoints listed.

#### 3. Frontend Test

Navigate to:

```
http://localhost:5173
```

Or:

```
http://localhost:8000
```

You should see the MBAS login page.

#### 4. Database Test

```cmd
cd backend
python -c "from src.core.db import engine; from sqlmodel import Session; session = Session(engine); print('Database connection: OK')"
```

Expected output:
```
Database connection: OK
```

#### 5. Create Test Invoice

1. Login as admin
2. Go to **Billing** page
3. Add a product to cart
4. Generate invoice
5. Verify invoice number format: `INV-20260428-0001`

#### 6. Test System Tray

1. Right-click system tray icon (green)
2. Verify menu options:
   - Open MBAS
   - Health Check
   - Exit MBAS

---

## 🔧 Troubleshooting

### Installation Issues

#### Problem: "Python is not recognized"

**Cause**: Python not added to PATH

**Solution**:
1. Reinstall Python
2. ✅ Check "Add Python to PATH"
3. Or manually add to PATH:
   - System Properties → Environment Variables
   - Add: `C:\Python312\` and `C:\Python312\Scripts\`

#### Problem: "pip install failed"

**Cause**: No internet connection or proxy blocking

**Solution**:
1. Verify internet connection
2. If behind proxy, configure pip:
   ```cmd
   set HTTP_PROXY=http://proxy.company.com:8080
   set HTTPS_PROXY=http://proxy.company.com:8080
   pip install -r requirements-lock.txt
   ```

#### Problem: "Virtual environment not found"

**Cause**: Installation incomplete or corrupted

**Solution**:
1. Delete `venv` folder
2. Run `INSTALL.bat` again

#### Problem: "Failed to install system tray dependencies"

**Cause**: No internet connection on first launch

**Solution**:
1. Connect to internet
2. Click MBAS icon again
3. Dependencies will install automatically

### Runtime Issues

#### Problem: "Failed to start server"

**Cause**: Port 8000 already in use

**Solution**:
1. Check if another MBAS instance is running (system tray)
2. Or find and stop conflicting process:
   ```cmd
   netstat -ano | findstr :8000
   taskkill /PID <process_id> /F
   ```

#### Problem: "Login failed"

**Cause**: Backend not running or database corrupted

**Solution**:
1. Verify backend is running: http://localhost:8000/health
2. If database corrupted, restore from backup:
   ```cmd
   copy backend\backups\mbas_backup_latest.db backend\mbas.db
   ```

#### Problem: "Blank page after login"

**Cause**: Frontend not loading or JavaScript errors

**Solution**:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Try different browser
3. Check console for errors (F12 → Console)

#### Problem: "System tray icon not appearing"

**Cause**: Tray dependencies missing or failed to install

**Solution**:
1. Manual installation:
   ```cmd
   venv\Scripts\activate
   pip install pystray Pillow psutil
   ```
2. Restart MBAS

### Database Issues

#### Problem: "Database locked"

**Cause**: Multiple processes accessing database

**Solution**:
1. Stop all MBAS instances
2. Run `STOP_MBAS.bat`
3. Delete `backend\mbas.db-wal` and `backend\mbas.db-shm`
4. Restart MBAS

#### Problem: "Disk I/O error"

**Cause**: Insufficient disk space or corrupted database

**Solution**:
1. Free up disk space (minimum 500 MB)
2. Run database integrity check:
   ```cmd
   sqlite3 backend\mbas.db "PRAGMA integrity_check;"
   ```
3. If corrupted, restore from backup

### Performance Issues

#### Problem: "Slow product search"

**Cause**: Database needs optimization

**Solution**:
```cmd
cd backend
python -c "import sqlite3; conn = sqlite3.connect('mbas.db'); conn.execute('VACUUM'); conn.close()"
```

#### Problem: "High memory usage"

**Cause**: Large dataset or memory leak

**Solution**:
1. Restart MBAS regularly (daily for heavy use)
2. Archive old invoices (move to separate database)
3. Upgrade RAM to 8 GB if processing > 10,000 products

---

## 🗑️ Uninstallation

### Complete Removal

1. **Stop MBAS**:
   - Right-click system tray icon → Exit MBAS
   - Or run `STOP_MBAS.bat`

2. **Backup Data** (if needed):
   - Copy `backend\mbas.db` to safe location
   - Copy `backend\backups\` folder

3. **Delete Installation Folder**:
   ```cmd
   rmdir /s /q C:\MBAS
   ```

4. **Remove Desktop Shortcut**:
   - Delete "MBAS" icon from desktop

5. **Clean Registry** (optional):
   - No registry entries created by MBAS
   - No system files modified

### Data Retention

After uninstallation, you can:
- Keep `mbas.db` file for data archive
- Import into new MBAS installation
- Query using any SQLite viewer

---

## 📞 Support & Resources

### Documentation

- **User Manual**: `USER_MANUAL.md` (end-user guide)
- **System Preview**: `SYSTEM_PREVIEW.md` (feature overview)
- **API Documentation**: http://localhost:8000/docs (when running)

### Common Issues

- **Path Fix**: See `PATH_FIX_v1.0.7_FINAL.md`
- **First-Click Reliability**: See `FIRST_CLICK_FIX_v1.0.7.md`
- **Currency Display**: See `CURRENCY_FIX_SUPPLIERS_PURCHASES.md`

### Logs

Check logs for detailed error information:
- Backend logs: `backend\logs\app.log`
- Installation logs: `installation.log`

### Quick Diagnostics

Run health check anytime:
```cmd
HEALTH_CHECK.bat
```

Or manual check:
```cmd
python -c "import sys; print(f'Python: {sys.version}'); import sqlite3; print(f'SQLite: {sqlite3.sqlite_version}')"
```

---

## 📊 Installation Verification Checklist

Use this checklist after installation:

### System Verification
- [ ] Python 3.11+ installed and in PATH
- [ ] SQLite3 functional
- [ ] Virtual environment created
- [ ] Backend dependencies installed
- [ ] System tray dependencies installed
- [ ] Desktop shortcut created

### Functional Verification
- [ ] MBAS launches without errors
- [ ] System tray icon appears
- [ ] Browser opens automatically
- [ ] Login page loads
- [ ] Can login with admin/admin123
- [ ] Dashboard displays correctly
- [ ] Can create test invoice
- [ ] Can add test product
- [ ] Can run health check

### Security Verification
- [ ] Default password changed
- [ ] Additional user accounts created
- [ ] Role-based access working
- [ ] Backup system configured
- [ ] Database file permissions correct

---

**Installation Guide Version**: 1.0.7
**Last Updated**: April 28, 2026
**Status**: Production-Ready
**Next Review**: July 2026
