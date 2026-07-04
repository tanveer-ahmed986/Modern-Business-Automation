# How to Generate Licenses - Easy Interactive Tools

## 🎯 Two Easy Options

I've created **TWO interactive tools** to make license generation super easy!

---

## **Option 1: Batch File (Recommended for Beginners)**

### **File:** `GENERATE_LICENSE.bat`

### **How to Use:**
1. Double-click `GENERATE_LICENSE.bat`
2. Answer the questions:
   - License tier (Basic/Standard/Premium)
   - License type (Perpetual/Subscription/Trial)
   - Business name
   - Hardware lock (optional)
3. Press Y to confirm
4. Done! `mbas.license` file created

### **Advantages:**
✅ Simple double-click to run
✅ No need to type commands
✅ Color-coded interface
✅ Step-by-step wizard

---

## **Option 2: PowerShell Script (More Features)**

### **File:** `GENERATE_LICENSE.ps1`

### **How to Use:**
1. Right-click `GENERATE_LICENSE.ps1`
2. Select "Run with PowerShell"
   (Or run: `powershell -ExecutionPolicy Bypass -File GENERATE_LICENSE.ps1`)
3. Answer the questions
4. Press Y to confirm
5. Done! `mbas.license` file created + summary file

### **Advantages:**
✅ More colorful interface
✅ Better error handling
✅ Creates summary file
✅ Auto-generates machine IDs
✅ Can view license file immediately

---

## 📝 **Example Walkthrough**

### **Creating a Standard Perpetual License:**

```
1. Run: GENERATE_LICENSE.bat

2. Step 1 - Select Tier:
   Enter choice: 2 (Standard)

3. Step 2 - Select Type:
   Enter choice: 1 (Perpetual)

4. Step 3 - Business Name:
   Enter: ABC Pharmacy

5. Step 4 - Hardware Lock:
   Your choice: N (No lock)

6. Confirmation:
   Generate license? Y

7. SUCCESS!
   File created: mbas.license
```

**Total time: 30 seconds!** ⚡

---

## 📋 **What Each Option Means:**

### **License Tiers:**

| Tier | Price | Features |
|------|-------|----------|
| **Basic** | $299 one-time | Dashboard, Inventory, Billing, Basic Reports |
| **Standard** | $799 one-time or $49/month | Basic + Advanced Reports, Multi-user |
| **Premium** | $599/year or $79/month | Standard + AI Insights, Forecasting |

### **License Types:**

| Type | Description | Use Case |
|------|-------------|----------|
| **Perpetual** | Never expires | One-time payment, lifetime access |
| **Subscription** | Expires after duration | Monthly/yearly recurring |
| **Trial** | 14 days free | Demo for potential customers |

### **Hardware Lock:**

- **Yes** - License only works on one specific computer
- **No** - License can be transferred between computers
- **Recommended:** No lock for flexibility

---

## 🎯 **Quick Start (Choose One):**

### **For Windows Users (Easy):**
```
1. Double-click: GENERATE_LICENSE.bat
2. Follow the prompts
3. Done!
```

### **For PowerShell Users (Advanced):**
```
1. Right-click: GENERATE_LICENSE.ps1
2. Run with PowerShell
3. Follow the prompts
4. Done!
```

### **For Command Line Users (Manual):**
```cmd
python tools/license_generator.py --licensee "ABC Pharmacy" --tier standard --type perpetual
```

---

## 📂 **Output Files:**

After generation, you'll have:

1. **mbas.license** - Send this to customer
2. **license_summary_YYYYMMDD_HHMMSS.txt** - Your records (PowerShell only)

---

## 🔄 **Common Scenarios:**

### **Scenario 1: New Customer - Perpetual**
```
Tier: Standard
Type: Perpetual
Business: XYZ Medical Store
Lock: No
```

### **Scenario 2: Trial Customer**
```
Tier: Premium (show all features)
Type: Trial
Business: Trial Customer Ltd
Lock: No
Duration: 14 days (automatic)
```

### **Scenario 3: Monthly Subscription**
```
Tier: Premium
Type: Subscription
Duration: 30 days
Business: Monthly Customer
Lock: No
```

### **Scenario 4: Hardware-Locked License**
```
Tier: Basic
Type: Perpetual
Business: Secure Business Inc
Lock: Yes
Machine ID: (auto-generated or manual)
```

---

## ⚠️ **Troubleshooting:**

### **Problem: "Python is not installed"**
**Solution:** Install Python from https://www.python.org/downloads/
Make sure to check "Add Python to PATH"

### **Problem: "Execution Policy" error (PowerShell)**
**Solution:** Run PowerShell as Administrator and run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Or run directly with:
```powershell
powershell -ExecutionPolicy Bypass -File GENERATE_LICENSE.ps1
```

### **Problem: License file already exists**
**Solution:** The new license will overwrite the old one. Backup if needed.

---

## 📧 **Sending License to Customer:**

### **Email Template:**

```
Subject: Your MBAS License File

Dear [Customer Name],

Thank you for purchasing MBAS [Tier] Edition!

Attached is your license file: mbas.license

Installation:
1. Extract MBAS zip file
2. Copy mbas.license to the MBAS folder
3. Run START_MBAS.bat
4. Login: admin / admin123

Your license details:
- Business: [Business Name]
- Tier: [Basic/Standard/Premium]
- Type: [Perpetual/Subscription]
- Expires: [Date or Never]

Need help? Contact us at support@yourdomain.com

Best regards,
MBAS Support Team
```

---

## 🎉 **You're Ready!**

Choose your preferred method:
- **Easiest:** Double-click `GENERATE_LICENSE.bat`
- **Best:** Run `GENERATE_LICENSE.ps1` in PowerShell
- **Manual:** Use command line (see GENERATE_LICENSE_EXAMPLES.md)

**All methods create the same valid license file!**

Happy licensing! 🚀
