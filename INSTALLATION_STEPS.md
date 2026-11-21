# MBAS v2.0.7 - Installation Steps

## Quick Start

Just run this batch file from the project root:
```
BUILD_AND_INSTALL_v2.0.7.bat
```

It will guide you through all steps automatically.

---

## Manual Steps (if you prefer)

### Step 1: Build the Installer (2 minutes)

**Option A - Use the build script:**
```batch
cd deployment\build_installer
REBUILD_INSTALLER_v2.0.7.bat
```

**Option B - Run directly:**
```batch
cd deployment\build_installer
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" MBAS_Installer_Professional_ZT_v2.0.7.iss
```

**Result:**
Installer created at:
```
deployment\build_installer\output\MBAS_Professional_Setup_v2.0.7_ZT_Technologies.exe
```

### Step 2: Uninstall Old Version (1 minute)

**Method 1 - Windows Settings:**
1. Press `Win + I` to open Settings
2. Go to: Apps → Installed apps
3. Search for "MBAS"
4. Click the 3 dots → Uninstall
5. Click "Uninstall" again
6. Wait for completion

**Method 2 - Control Panel:**
1. Press `Win + R`
2. Type: `appwiz.cpl`
3. Find "MBAS - Modern Business Automation System"
4. Click "Uninstall"
5. Wait for completion

**Method 3 - Direct uninstaller:**
```
C:\Program Files\MBAS\unins000.exe
```

**IMPORTANT:** Your data is safe!
- Database: `C:\ProgramData\MBAS\data\mbas_database.db` (preserved)
- Backups: `C:\ProgramData\MBAS\data\backups\` (preserved)

### Step 3: Install New Version (3-5 minutes)

1. **Run the installer:**
   ```
   deployment\build_installer\output\MBAS_Professional_Setup_v2.0.7_ZT_Technologies.exe
   ```

2. **Follow the wizard:**
   - Click "Next"
   - Accept license
   - Choose installation location (default: C:\Program Files\MBAS)
   - ✅ Check "Create desktop shortcut" (optional)
   - ❌ Uncheck "Start MBAS with Windows" (optional)
   - Click "Install"

3. **Wait for installation:**
   - Files are copied (~2 minutes)
   - Python virtual environment created
   - Dependencies installed
   - Database initialized **with categories!** ✅
   - Server starts automatically

4. **First launch:**
   - ✅ Check "Launch MBAS" (should be checked)
   - Click "Finish"
   - Browser opens automatically
   - System tray icon appears

### Step 4: Verify the Fixes (1 minute)

**Test 1: Categories Created ✅**
1. Login: `admin` / `admin123`
2. Go to: Products → Add Product
3. Click the "Category" dropdown
4. **Expected:** See 4 categories:
   - Electronics
   - Groceries
   - Clothing
   - Stationery

**Test 2: No CMD Windows ✅**
1. Watch during startup
2. **Expected:** No black command windows appear
3. Only system tray icon visible
4. Check Task Manager:
   - Should see: `pythonw.exe` processes
   - Should NOT see: `python.exe` processes

**Test 3: Basic Functionality ✅**
1. Add a test product with category
2. Create a test sale
3. Check dashboard
4. Verify everything works

---

## Troubleshooting

### Build Fails?

**Check Inno Setup:**
```batch
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /?
```
If not found, download from: https://jrsoftware.org/isdl.php

**Check Frontend:**
```batch
dir frontend\dist\index.html
```
If missing, build it:
```batch
cd frontend
npm install
npm run build
```

### Categories Still Missing?

**Check database:**
```
C:\ProgramData\MBAS\data\mbas_database.db
```

**Manual fix:**
```batch
cd "C:\Program Files\MBAS\backend"
"C:\ProgramData\MBAS\venv\Scripts\python.exe" -c "from src.scripts.init_db import bootstrap; bootstrap()"
```

**Or use the fix script:**
```batch
deployment\build_installer\APPLY_FIX_TO_EXISTING_INSTALLATION.bat
```

### CMD Windows Still Appear?

**Check process:**
1. Open Task Manager (Ctrl+Shift+Esc)
2. Look for MBAS processes
3. **Should be:** pythonw.exe
4. **Should NOT be:** python.exe

**Check logs:**
```
C:\ProgramData\MBAS\logs\mbas_tray.log
```

Look for: `Using pythonw: C:\ProgramData\MBAS\venv\Scripts\pythonw.exe`

### Installation Hangs?

**Check Python:**
```batch
python --version
```
Must be Python 3.11 or 3.12

**Check logs:**
```
C:\ProgramData\MBAS\logs\install_log.txt
C:\Program Files\MBAS\install_log.txt
```

**Force stop and retry:**
```batch
taskkill /F /IM python.exe /T
taskkill /F /IM pythonw.exe /T
```
Then reinstall.

---

## What Gets Preserved During Reinstall?

✅ **Kept:**
- All products
- All sales
- All customers
- All suppliers
- All purchases
- All settings
- All backups
- Database file

❌ **Removed:**
- Old program files
- Old virtual environment
- Old log files
- Old installation files

**Database Location (never touched):**
```
C:\ProgramData\MBAS\data\mbas_database.db
```

---

## After Installation

### Default Login
- **Username:** admin
- **Password:** admin123

### Access URLs
- **Main App:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Data Locations
- **Database:** `C:\ProgramData\MBAS\data\mbas_database.db`
- **Backups:** `C:\ProgramData\MBAS\data\backups\`
- **Logs:** `C:\ProgramData\MBAS\logs\`
- **Config:** `C:\ProgramData\MBAS\data\config\`

### System Tray
- **Right-click icon** for menu:
  - Open MBAS
  - Start Server
  - Stop Server
  - Status
  - Exit

### Shortcuts Created
- **Start Menu:** MBAS - Modern Business Automation System
- **Desktop:** MBAS (if checked during install)
- **Startup:** MBAS (if checked during install)

---

## Support

**If you encounter issues:**

📧 Email: zttechnologies12@gmail.com
🌐 Website: www.zttechnologies.org

**Include:**
1. MBAS version (v2.0.7)
2. Windows version
3. Python version
4. Log files from `C:\ProgramData\MBAS\logs\`

---

**Z&T Technologies**
*State-of-the-Art Business Solutions*

---

**End of Installation Guide**
