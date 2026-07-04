# MBAS v2.0.7 - User Fix Guide

**Date:** July 4, 2026
**Version:** 2.0.7
**Company:** Z&T Technologies - State-of-the-Art Business Solutions

---

## What's Fixed in v2.0.7?

### 1. Missing Categories ✅
**Problem:** When you tried to add products, the category dropdown was empty.

**Solution:** Categories are now automatically created during installation and on first startup.

**Categories Created:**
- Electronics
- Groceries
- Clothing
- Stationery

### 2. CMD Window Blinking ✅
**Problem:** Black command windows would flash on screen during MBAS operations.

**Solution:** All background processes now run completely hidden using pythonw.exe.

---

## How to Apply the Fix

### Option 1: Fresh Installation (Recommended)

1. **Download the new installer:**
   - File: `MBAS_Professional_Setup_v2.0.7_ZT_Technologies.exe`

2. **Uninstall old version:**
   - Go to: Settings → Apps → MBAS
   - Click "Uninstall"
   - Your data will be preserved!

3. **Install new version:**
   - Run the installer as Administrator
   - Follow the wizard
   - MBAS will start automatically with categories ready

### Option 2: Apply Fix Without Reinstalling

**For existing v2.0.6 or earlier installations:**

1. **Download the fix script:**
   - File: `APPLY_FIX_TO_EXISTING_INSTALLATION.bat`

2. **Run as Administrator:**
   - Right-click → Run as Administrator
   - Wait for the fix to complete

3. **Restart MBAS:**
   - Use system tray icon or Start Menu

---

## Verification Steps

### Check Categories

1. Open MBAS (http://localhost:8000)
2. Login: `admin` / `admin123`
3. Go to: Products → Add Product
4. Click the Category dropdown
5. **Expected:** You should see 4 categories

### Check CMD Windows

1. Start MBAS from Start Menu
2. **Expected:** No black command windows appear
3. Server runs completely in background
4. Only system tray icon is visible

---

## Troubleshooting

### Categories Still Missing?

**Check database location:**
```
C:\ProgramData\MBAS\data\mbas_database.db
```

**Verify categories exist:**
1. Download DB Browser for SQLite
2. Open: `C:\ProgramData\MBAS\data\mbas_database.db`
3. Browse data → categories table
4. Should show 4 rows

**Manual fix:**
```batch
cd "C:\Program Files\MBAS\backend"
"C:\ProgramData\MBAS\venv\Scripts\python.exe" -c "from src.scripts.init_db import bootstrap; bootstrap()"
```

### CMD Window Still Appears?

**Check process name:**
1. Open Task Manager
2. Look for MBAS processes
3. **Should see:** `pythonw.exe` (NOT python.exe)
4. **If you see python.exe:** Reinstall v2.0.7

**Check logs:**
```
C:\ProgramData\MBAS\logs\mbas_tray.log
```

Look for line: `Using pythonw: C:\ProgramData\MBAS\venv\Scripts\pythonw.exe`

### Installation Fails?

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

---

## What Happens to My Data?

### During Upgrade

✅ **Preserved:**
- All products
- All sales records
- All customers
- All settings
- All backups

❌ **Removed:**
- Old installation files
- Old virtual environment
- Old log files

### Database Location
```
C:\ProgramData\MBAS\data\mbas_database.db
```
This file is **NEVER** deleted during upgrade!

### Backup Location
```
C:\ProgramData\MBAS\data\backups\
```
All automatic backups are preserved.

---

## Technical Details

### Files Changed

1. **backend/src/scripts/init_db.py**
   - Added category creation logic
   - Creates 4 sample categories

2. **backend/src/main.py**
   - Ensures categories exist on startup
   - Auto-creates if missing

3. **backend/watchdog.py**
   - Uses pythonw.exe for restarts
   - Added CREATE_NO_WINDOW flags
   - Completely hidden execution

### Version Identification

**Check your version:**
1. Open MBAS
2. Look at browser tab title or footer
3. Should say: "MBAS v2.0.7" or higher

**Or check file version:**
```
C:\Program Files\MBAS\COMPANY_INFO.txt
```

---

## Support

### If You Still Have Issues

**Email:** zttechnologies12@gmail.com
**Website:** www.zttechnologies.org

**Include in your support request:**
1. MBAS version (from About page)
2. Windows version
3. Python version (`python --version`)
4. Log files:
   - `C:\ProgramData\MBAS\logs\mbas_tray.log`
   - `C:\ProgramData\MBAS\logs\install_log.txt`

### Common Questions

**Q: Will I lose my data?**
A: No! All data is preserved during upgrade.

**Q: Do I need to reinstall?**
A: No, you can apply the fix script. But reinstalling is cleaner.

**Q: How do I know if the fix worked?**
A: Categories appear in dropdown + No CMD windows flash.

**Q: Can I add more categories?**
A: Yes! Go to Settings → Categories → Add New

**Q: What if I deleted the database?**
A: Just start MBAS - categories will be auto-created.

---

## Version History

**v2.0.7** (July 4, 2026)
- ✅ Categories auto-created
- ✅ CMD window blinking eliminated

**v2.0.6** (July 4, 2026)
- ✅ Server runs in background
- ❌ Categories not created (fixed in v2.0.7)

**v2.0.5 and earlier**
- ❌ CMD window visible (fixed in v2.0.6)
- ❌ Categories not created (fixed in v2.0.7)

---

## Thank You!

Thank you for using MBAS - Modern Business Automation System!

We are committed to providing you with the best business automation solution.

**Z&T Technologies**
*State-of-the-Art Business Solutions*
www.zttechnologies.org

---

**End of User Guide**
