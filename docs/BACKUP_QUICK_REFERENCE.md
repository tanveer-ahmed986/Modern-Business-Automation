# Backup & Recovery - Quick Reference

## ⚡ Quick Answers

### How to recover data if system crashes?
1. Go to Backup page (Admin → Backup in sidebar)
2. Click "Restore" on most recent backup
3. Restart application
4. Data recovered ✅

### How much can SQLite store?
- **Technical limit:** 281 TB
- **Practical limit:** 10 GB (good performance)
- **Your business:** Likely < 2 GB for 5 years
- **Conclusion:** SQLite is perfect for 99% of users

### When to use PostgreSQL?
- Database > 10 GB ❌ (SQLite slows down)
- 50+ concurrent users ❌ (SQLite locks)
- Multiple locations/branches ❌ (Need central server)
- For single-location businesses ✅ (SQLite is better)

---

## 📋 Daily Backup Checklist

### Manual Backup (Current System)
```
1. Login as admin
2. Click "Backup" in left sidebar
3. Click "Create New Backup"
4. Copy backup to USB drive:
   - Source: backend\backups\
   - Destination: E:\MBAS_Backups\
5. Done! (Takes 1 minute)
```

### External Backup Script (Windows)
```batch
# Save as: daily_backup.bat
# Run daily or schedule in Task Scheduler

@echo off
set DATE=%date:~-4,4%%date:~-10,2%%date:~-7,2%
xcopy "backend\backups\*" "E:\MBAS_Backups\%DATE%\" /E /Y
echo Backup completed successfully!
pause
```

---

## 🚨 Emergency Recovery Scenarios

### Scenario 1: Database Corrupted
```
Symptoms: App crashes, "database locked" error
Fix:
1. Stop application
2. Backup → Click "Restore" on recent backup
3. Restart app
4. Recovered ✅
```

### Scenario 2: Computer Crashed (Hardware Failure)
```
Symptoms: Computer won't boot, hard drive failed
Fix:
1. Install MBAS on new computer
2. Copy backup from USB/cloud
3. Place backup as: backend\database\mbas_database.db
4. Start app
5. Recovered ✅
```

### Scenario 3: Accidental Data Deletion
```
Symptoms: Deleted important products/sales by mistake
Fix:
1. Restore from backup BEFORE deletion
2. Use DB Browser for SQLite to export specific data
3. Import back into current database
4. Recovered ✅
```

---

## 📊 Database Size Guide

### Estimated Storage (5 Years)

| Business Type | Sales/Day | Total Sales | Database Size |
|---------------|-----------|-------------|---------------|
| **Small Shop** | 20 | 36,500 | ~50 MB |
| **Medium Store** | 100 | 182,500 | ~200 MB |
| **Large Retail** | 500 | 912,500 | ~1 GB |
| **Very Large** | 2000 | 3,650,000 | ~4 GB |

### Performance Expectations

| Database Size | Performance | Action Needed |
|---------------|-------------|---------------|
| **< 1 GB** | ⚡ Excellent | None |
| **1-5 GB** | ✅ Good | Monitor growth |
| **5-10 GB** | ⚠️ Acceptable | Consider archival |
| **> 10 GB** | 🐌 Slow | Migrate to PostgreSQL |

---

## 🔧 Current Limitations

Your MBAS system has:
- ✅ Manual backup/restore
- ❌ No automatic backups
- ❌ No external storage sync
- ❌ No size monitoring
- ❌ No archival system

**Recommendation:** Add automatic daily backups

---

## 💡 Recommended Improvements

### Priority 1: Automatic Backups
- Daily backups at midnight
- Keep last 7 daily, 4 weekly, 3 monthly
- Auto-delete old backups

### Priority 2: Database Size Monitoring
- Dashboard widget showing size
- Warning when approaching 5 GB
- Growth rate prediction

### Priority 3: Data Archival
- Archive sales older than 2 years
- Keep main DB < 1 GB
- Access archived data when needed

---

## 📞 What to Implement?

Tell me which features you want:

1. **Automatic Backup System** ✅ (Recommended)
2. **Database Size Dashboard** ✅ (Simple to add)
3. **Data Archival System** ✅ (For long-term growth)
4. **PostgreSQL Migration Tool** ✅ (Future-proofing)

**Let me know what to build next!** 🚀
