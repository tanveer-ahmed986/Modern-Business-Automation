# MBAS Administrator Guide

## Advanced Configuration & Maintenance

This guide is for system administrators, IT personnel, and power users responsible for MBAS deployment, configuration, and maintenance.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [License Management](#license-management)
3. [Database Management](#database-management)
4. [User Management & Security](#user-management--security)
5. [Backup & Recovery](#backup--recovery)
6. [Performance Optimization](#performance-optimization)
7. [Troubleshooting](#troubleshooting)
8. [Network Deployment](#network-deployment)
9. [AI Model Configuration](#ai-model-configuration-premium)
10. [Maintenance Procedures](#maintenance-procedures)

---

## System Architecture

### Components

**Frontend** (React + Tauri):
- Location: Bundled in application
- Technology: React 19, TailwindCSS, Vite
- Port: Embedded (Tauri webview)

**Backend** (FastAPI):
- Location: `mbas-backend.exe` (embedded)
- Technology: Python, FastAPI, SQLModel
- Port: 8000 (localhost only)
- Auto-starts with application

**Database** (SQLite):
- Location: `C:\ProgramData\MBAS\mbas.db`
- Technology: SQLite 3 with FTS5
- Backup: File-based

**AI Model** (Optional - Premium):
- Location: `C:\Program Files\MBAS\resources\models\`
- Model: Phi-3-mini-4k-instruct (2.3 GB)
- Technology: llama.cpp

### File Locations

```
Application Files:
C:\Program Files\MBAS\
├── MBAS.exe (main application)
├── mbas-backend.exe (API server)
├── resources/
│   ├── models/ (AI models)
│   └── embedded/public_key.pem (license verification)
└── unins000.exe (uninstaller)

User Data:
C:\ProgramData\MBAS\
├── mbas.db (database)
├── mbas.license (system-wide license)
├── config/
│   └── secret.key (JWT signing key)
└── logs/ (application logs)

User-Specific:
C:\Users\<USERNAME>\AppData\Local\MBAS\
└── mbas.license (user-specific license)
```

### Process Architecture

On application launch:
1. Frontend (MBAS.exe) starts
2. Backend (mbas-backend.exe) auto-started as subprocess
3. License validation performed
4. Database initialized (if first run)
5. JWT secret key generated (if first run)
6. AI model loaded (if available)
7. Frontend connects to `localhost:8000`
8. User sees login screen

---

## License Management

### License File Structure

```json
{
  "licensee": "Business Name",
  "tier": "premium",
  "issued_date": "2026-04-23T00:00:00",
  "expiry_date": "2027-04-23T00:00:00",
  "machine_id_hash": "sha256_hash_or_null",
  "features": {
    "inventory": true,
    "billing": true,
    "suppliers": true,
    "ai_assistant": true,
    ...
  },
  "signature": "RSA-4096_signature"
}
```

### License Installation

**System-Wide** (Recommended for production):
```cmd
cd "C:\Program Files\MBAS\tools"
python install_license.py customer.mbas-license --location system
```

Installs to: `C:\ProgramData\MBAS\mbas.license`
- Requires administrator privileges
- Available to all users on the machine
- Protected from non-admin modification

**User-Specific**:
```cmd
python install_license.py customer.mbas-license --location user
```

Installs to: `C:\Users\<USERNAME>\AppData\Local\MBAS\mbas.license`
- No admin required
- Only available to specific user
- Each user needs their own license

### License Validation

MBAS validates license on:
- Application startup
- Every feature access (cached for 5 minutes)
- Manual re-validation via Settings

**Validation Checks**:
1. File exists and readable
2. Valid JSON format
3. RSA-4096 signature verification
4. Expiry date check (if set)
5. Machine ID hash (if set)
6. Feature flags loaded

### Upgrading License Tier

To upgrade from Basic → Standard or Standard → Premium:

1. Obtain new license file from vendor
2. Stop MBAS application
3. Replace license file:
   ```cmd
   copy /Y new-license.mbas-license C:\ProgramData\MBAS\mbas.license
   ```
4. Restart MBAS
5. Verify features in Settings → About

**No reinstallation required!**

### License Troubleshooting

**"License file not found"**:
- Check file location (system vs user)
- Verify file extension (.mbas-license)
- Ensure file permissions allow read access

**"License signature invalid"**:
- File has been modified/corrupted
- Re-download from vendor
- Never edit license files manually

**"License expired"**:
- Contact vendor for renewal
- Provide licensee name and current license

**Features disabled**:
- Verify tier supports feature
- Check feature_flags in license file
- Use `install_license.py --verify-only` to inspect

---

## Database Management

### Database Schema

MBAS uses SQLite with the following tables:
- `users` - User accounts and roles
- `settings` - System configuration
- `categories` - Product categories
- `products` - Inventory catalog
- `customers` - Customer records
- `sales` - Sales transactions
- `sale_items` - Line items for sales
- `suppliers` - Supplier information (Standard+)
- `purchases` - Purchase orders (Standard+)
- `purchase_items` - Purchase line items (Standard+)
- `ai_analytics` - AI predictions (Premium)

### Direct Database Access

**SQLite Browser** (Recommended):
1. Download DB Browser for SQLite: https://sqlitebrowser.org/
2. Open: `C:\ProgramData\MBAS\mbas.db`
3. View/query data (read-only recommended)

**Command Line**:
```cmd
cd C:\ProgramData\MBAS
sqlite3 mbas.db
.tables
SELECT * FROM users;
.exit
```

**⚠️ WARNING**: Direct database modification can corrupt data or violate constraints. Always backup first!

### Database Maintenance

**Vacuum** (Reclaim space after deletions):
```sql
VACUUM;
```

**Analyze** (Update statistics for query optimization):
```sql
ANALYZE;
```

**Check Integrity**:
```sql
PRAGMA integrity_check;
```

Run monthly or after any crashes.

### Database Size Management

Typical sizes:
- Empty: ~500 KB
- 1000 products, 10000 sales: ~5 MB
- 10000 products, 100000 sales: ~50 MB

If database exceeds 500 MB:
1. Archive old sales data
2. Run VACUUM
3. Consider partitioning (contact support)

---

## User Management & Security

### Password Security

**Default Password**: `admin123`
- **CRITICAL**: Change on first login!

**Password Policy** (Enforce manually):
- Minimum 8 characters
- Mix of letters, numbers, symbols
- Change every 90 days
- No reuse of last 3 passwords

**Password Hashing**:
- Algorithm: BCrypt (cost factor 12)
- Salted automatically
- One-way hash (cannot be decrypted)

### JWT Token Security

**Secret Key**:
- Location: `C:\ProgramData\MBAS\config\secret.key`
- Auto-generated on first run (64-byte random)
- **Never share or commit to version control**

**Token Expiry**:
- Default: 8 hours (480 minutes)
- Configurable in `backend/src/core/auth.py`

**Session Timeout**:
- Frontend redirects to login after 401
- Users must re-authenticate

### Role-Based Access Control (RBAC)

**Admin**:
- All features
- User management
- Settings configuration
- License management

**Manager**:
- Inventory management
- Sales & purchases
- Reports
- Cannot modify settings/users

**Sales User**:
- POS (billing) only
- View inventory (read-only)
- Basic dashboard
- No administrative access

**Enforcement**:
- Backend: Role checks on every endpoint
- Frontend: UI elements hidden for unauthorized roles
- Database: No direct user access (all via API)

---

## Backup & Recovery

### Automated Backup

**Windows Task Scheduler**:
1. Open Task Scheduler
2. Create Basic Task:
   - Name: "MBAS Daily Backup"
   - Trigger: Daily at 11:59 PM
   - Action: Start a program
   - Program: `C:\Program Files\MBAS\tools\backup.bat`
3. Save task

**backup.bat** (create this):
```batch
@echo off
set BACKUP_DIR=D:\MBAS_Backups
set DATE=%date:~-4,4%%date:~-7,2%%date:~-10,2%
mkdir %BACKUP_DIR% 2>nul
copy /Y C:\ProgramData\MBAS\mbas.db %BACKUP_DIR%\mbas-backup-%DATE%.db
forfiles /P %BACKUP_DIR% /M *.db /D -30 /C "cmd /c del @path"
```

Keeps 30 days of backups.

### Manual Backup

**Via Application**:
1. Settings → System → Backup
2. Click "Create Backup"
3. Save to external drive or cloud storage

**Via File Copy**:
```cmd
copy C:\ProgramData\MBAS\mbas.db D:\Backups\mbas-backup-20260423.db
```

### Recovery Procedures

**Restore from Backup** (Via Application):
1. Settings → System → Restore
2. Select backup file
3. Confirm (all current data will be lost)
4. Application restarts

**Manual Restore**:
1. Stop MBAS application
2. Replace database:
   ```cmd
   copy /Y D:\Backups\mbas-backup-20260423.db C:\ProgramData\MBAS\mbas.db
   ```
3. Restart MBAS

**Disaster Recovery**:
If database is corrupted beyond repair:
1. Restore from most recent backup
2. If no backup available:
   - Delete `mbas.db`
   - Restart application (creates fresh database)
   - **All data lost** - emphasizes importance of backups!

---

## Performance Optimization

### Database Optimization

**Enable WAL Mode** (Write-Ahead Logging):
```sql
PRAGMA journal_mode=WAL;
```
- Improves concurrent read/write performance
- Enables point-in-time recovery

**Increase Cache Size**:
```sql
PRAGMA cache_size = -64000;  -- 64 MB
```

**Create Indexes** (if needed):
```sql
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(created_at);
CREATE INDEX IF NOT EXISTS idx_sale_items_product ON sale_items(product_id);
```

### Application Performance

**Startup Time**:
- Cold start: 5-10 seconds
- With AI model: 15-30 seconds
- To improve: Use SSD, close unnecessary apps

**Query Performance**:
- Use date ranges in reports (not "All Time")
- Limit results to recent data
- Archive old records if needed

**AI Model Performance**:
- CPU-only: 5-15 seconds per query
- 4 threads: Optimal for most CPUs
- More threads = faster (if CPU supports)

### System Requirements

**For 10,000+ transactions**:
- RAM: 8 GB minimum
- Disk: SSD strongly recommended
- CPU: Quad-core 2.5 GHz+

---

## Troubleshooting

### Common Issues

**Backend won't start**:
```cmd
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process using port
taskkill /F /PID <PID>

# Restart MBAS
```

**Database locked**:
```cmd
# Close all MBAS instances
taskkill /F /IM MBAS.exe
taskkill /F /IM mbas-backend.exe

# Delete lock files
del C:\ProgramData\MBAS\mbas.db-shm
del C:\ProgramData\MBAS\mbas.db-wal

# Restart
```

**License validation fails**:
```cmd
# Verify license file
cd "C:\Program Files\MBAS\tools"
python install_license.py C:\ProgramData\MBAS\mbas.license --verify-only

# Check signature, expiry, features
```

**AI model not loading**:
```cmd
# Verify model exists
dir "C:\Program Files\MBAS\resources\models\"

# Check model size (~2.3 GB)
# Re-download if needed:
python scripts\download_model.py
```

### Log Files

**Backend Logs**:
Location: `C:\ProgramData\MBAS\logs\backend.log`

View recent errors:
```cmd
powershell Get-Content C:\ProgramData\MBAS\logs\backend.log -Tail 50
```

**Windows Event Viewer**:
- Application logs may contain MBAS errors
- Look for source: "MBAS" or "mbas-backend"

---

## Network Deployment

### Shared Database Setup

**Server Setup**:
1. Install MBAS on server/main computer
2. Share database directory:
   - Right-click `C:\ProgramData\MBAS`
   - Properties → Sharing → Advanced Sharing
   - Share name: `MBAS_Data`
   - Permissions: Full Control for authorized users

**Client Setup**:
1. Install MBAS on client computers
2. Map network drive:
   ```cmd
   net use Z: \\SERVER\MBAS_Data /persistent:yes
   ```
3. Create symlink to shared database:
   ```cmd
   mklink C:\ProgramData\MBAS\mbas.db Z:\mbas.db
   ```
4. Restart MBAS

**Limitations**:
- SQLite supports multiple readers, single writer
- High concurrency may cause locks
- Network latency affects performance
- Consider PostgreSQL for >10 concurrent users

---

## AI Model Configuration (Premium)

### Downloading AI Model

**Automated**:
```cmd
cd "C:\Program Files\MBAS"
python scripts\download_model.py
```

**Manual**:
1. Download from: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf
2. Save as: `C:\Program Files\MBAS\resources\models\Phi-3-mini-4k-instruct.q4.gguf`
3. Verify size: ~2.3 GB

### Model Performance Tuning

Edit `backend/src/ai/llm.py`:

```python
self.model = Llama(
    model_path=str(self.model_path),
    n_ctx=2048,         # Context window (increase for longer queries)
    n_threads=4,        # CPU threads (match your CPU cores)
    n_gpu_layers=0,     # GPU offload (0 = CPU only)
    verbose=False
)
```

**Recommended Settings**:
- 4-core CPU: `n_threads=4`
- 8-core CPU: `n_threads=6`
- 16-core CPU: `n_threads=8`

---

## Maintenance Procedures

### Daily Tasks

- [x] Verify application starts correctly
- [x] Check for error messages
- [x] Review low stock alerts

### Weekly Tasks

- [x] Review backup status
- [x] Check disk space (>10% free)
- [x] Test backup restore (monthly)
- [x] Review user activity logs

### Monthly Tasks

- [x] Run database integrity check
- [x] Run VACUUM and ANALYZE
- [x] Review and archive old data
- [x] Update documentation if processes changed
- [x] Check for MBAS updates (from vendor)

### License Renewal

30 days before expiry:
- [ ] Contact vendor for renewal
- [ ] Prepare payment/purchase order
- [ ] Test new license in development
- [ ] Deploy to production
- [ ] Verify features activated

---

## Advanced Topics

### Custom Branding

**Logo**: Settings → General → Upload Logo
- Format: PNG/JPG
- Size: 200x200 px recommended
- Appears on receipts and login screen

**Colors**: (Requires custom build - contact vendor)

### Data Export

**Sales Export** (Manual):
```sql
.mode csv
.output sales_export.csv
SELECT * FROM sales WHERE created_at >= '2026-01-01';
.output stdout
```

**Automated Export** (PowerShell):
```powershell
sqlite3 C:\ProgramData\MBAS\mbas.db ".mode csv" ".output export.csv" "SELECT * FROM sales" ".quit"
```

---

## Support Escalation

**Level 1** (User):
- Check user manual
- Try restarting application
- Verify license is valid

**Level 2** (Admin):
- Check this guide
- Review logs
- Test with different user/role
- Verify database integrity

**Level 3** (Vendor Support):
- Provide:
  - MBAS version
  - License tier
  - Error logs
  - Steps to reproduce
  - Screenshots
- Contact: support@mbas.local

---

**MBAS Administrator Guide v1.0**
Last Updated: 2026-04-23
