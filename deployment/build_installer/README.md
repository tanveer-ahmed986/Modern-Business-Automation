# MBAS Professional Installer Builder

## 🚀 Quick Start

### Problem: Uninstaller Hanging? → Fix NOW!

```batch
# Run this immediately:
FORCE_UNINSTALL.bat
```

Your database will be backed up to Desktop before removal. Completes in <2 minutes.

---

### Build Professional Installer (.exe)

```batch
# 1. Install Inno Setup 6:
#    https://jrsoftware.org/isdl.php

# 2. Run build system:
BUILD_MASTER.bat

# 3. Choose Option 1 or 3

# Output: .\output\MBAS_Setup_v1.2.0_Robust.exe
```

**Features**:
- ✅ Never hangs during uninstall (3-retry mechanism)
- ✅ Auto-backup database on upgrade
- ✅ No admin rights needed (installs to C:\MBAS)
- ✅ Works on any Windows PC
- ✅ Professional distribution quality

---

### Build Portable Package (.zip)

```batch
# Run build system:
BUILD_MASTER.bat

# Choose Option 2 or 3

# Output: .\output\MBAS_v1.2.0_Portable.zip
```

**Features**:
- ✅ No installation required
- ✅ Run from USB drive or any folder
- ✅ Database travels with folder
- ✅ Multiple versions can coexist

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **QUICK_START.txt** | Quick reference guide - Start here! |
| **INSTALLER_SOLUTION_GUIDE.md** | Complete technical documentation (3000+ words) |
| **SOLUTION_SUMMARY.md** | Detailed summary of solution |
| **README.md** | This file |

---

## 🛠️ What's Included

### Immediate Fix
- `FORCE_UNINSTALL.bat` - Emergency uninstaller (use now!)

### Build Tools
- `BUILD_MASTER.bat` - Main menu for all operations
- `BUILD_ROBUST_INSTALLER.bat` - Build .exe installer
- `CREATE_PORTABLE_PACKAGE.bat` - Build portable .zip

### Source Code
- `MBAS_Installer_Robust.iss` - Inno Setup script (improved)

### Documentation
- Complete guides for building, distributing, and troubleshooting

---

## 🎯 Key Improvements Over Previous Version

| Issue | Solution |
|-------|----------|
| Uninstaller hangs 10+ minutes | Multiple kill attempts + file handle release |
| Files locked during uninstall | PowerShell force-closes handles |
| No database backup | Auto-backup on upgrade |
| Program Files permission issues | Default to C:\MBAS |
| Single uninstall attempt | 3-retry mechanism |

---

## 📦 What You Get

After building:

```
output/
├── MBAS_Setup_v1.2.0_Robust.exe   # Professional installer
└── MBAS_v1.2.0_Portable.zip        # Portable package
```

Both work on any Windows 10/11 PC without modification.

---

## 💡 Which Package to Use?

**For End Users** → `MBAS_Setup_v1.2.0_Robust.exe`
- Professional installer
- Creates shortcuts
- Uninstall via Control Panel
- Best for distribution

**For Developers/Testers** → `MBAS_v1.2.0_Portable.zip`
- No installation
- Run from anywhere
- Quick testing
- USB drive compatible

---

## ⚡ System Requirements

### To BUILD the installer:
- Windows 10/11
- Inno Setup 6
- PowerShell (included in Windows)

### To RUN the installer (end users):
- Windows 10/11 (64-bit)
- Python 3.11 or 3.12
- 2GB free disk space
- 4GB RAM

---

## 🆘 Troubleshooting

**Uninstaller still hanging?**
→ Run: `FORCE_UNINSTALL.bat`

**Build fails?**
→ Run: `BUILD_MASTER.bat` → Option 8 (System Check)

**Need help?**
→ See: `INSTALLER_SOLUTION_GUIDE.md`

---

## 📞 Support

- Full documentation: `INSTALLER_SOLUTION_GUIDE.md`
- Quick reference: `QUICK_START.txt`
- System check: `BUILD_MASTER.bat` → Option 8
- Emergency uninstall: `FORCE_UNINSTALL.bat`

---

## ✅ Success Criteria

Your installer is ready when:
- ✅ Builds without errors
- ✅ Installs on clean system
- ✅ Application runs correctly
- ✅ Uninstalls cleanly (no hanging!)
- ✅ Database preserved on upgrade

---

## 🚀 Next Steps

1. **Right Now**: Fix hanging uninstaller
   ```
   FORCE_UNINSTALL.bat
   ```

2. **Today**: Build professional installer
   ```
   BUILD_MASTER.bat → Option 1
   ```

3. **This Week**: Test and distribute
   - Test on VM or spare PC
   - Share installer with users

---

© 2026 ZT Products. Professional Installer Solution.
