# How to Generate Licenses - Windows Command Examples

## ⚠️ Important: Windows Command Syntax

**DO NOT use backslash (\) for line continuation in Windows!**

Write the entire command on **ONE LINE**.

---

## 📝 License Generation Examples

### **1. Basic Tier (Perpetual License)**

```cmd
python tools/license_generator.py --licensee "ABC Pharmacy" --tier basic --type perpetual
```

**Output:** Creates `mbas.license` file for ABC Pharmacy with Basic features, no expiration.

---

### **2. Standard Tier (Annual Subscription)**

```cmd
python tools/license_generator.py --licensee "XYZ Medical Store" --tier standard --type subscription --duration 365
```

**Output:** Creates license valid for 365 days (1 year) with Standard features.

---

### **3. Premium Tier (Monthly Subscription)**

```cmd
python tools/license_generator.py --licensee "Premium Clinic" --tier premium --type subscription --duration 30
```

**Output:** Creates license valid for 30 days with Premium features.

---

### **4. Trial License (14 days)**

```cmd
python tools/license_generator.py --licensee "Trial Customer" --tier standard --type trial --duration 14
```

**Output:** Creates 14-day trial license.

---

### **5. Generate Keys (First Time Only)**

```cmd
python tools/license_generator.py --generate-keys
```

**Output:** Creates `private_key.pem` and `public_key.pem` (only need to do once)

---

## 🎯 Quick Reference

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--licensee` | Yes | Customer name | `"ABC Store"` |
| `--tier` | Yes | basic/standard/premium | `basic` |
| `--type` | Yes | perpetual/subscription/trial | `perpetual` |
| `--duration` | No* | Days (for subscription/trial) | `365` |
| `--machine-id` | No | Hardware lock | `ABC123XYZ` |
| `--generate-keys` | No | Generate RSA keys | (no value) |

*Required for subscription and trial types

---

## ✅ Your Correct Command

Based on your screenshot, try this:

```cmd
python tools/license_generator.py --licensee "ABC Pharmacy" --tier standard --type perpetual
```

Or if you want a 1-year subscription:

```cmd
python tools/license_generator.py --licensee "ABC Pharmacy" --tier standard --type subscription --duration 365
```

---

## 🔍 Common Errors

### Error: '--licensee' is not recognized
**Cause:** Using backslash line continuation in Windows
**Fix:** Put entire command on ONE line

### Error: Missing required arguments
**Cause:** Forgot --licensee, --tier, or --type
**Fix:** Include all required parameters

### Error: duration required for subscription
**Cause:** Didn't specify --duration for subscription/trial
**Fix:** Add `--duration 365` (or desired days)

---

## 📋 Step-by-Step

1. Open Command Prompt in `D:\gemini_modern_business_automation_system\`

2. Run command on ONE line:
   ```cmd
   python tools/license_generator.py --licensee "Your Customer Name" --tier standard --type perpetual
   ```

3. License file created: `mbas.license`

4. Send `mbas.license` to customer

5. Customer places it in their MBAS folder

6. Done! ✅

---

## 💡 Pro Tip

Create a batch file for common licenses:

**generate_basic_license.bat:**
```batch
@echo off
set /p CUSTOMER="Enter customer name: "
python tools/license_generator.py --licensee "%CUSTOMER%" --tier basic --type perpetual
echo.
echo License created: mbas.license
pause
```

Run: `generate_basic_license.bat`
