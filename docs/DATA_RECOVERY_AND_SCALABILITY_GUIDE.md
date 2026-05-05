# Data Recovery & Scalability Guide

## Table of Contents
1. [Data Recovery Strategies](#data-recovery-strategies)
2. [SQLite Storage Capacity](#sqlite-storage-capacity)
3. [When to Migrate to PostgreSQL](#when-to-migrate-to-postgresql)
4. [Migration Strategy](#migration-strategy)
5. [Disaster Recovery Plan](#disaster-recovery-plan)

---

## 1. Data Recovery Strategies

### 1.1 Current Backup System (Built-in)

Your MBAS system already has backup/restore functionality:

**Location:** Backup button in left sidebar (Admin only)

**How it works:**
```
✅ Manual Backups: Click "Create New Backup" button
✅ Storage: backend/backups/ folder
✅ Format: backup_YYYYMMDD_HHMMSS.db
✅ Restore: Click "Restore" on any backup file
```

**Limitations:**
- ❌ Manual only (not automatic)
- ❌ Backups stored on same machine (no cloud/external storage)
- ❌ No scheduled/automated backups

### 1.2 Recommended Backup Strategy

#### **Option A: Automatic Daily Backups (Recommended)**

I can add an automatic backup system that runs daily:

**Features:**
- Runs automatically at midnight every day
- Keeps last 7 daily backups
- Keeps last 4 weekly backups
- Keeps last 3 monthly backups
- Auto-deletes old backups to save space

**Implementation:** Would you like me to add this?

#### **Option B: External Backup Storage**

Copy backups to external locations:

**Windows:**
```batch
# Copy to USB drive
xcopy "backend\backups\*" "E:\MBAS_Backups\" /E /Y

# Copy to network drive
xcopy "backend\backups\*" "\\NetworkServer\MBAS_Backups\" /E /Y
```

**Scheduled Task (Windows):**
```batch
# Create scheduled task to backup daily at 11 PM
# Save as: backup_to_usb.bat
@echo off
set BACKUP_DIR=D:\gemini_modern_business_automation_system\backend\backups
set USB_DRIVE=E:\MBAS_Backups
set DATE=%date:~-4,4%%date:~-10,2%%date:~-7,2%

xcopy "%BACKUP_DIR%\*" "%USB_DRIVE%\%DATE%\" /E /Y
echo Backup completed: %DATE%
```

#### **Option C: Cloud Backup (Offline-Compatible)**

Even though MBAS is offline-first, you can upload backups to cloud:

**Using Dropbox/Google Drive:**
1. Install Dropbox/Google Drive desktop app
2. Create backup script that copies to synced folder
3. Backups auto-sync to cloud when internet available

**Example Script:**
```batch
# backup_to_cloud.bat
xcopy "backend\backups\*" "C:\Users\YourName\Dropbox\MBAS_Backups\" /E /Y
```

### 1.3 Data Recovery Scenarios

#### **Scenario 1: Database Corruption**

**Symptoms:**
- Application crashes on startup
- "Database is locked" errors
- Cannot open database file

**Recovery Steps:**
```bash
1. Stop MBAS application
2. Go to Backup page (or backend/backups/)
3. Find most recent backup: backup_20260425_235959.db
4. Click "Restore" or manually:
   - Copy backup to: backend/database/mbas_database.db
5. Restart application
```

**Alternative (Manual):**
```bash
cd backend
cp database/mbas_database.db database/mbas_database_corrupted.db
cp backups/backup_20260425_235959.db database/mbas_database.db
```

#### **Scenario 2: Accidental Data Deletion**

**Symptoms:**
- User accidentally deleted important records
- Need to recover specific data

**Recovery Steps:**
```bash
1. Create backup of current state (preserves recent data)
2. Restore older backup to temporary location
3. Export specific data from old backup (using DB Browser for SQLite)
4. Import into current database
```

**Using DB Browser for SQLite:**
```
1. Download: https://sqlitebrowser.org/
2. Open old backup file
3. Export specific table (File → Export → Table(s) as CSV)
4. Open current database
5. Import CSV (File → Import → Table from CSV)
```

#### **Scenario 3: Complete System Crash (Hardware Failure)**

**Symptoms:**
- Hard drive failure
- Computer won't boot
- Operating system corrupted

**Recovery Steps:**
```bash
# If you have external/cloud backups:
1. Install MBAS on new computer
2. Copy backup from USB/Cloud:
   - Copy backup_YYYYMMDD_HHMMSS.db
   - Paste to: backend/database/mbas_database.db
3. Start application
4. All data restored ✅

# If you only have backups on failed machine:
1. Remove hard drive from failed computer
2. Connect as external drive to working computer
3. Navigate to: D:\gemini_modern_business_automation_system\backend\backups\
4. Copy all backup files to new location
5. Install MBAS on new computer
6. Restore from backup
```

#### **Scenario 4: Ransomware/Malware Attack**

**Prevention:**
- Keep offline backups (USB drive disconnected when not backing up)
- Use cloud backups with version history (Dropbox keeps 30-day history)

**Recovery:**
```bash
1. Disconnect infected computer from network
2. Don't pay ransom
3. Install MBAS on clean computer
4. Restore from offline/cloud backup
5. All data recovered (up to last backup time)
```

---

## 2. SQLite Storage Capacity

### 2.1 SQLite Technical Limits

| Metric | Limit |
|--------|-------|
| **Max Database Size** | 281 Terabytes (281,474,976,710,656 bytes) |
| **Max Table Rows** | 2^64 (18,446,744,073,709,551,616 rows) |
| **Max Row Size** | 1 GB per row |
| **Max Column Count** | 32,767 columns per table |

**Source:** https://www.sqlite.org/limits.html

### 2.2 Practical Limits for MBAS

**Real-World Performance:**

| Database Size | Performance | Business Size | Estimated Records |
|---------------|-------------|---------------|-------------------|
| **< 100 MB** | ⚡ Excellent | Small (1-5 employees) | ~100,000 sales |
| **100 MB - 1 GB** | ✅ Good | Medium (5-20 employees) | ~1,000,000 sales |
| **1 GB - 10 GB** | ⚠️ Acceptable | Large (20-50 employees) | ~10,000,000 sales |
| **> 10 GB** | 🐌 Consider PostgreSQL | Enterprise (50+ employees) | ~100,000,000+ sales |

### 2.3 MBAS Storage Estimation

**For a typical retail/medical store:**

```
Average Sale Record Size: ~500 bytes
Average Product Record: ~300 bytes
Average Customer Record: ~200 bytes

Small Business (5 years):
- 50 sales/day × 365 days × 5 years = 91,250 sales
- Storage: 91,250 × 500 bytes = ~45 MB
- With products, customers, inventory logs: ~100 MB total

Medium Business (5 years):
- 200 sales/day × 365 days × 5 years = 365,000 sales
- Storage: 365,000 × 500 bytes = ~182 MB
- With products, customers, inventory logs: ~400 MB total

Large Business (5 years):
- 1000 sales/day × 365 days × 5 years = 1,825,000 sales
- Storage: 1,825,000 × 500 bytes = ~912 MB
- With products, customers, inventory logs: ~2 GB total
```

**Conclusion:** SQLite is sufficient for 99% of small-to-medium businesses running MBAS.

### 2.4 Monitoring Database Size

**Check current database size:**

```bash
# Windows
cd backend\database
dir mbas_database.db

# Or in Python
python -c "import os; size = os.path.getsize('backend/database/mbas_database.db'); print(f'Database size: {size / 1024 / 1024:.2f} MB')"
```

**Add to Dashboard (Optional):**
I can add a "Database Size" widget to the dashboard showing:
- Current size
- Growth rate
- Estimated time until 1 GB

Would you like me to add this?

---

## 3. When to Migrate to PostgreSQL

### 3.1 Signs You Need PostgreSQL

| Symptom | Meaning | Action |
|---------|---------|--------|
| Database > 10 GB | Large dataset | Consider migration |
| Slow queries (>5 seconds) | Performance degradation | Optimize or migrate |
| 50+ concurrent users | High concurrency | Migrate to PostgreSQL |
| Multiple locations | Need centralized DB | Migrate to PostgreSQL |
| Advanced features needed | Full-text search, JSON | Migrate to PostgreSQL |

### 3.2 Business Size Guidelines

**Stick with SQLite if:**
- ✅ Single location
- ✅ Less than 20 users
- ✅ Database < 5 GB
- ✅ Offline-first requirement
- ✅ Simple queries

**Migrate to PostgreSQL if:**
- ❌ Multiple locations/branches
- ❌ 50+ concurrent users
- ❌ Database > 10 GB
- ❌ Need cloud/server deployment
- ❌ Advanced analytics/reporting

### 3.3 Hybrid Approach (Recommended for Growth)

**Option: Keep SQLite + Archive Old Data**

Instead of migrating, archive old data to keep database small:

```python
# Archive sales older than 2 years
# Keep main database < 1 GB
# Move old data to archive_2024.db, archive_2023.db

Benefits:
✅ Keep using SQLite
✅ Maintain good performance
✅ Access old data when needed
✅ No migration complexity
```

Would you like me to implement an archival system?

---

## 4. Migration Strategy (SQLite → PostgreSQL)

If you decide to migrate, here's the plan:

### 4.1 When to Migrate

**Red Flags:**
1. Database file > 10 GB
2. Queries taking > 10 seconds
3. Frequent "database is locked" errors
4. Opening multiple branches/locations
5. Need for real-time synchronization

### 4.2 Migration Steps

#### **Step 1: Install PostgreSQL**

```bash
# Download PostgreSQL 16 from:
https://www.postgresql.org/download/windows/

# Install with default settings
# Remember password for postgres user
```

#### **Step 2: Export SQLite Data**

```bash
# Option A: Using pgloader (Recommended)
pgloader sqlite://backend/database/mbas_database.db postgresql://postgres:password@localhost/mbas

# Option B: Manual export/import
# Export to SQL
sqlite3 backend/database/mbas_database.db .dump > data.sql

# Import to PostgreSQL
psql -U postgres -d mbas < data.sql
```

#### **Step 3: Update MBAS Configuration**

```python
# backend/src/core/db.py

# Change from:
DATABASE_URL = "sqlite:///database/mbas_database.db"

# To:
DATABASE_URL = "postgresql://postgres:password@localhost:5432/mbas"
```

#### **Step 4: Test Migration**

```bash
# Run MBAS with PostgreSQL
cd backend
python -m uvicorn src.main:app --reload

# Verify:
✅ Login works
✅ Dashboard loads
✅ Can create sales
✅ Backup still works
```

### 4.3 PostgreSQL Benefits

After migration, you get:

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Max Size** | 281 TB (slow >10GB) | Unlimited (fast even at TB scale) |
| **Concurrent Users** | 1 writer at a time | Unlimited writers |
| **Performance** | Good for <1GB | Excellent at any size |
| **Backup** | File copy | Advanced (point-in-time recovery) |
| **Replication** | Not supported | Master-slave, multi-master |
| **Remote Access** | File access only | Network connection |
| **Multi-location** | Not supported | Central server for all branches |

### 4.4 Cost Comparison

| Solution | Setup Cost | Monthly Cost | Suitable For |
|----------|------------|--------------|--------------|
| **SQLite (Current)** | ₹0 | ₹0 | Single location, <20 users |
| **PostgreSQL (Local)** | ₹0 | ₹0 | Single location, unlimited users |
| **PostgreSQL (Cloud - AWS RDS)** | ₹0 | ₹2,000-10,000 | Multiple locations, cloud access |
| **PostgreSQL (Cloud - Azure)** | ₹0 | ₹2,500-12,000 | Enterprise, high availability |

---

## 5. Disaster Recovery Plan

### 5.1 3-2-1 Backup Rule (Recommended)

**Industry Standard:**
- **3** copies of data
- **2** different storage types
- **1** offsite/cloud copy

**For MBAS:**
```
Copy 1: Live database (backend/database/mbas_database.db)
Copy 2: Local backups (backend/backups/)
Copy 3: USB drive backup (E:\MBAS_Backups\)
Copy 4: Cloud backup (Dropbox/Google Drive)
```

### 5.2 Backup Frequency Recommendations

| Business Type | Backup Frequency | Retention |
|---------------|------------------|-----------|
| **Low Volume** (<10 sales/day) | Weekly | 4 weeks |
| **Medium Volume** (10-50 sales/day) | Daily | 7 days + 4 weekly |
| **High Volume** (>50 sales/day) | 4x per day | 7 days + 4 weekly + 3 monthly |
| **Critical** (cannot lose any data) | Hourly | 24 hours + 7 daily + 4 weekly |

### 5.3 Automated Backup Implementation

**Would you like me to implement this?**

Features I can add:
- ✅ Automatic daily backups at midnight
- ✅ Configurable schedule (hourly, daily, weekly)
- ✅ Retention policy (keep last 7 daily, 4 weekly, 3 monthly)
- ✅ Email notification on backup success/failure
- ✅ Copy to external location (USB, network drive)
- ✅ Backup verification (check if backup is valid)

### 5.4 Recovery Time Objective (RTO)

**How fast can you recover from disaster?**

| Scenario | Recovery Time | Downtime |
|----------|---------------|----------|
| **Manual restore from backup** | 5-10 minutes | Low |
| **Restore from USB/cloud** | 15-30 minutes | Medium |
| **Reinstall on new computer** | 1-2 hours | High |
| **No backup available** | Days/Weeks (data loss) | Critical |

---

## Implementation Options

### Option 1: Automatic Backup System (Recommended)

**Shall I implement:**
- Daily automatic backups at midnight
- Retention policy (7 daily + 4 weekly + 3 monthly)
- Settings page option to configure backup schedule
- Email/notification on backup failure

**Estimated time:** 2-3 hours

### Option 2: Data Archival System

**Shall I implement:**
- Archive sales/data older than X years
- Keep main database under 1 GB
- Access archived data when needed
- Automatic archival process

**Estimated time:** 3-4 hours

### Option 3: Database Size Monitoring

**Shall I implement:**
- Dashboard widget showing DB size
- Growth rate prediction
- Warning when approaching 5 GB
- Recommendations for optimization

**Estimated time:** 1 hour

### Option 4: PostgreSQL Migration Guide

**Shall I create:**
- Detailed step-by-step migration script
- Automated migration tool (one-click migrate)
- Rollback plan if migration fails
- Performance comparison tests

**Estimated time:** 4-5 hours

---

## Quick Answers to Your Questions

### Q1: How can user data be recovered if system crashes?

**Answer:**
1. Use built-in Backup/Restore feature (already implemented)
2. Keep external backups (USB drive, cloud)
3. In case of crash, restore from most recent backup
4. Maximum data loss: Time since last backup

**Recommendation:** Implement automatic daily backups (Option 1 above)

### Q2: How much can SQLite store?

**Answer:**
- **Theoretical:** 281 Terabytes
- **Practical:** Up to 10 GB with good performance
- **Your use case:** Likely stay under 2 GB for 5+ years
- **Conclusion:** SQLite is sufficient for 99% of MBAS users

### Q3: Should we use PostgreSQL if data exceeds SQLite capacity?

**Answer:**
- **If database < 5 GB:** Stick with SQLite (better for offline-first)
- **If database 5-10 GB:** Consider archival (move old data to separate files)
- **If database > 10 GB:** Migrate to PostgreSQL
- **If multiple locations:** Migrate to PostgreSQL immediately

**For most MBAS users:** SQLite is perfect. Only very large businesses need PostgreSQL.

---

## Next Steps

**Please tell me which option(s) you'd like me to implement:**

1. ✅ **Automatic Backup System** (Daily backups, retention policy)
2. ✅ **Data Archival System** (Keep DB small by archiving old data)
3. ✅ **Database Monitoring** (Dashboard widget for DB size)
4. ✅ **PostgreSQL Migration Tool** (One-click migration when needed)
5. ✅ **All of the above**

I recommend starting with **Option 1 (Automatic Backup System)** to protect against data loss.

---

## Current Backup Status

**Your system currently has:**
- ✅ Manual backup/restore (Admin → Backup page)
- ❌ No automatic backups
- ❌ No external storage
- ❌ No retention policy
- ❌ No database size monitoring

**Let me know what you'd like me to add!** 🚀
