# Windows Installation Guide - Fix Compiler Errors

## Problem

When installing MBAS on Windows, you may see this error:
```
ERROR: Unknown compiler(s): ['icl'], ['cl'], ['cc'], ['gcc'], ['clang']
ERROR: Failed to build pandas when installing build dependencies for pandas
ERROR: Failed to install dependencies
```

**Cause:** Some Python packages (pandas, numpy, scikit-learn) need C++ compilation, but Windows doesn't have a C++ compiler installed by default.

---

## ✅ Solution 1: Use Pre-Built Packages (EASIEST - RECOMMENDED)

### **Quick Fix:**

1. **Run the automated installer:**
   ```cmd
   INSTALL_FIX_WINDOWS.bat
   ```

2. **That's it!** The script will install all dependencies using pre-built packages (no compiler needed).

### **Manual Steps (if automated script fails):**

1. **Upgrade pip:**
   ```cmd
   python -m pip install --upgrade pip
   ```

2. **Install backend dependencies:**
   ```cmd
   cd backend
   pip install --only-binary :all: -r requirements.txt
   ```

   The `--only-binary :all:` flag forces pip to use pre-compiled wheels only.

3. **If that fails, install packages individually:**
   ```cmd
   pip install fastapi uvicorn sqlmodel pydantic pydantic-settings
   pip install python-jose passlib python-multipart email-validator
   pip install apscheduler
   pip install --only-binary :all: pandas numpy scikit-learn
   ```

4. **Verify installation:**
   ```cmd
   python -c "import pandas; import numpy; import sklearn; print('Success!')"
   ```

---

## ✅ Solution 2: Install C++ Build Tools (For Advanced Users)

If you need to compile packages or prefer building from source:

### **Option A: Microsoft C++ Build Tools (Lightweight)**

1. **Download:** https://visualstudio.microsoft.com/visual-cpp-build-tools/

2. **Install with these workloads:**
   - ✅ Desktop development with C++
   - ✅ MSVC v143 - VS 2022 C++ x64/x86 build tools
   - ✅ Windows 10/11 SDK

3. **Restart your computer**

4. **Install dependencies normally:**
   ```cmd
   cd backend
   pip install -r requirements.txt
   ```

### **Option B: Visual Studio Community (Full IDE)**

1. **Download:** https://visualstudio.microsoft.com/downloads/

2. **Install with:**
   - ✅ Desktop development with C++

3. **Restart and install dependencies**

---

## 🎯 Recommended Installation Order

### **For New Windows Installation:**

1. **Install Python 3.11+**
   - Download from https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install pip"

2. **Install Node.js 18+**
   - Download from https://nodejs.org/
   - Use LTS version

3. **Run the automated installer:**
   ```cmd
   INSTALL_FIX_WINDOWS.bat
   ```

4. **Initialize database:**
   ```cmd
   cd backend
   python src/scripts/init_db.py
   ```

5. **Generate license (optional):**
   ```cmd
   GENERATE_LICENSE.bat
   ```

6. **Start MBAS:**
   ```cmd
   start-backend.bat
   start-frontend.bat
   ```

---

## 🔧 Troubleshooting

### **Error: "Python is not recognized"**
**Fix:**
```cmd
# Add Python to PATH manually
# Go to: System Properties > Environment Variables
# Add to PATH: C:\Users\YourName\AppData\Local\Programs\Python\Python311
```

### **Error: "pip is not recognized"**
**Fix:**
```cmd
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### **Error: "No module named 'fastapi'"**
**Fix:**
```cmd
cd backend
pip install -r requirements.txt
```

### **Error: "Address already in use (port 8000)"**
**Fix:**
```cmd
# Kill existing Python processes
taskkill /F /IM python.exe
```

### **Error: "npm is not recognized"**
**Fix:**
```cmd
# Install Node.js from https://nodejs.org/
# Restart command prompt after installation
```

---

## 📋 System Requirements

- **OS:** Windows 10/11 (64-bit)
- **Python:** 3.11 or higher
- **Node.js:** 18 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Disk Space:** 5GB free space
- **Internet:** Required for initial dependency download

---

## ✅ Verification Checklist

After installation, verify everything works:

```cmd
# Check Python
python --version
# Should show: Python 3.11.x or higher

# Check pip
pip --version

# Check Node.js
node --version
# Should show: v18.x.x or higher

# Check npm
npm --version

# Test backend dependencies
cd backend
python -c "import fastapi; import pandas; print('Backend OK')"

# Test frontend dependencies
cd ../frontend
npm --version

# Start MBAS
cd ..
start-backend.bat
```

Open browser: http://localhost:5173
Login: admin / admin123

---

## 🎉 Success Criteria

You should see:
- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:5173
- ✅ Login page loads successfully
- ✅ Can login with admin/admin123
- ✅ Dashboard displays without errors

---

## 📧 Still Having Issues?

If you still encounter errors:

1. **Check the error log:**
   - Backend errors: Check the terminal where `start-backend.bat` is running
   - Frontend errors: Check browser console (F12)

2. **Try clean installation:**
   ```cmd
   # Delete virtual environment (if exists)
   rmdir /s /q backend\venv

   # Reinstall
   INSTALL_FIX_WINDOWS.bat
   ```

3. **Verify Python path:**
   ```cmd
   where python
   # Should show: C:\Users\...\Python\Python311\python.exe
   ```

---

## 📦 Portable Installation

For customer deployment on machines without compiler:

1. **Create requirements with specific versions:**
   ```cmd
   pip freeze > requirements_locked.txt
   ```

2. **Download wheels in advance:**
   ```cmd
   pip download -r requirements.txt -d wheels/
   ```

3. **Install from local wheels:**
   ```cmd
   pip install --no-index --find-links=wheels/ -r requirements.txt
   ```

This ensures customers can install without internet or compiler.

---

## 🚀 Quick Start (TL;DR)

```cmd
# 1. Install Python + Node.js
# 2. Run this:
INSTALL_FIX_WINDOWS.bat

# 3. Initialize database:
cd backend
python src/scripts/init_db.py

# 4. Start MBAS:
start-backend.bat
start-frontend.bat

# 5. Open: http://localhost:5173
# Login: admin / admin123
```

Done! 🎉
