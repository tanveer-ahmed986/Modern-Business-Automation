# MBAS Installation Guide

## System Requirements

### Minimum Requirements

- **Operating System**: Windows 10 (64-bit) or Windows 11
- **RAM**: 4 GB
- **Disk Space**: 5 GB free (10 GB recommended with AI model)
- **Processor**: Intel Core i3 or equivalent (2 GHz+)
- **Display**: 1280x720 resolution minimum

### Recommended Requirements

- **RAM**: 8 GB or more
- **Disk Space**: 10 GB+ free
- **Processor**: Intel Core i5 or equivalent (2.5 GHz+)
- **Display**: 1920x1080 resolution

### Prerequisites

- **.NET Framework**: 4.7.2 or later (usually pre-installed on Windows 10/11)
- **Administrator Access**: Required for initial installation

## Installation Steps

### Step 1: Download Installer

1. Obtain the MBAS installer file: `MBAS_1.0.0_x64.msi`
2. Save to a location you can easily access (e.g., Downloads folder)
3. Verify file size (should be ~50-100 MB without AI model)

### Step 2: Run Installer

1. **Right-click** on `MBAS_1.0.0_x64.msi`
2. Select **"Run as administrator"**
3. If User Account Control (UAC) prompts appear, click **"Yes"**

### Step 3: Installation Wizard

1. **Welcome Screen**
   - Click **"Next"** to continue

2. **License Agreement**
   - Read the End User License Agreement (EULA)
   - Check **"I accept the terms"**
   - Click **"Next"**

3. **Installation Location**
   - Default: `C:\Program Files\MBAS\`
   - Click **"Browse"** to change (not recommended)
   - Click **"Next"**

4. **Select Features** (Optional)
   - **MBAS Application** (required)
   - **Desktop Shortcut** (recommended)
   - **Start Menu Shortcut** (recommended)
   - Click **"Next"**

5. **Ready to Install**
   - Review settings
   - Click **"Install"**
   - Installation takes 2-5 minutes

6. **Completion**
   - Click **"Finish"**
   - Choose **"Launch MBAS"** (optional)

### Step 4: Install License File

**IMPORTANT:** MBAS requires a valid license file to activate all features.

1. Locate your `.mbas-license` file (provided by your vendor)
2. **Option A: Automated Installation (Recommended)**
   ```
   - Right-click the .mbas-license file
   - Select "Install for MBAS" (if available)
   - Follow prompts
   ```

3. **Option B: Manual Installation**
   ```
   System-wide (requires admin):
   C:\ProgramData\MBAS\mbas.license

   User-specific (no admin required):
   C:\Users\YOUR_USERNAME\AppData\Local\MBAS\mbas.license
   ```

4. **Option C: Using Installation Tool**
   ```cmd
   cd "C:\Program Files\MBAS\tools"
   python install_license.py path\to\your-license.mbas-license --location system
   ```

### Step 5: First Launch

1. **Launch MBAS**
   - Double-click desktop shortcut, or
   - Start Menu → MBAS

2. **License Validation**
   - Application verifies license on startup
   - You'll see: "License validated: [Your Business Name]"
   - If validation fails, check license file location

3. **Database Initialization**
   - First launch creates database automatically
   - Location: `C:\ProgramData\MBAS\mbas.db`
   - Takes ~10-30 seconds

4. **Login Screen**
   - Default credentials:
     - **Username**: `admin`
     - **Password**: `admin123`
   - Click **"Sign In"**

### Step 6: Initial Setup

1. **Change Default Password** (CRITICAL)
   - Go to **Settings** → **Users**
   - Click on **admin** user
   - Click **"Change Password"**
   - Enter new secure password
   - Click **"Save"**

2. **Configure Business Settings**
   - Go to **Settings** → **General**
   - Update:
     - Business Name
     - Tax Rate (%)
     - Currency
     - Logo (optional)
   - Click **"Save Settings"**

3. **Add Product Categories** (Optional)
   - Go to **Inventory** → **Categories**
   - Click **"Add Category"**
   - Create your initial categories

4. **Create Additional Users** (Optional)
   - Go to **Settings** → **Users**
   - Click **"Add User"**
   - Fill in details:
     - Username
     - Full Name
     - Password
     - Role (Admin/Manager/Sales User)
   - Click **"Create User"**

## Package Tiers

MBAS offers three tiers based on your license:

### Basic Package
- ✅ Dashboard
- ✅ Inventory Management
- ✅ Billing/Sales (POS)
- ✅ Customer Management
- ❌ Suppliers & Purchases
- ❌ Advanced Reports
- ❌ Backup & Restore
- ❌ AI Features

### Standard Package
- ✅ All Basic features
- ✅ Suppliers & Purchases
- ✅ Advanced Reports (Monthly, Product-wise)
- ✅ Backup & Restore
- ❌ Profit & Loss Reports
- ❌ AI Features

### Premium Package
- ✅ All Standard features
- ✅ Profit & Loss Reports
- ✅ AI Sales Forecasting
- ✅ AI Natural Language Queries
- ✅ Advanced Analytics

To upgrade your tier, contact your vendor for a new license file.

## Troubleshooting

### Installation Issues

**Error: "Installation failed - Error 1603"**
- **Solution**: Run installer as administrator
- Ensure no other MBAS version is running
- Disable antivirus temporarily

**Error: "License file not found"**
- **Solution**: Install license file to correct location
- See Step 4 above
- Verify file extension is `.mbas-license`

**Error: "License signature invalid"**
- **Solution**: Re-download license file from vendor
- Do not edit license file manually
- Contact vendor if issue persists

### Startup Issues

**Application won't start**
- Check Windows Event Viewer for errors
- Verify .NET Framework 4.7.2+ installed
- Restart computer

**"Database locked" error**
- Close any other MBAS instances
- Delete `mbas.db-shm` and `mbas.db-wal` files (if present)
- Restart application

**Login screen doesn't appear**
- Check backend is running (should start automatically)
- Look for `mbas-backend.exe` in Task Manager
- Check logs in `C:\ProgramData\MBAS\logs\`

### License Issues

**Features are disabled/grayed out**
- Verify license tier supports the feature
- Check license expiry date
- Re-install license file
- Contact vendor for upgrade

**"License expired" message**
- License has reached expiry date
- Contact vendor for license renewal
- Provide your business name and current license details

## Uninstallation

### Standard Uninstall

1. Open **Settings** → **Apps**
2. Find **MBAS** in the list
3. Click **"Uninstall"**
4. Follow prompts
5. Choose to keep or remove data

### Complete Removal

To remove all data and settings:

1. Uninstall application (above)
2. Delete data directories:
   ```
   C:\ProgramData\MBAS\
   C:\Users\YOUR_USERNAME\AppData\Local\MBAS\
   ```
3. (Optional) Remove desktop/start menu shortcuts

### Data Backup Before Uninstall

**IMPORTANT**: Back up your data before uninstalling!

1. Go to **Settings** → **System**
2. Click **"Create Backup"**
3. Save backup file to safe location
4. To restore later: Click **"Restore Backup"** and select file

## Network Installation (Optional)

For multi-user setups with shared database:

1. Install MBAS on a server/main computer
2. Share the database directory:
   - `C:\ProgramData\MBAS\` → Share with read/write permissions
3. On client computers:
   - Install MBAS normally
   - Configure database path in settings to point to shared location
   - Requires network connectivity

**Note**: Advanced feature - contact support for assistance.

## Support

### Getting Help

- **User Manual**: See `user-manual.md` for feature documentation
- **Admin Guide**: See `admin-guide.md` for advanced configuration
- **Vendor Support**: Contact your license vendor
- **Email**: support@mbas.local (if available)

### Before Contacting Support

Please have ready:
- MBAS version number (Settings → About)
- License tier (Basic/Standard/Premium)
- Error messages or screenshots
- Steps to reproduce the issue

## Next Steps

After installation:

1. ✅ Read the **User Manual** (`user-manual.md`)
2. ✅ Configure business settings
3. ✅ Create user accounts
4. ✅ Add initial inventory
5. ✅ Process your first sale
6. ✅ Review available reports

Welcome to MBAS! 🎉
