# MBAS Watchdog Auto-Recovery System - Complete Guide

## 🛡️ What is the Watchdog System?

The MBAS Watchdog is an **automatic recovery system** that monitors your backend server and automatically restarts it if it becomes unresponsive or hangs. This prevents system downtime and ensures your business operations continue smoothly.

### Key Features

✅ **Automatic Health Monitoring** - Checks server health every 30 seconds
✅ **Auto-Restart on Failure** - Restarts backend if 3 consecutive checks fail
✅ **Smart Recovery** - Waits 60 seconds after restart before checking again
✅ **Detailed Logging** - All events logged to `watchdog.log`
✅ **Process Management** - Cleanly terminates hung processes
✅ **Background Operation** - Runs silently without user intervention

## 🔧 How It Works

### Health Check Process

1. **Every 30 seconds**, the watchdog checks: `http://127.0.0.1:8000/health`
2. **If healthy** (HTTP 200 with `status: "healthy"`):
   - ✅ Reset failure counter
   - Continue monitoring
3. **If unhealthy** (timeout, connection error, wrong response):
   - ❌ Increment failure counter (1/3, 2/3, 3/3)
   - Log the issue
4. **After 3 failures**:
   - 🔄 Kill the hung backend process
   - 🚀 Start a new backend instance
   - 📝 Log the restart event
   - ⏳ Wait 60 seconds before next check

### Process Flow

```
┌─────────────────────────────────────────────────┐
│  Watchdog Starts                                │
│  └─> Monitors http://127.0.0.1:8000/health     │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  Health Check (every 30s)                       │
├─────────────────────────────────────────────────┤
│  ✓ HTTP 200 + "healthy" → Continue             │
│  ✗ Timeout/Error → Failure Count++             │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  Failure Count = 3?                             │
├─────────────────────────────────────────────────┤
│  YES → Auto-Restart Backend                    │
│  NO  → Continue Monitoring                      │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  Auto-Restart Process                           │
├─────────────────────────────────────────────────┤
│  1. Find processes on port 8000                 │
│  2. Kill hung backend (taskkill /F)             │
│  3. Wait 3 seconds for cleanup                  │
│  4. Start new backend (uvicorn)                 │
│  5. Wait 60 seconds cooldown                    │
│  6. Resume monitoring                           │
└─────────────────────────────────────────────────┘
```

## 📋 How to Use the Watchdog

### Method 1: System Tray (Recommended) ⭐

The **easiest and most professional** way - watchdog is built-in!

```batch
START_MBAS_TRAY.bat
```

**Features**:
- ✅ Automatically starts watchdog in background
- ✅ System tray icon for status
- ✅ No visible CMD windows
- ✅ Perfect for daily use

**What Happens**:
1. Tray icon appears (🟢 green)
2. Watchdog starts automatically
3. Backend starts with auto-recovery
4. Browser opens to MBAS

**The watchdog runs invisibly and protects your system!**

---

### Method 2: Standalone Watchdog

For administrators who want visible monitoring:

```batch
START_WITH_WATCHDOG.bat
```

**Features**:
- ✅ Visible CMD window showing health checks
- ✅ Real-time monitoring logs
- ✅ Press Ctrl+C to stop
- ✅ Good for troubleshooting

**What Happens**:
1. CMD window opens showing watchdog status
2. You see each health check in real-time
3. Backend starts automatically
4. Watchdog monitors continuously

**Output Example**:
```
[2026-04-30 10:00:00] [INFO] MBAS Backend Watchdog started
[2026-04-30 10:00:00] [INFO] Monitoring: http://127.0.0.1:8000/health
[2026-04-30 10:00:00] [INFO] Check interval: 30s
[2026-04-30 10:00:30] [INFO] Backend started (PID: 12345)
[2026-04-30 10:01:00] [INFO] Health check passed ✓
[2026-04-30 10:01:30] [INFO] Health check passed ✓
```

---

### Method 3: Complete Auto-Recovery System

For running both frontend and backend with watchdog:

```batch
AUTO_START_WITH_RECOVERY.bat
```

**Features**:
- ✅ Starts backend watchdog (minimized)
- ✅ Starts frontend
- ✅ Both run with visible windows
- ✅ Good for development/testing

**What Happens**:
1. Watchdog starts in minimized window
2. Frontend starts in visible window
3. Both monitor each other
4. Press any key to stop all

---

## 📊 Watchdog Log File

All watchdog events are logged to: `watchdog.log` (root directory)

### Reading the Log

```log
[2026-04-30 10:00:00] [INFO] MBAS Backend Watchdog started
[2026-04-30 10:00:00] [INFO] Monitoring: http://127.0.0.1:8000/health
[2026-04-30 10:00:30] [INFO] Backend started (PID: 12345)
[2026-04-30 10:05:00] [WARN] Health check failed (1/3)
[2026-04-30 10:05:30] [WARN] Health check failed (2/3)
[2026-04-30 10:06:00] [WARN] Health check failed (3/3)
[2026-04-30 10:06:00] [ERROR] Max failures reached - restarting backend
[2026-04-30 10:06:00] [INFO] Killed process on port 8000 (PID: 12345)
[2026-04-30 10:06:03] [INFO] Backend processes terminated
[2026-04-30 10:06:06] [INFO] Backend started (PID: 67890)
[2026-04-30 10:06:06] [INFO] Backend restarted successfully
[2026-04-30 10:07:06] [INFO] Backend recovered
```

### Log Levels

| Level | Meaning | Action Required |
|-------|---------|-----------------|
| **INFO** | Normal operation | None |
| **WARN** | Temporary issue detected | Monitor |
| **ERROR** | Critical issue, restart initiated | Check if recurring |

### Common Log Patterns

**✅ Normal Operation**:
```
[INFO] Health check passed
[INFO] Health check passed
[INFO] Health check passed
```

**⚠️ Temporary Network Glitch**:
```
[WARN] Health check failed (1/3)
[INFO] Backend recovered
[INFO] Health check passed
```

**🔄 Auto-Restart Triggered**:
```
[WARN] Health check failed (1/3)
[WARN] Health check failed (2/3)
[WARN] Health check failed (3/3)
[ERROR] Max failures reached - restarting backend
[INFO] Backend restarted successfully
[INFO] Backend recovered
```

---

## ⚙️ Configuration

Edit `backend/watchdog.py` to customize behavior:

```python
# Configuration at top of watchdog.py
HEALTH_CHECK_URL = "http://127.0.0.1:8000/health"
CHECK_INTERVAL = 30          # seconds between checks
MAX_FAILURES = 3             # failures before restart
RESTART_COOLDOWN = 60        # seconds to wait after restart
```

### Recommended Settings

| Use Case | CHECK_INTERVAL | MAX_FAILURES | RESTART_COOLDOWN |
|----------|---------------|--------------|------------------|
| **Production** | 30s | 3 | 60s |
| **High Traffic** | 15s | 2 | 30s |
| **Development** | 60s | 5 | 120s |

---

## 🔍 Troubleshooting

### Problem: Watchdog keeps restarting backend

**Symptoms**:
```
[ERROR] Max failures reached - restarting backend
[ERROR] Max failures reached - restarting backend
[ERROR] Max failures reached - restarting backend
```

**Possible Causes**:
1. Backend has a real bug/crash on startup
2. Port 8000 is blocked by firewall
3. Database file is corrupted
4. Missing dependencies

**Solutions**:
1. Check backend logs in CMD window
2. Try starting without watchdog: `START_MBAS.bat`
3. Check if port 8000 is free: `netstat -ano | findstr 8000`
4. Re-run `INSTALL.bat` to fix dependencies
5. Run `HEALTH_CHECK.bat` for diagnostics

---

### Problem: Watchdog doesn't start

**Symptoms**:
- No watchdog.log file
- System hangs but doesn't recover
- Error: "module 'requests' not found"

**Solutions**:

1. **Re-run INSTALL.bat**:
   ```batch
   INSTALL.bat
   ```
   This installs `requests` and `psutil` needed by watchdog

2. **Check virtual environment**:
   ```batch
   venv\Scripts\python -c "import requests, psutil"
   ```
   Should run without errors

3. **Manual dependency install**:
   ```batch
   call venv\Scripts\activate.bat
   pip install requests psutil
   ```

---

### Problem: Log file gets too large

**Symptoms**:
- `watchdog.log` is several MB
- System slows down

**Solution**:

1. **Stop MBAS**:
   ```batch
   STOP_MBAS.bat
   ```

2. **Archive old log**:
   ```batch
   move watchdog.log watchdog_backup_2026-04-30.log
   ```

3. **Restart MBAS**:
   ```batch
   START_MBAS_TRAY.bat
   ```

4. **Or clear the log**:
   ```batch
   del watchdog.log
   ```

---

## 🎯 Best Practices

### ✅ DO:

- ✅ Use `START_MBAS_TRAY.bat` for daily operations (watchdog included)
- ✅ Check `watchdog.log` weekly for unusual patterns
- ✅ Keep watchdog.log file under 10 MB
- ✅ Run `HEALTH_CHECK.bat` monthly to verify system health
- ✅ Archive old logs before deleting

### ❌ DON'T:

- ❌ Disable watchdog in production environments
- ❌ Delete watchdog.log while system is running
- ❌ Set CHECK_INTERVAL below 10 seconds (too aggressive)
- ❌ Set MAX_FAILURES to 1 (too sensitive to network glitches)
- ❌ Run multiple watchdog instances simultaneously

---

## 🔒 Security Notes

### What the Watchdog Does:

✅ **Safe Operations**:
- Monitors local health endpoint (localhost only)
- Terminates only MBAS processes
- Uses standard Windows process management
- Logs all actions for audit trail

❌ **Does NOT**:
- Access external networks
- Modify system files
- Run with elevated privileges
- Access sensitive data

### Process Termination

The watchdog uses:
```batch
taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq MBAS*"
```

This only kills processes:
- Running Python
- With "MBAS" in window title
- **Does NOT affect** other Python programs or system processes

---

## 📈 Performance Impact

### Resource Usage

| Component | CPU | RAM | Disk I/O |
|-----------|-----|-----|----------|
| Watchdog Process | <1% | ~10 MB | Minimal |
| Health Checks | <0.1% | N/A | None |
| Log Writing | <0.01% | N/A | ~1 KB/min |

**Total Impact**: Negligible (< 1% system resources)

### Network Impact

- **Health check**: ~100 bytes every 30 seconds
- **Localhost only**: No internet traffic
- **Total**: ~200 bytes/minute

---

## 🚀 Advanced Usage

### Running Watchdog as Windows Service

For 24/7 operation, use Windows Task Scheduler:

1. **Open Task Scheduler**
2. **Create Basic Task**:
   - Name: "MBAS Watchdog"
   - Trigger: "At startup"
   - Action: Start program
   - Program: `C:\MBAS\START_MBAS_TRAY.bat`
   - Start in: `C:\MBAS\`

3. **Properties**:
   - ✅ Run whether user is logged on or not
   - ✅ Run with highest privileges
   - ✅ Hidden

### Custom Health Checks

Edit `backend/watchdog.py` to add custom checks:

```python
def check_health(self):
    """Check if backend is healthy."""
    try:
        # Standard health check
        response = requests.get(HEALTH_CHECK_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":

                # ADD CUSTOM CHECKS HERE
                # Example: Check database connectivity
                db_check = requests.get("http://127.0.0.1:8000/api/system/db-health")
                if db_check.status_code != 200:
                    self.log("Database health check failed", "WARN")
                    return False

                return True
        return False
    except Exception as e:
        self.log(f"Health check error: {e}", "ERROR")
        return False
```

---

## 📞 Support

### If Watchdog Issues Persist:

1. **Collect Diagnostics**:
   ```batch
   HEALTH_CHECK.bat > diagnostics.txt
   ```

2. **Gather Logs**:
   - `watchdog.log`
   - `backend/logs/*.log`
   - Screenshot of any errors

3. **Contact Support** with:
   - Diagnostic file
   - Log files
   - Description of issue
   - When it started happening

---

## 📋 Quick Reference

| Task | Command |
|------|---------|
| **Start with watchdog** | `START_MBAS_TRAY.bat` |
| **View watchdog logs** | `type watchdog.log` |
| **Stop watchdog** | Right-click tray icon → Exit |
| **Clear logs** | `del watchdog.log` (when stopped) |
| **Check health** | `HEALTH_CHECK.bat` |
| **Standalone watchdog** | `START_WITH_WATCHDOG.bat` |

---

## ✅ Verification Checklist

After installation, verify watchdog is working:

- [ ] Run `INSTALL.bat` successfully
- [ ] Start `START_MBAS_TRAY.bat`
- [ ] System tray icon appears (🟢 green)
- [ ] Open MBAS in browser
- [ ] Check `watchdog.log` file exists
- [ ] Open watchdog.log - should see:
  - `[INFO] MBAS Backend Watchdog started`
  - `[INFO] Backend started (PID: ...)`
  - `[INFO] Health check passed` (repeating)
- [ ] Simulate failure (kill backend manually):
  ```batch
  taskkill /F /IM python.exe
  ```
- [ ] Wait 2 minutes
- [ ] Check watchdog.log shows auto-restart
- [ ] Verify MBAS is accessible again
- [ ] System recovers automatically ✅

---

**Status**: ✅ Watchdog system fully operational in MBAS v1.0.9

**Last Updated**: 2026-04-30

**Dependencies**: requests, psutil (auto-installed by INSTALL.bat)

**Log Location**: `watchdog.log` (root directory)

**Included In**: `MBAS_v1.0.9_Production_Ready.zip`
