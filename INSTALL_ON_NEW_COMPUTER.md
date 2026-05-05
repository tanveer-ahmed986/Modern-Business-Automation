# Install MBAS on New Computer - Step by Step

## What You Need

1. **Python 3.11+** - https://www.python.org/downloads/
2. **Node.js 18+** - https://nodejs.org/
3. **MBAS Package** - The zip file you received

---

## Installation Steps

### Step 1: Install Python

1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT:** Check these boxes:
   - ✅ Add Python to PATH
   - ✅ Install pip
4. Click "Install Now"
5. Restart your computer

### Step 2: Install Node.js

1. Download Node.js from https://nodejs.org/
2. Run the installer
3. Click "Next" through all steps (use defaults)
4. Restart your computer

### Step 3: Extract MBAS Package

1. Extract the MBAS zip file to your desired location
   - Example: `F:\MBAS\` or `C:\MBAS\`
2. Open the extracted folder

### Step 4: Run the Automated Installer

1. **Double-click:** `INSTALL_FIX_WINDOWS.bat`
2. Wait for it to finish (may take 5-10 minutes)
3. You should see "SUCCESS! Dependencies installed successfully"

**If you see an error about compilers:**
- This is normal on fresh Windows installations
- The script will automatically use pre-built packages
- Just wait for it to complete

### Step 5: Initialize Database

1. Open Command Prompt in the MBAS folder
2. Run:
   ```cmd
   cd backend
   python src/scripts/init_db.py
   ```
3. Wait for "Database initialized successfully"

### Step 6: Add License File (Optional)

1. If you have a license file (`mbas.license`):
   - Copy it to the MBAS root folder
   - Example: `F:\MBAS\mbas.license`
2. If you don't have a license:
   - Double-click `GENERATE_LICENSE.bat`
   - Follow the prompts to create one

### Step 7: Start MBAS

1. **Start Backend:**
   - Double-click `start-backend.bat`
   - Wait for "Uvicorn running on http://0.0.0.0:8000"
   - **Keep this window open**

2. **Start Frontend:**
   - Double-click `start-frontend.bat`
   - Wait for "Local: http://localhost:5173"
   - **Keep this window open**

3. **Open in Browser:**
   - Open your web browser
   - Go to: http://localhost:5173
   - Login: admin / admin123

---

## ✅ Success!

You should now see the MBAS dashboard!

**First Steps:**
1. Change the default password (Settings > Users)
2. Update business information (Settings > General)
3. Add your products (Inventory > Products)
4. Start making sales!

---

## 🔧 Troubleshooting

### "Python is not recognized"

**Fix:**
1. Reinstall Python
2. **Make sure** to check "Add Python to PATH"
3. Restart computer

### "ERROR: Failed to install dependencies"

**Fix:**
```cmd
cd backend
pip install --only-binary :all: -r requirements.txt
```

### "Port 8000 already in use"

**Fix:**
```cmd
taskkill /F /IM python.exe
```

Then restart the backend.

### "npm is not recognized"

**Fix:**
1. Reinstall Node.js
2. Restart computer
3. Verify: Open Command Prompt and type `node --version`

### Database initialization fails

**Fix:**
```cmd
# Delete old database
del database\mbas_database.db

# Reinitialize
cd backend
python src/scripts/init_db.py
```

### Can't login / forgot password

**Fix:**
```cmd
cd backend
python src/scripts/init_db.py
# This resets to default: admin / admin123
```

---

## 📞 Need Help?

**Common Issues:**

1. **Blank screen after login**
   - Check browser console (F12)
   - Make sure both backend and frontend are running

2. **"License validation failed"**
   - Make sure `mbas.license` is in the root folder
   - Regenerate license with `GENERATE_LICENSE.bat`

3. **Slow performance**
   - Close other applications
   - Minimum 4GB RAM required (8GB recommended)

**Log Files:**
- Backend errors: Check the terminal where backend is running
- Frontend errors: Press F12 in browser, check Console tab

---

## 🎯 Quick Installation (Summary)

1. Install Python + Node.js
2. Extract MBAS package
3. Run `INSTALL_FIX_WINDOWS.bat`
4. Run `cd backend && python src/scripts/init_db.py`
5. Start `start-backend.bat`
6. Start `start-frontend.bat`
7. Open http://localhost:5173
8. Login: admin / admin123

**Done!** 🎉

---

## 📋 System Requirements

- **OS:** Windows 10/11 (64-bit)
- **Python:** 3.11 or higher
- **Node.js:** 18 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Disk:** 5GB free space
- **Internet:** Required only for initial setup

---

## 🔐 Default Credentials

**Username:** admin
**Password:** admin123

**IMPORTANT:** Change this password immediately after first login!

Go to: Settings > Users > Edit admin user > Change password
