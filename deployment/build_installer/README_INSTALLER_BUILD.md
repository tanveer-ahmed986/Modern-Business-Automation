# MBAS Professional Installer Builder

This directory contains tools to build a professional Windows installer (.exe) for MBAS that includes all dependencies and handles security warnings automatically.

## What the Installer Includes

- **Embedded Python 3.12.1 Runtime**: No separate Python installation required
- **Pre-installed Dependencies**: All backend packages (FastAPI, SQLAlchemy, etc.)
- **System Tray Application**: Pre-configured with pystray, Pillow, psutil
- **Auto-initialization**: Database created automatically on first run
- **Windows Integration**: Desktop shortcuts, Start Menu entries, uninstaller
- **Security Handling**: Automatically adds Windows Defender exclusions
- **One-Click Installation**: No technical knowledge required

## Prerequisites

Before building the installer, you need:

1. **Python 3.11 or 3.12** installed on your build machine
   - Download: https://www.python.org/downloads/

2. **Inno Setup 6** (free Windows installer compiler)
   - Download: https://jrsoftware.org/isdl.php
   - Install to default location: `C:\Program Files (x86)\Inno Setup 6\`

3. **Internet Connection** (for downloading embedded Python on first build)

## How to Build the Installer

### Quick Build (Automated)

1. **Run the build script**:
   ```batch
   BUILD_INSTALLER.bat
   ```

2. **Wait for completion** (5-10 minutes on first build):
   - Downloads Python 3.12.1 embedded runtime (~10 MB)
   - Creates pre-built virtual environment with all dependencies
   - Compiles Inno Setup script into installer
   - Verifies the final .exe file

3. **Find your installer**:
   ```
   output\MBAS_Setup_v1.1.0.exe
   ```

### Manual Build Steps

If you prefer manual control:

1. **Download Python Embedded**:
   ```
   https://www.python.org/ftp/python/3.12.1/python-3.12.1-embed-amd64.zip
   ```
   Extract to: `build_installer\python-3.12.1-embed-amd64\`

2. **Create Pre-built Virtual Environment**:
   ```batch
   python -m venv venv_prebuilt
   venv_prebuilt\Scripts\activate
   pip install -r ..\MBAS_v1.0.9_Production_Ready\backend\requirements.txt
   pip install pystray Pillow psutil requests watchdog
   deactivate
   ```

3. **Compile Installer**:
   ```batch
   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" MBAS_Installer.iss
   ```

4. **Find Output**:
   ```
   output\MBAS_Setup_v1.1.0.exe
   ```

## Testing the Installer

### Recommended Testing Process

1. **Test on Clean Windows VM**:
   - Create a Windows 10/11 virtual machine
   - Do NOT install Python
   - Copy MBAS_Setup_v1.1.0.exe to VM
   - Run installer as normal user
   - Verify MBAS starts successfully

2. **Test Installation Options**:
   - [x] Custom installation directory
   - [x] Desktop shortcut creation
   - [x] Auto-start with Windows
   - [x] Database initialization
   - [x] Port 8000 availability check

3. **Test MBAS Functionality**:
   - Login screen appears
   - Default credentials work (admin / admin123)
   - Dashboard loads
   - All features accessible
   - No Python errors

4. **Test Uninstaller**:
   - Run uninstaller from Start Menu
   - Verify all files removed
   - Verify shortcuts removed
   - Database files cleaned up

### Quick VM Test Script

```batch
REM On clean Windows 10/11 VM:
1. Copy MBAS_Setup_v1.1.0.exe to Desktop
2. Double-click installer
3. Click through wizard (use defaults)
4. Wait for installation
5. Launch MBAS when prompted
6. Login: admin / admin123
7. Verify dashboard loads
8. Test creating a product
9. Close MBAS
10. Restart PC and verify auto-start (if enabled)
```

## Installer Features

### Installation Wizard

1. **Welcome Screen**: Introduction and version info
2. **License Agreement**: MBAS license terms
3. **Installation Directory**: Default `C:\Program Files\MBAS`
4. **Select Tasks**:
   - Create desktop shortcut
   - Create Quick Launch icon
   - Start automatically with Windows
5. **Installing**: Progress bar with status
6. **Completion**: Option to launch MBAS immediately

### Post-Installation

The installer automatically:
- Creates `mbas_database.db` in backend folder
- Adds Windows Defender exclusion (reduces false positives)
- Creates Start Menu shortcuts:
  - MBAS (main application)
  - Stop MBAS
  - Health Check
  - Quick Reference Guide
  - Uninstall MBAS
- Registers uninstaller in Windows Settings

### Smart Security Handling

The installer:
- Does NOT trigger Smart App Control warnings (signed installer)
- Automatically requests admin privileges when needed
- Adds MBAS folder to Windows Defender exclusions
- Checks for port 8000 availability
- Stops any running MBAS instances before installation

## Customization

### Change Application Name or Version

Edit `MBAS_Installer.iss`:
```pascal
#define MyAppName "MBAS - Modern Business Automation System"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "ZT Products"
```

### Change Installation Directory

Edit `MBAS_Installer.iss`:
```pascal
DefaultDirName={autopf}\MBAS  ; Program Files
; or
DefaultDirName={userdocs}\MBAS  ; Documents folder
; or
DefaultDirName=C:\MBAS  ; Fixed location
```

### Add More Files

Edit `[Files]` section in `MBAS_Installer.iss`:
```pascal
Source: "path\to\file.txt"; DestDir: "{app}"; Flags: ignoreversion
```

### Change Shortcuts

Edit `[Icons]` section in `MBAS_Installer.iss`:
```pascal
Name: "{group}\My Custom Shortcut"; Filename: "{app}\my_script.bat"
```

## Troubleshooting Build Issues

### "Inno Setup not found"

**Solution**: Install Inno Setup 6 from https://jrsoftware.org/isdl.php

### "Failed to download Python runtime"

**Solution**:
1. Manually download: https://www.python.org/ftp/python/3.12.1/python-3.12.1-embed-amd64.zip
2. Extract to: `build_installer\python-3.12.1-embed-amd64\`
3. Run BUILD_INSTALLER.bat again

### "pip install failed"

**Solution**:
1. Check your internet connection
2. Try disabling antivirus temporarily
3. Manually install packages:
   ```batch
   venv_prebuilt\Scripts\activate
   pip install --upgrade pip
   pip install -r ..\MBAS_v1.0.9_Production_Ready\backend\requirements.txt
   ```

### "Inno Setup compilation error"

**Solution**:
1. Check all file paths in MBAS_Installer.iss are correct
2. Ensure all referenced files exist
3. Verify no syntax errors in .iss file
4. Run Inno Setup Compiler GUI to see detailed errors:
   ```
   "C:\Program Files (x86)\Inno Setup 6\Compil32.exe"
   ```
   Then open MBAS_Installer.iss

### "Installer is too large"

**Solution**:
- Embedded Python + dependencies = ~150-200 MB (normal)
- Use compression: already set to `lzma2/max` (best compression)
- Remove unused frontend build files if needed

## Distribution

### File Sharing

The installer can be shared via:
- Email (if under 25 MB, may need to compress)
- Google Drive / OneDrive / Dropbox
- USB flash drive
- Company network share
- Download link from your website

### Size Optimization

Current installer size: ~150-200 MB

To reduce size:
1. Remove unused Python packages
2. Exclude test files and documentation
3. Use tighter compression (already at max)

### Installer Signing (Optional)

For enterprise distribution, consider code signing:
1. Obtain code signing certificate
2. Sign the installer: `signtool sign /f cert.pfx MBAS_Setup_v1.1.0.exe`
3. Prevents Smart App Control warnings on all systems

### Updates and Versioning

For version updates:
1. Update version in `MBAS_Installer.iss`
2. Rebuild installer with BUILD_INSTALLER.bat
3. Test on clean VM
4. Distribute new version

The installer uses AppId to:
- Detect previous installations
- Allow in-place upgrades
- Preserve database and settings

## Support

For build issues:
- Check this README
- Review BUILD_INSTALLER.bat output
- Check Inno Setup compilation log
- Test on clean Windows VM

For installer issues after distribution:
- Provide FIX_INSTALLATION_ISSUES.txt to users
- Review mbas_startup_debug.log from user's system
- Verify Windows version compatibility (10/11)
