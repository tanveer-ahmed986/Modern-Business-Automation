# MBAS v2.1.0 - PWA Deployment Guide

**Z&T Technologies | State-of-the-Art Business Solutions**
**Website**: www.zttechnologies.org
**Email**: zttechnologies12@gmail.com

---

## What's New in v2.1.0

### 🌍 Cross-Platform Support (NEW!)
- ✅ Windows 7, 10, 11 (previously Windows 10/11 only)
- ✅ Android phones and tablets
- ✅ iOS (iPhone, iPad)
- ✅ Any device with a modern browser

### ⚡ Performance Improvements
- 60-80% faster page loads
- 50% lower memory usage
- Instant search (debounced)
- Pagination (load 50 items vs 1000+)

### 📱 Progressive Web App (PWA)
- Install like a native app
- Works offline
- Auto-updates (no reinstallation)
- Responsive design (mobile, tablet, desktop)

---

## Deployment Options

### Option 1: Local WiFi Server (Recommended for Offline Use)

**Best for**: Single location (shop, office) with multiple devices

**How it works**:
1. Run MBAS server on one computer (shop owner's laptop/desktop)
2. Other devices access via WiFi (employees' tablets, phones, laptops)
3. No internet required - works 100% offline

**Setup**:
```batch
1. Double-click START_MBAS_SERVER.bat
2. Wait for "Server running..."
3. Note the IP address shown (e.g., http://192.168.1.100:8000)
4. On mobile devices, open that URL in browser
5. Tap "Add to Home Screen" → App installs!
```

**Requirements**:
- One Windows PC with Python 3.10+ (can be Windows 7)
- WiFi network (all devices connected)
- No internet needed

---

### Option 2: USB Portable (For Testing/Demo)

**Best for**: Running on different PCs without installation

**Setup**:
```batch
1. Copy entire MBAS folder to USB drive
2. Plug USB into any Windows PC
3. Run START_MBAS_SERVER.bat from USB
4. Server starts → Open http://localhost:8000
```

**Requirements**:
- Python 3.10+ installed on target PC
- USB drive (8GB+)

---

### Option 3: Cloud Hosted (For Multi-Location Access)

**Best for**: Multiple branches, remote access

**Platforms**:
- **Render.com** (Free tier available)
- **Railway.app** ($5/month credit)
- **DigitalOcean** ($6/month VPS)

**Setup**:
See `CLOUD_DEPLOYMENT.md` for detailed instructions.

---

## Installation Instructions

### For Desktop/Laptop Users

1. **Start Server**:
   - Double-click `START_MBAS_SERVER.bat`
   - Wait for "Server running..."

2. **Open Browser**:
   - Chrome, Edge, or Firefox
   - Navigate to http://localhost:8000

3. **Install PWA** (Optional but recommended):
   - Click "Install" button in address bar (Chrome/Edge)
   - Or: Menu → Install MBAS
   - App installs to desktop/start menu
   - Works offline after installation!

4. **Login**:
   - Username: `admin`
   - Password: `admin123`
   - Change password immediately!

---

### For Mobile/Tablet Users (Android/iOS)

1. **Connect to WiFi**:
   - Same network as the server computer

2. **Find Server IP**:
   - Server shows IP on startup (e.g., http://192.168.1.100:8000)
   - Or ask person running the server

3. **Open Browser**:
   - Chrome (Android) or Safari (iOS)
   - Navigate to http://192.168.x.x:8000 (use actual IP)

4. **Install App**:
   **Android (Chrome)**:
   - Tap menu (⋮) → "Add to Home screen"
   - Tap "Install" on popup
   - Icon appears on home screen

   **iOS (Safari)**:
   - Tap Share button (square with arrow)
   - Scroll down → "Add to Home Screen"
   - Tap "Add"
   - Icon appears on home screen

5. **Launch**:
   - Tap MBAS icon on home screen
   - Runs like a native app!
   - Works offline (after first load)

---

## System Requirements

### Server Computer (Runs Backend)
- **OS**: Windows 7, 10, or 11
- **Python**: 3.10, 3.11, or 3.12
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 500MB minimum
- **Network**: WiFi or Ethernet (for multi-device access)

### Client Devices (Access PWA)
- **Browsers**:
  - Chrome 90+ (Windows, Android, macOS)
  - Edge 90+ (Windows)
  - Safari 14+ (iOS, macOS)
  - Firefox 88+ (Windows, Android)

- **Mobile**:
  - Android 8.0+
  - iOS 14.0+

- **No Python needed on client devices!**

---

## Features

### ✅ Inventory Management
- Product catalog with categories
- Stock tracking
- Low stock alerts
- Barcode search
- Cost & selling price tracking

### ✅ Billing & Sales
- POS (Point of Sale) interface
- Customer management
- Payment tracking
- Receipt generation
- Sales history

### ✅ Supplier & Purchases
- Supplier management
- Purchase orders
- Stock replenishment
- Supplier ledger
- Payment tracking

### ✅ Reports & Analytics
- Sales reports (daily, monthly, yearly)
- Profit & loss statements
- Stock reports
- Top products/customers
- Export to Excel (Premium)

### ✅ Dashboard
- Today's sales overview
- Low stock alerts
- Recent transactions
- Quick stats

### ✅ User Management
- Role-based access (Admin, Manager, Sales User)
- User accounts
- Permission control

### ✅ Automatic Backups (NEW!)
- Scheduled backups
- Manual backup/restore
- Data protection

### ✅ AI Analytics (Premium)
- Sales forecasting
- Demand prediction
- Inventory optimization

---

## Offline Mode

### How Offline Works
1. **First Load**: Requires internet/WiFi (downloads app)
2. **After Installation**: Works 100% offline
3. **Service Worker**: Caches app for offline use
4. **Local Database**: SQLite (no cloud dependency)

### What Works Offline
- ✅ All core features (inventory, billing, reports)
- ✅ View data (products, sales, customers)
- ✅ Create new sales/purchases
- ✅ Search functionality
- ✅ Generate reports

### What Doesn't Work Offline
- ❌ Updates/new versions (requires connection to check)
- ❌ AI analytics (if using cloud API)

### Reconnecting
- App auto-detects when online
- Shows "Back online!" message
- Syncs any pending changes

---

## Troubleshooting

### Server Won't Start

**Problem**: "Python not found"
**Solution**:
```batch
1. Install Python from python.org
2. Download Windows installer (3.10, 3.11, or 3.12)
3. IMPORTANT: Check "Add Python to PATH" during install
4. Restart computer
5. Try again
```

**Problem**: "Port 8000 already in use"
**Solution**:
```batch
1. Close other MBAS instances
2. Or kill process:
   - Open Task Manager (Ctrl+Shift+Esc)
   - Find "python.exe" → End Task
3. Try again
```

---

### Mobile Can't Connect

**Problem**: Can't access http://192.168.x.x:8000
**Solution**:
```
1. Check WiFi:
   - Mobile and server on SAME WiFi network
   - Not on mobile data!

2. Check IP:
   - Server shows IP on startup
   - Or run "ipconfig" on server PC
   - Look for "IPv4 Address"

3. Check Firewall:
   - Windows may block port 8000
   - Allow Python through firewall:
     Control Panel → Firewall → Allow App
     → Find Python → Check Private/Public

4. Try localhost first:
   - On server PC, open http://localhost:8000
   - If works → firewall issue
   - If doesn't work → server issue
```

---

### App Won't Install

**Problem**: No "Install" button
**Solution**:
```
1. Use Chrome or Edge (not Firefox/Internet Explorer)
2. Wait for page to fully load
3. Look for install icon in address bar
4. Android: Menu → "Add to Home screen"
5. iOS: Share → "Add to Home Screen"
```

**Problem**: "Not secure" warning
**Solution**:
```
Normal! Local servers (http://) show this.
HTTPS not needed for local WiFi.
Safe to proceed.
```

---

### Login Issues

**Problem**: "Invalid credentials"
**Solution**:
```
Default login:
Username: admin
Password: admin123

If changed and forgotten:
1. Stop server (Ctrl+C)
2. Run: python backend/reset_admin_password.py
3. Restart server
```

---

## Security Best Practices

### 1. Change Default Password
```
Login → Users → admin → Change Password
Use strong password (12+ characters)
```

### 2. Create User Accounts
```
Don't share admin account
Create separate accounts for employees
Assign appropriate roles:
- Admin: Full access
- Manager: Inventory, reports
- Sales User: Billing only
```

### 3. Regular Backups
```
Dashboard → Automatic Backup
Enable: Daily backups
Keep: 7-30 days of backups
Test restore occasionally
```

### 4. Network Security
```
Local WiFi only (not public WiFi)
Change WiFi password regularly
Use router firewall
```

### 5. Physical Security
```
Lock server computer when unattended
Restrict access to server room
Log out after use
```

---

## Updating MBAS

### Auto-Update (PWA)
1. Open MBAS (online)
2. If update available → Popup appears
3. Click "Update Now"
4. Page reloads with new version
5. Done!

### Manual Update
1. Download new version
2. Stop server (Ctrl+C)
3. Replace backend/ and frontend/ folders
4. Restart server
5. Force refresh in browser (Ctrl+F5)

---

## Support

### Self-Help Resources
- User Manual: `docs/USER_MANUAL.md`
- Video Tutorials: www.zttechnologies.org/tutorials
- FAQ: `docs/FAQ.md`

### Contact Support
- Email: zttechnologies12@gmail.com
- Website: www.zttechnologies.org
- Response time: 24-48 hours

### Reporting Bugs
Include:
1. MBAS version (shown in About)
2. Device/browser (e.g., "Android Chrome")
3. Steps to reproduce
4. Screenshots (if applicable)

---

## License

Modern Business Automation System (MBAS)
Copyright © 2024-2026 Z&T Technologies

Licensed under MBAS License Agreement.
See `LICENSE.md` for details.

---

## Changelog

### v2.1.0 (2026-06-20)
**New Features**:
- Progressive Web App (PWA) support
- Cross-platform compatibility (Windows 7, Android, iOS)
- Offline mode with Service Worker
- Mobile-responsive design
- Local WiFi deployment option

**Performance**:
- 60-80% faster page loads
- 50% lower memory usage
- API pagination (50 items/page)
- Search debouncing
- Code splitting

**Backend**:
- Python 3.10+ compatibility (down from 3.12)
- CORS support for WiFi access
- Version API endpoint
- Enhanced health check

### v2.0.6 (2026-06-20)
**Performance Fixes**:
- Optimized JavaScript bundles
- Lazy loading routes
- Fixed UI freezing issues
- Reduced bundle size (487KB → 300KB)

---

END OF PWA DEPLOYMENT GUIDE
