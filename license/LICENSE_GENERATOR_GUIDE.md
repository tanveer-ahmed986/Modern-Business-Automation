# 🔐 MBAS License Generator - Quick Guide

## 🚀 Quick Start

### **Windows (Recommended):**
1. Double-click `GENERATE_LICENSE.bat`
2. Follow the prompts
3. License saved to `license\mbas.license`

### **PowerShell:**
```powershell
cd license
powershell -ExecutionPolicy Bypass -File GENERATE_LICENSE.ps1
```

---

## 📋 Generation Steps

Both scripts ask you 4 simple questions:

### **Step 1: Select Tier**
- `1` = Basic Edition
- `2` = Standard Edition
- `3` = Premium Edition

### **Step 2: Select Type**
- `1` = Perpetual (lifetime, one-time payment)
- `2` = Subscription (recurring, expires)
- `3` = Trial (14 days free)

### **Step 3: Business Name**
- Enter customer's business name
- Example: "ABC Pharmacy"

### **Step 4: Hardware Lock (Optional)**
- `Y` = Lock to specific computer
- `N` = Works on any computer

---

## 📦 After Generation

**License created at:** `license\mbas.license`

**Automatically copied to:** `deployment\MBAS_Package\mbas.license`

**Next steps:**
1. Rebuild deployment package:
   ```bash
   python scripts\build_deployment_package.py Basic
   ```
2. Send zip file to customer
3. Customer installs and license validates automatically

---

## 🎯 License Tiers

| Tier | Features |
|------|----------|
| **Basic** | Dashboard, Inventory, Billing, Reports, Backup |
| **Standard** | Basic + Advanced Reports, Multi-user |
| **Premium** | Standard + AI Forecasting, Premium Analytics |

---

## 📅 License Types

| Type | Duration | Payment |
|------|----------|---------|
| **Perpetual** | Forever | One-time |
| **Subscription** | 30-365 days | Recurring |
| **Trial** | 14 days | Free |

---

## ✅ Verification

Check if license is properly signed:

```bash
cd license
python -c "import json; lic = json.load(open('mbas.license')); print('Tier:', lic['tier'], '| Signature:', lic['signature'][:30] + '...')"
```

Expected output:
```
Tier: standard | Signature: SyPu7Dx0heCG1PvPfBY39G3a...
```

---

## 🚨 Troubleshooting

**Q: "Python not found"**
- Install Python 3.11+ from python.org
- Check "Add to PATH" during installation

**Q: "Private key not found"**
- Ensure `tools\keys\private_key.pem` exists
- Contact administrator if missing

**Q: License doesn't validate**
- Check file is named exactly: `mbas.license`
- Verify it's in MBAS_Package root folder
- Delete `backend\mbas_database.db` and reinstall

---

## 📞 Support

For detailed documentation, see:
- Full guide: `license\HOW_TO_GENERATE_LICENSES.md` (coming soon)
- License fix: `deployment\LICENSE_AND_ICON_FIX.md`
- Deployment: `deployment\FINAL_FIX_SUMMARY.md`

---

**Generated licenses are cryptographically signed and tamper-proof! 🔒**
