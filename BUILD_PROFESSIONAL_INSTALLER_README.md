# Building MBAS Professional Installer

**Z&T Technologies - State-of-the-Art Business Solutions**
**Website:** www.zttechnologies.org

---

## Overview

This guide explains how to build a **professional, distribution-ready** MBAS installer for end users with:

✅ **Windows .exe installer** (not .bat files)
✅ **Z&T Technologies branding** throughout
✅ **No CMD windows** (system tray mode)
✅ **Professional appearance**
✅ **Easy installation** for customers

---

## Prerequisites

Before building, ensure you have:

1. **Python 3.11 or 3.12** installed
2. **Node.js** installed (for frontend build)
3. **Inno Setup 6** - Download from: https://jrsoftware.org/isdl.php
4. **Git** (optional, for version control)

---

## Quick Build (5 Steps)

### Step 1: Build Frontend

```cmd
cd frontend
npm install
npm run build
```

This creates: `frontend/dist/` with production build

### Step 2: Copy Icon

```cmd
copy mbas_icon.ico deployment\build_installer\mbas_icon.ico
```

### Step 3: Run Build Script

```cmd
cd deployment\build_installer
BUILD_INSTALLER_FINAL_ZT.bat
```

### Step 4: Compile Installer

Open **Inno Setup** and compile:
```
deployment\build_installer\MBAS_Installer_Professional_ZT.iss
```

### Step 5: Test Installer

The installer will be created at:
```
deployment\build_installer\output\MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe
```

Test on a clean Windows machine!

---

## Detailed Build Process

### Building the Frontend

The frontend must be built into static files:

```cmd
cd D:\gemini_modern_business_automation_system\frontend

# Install dependencies (first time only)
npm install

# Build production bundle
npm run build
```

**Output:** `frontend/dist/` folder with:
- `index.html`
- `assets/` folder containing:
  - JavaScript bundles (`.js`)
  - CSS stylesheets (`.css`)

**Verify:** Check that `frontend/dist/assets/` contains files like:
- `index-[hash].js`
- `index-[hash].css`

### Preparing the Package

The installer packages these components:

```
MBAS Package Structure:
├── backend/                 # Python FastAPI backend
│   ├── src/                # Application code
│   ├── requirements.txt    # Dependencies
│   └── mbas_database.db    # (created on first run)
├── frontend/               # React frontend
│   └── dist/              # Built production files
├── scripts/               # Launcher and utility scripts
├── mbas_icon.ico         # Application icon
└── mbas.license          # License file
```

### Creating the Installer

#### Option A: Using Automated Script

```cmd
cd deployment\build_installer
BUILD_COMPLETE_PROFESSIONAL_PACKAGE.bat
```

This will:
1. Build frontend automatically
2. Copy all files to staging area
3. Apply Z&T Technologies branding
4. Launch Inno Setup compiler

#### Option B: Manual Build

1. **Open Inno Setup**
2. **Open file:** `MBAS_Installer_Professional_ZT.iss`
3. **Click:** Build → Compile
4. **Wait** for compilation (2-5 minutes)
5. **Find installer** in: `output/` folder

---

## Installer Features

The professional installer includes:

### Branding
- ✅ Z&T Technologies company name
- ✅ "State-of-the-Art Business Solutions" tagline
- ✅ Website: www.zttechnologies.org
- ✅ Professional installer wizard
- ✅ Company info page during installation

### Installation Process
- ✅ Checks for Python 3.11/3.12
- ✅ Creates virtual environment
- ✅ Installs all dependencies automatically
- ✅ Initializes database
- ✅ Creates desktop shortcut
- ✅ Adds Start Menu entries
- ✅ Optional auto-start with Windows

### End-User Experience
- ✅ No CMD windows (runs in system tray)
- ✅ Auto-opens browser on first launch
- ✅ Professional icon in system tray
- ✅ Easy uninstall process
- ✅ Automatic updates (future feature)

---

## Customizing Branding

### Update Company Information

Edit: `deployment\build_installer\MBAS_Installer_Professional_ZT.iss`

```pascal
#define MyAppPublisher "Z&T Technologies"
#define MyAppURL "https://www.zttechnologies.org"
#define MyCompanySlogan "State-of-the-Art Business Solutions"
```

### Update Backend Branding

Already updated in: `backend/src/main.py`

```python
app = FastAPI(
    title="MBAS API - Z&T Technologies",
    version="2.0.0",
    description="Modern Business Automation System - A Product of Z&T Technologies | State-of-the-Art Business Solutions | www.zttechnologies.org",
    contact={
        "name": "Z&T Technologies Support",
        "url": "https://www.zttechnologies.org",
        "email": "zttechnologies12@gmail.com"
    }
)
```

### Update Frontend Branding

Edit: `frontend/src/App.tsx` or relevant components

Add footer:
```tsx
<footer>
  <p>A Product of Z&T Technologies</p>
  <p>State-of-the-Art Business Solutions</p>
  <a href="https://www.zttechnologies.org">www.zttechnologies.org</a>
</footer>
```

---

## Testing the Installer

### Test Environment

**CRITICAL:** Test on a **clean** Windows machine that:
- Has **NO** Python installed
- Has **NO** MBAS installed previously
- Is a **fresh** Windows 10 or 11 installation

### Testing Checklist

- [ ] Installer runs without errors
- [ ] Python check works (prompts if missing)
- [ ] Dependencies install successfully
- [ ] Database initializes properly
- [ ] Desktop shortcut created
- [ ] Start Menu shortcuts created
- [ ] MBAS launches successfully
- [ ] No CMD windows appear
- [ ] System tray icon shows (green)
- [ ] Browser opens to http://localhost:8000
- [ ] Login page loads with proper styling
- [ ] Can login with admin/admin123
- [ ] All features work correctly
- [ ] Uninstaller works properly
- [ ] No files left after uninstall

### Testing on Virtual Machine

**Recommended:** Use VMware/VirtualBox with Windows 10/11:

1. Create clean Windows VM
2. Take snapshot
3. Install MBAS
4. Test all features
5. Uninstall MBAS
6. Revert to snapshot
7. Test again with different settings

---

## Distribution

### Preparing for Release

1. **Test thoroughly** (see Testing Checklist)
2. **Rename installer:**
   ```
   MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe
   ```
3. **Create checksums:**
   ```cmd
   certutil -hashfile MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe SHA256 > checksum.txt
   ```
4. **Sign installer** (optional, requires code signing certificate)
5. **Create release notes**

### Distribution Channels

Upload to:
- ✅ Your website: www.zttechnologies.org/downloads
- ✅ File hosting (Google Drive, Dropbox, etc.)
- ✅ Customer portal
- ✅ Direct email to customers

### Release Package Contents

Include in download package:
```
MBAS_Release_v2.0.0/
├── MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe
├── Installation_Guide.pdf
├── User_Manual.pdf
├── checksum.txt
├── README.txt
└── Release_Notes.txt
```

---

## Troubleshooting Build Issues

### Frontend Build Fails

**Problem:** `npm run build` fails

**Solutions:**
```cmd
# Clean install
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Installer Compilation Fails

**Problem:** Inno Setup shows errors

**Common Issues:**
1. **Missing files** - Check all [Files] paths exist
2. **Icon not found** - Verify `mbas_icon.ico` exists
3. **Syntax errors** - Check for typos in .iss file

### Python Not Detected

**Problem:** Installer doesn't find Python

**Solution:** Update detection logic in .iss:
```pascal
function CheckPython(): Boolean;
```

### Dependencies Installation Fails

**Problem:** `pip install` fails during setup

**Solution:** Check `requirements.txt` is up to date:
```cmd
cd backend
pip freeze > requirements-lock.txt
```

---

## Advanced Configuration

### Silent Installation

For IT departments deploying to multiple PCs:

```cmd
MBAS_Professional_Setup_v2.0.0_ZT_Technologies.exe /SILENT /DIR="C:\MBAS"
```

Parameters:
- `/SILENT` - Silent mode with progress
- `/VERYSILENT` - Completely silent
- `/DIR="path"` - Custom installation directory
- `/NOICONS` - Don't create desktop icons
- `/LOG="file"` - Create installation log

### Custom Installation Path

Users can choose installation location:
- Default: `C:\Program Files\MBAS`
- Recommended: `C:\MBAS` (no admin needed)

### Network Installation

Server mode for multi-user access:
1. Install on one computer (server)
2. Configure firewall for port 8000
3. Enable network access in settings
4. Other PCs access via browser: `http://[server-ip]:8000`

---

## Maintaining the Installer

### Updating Version

When releasing new version:

1. Update version in `MBAS_Installer_Professional_ZT.iss`:
   ```pascal
   #define MyAppVersion "2.1.0"
   ```

2. Update version in `backend/src/main.py`:
   ```python
   app = FastAPI(
       title="MBAS API - Z&T Technologies",
       version="2.1.0",
       ...
   )
   ```

3. Update frontend `package.json`:
   ```json
   {
     "version": "2.1.0"
   }
   ```

4. Create changelog

5. Rebuild installer

### Adding New Features

When adding features:
1. Update backend code
2. Update frontend code
3. Rebuild frontend (`npm run build`)
4. Test locally
5. Rebuild installer
6. Test installer on clean machine
7. Update documentation
8. Release

---

## Support & Contact

**Z&T Technologies**
- **Website:** www.zttechnologies.org
- **Support:** zttechnologies12@gmail.com
- **Sales:** zttechnologies12@gmail.com

For installer build issues:
1. Check this README
2. Review error messages
3. Test on clean VM
4. Contact support with:
   - Build error messages
   - Inno Setup version
   - Windows version
   - Steps to reproduce

---

## Quick Reference

### Build Commands

```cmd
# Build everything
cd deployment\build_installer
BUILD_COMPLETE_PROFESSIONAL_PACKAGE.bat

# Build frontend only
cd frontend
npm run build

# Build installer only
# Open MBAS_Installer_Professional_ZT.iss in Inno Setup and compile
```

### Important Files

| File | Purpose |
|------|---------|
| `MBAS_Installer_Professional_ZT.iss` | Inno Setup script |
| `frontend/dist/` | Built frontend |
| `backend/src/main.py` | Backend with branding |
| `mbas_icon.ico` | Application icon |
| `BUILD_INSTALLER_FINAL_ZT.bat` | Build automation script |

### Default Paths

| Item | Path |
|------|------|
| Installation | `C:\Program Files\MBAS` |
| Database | `C:\Program Files\MBAS\backend\mbas_database.db` |
| Logs | `C:\Program Files\MBAS\backend\*.log` |
| Shortcuts | Desktop + Start Menu |

---

**Thank you for choosing MBAS!**

**Z&T Technologies - State-of-the-Art Business Solutions**

*Build Guide v2.0 - May 2026*
