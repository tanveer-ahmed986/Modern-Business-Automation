# License Generator Troubleshooting

## Issue: Batch file closes immediately

### **Solution 1: Use the Simple Version**

Try the simplified batch file:
```
Double-click: GENERATE_LICENSE_SIMPLE.bat
```

This version:
- ✅ Has better error handling
- ✅ Won't close on errors
- ✅ Shows detailed error messages
- ✅ Simpler prompts

---

### **Solution 2: Run from Command Prompt**

1. Open Command Prompt:
   - Press `Win + R`
   - Type: `cmd`
   - Press Enter

2. Navigate to license folder:
   ```cmd
   cd D:\gemini_modern_business_automation_system\license
   ```

3. Run the script:
   ```cmd
   GENERATE_LICENSE.bat
   ```

This way you'll see any errors before the window closes.

---

### **Solution 3: Check Requirements**

Run the test script to check everything:
```
Double-click: TEST_LICENSE_GEN.bat
```

This will verify:
- ✅ Python is installed
- ✅ sign_license.py exists
- ✅ Private key exists
- ✅ Can generate a test license

---

## Common Errors

### Error: "Python is not installed"

**Fix:**
```
1. Download Python 3.11 from python.org
2. Install with "Add to PATH" checked
3. Restart Command Prompt
4. Try again
```

### Error: "cryptography module not found"

**Fix:**
```cmd
pip install cryptography
```

### Error: "Private key not found"

**Fix:**
```
Check if file exists:
D:\gemini_modern_business_automation_system\tools\keys\private_key.pem

If missing, contact administrator.
```

### Error: "Permission denied"

**Fix:**
```
Run Command Prompt as Administrator:
1. Right-click Command Prompt
2. Select "Run as administrator"
3. Navigate to license folder
4. Run batch file
```

---

## Manual Generation (If Batch Files Don't Work)

Open Command Prompt and run directly:

```cmd
cd D:\gemini_modern_business_automation_system

python tools\sign_license.py ^
    --licensee "ABC Pharmacy" ^
    --tier standard ^
    --type perpetual ^
    --output license\mbas.license
```

**Parameters:**
- `--licensee` = Business name (in quotes)
- `--tier` = basic, standard, or premium
- `--type` = perpetual, subscription, or trial
- `--duration` = Days (only for subscription/trial)
- `--output` = Output file path

**Examples:**

```cmd
# Standard perpetual
python tools\sign_license.py --licensee "ABC Pharmacy" --tier standard --type perpetual --output license\abc.license

# Premium 1-year subscription
python tools\sign_license.py --licensee "XYZ Hospital" --tier premium --type subscription --duration 365 --output license\xyz.license

# Trial (14 days)
python tools\sign_license.py --licensee "Trial Customer" --tier standard --type trial --duration 14 --output license\trial.license
```

---

## Verify Installation

Check if everything is set up correctly:

### 1. Check Python
```cmd
python --version
```
Should show: `Python 3.11.x` or higher

### 2. Check cryptography
```cmd
python -c "import cryptography; print('OK')"
```
Should show: `OK`

### 3. Check files exist
```cmd
dir D:\gemini_modern_business_automation_system\tools\sign_license.py
dir D:\gemini_modern_business_automation_system\tools\keys\private_key.pem
```
Both should exist.

### 4. Test generation
```cmd
cd D:\gemini_modern_business_automation_system
python tools\sign_license.py --licensee "Test" --tier basic --type perpetual --output license\test.license
```
Should create: `license\test.license`

---

## Still Not Working?

### Option 1: Use PowerShell Script

```powershell
cd D:\gemini_modern_business_automation_system\license
powershell -ExecutionPolicy Bypass -File GENERATE_LICENSE.ps1
```

### Option 2: Contact Support

Provide this information:
1. Python version: `python --version`
2. Error message (screenshot)
3. Output of TEST_LICENSE_GEN.bat
4. Windows version

---

## Quick Reference

| File | Purpose |
|------|---------|
| `GENERATE_LICENSE.bat` | Full interactive generator |
| `GENERATE_LICENSE_SIMPLE.bat` | Simplified version (recommended) |
| `GENERATE_LICENSE.ps1` | PowerShell version |
| `TEST_LICENSE_GEN.bat` | Test if everything works |
| `TROUBLESHOOTING.md` | This file |

---

**Recommended:** Use `GENERATE_LICENSE_SIMPLE.bat` for most reliable experience!
