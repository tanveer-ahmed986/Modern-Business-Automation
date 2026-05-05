# MBAS - Modern Business Automation System
## Complete Installation Package

---

## 📦 Package Contents

This package contains everything you need to run MBAS:

```
MBAS/
├── backend/              ✓ Python FastAPI backend
├── frontend/             ✓ React TypeScript frontend
├── START_MBAS.bat        ✓ Main startup script (USE THIS)
├── STOP_MBAS.bat         ✓ Stop all services
├── start-backend.bat     ✓ Start backend only
├── start-frontend.bat    ✓ Start frontend only
├── INSTALL_FIX_WINDOWS.bat  ✓ Automated dependency installer
├── INSTALL_DEPENDENCIES.bat ✓ Alternative installer
├── mbas.license          ✓ License file (replace with yours)
├── README.txt            ✓ Quick reference
├── docs/                 ✓ Documentation
└── runtime/              ✓ Python installation guide
```

---

## ⚡ QUICK START (3 Steps)

### Step 1: Install Prerequisites

**Install Python 3.11+**
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or higher
3. Run installer
4. ✅ **CHECK "Add Python to PATH"** (IMPORTANT!)
5. Click "Install Now"

**Install Node.js 18+**
1. Go to https://nodejs.org/
2. Download LTS version
3. Run installer (use all defaults)

**Restart your computer after installing both**

### Step 2: Install Dependencies

Double-click:
```
INSTALL_FIX_WINDOWS.bat
```

This will:
- Install all Python packages (5-10 minutes)
- Install all Node.js packages
- Create database structure
- Verify everything is ready

### Step 3: Start MBAS

Double-click:
```
START_MBAS.bat
```

**What happens:**
1. Two windows open (Backend + Frontend)
2. Wait 15 seconds
3. Browser opens automatically
4. Login with admin/admin123

**That's it! You're done!** 🎉

---

## 🎯 What You'll See

### Window 1: Backend Server (Black/Green)
```
[OK] Python found
[*] Starting FastAPI backend on http://localhost:8000
[i] Keep this window open while using MBAS
INFO:     Uvicorn running on http://127.0.0.1:8000
```
✅ Keep this window OPEN

### Window 2: Frontend Server (Blue)
```
[OK] Node.js found
[*] Starting Vite dev server on http://localhost:5173
  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```
✅ Keep this window OPEN

### Window 3: Your Browser
```
Login Page appears
Username: admin
Password: admin123
```
✅ Use this to access MBAS

---

## 🛑 Stopping MBAS

**Option 1: Close Windows**
- Press Ctrl+C in Backend window, then Y
- Press Ctrl+C in Frontend window, then Y

**Option 2: Use Stop Script**
Double-click:
```
STOP_MBAS.bat
```

---

## 🔧 Troubleshooting

### Problem: "Python is not recognized"

**Fix:**
1. Reinstall Python
2. ✅ CHECK "Add Python to PATH"
3. Restart computer
4. Verify: Open Command Prompt and type `python --version`

### Problem: "npm is not recognized"

**Fix:**
1. Reinstall Node.js
2. Restart computer
3. Verify: Open Command Prompt and type `node --version`

### Problem: "Can't reach this page" in browser

**Fix:**
1. Make sure BOTH windows are running
2. Backend should show "Uvicorn running"
3. Frontend should show "Local: http://localhost:5173"
4. If frontend has errors:
   ```cmd
   cd frontend
   npm install
   ```

### Problem: "Port 8000 already in use"

**Fix:**
```cmd
STOP_MBAS.bat
```
Then start again with `START_MBAS.bat`

### Problem: Blank page after login

**Fix:**
1. Press F12 in browser
2. Check Console tab for errors
3. Make sure backend is running
4. Check backend window for errors

### Problem: Installation dependencies failed

**Fix:**
```cmd
cd backend
pip install --only-binary :all: -r requirements.txt

cd ..\frontend
npm install
```

---

## 📋 System Requirements

- **OS:** Windows 10/11 (64-bit)
- **Python:** 3.11 or higher
- **Node.js:** 18 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Disk:** 5GB free space
- **Internet:** Required for initial setup only (runs offline after installation)

---

## 🔐 Default Login

```
URL:      http://localhost:5173
Username: admin
Password: admin123
```

**⚠️ IMPORTANT: Change this password after first login!**
Go to: Settings → Users → Edit admin → Change password

---

## 📁 Data Storage

All your business data is stored locally in:
```
backend/database/mbas_database.db
```

**Backups are stored in:**
```
backend/backups/
```

MBAS automatically creates backups:
- Daily backups (kept for 7 days)
- Weekly backups (kept for 4 weeks)
- Monthly backups (kept for 3 months)

---

## ✅ Verification Checklist

After installation, verify these steps work:

1. [ ] `python --version` shows Python 3.11+
2. [ ] `node --version` shows Node 18+
3. [ ] `INSTALL_FIX_WINDOWS.bat` completes without errors
4. [ ] `START_MBAS.bat` opens two windows
5. [ ] Backend window shows "Uvicorn running"
6. [ ] Frontend window shows "Local: http://localhost:5173"
7. [ ] Browser opens automatically
8. [ ] Login page appears (not blank)
9. [ ] Can login with admin/admin123
10. [ ] Dashboard displays with cards and charts

---

## 🎯 First Steps After Installation

1. **Change default password**
   - Settings → Users → Edit admin user

2. **Update business information**
   - Settings → General Settings

3. **Add products**
   - Inventory → Products → Add Product

4. **Add customers**
   - Customers → Add Customer

5. **Start making sales!**
   - Billing → New Sale

---

## 📚 Additional Documentation

- **README.txt** - Quick reference guide
- **docs/** folder - Complete user manual
- **runtime/** folder - Python installation help

---

## 🆘 Need Help?

### Common Questions

**Q: Do I need internet to use MBAS?**
A: Only for initial installation. After setup, MBAS works 100% offline.

**Q: Can I install on multiple computers?**
A: Yes! Extract the package on each computer and follow the same steps.

**Q: How do I backup my data?**
A: MBAS backs up automatically. Manual backup: Settings → Backup & Restore

**Q: Can I use this on a laptop?**
A: Yes! Works on any Windows 10/11 laptop.

**Q: What if my computer crashes?**
A: Your data is in `backend/database/` folder. Copy this folder to backup.

---

## 📞 Support

If you encounter issues:

1. Check troubleshooting section above
2. Verify Python and Node.js are installed
3. Make sure both windows are running
4. Check for error messages in windows
5. Try restarting your computer

---

## 🎉 You're Ready!

Your MBAS installation package is complete and tested.

**To start using MBAS:**
1. Double-click `START_MBAS.bat`
2. Wait for browser to open
3. Login and start managing your business!

**Enjoy your Modern Business Automation System!** 🚀

---

## 📝 Package Version

- **Version:** 1.0.0
- **Edition:** Basic
- **Build Date:** 2026-04-25
- **Package Type:** Complete Installation Package
- **Includes:** Backend + Frontend + All Dependencies

---

**© Modern Business Automation System**
**Offline Business Management Solution**
