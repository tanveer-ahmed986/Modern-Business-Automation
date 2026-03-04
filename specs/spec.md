# Modern Business Automation System (Offline Desktop)
## Software Specification Document (spec.md)

---

# 1. Project Overview

## 1.1 Project Name
Modern Business Automation System (MBAS)

## 1.2 Objective
A fully offline Windows desktop system to automate small and medium business operations including:

- Billing / invoicing
- Inventory & stock management
- Reports & analytics
- Role-based access
- Optional AI assistant (Premium)
- Rebrandable for multiple businesses

Must be modular to support **Basic, Standard, Premium packages** via **feature toggles**.

---

# 2. Target Businesses

- Retail shops, grocery stores, clothing stores, pharmacies, hardware shops, small wholesalers  
- Rebrandable: business name, logo, address, contact info, currency, tax settings  

---

# 3. User Roles & Permissions

| Role | Access |
|------|--------|
| Admin | Full access: all modules, AI, backup, settings |
| Manager | Standard modules, reports; cannot modify system settings |
| Sales User | Billing & stock; cannot view profit, AI, or supplier balances |

---

# 4. Packages & Feature Toggles

| Module / Feature | Basic | Standard | Premium |
|-----------------|-------|---------|---------|
| Billing / Invoicing | ✅ | ✅ | ✅ |
| Stock Management | ✅ | ✅ | ✅ |
| Reports | Basic (daily) | Advanced (monthly, product-wise) | Advanced + profit analysis |
| Supplier & Purchase | ❌ | ✅ | ✅ |
| Backup & Restore | ❌ | ✅ | ✅ |
| Multi-user / Roles | ✅ | ✅ | ✅ |
| AI Assistant | ❌ | ❌ | ✅ |
| Dashboard Metrics | Basic | Advanced | Advanced + AI Insights |
| Rebranding | ✅ | ✅ | ✅ |

**Implementation:**  
- Feature flags stored in **Settings/License table**  
- UI menus & logic render modules conditionally  
- Business logic checks enforce access, not just UI  

---

# 5. Core Modules

## 5.1 Authentication Module
- Username & password login  
- Secure password hashing  
- Role-based UI access  
- Session timeout  

## 5.2 Dashboard Module
- Display metrics based on role/package  
- Admin: total sales, gross profit, low stock, AI insights (Premium)  
- Sales User: quick sales, today's transactions  

## 5.3 Billing / Invoice Module
- Auto invoice number & date  
- Multiple products per invoice  
- Payment methods: Cash / Card / Other  
- Discount & tax calculation  
- Stock auto-deduction  
- Printable invoices  
- Real-time calculation: Subtotal, Tax, Discount, Total  

## 5.4 Inventory / Stock Module
- Product fields: Name, Category, Barcode, Cost Price (Admin), Selling Price, Stock Quantity, Low Stock Threshold, Status  
- Stock updates: auto-deduct on sale, auto-add on purchase  
- Low stock alerts  
- Manual adjustments for admins  

## 5.5 Supplier / Purchase Module (Standard & Premium)
- Supplier info: Name, Phone, Address, Opening Balance  
- Record purchase invoices  
- Update stock & supplier outstanding  
- Supplier balance = OpeningBalance + Purchases - Payments  

## 5.6 Reports Module
- **Basic:** Daily sales, basic inventory  
- **Standard:** Monthly, product-wise sales, low stock  
- **Premium:** Advanced financial reports including profit per product, category, AI insights  
- Export: PDF / CSV optional  

## 5.7 Backup & Restore Module (Standard & Premium)
- Backup: Export SQLite DB file (or SQL Server backup)  
- Timestamped backups  
- Option to save to USB or external drive  
- Restore: Select backup file → validate → replace DB → restart software  
- Feature toggle: enable/disable based on package  

## 5.8 System Settings & Rebranding
- Editable fields: Business name, logo, address, contact, currency, tax %, invoice footer  
- Stored in **Settings table**  
- Rebrandable for multi-branch resale  

## 5.9 AI Assistant Module (Premium)
- Fully offline, no external API  
- Sales prediction: next month revenue  
- Inventory optimization: reorder alerts, slow-moving items  
- Business insights: top products, low-profit items, salesperson ranking  
- Optional natural query assistant: e.g., “Show last month profit”  

---

# 6. Database Schema

## Tables

### Users
- Id, Username, PasswordHash, Role

### Settings
- Id, BusinessName, LogoPath, Address, Phone, CurrencySymbol, TaxPercentage, InvoiceFooter, PackageType, FeatureFlags

### Categories
- Id, Name

### Products
- Id, Name, CategoryId, Barcode, CostPrice, SellingPrice, StockQuantity, LowStockThreshold, IsActive

### Customers
- Id, Name, Phone, Address

### Suppliers
- Id, Name, Phone, Address, OpeningBalance

### Purchases
- Id, InvoiceNumber, SupplierId, Date, TotalAmount

### PurchaseItems
- Id, PurchaseId, ProductId, Quantity, CostPrice

### Sales
- Id, InvoiceNumber, Date, CustomerId, UserId, SubTotal, TaxAmount, DiscountAmount, TotalAmount

### SaleItems
- Id, SaleId, ProductId, Quantity, SellingPrice, CostPrice

### SupplierPayments
- Id, SupplierId, Date, Amount

### AIAnalytics (Premium)
- Id, Type, EntityId, Metric, PredictionValue, DateGenerated

---

# 7. UI / UX Design

- Modern, clean, flat UI  
- Sidebar navigation (Dashboard, Billing, Stock, Suppliers, Reports, AI, Settings)  
- Top header: Business name, logged-in user, logout  
- Card-based dashboard, responsive tables, search/filter  
- Color palette: soft blue/gray, optional dark mode  
- Quick actions for sales & stock  

---

# 8. Non-Functional Requirements

- Load time < 3s  
- Support 100,000+ records  
- Database transactions for financial safety  
- Secure password hashing  
- Fully offline operation  
- Clean error handling  

---

# 9. Reuse & Upgrade Strategy

- Single codebase for all packages  
- Feature toggles determine active modules  
- Upgrade path: Basic → Standard → Premium by updating feature flags  
- Data preserved during upgrades/downgrades  

---

# 10. Acceptance Criteria

- Billing, stock, reports function correctly per package  
- Backup & restore works  
- Role-based access enforced  
- AI generates insights offline (Premium)  
- UI is clean, responsive, modern  
- Feature toggles correctly enable/disable modules  
- No critical bugs  

---

END OF SPECIFICATION