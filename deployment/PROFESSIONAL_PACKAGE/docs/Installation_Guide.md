# MBAS Installation Guide

**Z&T Technologies - State-of-the-Art Business Solutions**
**Website:** www.zttechnologies.org

---

## 📋 Pre-Installation Checklist

Before installing MBAS, ensure your system meets these requirements:

### System Requirements
- ✅ Windows 10 or 11 (64-bit)
- ✅ 4GB RAM minimum (8GB recommended)
- ✅ 2GB free disk space
- ✅ Administrator access (for installation)
- ✅ Internet connection (for initial setup)
- ✅ Modern web browser (Chrome, Firefox, or Edge)

### Before You Begin
- [ ] Close all other applications
- [ ] Disable antivirus temporarily (re-enable after installation)
- [ ] Ensure you have administrator privileges
- [ ] Download latest MBAS installer from www.zttechnologies.org

---

## 🚀 Installation Steps

### Step 1: Download Installer

1. Visit **www.zttechnologies.org**
2. Navigate to **Downloads** section
3. Download: `MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe`
4. Save to your **Downloads** folder

**File Size:** Approximately 50-100MB
**Download Time:** 1-5 minutes (depending on connection)

### Step 2: Run Installer

1. Locate downloaded file in your Downloads folder
2. **Right-click** on `MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe`
3. Select **"Run as administrator"**
4. If Windows SmartScreen appears, click **"More info"** then **"Run anyway"**

### Step 3: Installation Wizard

**Welcome Screen:**
- Read the welcome message
- Click **Next** to continue

**Company Information:**
- Learn about Z&T Technologies
- Click **Continue**

**Choose Installation Location:**
- Default: `C:\Program Files\MBAS`
- **Recommended:** Keep default location
- Click **Next**

**Select Components:**
- ✓ MBAS Application (Required)
- ✓ Desktop Shortcut (Recommended)
- ✓ Start Menu Shortcuts (Recommended)
- ☐ Start with Windows (Optional)
- Click **Next**

**Ready to Install:**
- Review installation settings
- Click **Install**

### Step 4: Installation Progress

The installer will now:
1. Copy application files (1 minute)
2. Install Python runtime (1-2 minutes)
3. Install dependencies (2-4 minutes)
4. Initialize database (30 seconds)
5. Configure system settings (30 seconds)

**Total Time:** 5-10 minutes

**DO NOT:**
- Close the installer
- Turn off your computer
- Disconnect from internet

### Step 5: Completion

When installation completes:
1. ✓ Check **"Launch MBAS"**
2. Click **Finish**
3. MBAS will start automatically

---

## 🎯 First Launch

### What to Expect

1. **System Tray Icon Appears**
   - Look for MBAS icon near the clock (system tray)
   - Icon will be **GRAY** for 20-30 seconds (starting)
   - Icon turns **GREEN** when ready

2. **Browser Opens Automatically**
   - Opens to: http://localhost:8000
   - Login page appears
   - May take 30 seconds on first launch (database initialization)

3. **Login Screen**
   - **Username:** admin
   - **Password:** admin123
   - Click **Login**

4. **Dashboard Loads**
   - Welcome message appears
   - Quick setup wizard may launch
   - You're ready to use MBAS!

### If Browser Doesn't Open

Manually open browser and navigate to:
```
http://localhost:8000
```

---

## ⚙️ Post-Installation Setup

### Step 1: Change Default Password
**CRITICAL SECURITY STEP!**

1. Click **Settings** (gear icon)
2. Click **User Management**
3. Click **Change Password**
4. Enter:
   - Current password: `admin123`
   - New password: `[your secure password]`
   - Confirm password
5. Click **Save**

### Step 2: Configure Company Information

1. Go to **Settings** → **Company Settings**
2. Enter your business details:
   - Company name
   - Address
   - Phone/Email
   - Tax ID
   - Logo (optional)
3. Click **Save**

### Step 3: Set Currency

1. Go to **Settings** → **System Settings**
2. Select **Currency** tab
3. Choose your default currency
4. Set exchange rates (if using multiple currencies)
5. Click **Save**

### Step 4: Configure Tax

1. Go to **Settings** → **Tax Configuration**
2. Add your tax rates:
   - Tax name (e.g., "VAT", "Sales Tax")
   - Tax percentage
   - Applicable to (Sales/Purchases/Both)
3. Click **Save**

### Step 5: Create User Accounts

1. Go to **Settings** → **User Management**
2. Click **Add New User**
3. Enter user details:
   - Username
   - Password
   - Email
   - Role (Admin/Manager/Sales User)
4. Click **Save**
5. Repeat for all users

### Step 6: Set Up Automatic Backups

1. Go to **Settings** → **Backup Settings**
2. Enable **Automatic Backups**
3. Set backup frequency (Daily recommended)
4. Set backup location
5. Click **Save**

---

## 🔐 Security Recommendations

### After Installation:

1. **Change Default Password** (CRITICAL!)
2. **Create Individual User Accounts** (don't share admin account)
3. **Enable Windows Firewall** exception for MBAS
4. **Add Antivirus Exclusion** for MBAS folder
5. **Enable Automatic Backups**
6. **Keep Software Updated**

### Windows Firewall Configuration

MBAS uses port 8000 locally. No firewall configuration needed for local use.

If accessing from other computers (network mode):
1. Open Windows Firewall settings
2. Add inbound rule for port 8000
3. Allow TCP connections
4. Name rule: "MBAS Server"

### Antivirus Exclusion

Add this folder to antivirus exclusions:
```
C:\Program Files\MBAS\
```

**Why?** Some antivirus software may slow down MBAS or block database operations.

---

## 🔄 Network Installation (Multiple Computers)

### Server Installation

1. Install MBAS on **one main computer** (server)
2. Note the server's IP address:
   - Open Command Prompt
   - Type: `ipconfig`
   - Note IPv4 Address (e.g., 192.168.1.100)

3. Configure MBAS for network mode:
   - Go to **Settings** → **Network**
   - Enable **"Allow Network Access"**
   - Note the access URL (e.g., http://192.168.1.100:8000)

4. Configure Windows Firewall (see above)

### Client Installation

On other computers (clients):

1. **DO NOT** install MBAS
2. Just open web browser
3. Navigate to server URL: `http://[server-ip]:8000`
4. Login with your credentials

**Note:** Server computer must be running for clients to access MBAS.

---

## ❗ Troubleshooting Installation

### Installation Fails

**Problem:** "Installation failed" error

**Solutions:**
1. Run installer as Administrator
2. Disable antivirus temporarily
3. Ensure enough disk space (2GB free)
4. Close all other applications
5. Restart computer and try again

### Python Installation Fails

**Problem:** "Python runtime error"

**Solutions:**
1. Manually install Python 3.11 or 3.12 from python.org
2. During installation, check **"Add Python to PATH"**
3. Restart installer

### Dependencies Installation Fails

**Problem:** "Failed to install dependencies"

**Solutions:**
1. Check internet connection
2. Disable firewall temporarily
3. Try different network (if using VPN, disconnect)
4. Run Command Prompt as Admin:
   ```
   cd "C:\Program Files\MBAS"
   python -m pip install -r backend\requirements.txt
   ```

### Database Initialization Fails

**Problem:** "Database error"

**Solutions:**
1. Ensure you have write permissions to installation folder
2. Check disk space
3. Run as Administrator
4. Manually initialize:
   ```
   cd "C:\Program Files\MBAS\backend"
   python src\scripts\init_db.py
   ```

### MBAS Won't Start After Installation

**Problem:** No system tray icon appears

**Solutions:**
1. Manually launch: `C:\Program Files\MBAS\MBAS.exe`
2. Check Task Manager for pythonw.exe process
3. Check logs: `C:\Program Files\MBAS\mbas_tray.log`
4. Restart computer
5. Reinstall MBAS

### Port 8000 Already in Use

**Problem:** "Port 8000 is already in use"

**Solutions:**
1. Find what's using port 8000:
   ```
   netstat -ano | findstr :8000
   ```
2. Stop that application
3. Or change MBAS port in settings

---

## 🔧 Advanced Installation Options

### Custom Installation Path

If you want to install to a different location:

1. During installation, click **Browse**
2. Select different folder
3. **Recommended locations:**
   - `C:\MBAS` (faster, no UAC prompts)
   - `D:\Programs\MBAS` (if C: drive is full)

**NOT recommended:**
- Desktop (too cluttered)
- Documents (backed up by OneDrive)
- System folders (requires admin for every operation)

### Silent Installation (IT Admins)

For deploying to multiple computers:

```cmd
MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe /SILENT /DIR="C:\MBAS" /NOICONS
```

Parameters:
- `/SILENT` - No UI, automatic installation
- `/VERYSILENT` - Complete silent mode
- `/DIR="path"` - Custom installation directory
- `/NOICONS` - Don't create desktop icons
- `/TASKS="!startupicon"` - Don't start with Windows

### Unattended Installation Script

```batch
@echo off
REM MBAS Silent Installation Script
REM Z&T Technologies

echo Installing MBAS...

MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe ^
  /VERYSILENT ^
  /NORESTART ^
  /DIR="C:\MBAS" ^
  /LOG="C:\MBAS_Install.log"

echo Installation complete!
echo Check log: C:\MBAS_Install.log
pause
```

---

## 📞 Installation Support

### Need Help?

If you encounter issues during installation:

**Email:** zttechnologies12@gmail.com
**Subject:** MBAS Installation Issue

**Include:**
1. Windows version (run `winver`)
2. Error message (screenshot)
3. Installation log (if available)
4. Steps you've tried

**Response Time:**
- Standard: Within 24 hours
- Premium: Within 4 hours
- Emergency: Within 1 hour (Premium only)

### Remote Installation Assistance

Available for Premium license holders:
- Schedule remote session
- Our technician will install and configure
- Includes staff training
- Contact: zttechnologies12@gmail.com

---

## ✅ Installation Checklist

After installation, verify:

- [ ] MBAS icon in system tray (green)
- [ ] Can access http://localhost:8000
- [ ] Can login with admin/admin123
- [ ] Dashboard loads without errors
- [ ] Changed default password
- [ ] Configured company information
- [ ] Set up user accounts
- [ ] Enabled automatic backups
- [ ] Created desktop shortcut works
- [ ] All features accessible

If all checked: **Installation Successful!** 🎉

---

## 🎓 Next Steps

After successful installation:

1. **Watch Tutorial Videos** - www.zttechnologies.org/tutorials
2. **Read User Guide** - Comprehensive feature documentation
3. **Import Initial Data** - Products, customers, suppliers
4. **Train Your Staff** - Schedule training session
5. **Start Using MBAS** - Begin automating your business!

---

**Thank you for choosing MBAS!**

**Z&T Technologies**
*State-of-the-Art Business Solutions*
www.zttechnologies.org

---

*Installation Guide v2.0.0 - May 2026*
