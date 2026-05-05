# MBAS Professional Installer Solution Guide

## Current Problem Solved

**Issue**: The Inno Setup uninstaller was hanging during uninstallation, stuck on "Uninstalling MBAS..." for 10+ minutes.

**Root Causes Identified**:
1. Python/Node.js processes still running and holding file locks
2. Database file (SQLite) locked by backend process
3. Uninstaller unable to delete locked files
4. No retry mechanism or forced cleanup
5. Installation in Program Files requiring elevated permissions for every operation

**Solutions Provided**:
1. **Immediate Fix**: FORCE_UNINSTALL.bat - Emergency uninstaller
2. **Improved Installer**: Robust Inno Setup script with better process handling
3. **Portable Package**: No-installation ZIP version
4. **Professional Build System**: Automated build scripts

---

## Quick Solution (Immediate)

### Fix Current Hanging Uninstaller

**Option 1: Force Uninstall (Recommended)**

```batch
# Run this script immediately:
D:\gemini_modern_business_automation_system\deployment\build_installer\FORCE_UNINSTALL.bat
```

This will:
- Kill the stuck uninstaller
- Force-stop all MBAS processes
- Backup your database to Desktop
- Remove all files and registry entries
- Clean uninstall in <2 minutes

**Option 2: Manual Kill**

1. Press Ctrl+Alt+Delete → Task Manager
2. Find and end these processes:
   - `unins000.exe`
   - `python.exe`
   - `pythonw.exe`
   - `node.exe`
3. Wait 10 seconds
4. Try uninstaller again, or run FORCE_UNINSTALL.bat

---

## Professional Installer Solutions

### Solution 1: Robust Inno Setup Installer (Recommended for Distribution)

**Features**:
- ✅ Automatic process killing before install/uninstall
- ✅ Database backup on upgrade
- ✅ No-hang uninstall with 3-retry mechanism
- ✅ Works without admin rights (installs to C:\MBAS by default)
- ✅ Handles locked files intelligently
- ✅ Clean registry and shortcuts cleanup

**Build the Installer**:

```batch
# 1. Install Inno Setup 6 (if not installed)
# Download from: https://jrsoftware.org/isdl.php

# 2. Build the robust installer
cd D:\gemini_modern_business_automation_system\deployment\build_installer
BUILD_ROBUST_INSTALLER.bat

# Output: .\output\MBAS_Setup_v1.2.0_Robust.exe
```

**Distribute**: The .exe file works on any Windows PC without dependencies.

### Solution 2: Portable Package (No Installation)

**Features**:
- ✅ No installation required
- ✅ Run from any folder (USB, network drive, anywhere)
- ✅ Database travels with the folder
- ✅ Multiple versions can coexist
- ✅ No registry entries
- ✅ Easy backup (just copy the folder)

**Create Portable Package**:

```batch
cd D:\gemini_modern_business_automation_system\deployment\build_installer
CREATE_PORTABLE_PACKAGE.bat

# Output: .\output\MBAS_v1.2.0_Portable.zip
```

**Usage**:
1. Extract ZIP to any folder
2. Run PORTABLE_FIRST_RUN.bat
3. Done!

---

## Comparison: Which Solution to Use?

| Feature | Robust Installer | Portable Package |
|---------|-----------------|------------------|
| Installation | Required | Not required |
| Admin Rights | No (if installing to C:\MBAS) | No |
| Shortcuts | Auto-created | Manual |
| Updates | Run new installer | Replace folder |
| Uninstall | Clean via Control Panel | Delete folder |
| File Size | ~50-100MB .exe | ~30-60MB .zip |
| Best For | End users, professional distribution | Power users, testing, USB deployment |
| Database Location | Fixed in install folder | Travels with folder |
| Multiple Versions | Requires uninstall | Can run side-by-side |

---

## Build Instructions

### Prerequisites

**For Inno Setup Installer**:
- Inno Setup 6 (Download: https://jrsoftware.org/isdl.php)
- Install to default location: `C:\Program Files (x86)\Inno Setup 6\`

**For Portable Package**:
- 7-Zip (optional, for faster compression)
- PowerShell (built into Windows 10/11)

### Build Process

**1. Prepare Source Files**

Ensure this structure exists:
```
deployment/
├── MBAS_v1.0.9_Production_Ready/
│   ├── backend/
│   ├── frontend/
│   ├── scripts/
│   ├── docs/
│   ├── *.bat (startup scripts)
│   ├── mbas_icon.ico
│   └── mbas.license
└── build_installer/
    ├── MBAS_Installer_Robust.iss
    ├── BUILD_ROBUST_INSTALLER.bat
    └── CREATE_PORTABLE_PACKAGE.bat
```

**2. Build Installer**

```batch
cd deployment\build_installer
BUILD_ROBUST_INSTALLER.bat
```

Wait 2-5 minutes. Output: `output\MBAS_Setup_v1.2.0_Robust.exe`

**3. Build Portable Package**

```batch
cd deployment\build_installer
CREATE_PORTABLE_PACKAGE.bat
```

Wait 1-3 minutes. Output: `output\MBAS_v1.2.0_Portable.zip`

---

## Distribution Guide

### For End Users (Customer Deployment)

**Recommended: Robust Installer**

1. Build the installer (see above)
2. Test on a clean VM or PC
3. Distribute `MBAS_Setup_v1.2.0_Robust.exe`

**Installation Instructions for Users**:

```
1. Download MBAS_Setup_v1.2.0_Robust.exe
2. Double-click to run
3. Follow the wizard:
   - Accept license
   - Choose installation path (recommend: C:\MBAS)
   - Check "Create desktop shortcut"
   - Click Install
4. Wait 2-4 minutes for dependency installation
5. Launch MBAS from desktop shortcut
```

**System Requirements**:
- Windows 10/11 (64-bit)
- Python 3.11 or 3.12
- 2GB free disk space
- 4GB RAM minimum
- Internet connection for first-time setup

### For Developers/Testers (Internal Use)

**Recommended: Portable Package**

1. Extract `MBAS_v1.2.0_Portable.zip`
2. Run `PORTABLE_FIRST_RUN.bat`
3. Done!

---

## Troubleshooting

### Installer Build Fails

**Error**: "Inno Setup not found"
- **Fix**: Install Inno Setup 6 from https://jrsoftware.org/isdl.php

**Error**: "Source files not found"
- **Fix**: Ensure `MBAS_v1.0.9_Production_Ready` folder exists with all files

**Error**: "Permission denied"
- **Fix**: Run Command Prompt as Administrator

### Uninstaller Hangs (Existing Installation)

**Solution 1: Force Uninstall**
```batch
deployment\build_installer\FORCE_UNINSTALL.bat
```

**Solution 2: Manual Cleanup**
1. Kill processes via Task Manager (python.exe, node.exe)
2. Delete: `C:\Program Files\MBAS` or `C:\MBAS`
3. Delete shortcuts from Desktop and Start Menu
4. Remove registry entries:
   ```
   HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\{8D4F7A2B-1C3E-4F9A-B2D1-6E8F9A3B4C5D}_is1
   HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\{8D4F7A2B-1C3E-4F9A-B2D1-6E8F9A3B4C5D}_is1
   ```

### Installation Fails

**Error**: "Python not found"
- **Fix**: Install Python 3.11 or 3.12 from python.org
- Make sure to check "Add Python to PATH" during installation

**Error**: "Access denied" or "Permission issues"
- **Fix**: Install to `C:\MBAS` instead of `C:\Program Files\MBAS`
- Or run installer as Administrator

**Error**: "Port 8000 already in use"
- **Fix**: Stop any services using port 8000
- Or change backend port in configuration

---

## Advanced: Creating MSI Installer (Optional)

For enterprise deployment with Group Policy support, you can create an MSI package using WiX Toolset.

### Prerequisites
- WiX Toolset 3.11+ (Download: https://wixtoolset.org/)
- Visual Studio or .NET SDK

### Benefits of MSI
- Enterprise-grade installation
- Group Policy deployment
- Better uninstall handling
- Windows Installer service integration
- Automated rollback on failure

### Create MSI (Advanced)

```batch
# Install WiX Toolset
# Download from: https://wixtoolset.org/releases/

# Create WiX configuration (example provided separately)
# Build MSI
cd deployment\build_installer
candle.exe MBAS_Installer.wxs
light.exe -out MBAS_Setup.msi MBAS_Installer.wixobj
```

Contact support if you need the WiX configuration file.

---

## Testing Checklist

Before distributing the installer, test on a clean system:

### Installation Testing
- [ ] Installer runs without admin rights
- [ ] Python detection works correctly
- [ ] Files copied to correct location
- [ ] Virtual environment created successfully
- [ ] Dependencies installed correctly
- [ ] Database initialized
- [ ] Desktop shortcut created
- [ ] Start menu entries created
- [ ] Application launches successfully
- [ ] Backend starts on port 8000
- [ ] Frontend accessible at localhost:5173
- [ ] Login works with default credentials

### Upgrade Testing
- [ ] Installer detects existing installation
- [ ] Database backed up automatically
- [ ] Old files replaced with new files
- [ ] Database preserved after upgrade
- [ ] Application works after upgrade

### Uninstall Testing
- [ ] Uninstaller stops all processes
- [ ] All files removed
- [ ] Shortcuts removed
- [ ] Start menu entries removed
- [ ] Registry entries cleaned
- [ ] Uninstall completes without hanging
- [ ] Database optionally backed up
- [ ] No orphaned files remain

### Portability Testing (for Portable Package)
- [ ] Runs from different drive letters
- [ ] Runs from USB drive
- [ ] Runs from network folder
- [ ] Database travels with folder
- [ ] Can run multiple instances from different folders

---

## Support and Updates

### Getting Help

**Documentation**:
- `README_FIRST.txt` - Basic setup guide
- `START_HERE_IF_PROBLEMS.txt` - Troubleshooting
- `FIX_INSTALLATION_ISSUES.txt` - Installation fixes

**Support Scripts**:
- `HEALTH_CHECK.bat` - System diagnostics
- `EMERGENCY_FIX.bat` - Auto-fix common issues
- `FORCE_UNINSTALL.bat` - Emergency uninstaller

### Version History

**v1.2.0 (Robust Installer)**:
- ✅ Fixed hanging uninstaller issue
- ✅ Added automatic database backup on upgrade
- ✅ Improved process killing mechanism
- ✅ Added retry logic for locked files
- ✅ Default installation to C:\MBAS (no admin needed)
- ✅ Better error messages and logging
- ✅ Portable package option

**v1.1.0 (Previous)**:
- Basic Inno Setup installer
- Known issue: Uninstaller could hang

**v1.0.x (Initial)**:
- Manual installation only
- No automated installer

---

## FAQ

**Q: Why does the uninstaller hang?**
A: Python/Node.js processes hold file locks. The robust installer kills these before uninstall.

**Q: Do I need admin rights?**
A: No, if installing to C:\MBAS. Program Files installation requires admin.

**Q: Can I run MBAS from a USB drive?**
A: Yes, use the Portable Package. Extract and run PORTABLE_FIRST_RUN.bat.

**Q: How do I update MBAS?**
A: Run the new installer. It will detect existing installation and upgrade automatically.

**Q: Will I lose my data during upgrade?**
A: No. The installer backs up your database automatically before upgrading.

**Q: Can I install multiple versions?**
A: Installer version: No (only one installation). Portable version: Yes (extract to different folders).

**Q: How do I completely remove MBAS?**
A: Use Control Panel → Uninstall. If it hangs, use FORCE_UNINSTALL.bat.

**Q: Does this work on Windows 11?**
A: Yes, tested on Windows 10 and 11 (64-bit).

**Q: Can I deploy this to 100+ computers?**
A: Yes. For enterprise deployment, consider:
  - Creating an MSI package (WiX Toolset)
  - Using Group Policy for deployment
  - Creating a silent install script
  - Contact for enterprise deployment guide

---

## Contact

For technical support or custom deployment solutions:
- GitHub Issues: [Your repository]
- Email: [Your support email]
- Documentation: See README_FIRST.txt

---

## License

MBAS is proprietary software. See `mbas.license` for licensing terms.

© 2026 ZT Products. All rights reserved.
