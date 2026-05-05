# MBAS - End User Installation Guide

**Version:** 1.2.1
**Date:** 2026-05-03
**System:** Modern Business Automation System

---

## ⚡ Quick Start (5 Minutes)

### Option 1: Portable Installation (Recommended for systems with errors)

1. **Run the installer:**
   ```
   Double-click: PORTABLE_INSTALL_MBAS.bat
   ```

2. **Follow the prompts:**
   - Choose installation directory (default: C:\MBAS)
   - Wait 3-5 minutes for installation
   - Click "Yes" to start MBAS

3. **Access MBAS:**
   - Open browser: http://localhost:3000
   - Login: admin / admin123
   - **IMPORTANT:** Change password immediately!

### Option 2: Standard Installer (If no taskkill errors)

1. **Run:**
   ```
   Double-click: MBAS_Setup_v1.2.1_NoTaskkill.exe
   ```

2. **Installation wizard:**
   - Accept license
   - Choose installation directory (C:\MBAS recommended)
   - Wait 5-10 minutes for installation
   - Click "Launch MBAS" when complete

3. **Access MBAS:**
   - Open browser: http://localhost:3000
   - Login: admin / admin123
   - **IMPORTANT:** Change password immediately!

---

## 📋 System Requirements

### Minimum Requirements
- **OS:** Windows 10/11 (64-bit)
- **RAM:** 4 GB
- **Disk:** 2 GB free space
- **Python:** 3.11 or 3.12 (auto-installed if using installer)
- **Browser:** Chrome, Firefox, Edge (latest versions)

### Recommended
- **RAM:** 8 GB or more
- **Disk:** 5 GB free space (for data growth)
- **SSD:** For better performance

---

## 🔧 Installation Methods

### Method 1: Portable Installation ✅ RECOMMENDED

**Best for:**
- Systems with corrupted taskkill.exe
- No administrator privileges
- Quick setup without installer
- USB/portable installations

**Steps:**
1. Extract all files to a folder (e.g., Downloads\MBAS)
2. Run: `PORTABLE_INSTALL_MBAS.bat`
3. Choose installation directory
4. Wait for installation to complete
5. Start MBAS from desktop shortcut

**Time:** 3-5 minutes

### Method 2: Standard Installer

**Best for:**
- Clean Windows installations
- First-time installations
- Non-technical users

**Steps:**
1. Run: `MBAS_Setup_v1.2.1_NoTaskkill.exe`
2. Follow installation wizard
3. Choose options (desktop shortcut, auto-start, etc.)
4. Wait for completion
5. Launch MBAS

**Time:** 5-10 minutes

---

## 🚀 First Time Setup

### 1. Start MBAS

**From Desktop:**
- Double-click "MBAS" icon

**From Start Menu:**
- Start → MBAS → Modern Business Automation System

**Manual Start:**
- Navigate to: C:\MBAS
- Run: `START_MBAS_TRAY.bat`

**Wait:** 10-20 seconds for services to start

### 2. Access Web Interface

1. Open your browser
2. Navigate to: http://localhost:3000
3. You should see the MBAS login page

**Bookmark this URL!**

### 3. First Login

**Default Credentials:**
```
Username: admin
Password: admin123
```

**⚠️ CRITICAL SECURITY STEP:**
1. Login with default credentials
2. Go to Settings → Users
3. Change admin password immediately
4. Use a strong password (8+ characters, mixed case, numbers)

### 4. Configure Your Business

1. **Business Information:**
   - Go to Settings → Business
   - Enter your company name, address, phone
   - Upload logo (optional)

2. **Add Users (if needed):**
   - Settings → Users
   - Create accounts for employees
   - Assign roles (Admin, Manager, Sales User)

3. **Add Product Categories:**
   - Inventory → Categories
   - Create your product categories

4. **Add Products:**
   - Inventory → Products
   - Add your inventory items
   - Set prices, stock levels

5. **Add Customers:**
   - Billing → Customers
   - Add customer information

6. **Add Suppliers (if using Purchase Orders):**
   - Purchases → Suppliers
   - Add supplier information

---

## 📊 Daily Usage

### Starting MBAS
- **Auto-start:** System tray icon appears automatically (if enabled)
- **Manual start:** Double-click desktop shortcut
- **Always available at:** http://localhost:3000

### Stopping MBAS
- **From system tray:** Right-click MBAS icon → Exit
- **From folder:** Run `STOP_MBAS.bat`
- **Force stop:** Run `EMERGENCY_FIX.bat`

### Common Tasks

**1. Create a Sale:**
- Billing → New Sale
- Select customer
- Add products
- Generate invoice
- Print or email

**2. Add Inventory:**
- Inventory → Products → Add Product
- Fill in details
- Set stock quantity

**3. View Dashboard:**
- Dashboard → See sales, revenue, inventory levels
- View charts and graphs

**4. Generate Reports:**
- Reports → Choose report type
- Select date range
- Export to PDF or Excel

**5. Process Purchase Order:**
- Purchases → New Purchase Order
- Select supplier
- Add items
- Submit order

---

## 🔒 Security Best Practices

### Password Security
- ✅ Change default password immediately
- ✅ Use strong passwords (8+ characters)
- ✅ Don't share passwords
- ✅ Change passwords every 90 days

### Data Security
- ✅ Enable automatic backups (Settings → Backup)
- ✅ Store backups on external drive
- ✅ Test backup restoration quarterly
- ✅ Restrict user access by role

### System Security
- ✅ Keep Windows updated
- ✅ Use antivirus software
- ✅ Don't open MBAS to internet without VPN
- ✅ Use https for production deployments

---

## 🛠️ Troubleshooting

### MBAS Won't Start

**Solution 1: Health Check**
```
Run: HEALTH_CHECK.bat
Follow the diagnostics
```

**Solution 2: Emergency Fix**
```
Run: EMERGENCY_FIX.bat
Wait for automatic repair
```

**Solution 3: Check Port Conflicts**
```
Another program might be using port 8000 or 3000
Close other applications and try again
```

### Can't Access http://localhost:3000

**Checks:**
1. Is MBAS running? (Check system tray for icon)
2. Wait 30 seconds after starting
3. Try: http://127.0.0.1:3000
4. Check firewall settings
5. Run: `DIAGNOSE_AND_FIX.bat`

### Login Not Working

**Solutions:**
1. Verify credentials: admin / admin123 (if not changed)
2. Check Caps Lock is off
3. Clear browser cache
4. Try different browser
5. Run database repair: `EMERGENCY_FIX.bat`

### Installation Errors

**Error: taskkill.exe (0xc0000142)**
- Use portable installation instead
- OR run: `FIX_TASKKILL_ERROR_AND_INSTALL.bat`

**Error: Python not found**
- Install Python 3.11 or 3.12
- Download: https://www.python.org/downloads/
- Check "Add Python to PATH" during installation

**Error: Permission denied**
- Run installer as Administrator
- OR install to C:\MBAS (no admin required)

### Slow Performance

**Solutions:**
1. Close unnecessary programs
2. Check disk space (need 1GB+ free)
3. Restart MBAS
4. Compact database (Settings → System → Compact Database)
5. Check antivirus isn't scanning MBAS files

---

## 💾 Backup & Recovery

### Automatic Backups (Recommended)

1. Go to: Settings → Backup
2. Enable automatic backups
3. Set schedule (daily recommended)
4. Choose backup location (external drive recommended)

### Manual Backup

**Method 1: Using MBAS**
- Settings → Backup → Create Backup Now
- Save to external drive or cloud storage

**Method 2: File Copy**
- Close MBAS
- Copy entire folder: `C:\MBAS\backend\mbas_database.db`
- Copy to safe location

### Restore from Backup

**Method 1: Using MBAS**
- Settings → Backup → Restore Backup
- Choose backup file
- Confirm restoration

**Method 2: Manual**
1. Stop MBAS
2. Replace: `C:\MBAS\backend\mbas_database.db`
3. Start MBAS

---

## 📱 Multi-User Setup

### Network Access (Optional)

**To allow other computers to access MBAS:**

1. **Find your IP address:**
   ```
   Run: cmd
   Type: ipconfig
   Look for: IPv4 Address (e.g., 192.168.1.100)
   ```

2. **Configure firewall:**
   - Windows Defender Firewall
   - Allow port 8000 and 3000
   - Allow Python and Node.js

3. **Access from other computers:**
   - Open browser
   - Navigate to: http://[YOUR-IP]:3000
   - Example: http://192.168.1.100:3000

**⚠️ Security Warning:**
- Only use on trusted local networks
- Don't expose to internet without proper security
- Consider VPN for remote access

---

## 🔄 Updates & Maintenance

### Checking for Updates
- Visit: Settings → About
- Check current version
- Download updates from official source

### Installing Updates
1. Backup your data first!
2. Run new installer
3. Choose "Upgrade" option
4. Database automatically migrated

### Database Maintenance

**Weekly:**
- No action needed (automatic)

**Monthly:**
- Settings → System → Compact Database
- Review and archive old data

**Quarterly:**
- Test backup restoration
- Review user accounts
- Clean up old records

---

## 📞 Support & Help

### Built-in Help
- Help button in top right corner
- Tooltips on form fields
- Settings → Documentation

### System Diagnostics
- Run: `HEALTH_CHECK.bat`
- Run: `DIAGNOSE_AND_FIX.bat`
- Check logs: `backend\*.log`

### Log Files
- Backend logs: `C:\MBAS\backend\*.log`
- Frontend logs: Browser console (F12)
- Debug mode: Run `START_MBAS_TRAY_DEBUG.bat`

### Getting Help
1. Check this guide first
2. Run diagnostics
3. Review error messages
4. Contact your IT support
5. Check documentation in `docs\` folder

---

## 📚 Additional Resources

### Included Documentation
- `README_FIRST.txt` - Quick overview
- `FIX_INSTALLATION_ISSUES.txt` - Troubleshooting
- `docs\` folder - Detailed documentation

### Quick Reference Card
- `QUICK_REFERENCE.txt` - Common tasks and shortcuts

### Video Tutorials (if available)
- Check `docs\tutorials\` folder

---

## ✅ Installation Checklist

Before considering installation complete:

- [ ] MBAS starts without errors
- [ ] Can access http://localhost:3000
- [ ] Successfully logged in
- [ ] Changed default admin password
- [ ] Added business information
- [ ] Created at least one user (if needed)
- [ ] Added product categories
- [ ] Added sample products
- [ ] Tested creating a sale
- [ ] Configured automatic backups
- [ ] Created manual backup
- [ ] Tested backup restoration
- [ ] Desktop shortcut working
- [ ] System tray icon appearing
- [ ] All users can access (if multi-user)

---

## 🎓 Training Recommendations

### For Administrators
1. Complete all setup steps
2. Practice backup/restore
3. Learn user management
4. Understand reports

### For Sales Users
1. How to create sales
2. How to add customers
3. How to print invoices
4. How to search products

### For Managers
1. How to view dashboard
2. How to generate reports
3. How to manage inventory
4. How to view analytics

**Estimated Training Time:**
- Admin: 2-3 hours
- Manager: 1-2 hours
- Sales User: 30-60 minutes

---

## 🏁 Final Checklist

**You're ready to use MBAS when:**
- ✅ Installation completed successfully
- ✅ Can login and access all features
- ✅ Changed default password
- ✅ Configured business information
- ✅ Backup system configured
- ✅ All users trained
- ✅ Sample data entered and tested

**Congratulations! Your MBAS installation is complete.**

---

## 📄 License Information

**Version:** 1.2.1 (STANDARD)
**Licensed For:** Electronics
**Expires:** 2027-04-26
**Features Enabled:** 8

To upgrade license or extend expiration, contact your vendor.

---

**End of Guide**

For additional help, see `README_FIRST.txt` or run `HEALTH_CHECK.bat`
