# MBAS Pre-Release QA Checklist

**Version**: 1.0.0
**Date**: 2026-04-23
**Tester**: _______________
**Environment**: _______________

---

## 1. Build & Installation

### 1.1 Build Process
- [ ] `build-all.bat` completes without errors
- [ ] Backend compiles successfully (mbas-backend.exe created)
- [ ] Frontend builds successfully (dist/ folder populated)
- [ ] Tauri MSI installer generated
- [ ] `verify-build.bat` passes all checks
- [ ] Installer size is reasonable (~50-100 MB without AI model)

### 1.2 Installation
- [ ] MSI installer runs without errors
- [ ] Can install to default location (C:\Program Files\MBAS\)
- [ ] Can install to custom location
- [ ] Desktop shortcut created (if selected)
- [ ] Start menu shortcut created (if selected)
- [ ] No errors in installation logs

### 1.3 First Launch
- [ ] Application launches successfully after install
- [ ] Backend starts automatically (mbas-backend.exe in Task Manager)
- [ ] Database initializes correctly (mbas.db created)
- [ ] Secret key generated (config/secret.key exists)
- [ ] Login screen appears
- [ ] No console windows visible (production mode)

---

## 2. License Management

### 2.1 License Validation
- [ ] App starts without license (demo/basic mode)
- [ ] License file validates successfully when installed
- [ ] System-wide license location works (C:\ProgramData\MBAS\)
- [ ] User-specific license location works (AppData\Local\)
- [ ] Invalid license rejected with clear error message
- [ ] Expired license detected and blocked
- [ ] Tampered license rejected (signature validation)

### 2.2 License Tiers
- [ ] **Basic**: Only basic features accessible
- [ ] **Standard**: Suppliers, Purchases, Advanced Reports accessible
- [ ] **Premium**: AI features accessible
- [ ] Feature upgrade prompt shows when accessing disabled features
- [ ] License info displayed in Settings → About

### 2.3 License Tools
- [ ] `license_generator.py` creates valid licenses
- [ ] Generated licenses validate successfully
- [ ] `install_license.py` installs to correct location
- [ ] License verification (--verify-only) shows correct info

---

## 3. Authentication & Authorization

### 3.1 Login
- [ ] Can login with default credentials (admin/admin123)
- [ ] Invalid credentials rejected
- [ ] JWT token generated on successful login
- [ ] Token stored in localStorage
- [ ] Session expires after timeout (401 redirect)
- [ ] Login page shows session expired message when redirected

### 3.2 User Management
- [ ] Can create new users (Admin, Manager, Sales User)
- [ ] Can edit existing users
- [ ] Can change passwords
- [ ] Can disable users
- [ ] Can delete users
- [ ] Passwords are hashed (not visible in database)

### 3.3 Role-Based Access
- [ ] **Admin**: Full access to all features
- [ ] **Manager**: Cannot access Users or Settings
- [ ] **Sales User**: Only Billing and Dashboard accessible
- [ ] Unauthorized endpoints return 403
- [ ] UI hides unavailable features based on role

---

## 4. Core Features - All Tiers

### 4.1 Dashboard
- [ ] Metrics display correctly (Today's Sales, Monthly Revenue, etc.)
- [ ] Sales chart renders
- [ ] Low stock alerts show products below reorder level
- [ ] Quick actions navigate to correct pages
- [ ] Real-time updates after transactions

### 4.2 Inventory Management
- [ ] Can add new products
- [ ] Can edit existing products
- [ ] Can delete products
- [ ] Can add categories
- [ ] Search function works (name, SKU, barcode)
- [ ] Filter by category works
- [ ] Low stock filter works
- [ ] Pagination works (if many products)

### 4.3 Billing (POS)
- [ ] Can add products to cart
- [ ] Quantity adjustment works (+/- buttons)
- [ ] Can remove items from cart
- [ ] Discount calculation correct
- [ ] Tax calculation correct (matches settings tax rate)
- [ ] Grand total calculation correct
- [ ] Invoice number generated (INV-YYYYMMDD-XXXX format)
- [ ] Stock decreases correctly after sale
- [ ] Sale saved to database
- [ ] Receipt displays correctly

### 4.4 Customers
- [ ] Can add new customers
- [ ] Can edit customers
- [ ] Can link customer to sale
- [ ] Customer purchase history visible
- [ ] Total spent calculated correctly

---

## 5. Standard/Premium Features

### 5.1 Suppliers (Standard+)
- [ ] Can add suppliers
- [ ] Can edit suppliers
- [ ] Supplier list displays correctly

### 5.2 Purchases (Standard+)
- [ ] Can create purchase orders
- [ ] Can add items to purchase
- [ ] Total calculated correctly
- [ ] Can mark as received
- [ ] Stock increases when received
- [ ] Cost prices updated

### 5.3 Advanced Reports (Standard+)
- [ ] Sales report generates correctly
- [ ] Date range filter works
- [ ] Product report shows per-product data
- [ ] Monthly report displays trends
- [ ] Data matches database queries
- [ ] Export to PDF works (if implemented)

### 5.4 P&L Reports (Premium)
- [ ] Profit & Loss report generates
- [ ] Revenue calculated correctly
- [ ] COGS uses snapshotted cost prices
- [ ] Gross profit calculation correct
- [ ] Margin percentage accurate

### 5.5 Backup & Restore (Standard+)
- [ ] Create backup generates .db file
- [ ] Backup file is valid SQLite database
- [ ] Restore backup replaces current data
- [ ] Application restarts after restore
- [ ] Restored data is intact

---

## 6. AI Features (Premium)

### 6.1 AI Model Setup
- [ ] `download_model.py` downloads model successfully
- [ ] Model file is ~2.3 GB
- [ ] Model loads on backend startup (if Premium license)
- [ ] Loading message appears during model init
- [ ] Fallback messages shown if model missing

### 6.2 Sales Forecasting
- [ ] `/ai/predict` endpoint works
- [ ] Predictions generate for 7, 14, 30 days
- [ ] Confidence scores provided
- [ ] Predictions saved to ai_analytics table
- [ ] Requires minimum historical data (shows error if insufficient)
- [ ] Chart displays predictions

### 6.3 Natural Language Queries
- [ ] `/ai/query` endpoint works
- [ ] LLM responds to business queries
- [ ] Responses are relevant and concise
- [ ] Handles follow-up questions
- [ ] Fallback responses work when model unavailable
- [ ] Response time acceptable (< 30 seconds)

### 6.4 AI Analytics Persistence
- [ ] Predictions saved to database
- [ ] `/ai/predictions/history` returns historical data
- [ ] `/ai/predictions/accuracy` calculates metrics
- [ ] `/ai/predictions/cleanup` removes expired records

---

## 7. Financial Calculations (CRITICAL)

### 7.1 Sale Calculations
- [ ] **Test 1**: Subtotal = price × quantity
  - Product: $100, Qty: 2 → Subtotal: $200 ✓
- [ ] **Test 2**: Tax calculated on subtotal
  - Subtotal: $100, Tax: 15% → Tax: $15, Total: $115 ✓
- [ ] **Test 3**: Discount applied correctly
  - Subtotal: $100, Discount: $10, Tax: 15% → Total: ($100 - $10) × 1.15 = $103.50 ✓
- [ ] **Test 4**: Multiple items total correct
  - Item 1: $50 × 2, Item 2: $30 × 1 → Subtotal: $130 ✓

### 7.2 Stock Deduction
- [ ] **Test 5**: Stock decreases by exact amount sold
  - Initial: 50, Sold: 5 → Final: 45 ✓
- [ ] **Test 6**: Insufficient stock prevents sale
  - Stock: 3, Attempt to sell: 5 → ERROR ✓
- [ ] **Test 7**: Multiple sales deduct correctly
  - Stock: 100, Sale 1: 10, Sale 2: 15 → Final: 75 ✓

### 7.3 Cost Price Snapshotting
- [ ] **Test 8**: Cost price saved in sale_items
  - Product cost: $60, Sale created → sale_item.cost_price = $60 ✓
- [ ] **Test 9**: P&L uses snapshotted cost
  - Sale: cost=$60, Later: product.cost_price=$70 → P&L still uses $60 ✓

### 7.4 Invoice Numbering
- [ ] **Test 10**: Invoices are unique
  - Create 10 sales → 10 unique invoice numbers ✓
- [ ] **Test 11**: Format is correct
  - INV-YYYYMMDD-XXXX (e.g., INV-20260423-0001) ✓

---

## 8. Security

### 8.1 Password Security
- [ ] Passwords hashed with BCrypt
- [ ] Passwords not visible in database
- [ ] Cannot login with hashed password
- [ ] Password requirements enforced (UI)

### 8.2 JWT Security
- [ ] Secret key generated uniquely per install
- [ ] Secret key not hardcoded
- [ ] Tokens expire correctly
- [ ] Invalid tokens rejected (401)
- [ ] Token tampering detected

### 8.3 License Security
- [ ] License signature validated
- [ ] Tampered license rejected
- [ ] License file in protected location (C:\ProgramData)
- [ ] Non-admin cannot modify system-wide license

### 8.4 SQL Injection
- [ ] Test injection in search: `' OR '1'='1` → Safe ✓
- [ ] Test injection in login: `admin'--` → Rejected ✓
- [ ] All queries use parameterization

---

## 9. Performance

### 9.1 Load Testing
- [ ] 100 products: Search responsive (< 1 second)
- [ ] 1,000 sales: Reports generate (< 3 seconds)
- [ ] 10,000 sales: Dashboard loads (< 2 seconds)
- [ ] 100,000+ sales: Application remains stable

### 9.2 Resource Usage
- [ ] RAM usage reasonable (< 500 MB without AI)
- [ ] RAM usage with AI model (< 3 GB)
- [ ] CPU usage at idle (< 5%)
- [ ] Database size growth reasonable
- [ ] No memory leaks after extended use

### 9.3 Startup Time
- [ ] Cold start without AI: < 10 seconds
- [ ] Cold start with AI: < 30 seconds
- [ ] Subsequent launches faster

---

## 10. User Interface

### 10.1 Responsiveness
- [ ] Layout adapts to window resize
- [ ] Minimum resolution (1280x720) usable
- [ ] Recommended resolution (1920x1080) optimal
- [ ] All buttons clickable
- [ ] Forms validate input
- [ ] Error messages clear and helpful

### 10.2 Navigation
- [ ] Sidebar navigation works
- [ ] Breadcrumbs show current location
- [ ] Back button works
- [ ] Keyboard shortcuts work (if implemented)
- [ ] Modal dialogs close correctly

### 10.3 Data Display
- [ ] Tables paginate correctly
- [ ] Sorting works
- [ ] Filters apply correctly
- [ ] Empty states show helpful messages
- [ ] Loading states display during operations

---

## 11. Error Handling

### 11.1 Graceful Degradation
- [ ] Missing license file → Clear error, fallback to basic
- [ ] Missing AI model → Fallback messages shown
- [ ] Backend offline → Error message, reconnect prompt
- [ ] Network error → Retry mechanism
- [ ] Invalid input → Validation errors shown

### 11.2 Database Errors
- [ ] Locked database → Wait and retry
- [ ] Corrupted database → Clear error, restore prompt
- [ ] Disk full → Error message
- [ ] Permission denied → Helpful troubleshooting

### 11.3 User Errors
- [ ] Insufficient stock → Clear message
- [ ] Duplicate SKU → Validation error
- [ ] Invalid date range → Corrected or rejected
- [ ] Required fields → Highlighted in red

---

## 12. Documentation

### 12.1 User Documentation
- [ ] Installation guide complete and accurate
- [ ] User manual covers all features
- [ ] Admin guide covers advanced topics
- [ ] Screenshots/examples provided
- [ ] Troubleshooting section helpful

### 12.2 Build Documentation
- [ ] BUILD_INSTRUCTIONS.md accurate
- [ ] Prerequisites listed
- [ ] Step-by-step instructions work
- [ ] Troubleshooting section included

### 12.3 Inline Documentation
- [ ] Error messages helpful
- [ ] Tooltips on complex UI elements
- [ ] Settings descriptions clear
- [ ] Feature descriptions accurate

---

## 13. Deployment Testing

### 13.1 Clean Machine Test
- [ ] Installed on fresh Windows 10 VM
- [ ] Installed on fresh Windows 11 VM
- [ ] No development tools required
- [ ] Application works standalone
- [ ] All features functional

### 13.2 Upgrade Testing
- [ ] Can upgrade from Basic to Standard (license replacement)
- [ ] Can upgrade from Standard to Premium
- [ ] Features unlock correctly after upgrade
- [ ] No data loss during upgrade

### 13.3 Uninstallation
- [ ] Uninstaller runs successfully
- [ ] Application files removed
- [ ] Option to keep/remove data works
- [ ] Registry entries cleaned
- [ ] No orphaned processes

---

## 14. Regression Testing

### 14.1 After Bug Fixes
- [ ] Original bug fixed
- [ ] No new bugs introduced
- [ ] Related features still work
- [ ] Tests pass

### 14.2 After New Features
- [ ] New feature works
- [ ] Existing features unaffected
- [ ] Performance not degraded
- [ ] Documentation updated

---

## 15. Acceptance Criteria

### 15.1 Functional
- [ ] All core features work (Inventory, Billing, Reports)
- [ ] All tier-specific features work correctly
- [ ] AI features work with model installed (Premium)
- [ ] No critical bugs
- [ ] No data corruption

### 15.2 Performance
- [ ] Meets performance benchmarks
- [ ] Resource usage acceptable
- [ ] Scales to 100,000+ transactions

### 15.3 Security
- [ ] No SQL injection vulnerabilities
- [ ] Passwords hashed
- [ ] Licenses validated
- [ ] RBAC enforced

### 15.4 Usability
- [ ] UI intuitive and responsive
- [ ] Error messages helpful
- [ ] Documentation complete
- [ ] Installation straightforward

### 15.5 Reliability
- [ ] No crashes during normal use
- [ ] Database integrity maintained
- [ ] Backup/restore works
- [ ] Handles errors gracefully

---

## Sign-Off

### Testing Complete
**Date**: _______________
**Tester Name**: _______________
**Signature**: _______________

### Approval for Release
**Product Manager**: _______________
**Technical Lead**: _______________
**QA Lead**: _______________

### Release Notes
**Version**: 1.0.0
**Release Date**: _______________
**Known Issues**: _______________

---

## Post-Release Checklist

After deploying to first customer:

- [ ] Monitor for crash reports
- [ ] Collect user feedback
- [ ] Track performance metrics
- [ ] Document common support issues
- [ ] Plan v1.1 improvements

---

**MBAS QA Checklist v1.0**
Last Updated: 2026-04-23
