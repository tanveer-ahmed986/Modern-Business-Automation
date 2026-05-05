# Customer Deployment Guide - Data Storage Locations

## Where Customer Data Will Be Stored

### Current Development Setup (Your System):
```
D:\gemini_modern_business_automation_system\
├── backend\
│   ├── mbas_database.db          ← Main database
│   └── backups\                  ← Backup files
│       ├── mbas_backup_20260425_120000.db
│       └── mbas_backup_20260424_000000.db
└── frontend\
```

---

## Customer Installation Scenarios

### **Scenario 1: Portable Installation (Recommended)**

**What You Deliver to Customer:**
```
MBAS_v1.0.zip (100-200 MB)
```

**Customer Extracts to Any Location:**

**Example 1: C Drive**
```
C:\MBAS\
├── MBAS.exe                      ← Desktop app
├── backend\
│   ├── mbas_database.db          ← Customer data stored here
│   └── backups\                  ← Automatic backups here
├── User_Manual.pdf
└── README.txt
```

**Example 2: D Drive (Like Your Setup)**
```
D:\MyBusinessSoftware\MBAS\
├── MBAS.exe
├── backend\
│   ├── mbas_database.db          ← Customer data
│   └── backups\
```

**Example 3: USB Drive (Portable)**
```
E:\MBAS\                          ← Entire business on USB!
├── MBAS.exe
├── backend\
│   ├── mbas_database.db
│   └── backups\
```

**Example 4: Network Drive (Multi-User)**
```
\\CompanyServer\SharedDrive\MBAS\
├── MBAS.exe
├── backend\
│   ├── mbas_database.db          ← Shared database
│   └── backups\
```

---

### **Scenario 2: Installed Application**

**Customer Runs Installer:**

**User-Specific Installation:**
```
C:\Users\ShopOwner\AppData\Local\MBAS\
├── MBAS.exe
├── database\
│   └── mbas_database.db
└── backups\
```

**System-Wide Installation:**
```
C:\Program Files\MBAS\
├── MBAS.exe
└── Data\                         ← Writable data folder
    ├── database\
    │   └── mbas_database.db
    └── backups\
```

---

## Data Path Configuration

### Current Code (Relative Paths - Good!):

**Database Location:**
```python
# backend/src/core/db.py
DB_FILE = "mbas_database.db"
DB_URL = f"sqlite:///{DB_FILE}"

# Resolves to:
[Installation Directory]/backend/mbas_database.db
```

**Backup Location:**
```python
# backend/src/core/backup.py
backup_dir = "backups"

# Resolves to:
[Installation Directory]/backend/backups/
```

**This means:**
- ✅ Data stores relative to where MBAS runs
- ✅ Customer can install anywhere they want
- ✅ Portable - can move entire folder
- ✅ No hardcoded paths

---

## Customer Data Storage Summary

| Installation Type | Database Location | Backup Location | Portable? |
|-------------------|-------------------|-----------------|-----------|
| **Portable Zip** | `[ExtractFolder]\backend\mbas_database.db` | `[ExtractFolder]\backend\backups\` | ✅ Yes |
| **USB Drive** | `E:\MBAS\backend\mbas_database.db` | `E:\MBAS\backend\backups\` | ✅ Yes |
| **C Drive** | `C:\MBAS\backend\mbas_database.db` | `C:\MBAS\backend\backups\` | ✅ Yes |
| **Network** | `\\Server\MBAS\backend\mbas_database.db` | `\\Server\MBAS\backend\backups\` | ✅ Yes |
| **Program Files** | `C:\Program Files\MBAS\Data\database\mbas_database.db` | `C:\Program Files\MBAS\Data\backups\` | ❌ No |

---

## What Customers Need to Know

### **1. Data Location:**

Tell your customers:
```
"Your business data is stored in the 'backend' folder
where you extracted MBAS.

Database: backend\mbas_database.db
Backups: backend\backups\

To backup your entire business:
1. Copy the entire MBAS folder to USB drive
2. Or copy just the 'backend' folder

To restore:
1. Copy the MBAS folder back
2. Start the application
3. All your data is there!"
```

### **2. Backup Strategy:**

Recommend to customers:
```
Option 1: Use Built-in Automatic Backups
- Runs daily at midnight
- Keeps 7 daily, 4 weekly, 3 monthly backups
- Stored in: backend\backups\

Option 2: Manual Full Backup (Best!)
- Copy entire MBAS folder to USB drive weekly
- Copy to cloud (Dropbox/Google Drive) monthly
- Keep one copy off-site

Option 3: Combination (Recommended)
- Let automatic backups run daily
- Copy backups folder to USB weekly
- Full folder backup monthly
```

### **3. Moving to New Computer:**

Tell customers:
```
Step 1: On old computer
- Copy entire MBAS folder to USB drive
  Example: Copy E:\MBAS\ to USB

Step 2: On new computer
- Copy MBAS folder from USB to new location
  Example: Paste to C:\MBAS\

Step 3: Start application
- Double-click MBAS.exe
- All data, settings, and history intact!

Time required: 5-10 minutes
Data loss: ZERO ✅
```

---

## Packaging for Customers

### **Option A: Simple Zip File (Recommended)**

**Create delivery package:**
```
MBAS_v1.0_Basic.zip
├── MBAS.exe
├── backend\
│   ├── mbas_database.db (empty starter database)
│   ├── backups\ (empty folder)
│   └── [Python runtime files]
├── README.txt
├── User_Manual.pdf
├── Installation_Guide.pdf
└── mbas.license (customer's license file)
```

**Customer process:**
1. Extract zip to desired location
2. Double-click MBAS.exe
3. Login with default credentials
4. Start using!

**Pros:**
- ✅ Simple for customers
- ✅ No installation required
- ✅ Works from any location
- ✅ Easy to backup (copy folder)
- ✅ Portable across computers

**Cons:**
- ❌ Less "professional" feel
- ❌ Customer needs to manage folder
- ❌ No automatic updates

---

### **Option B: Windows Installer (.msi or .exe)**

**Create installer that:**
1. Asks customer for installation location
2. Default: `C:\Program Files\MBAS\`
3. Creates desktop shortcut
4. Registers in Windows Programs list
5. Creates Start Menu entry

**Data stored at:**
```
Installation:
C:\Program Files\MBAS\MBAS.exe

Data (writable):
C:\ProgramData\MBAS\database\mbas_database.db
C:\ProgramData\MBAS\backups\

Or per-user:
C:\Users\[Username]\AppData\Local\MBAS\database\
C:\Users\[Username]\AppData\Local\MBAS\backups\
```

**Pros:**
- ✅ Professional installation experience
- ✅ Desktop shortcut created
- ✅ Uninstaller included
- ✅ Auto-update capability

**Cons:**
- ❌ More complex to create
- ❌ Customer can't easily move installation
- ❌ Data in hidden AppData folder

---

### **Option C: Hybrid (Best of Both)**

**Provide both options:**

**For small shops (1-5 users):**
- Portable zip version
- Extract and run
- Simple and flexible

**For larger businesses (5+ users):**
- Professional installer
- Network installation
- Centralized database

---

## Current Configuration Status

### ✅ Your Code is Already Portable!

The current MBAS code uses relative paths, which means:

**When customer extracts to:**
```
C:\MyShop\MBAS\
```

**Data automatically goes to:**
```
C:\MyShop\MBAS\backend\mbas_database.db
C:\MyShop\MBAS\backend\backups\
```

**When customer extracts to:**
```
E:\BusinessApps\MBAS\
```

**Data automatically goes to:**
```
E:\BusinessApps\MBAS\backend\mbas_database.db
E:\BusinessApps\MBAS\backend\backups\
```

**No code changes needed!** ✅

---

## Customer Installation Instructions

### Create this README.txt for customers:

```txt
=======================================================
   MBAS - Modern Business Automation System
   Installation & Data Location Guide
=======================================================

INSTALLATION STEPS:
-------------------
1. Extract this zip file to any location on your computer
   Examples: C:\MBAS  or  D:\MyBusiness\MBAS

2. Your data will be stored in the "backend" folder:
   - Database: backend\mbas_database.db
   - Backups:  backend\backups\

3. Double-click MBAS.exe to start the application

4. Login with:
   Username: admin
   Password: admin123

5. Change password immediately in Settings!


WHERE IS MY DATA STORED?
------------------------
Your business data is stored in the same folder where
you extracted MBAS:

If you extracted to C:\MBAS, your data is at:
  C:\MBAS\backend\mbas_database.db
  C:\MBAS\backend\backups\

If you extracted to D:\MyShop, your data is at:
  D:\MyShop\backend\mbas_database.db
  D:\MyShop\backend\backups\


BACKUP YOUR DATA:
-----------------
Option 1 (Automatic):
  - Go to "Backup" in the application menu
  - Automatic daily backups are enabled by default
  - Backups saved in: backend\backups\

Option 2 (Manual - Recommended):
  - Copy the entire MBAS folder to USB drive weekly
  - This backs up everything: data, settings, backups
  - Store one copy off-site (another location)


MOVING TO NEW COMPUTER:
-----------------------
1. Copy entire MBAS folder to USB drive
2. Paste on new computer (any location)
3. Double-click MBAS.exe
4. All data is intact! No re-configuration needed.


SUPPORT:
--------
For issues or questions, contact:
Email: your-support@email.com
Phone: your-phone-number

=======================================================
```

---

## Summary

### Your Development System:
```
D:\gemini_modern_business_automation_system\backend\
  ├── mbas_database.db
  └── backups\
```

### Customer Systems:
```
[Wherever they extract/install]\backend\
  ├── mbas_database.db
  └── backups\
```

**Key Point:**
- ✅ Code uses relative paths
- ✅ Customer can install anywhere
- ✅ Data stays with the application
- ✅ Easy to backup (copy folder)
- ✅ Portable across computers
- ✅ No hardcoded paths

**Your customers have full control over where their data is stored!**
