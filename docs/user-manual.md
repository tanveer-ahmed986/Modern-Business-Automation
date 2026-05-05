# MBAS User Manual

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard](#dashboard)
3. [Inventory Management](#inventory-management)
4. [Billing & Sales (POS)](#billing--sales-pos)
5. [Customer Management](#customer-management)
6. [Suppliers & Purchases](#suppliers--purchases-standard)
7. [Reports](#reports)
8. [AI Features](#ai-features-premium)
9. [Settings](#settings)
10. [Keyboard Shortcuts](#keyboard-shortcuts)

---

## Getting Started

### First Login

1. Launch MBAS application
2. Enter credentials:
   - Default username: `admin`
   - Default password: `admin123`
3. **IMPORTANT**: Change your password immediately after first login

### Main Interface

The MBAS interface consists of:

- **Sidebar**: Main navigation menu
- **Top Bar**: User info, search, notifications
- **Content Area**: Active feature/page
- **Status Bar**: License info, connection status (bottom)

### User Roles

**Admin**
- Full system access
- User management
- Settings configuration
- All reports and features

**Manager**
- Inventory management
- View reports
- Process sales and purchases
- Cannot modify settings or users

**Sales User**
- Process sales only
- View inventory (read-only)
- Basic dashboard access
- Limited reporting

---

## Dashboard

The dashboard provides at-a-glance business insights.

### Metrics Displayed

- **Today's Sales**: Total revenue for current day
- **Monthly Revenue**: Current month's total
- **Total Products**: Inventory count
- **Low Stock Alerts**: Products below reorder level

### Quick Actions

- **Create Sale**: Opens POS (billing)
- **Add Product**: Opens inventory form
- **View Reports**: Navigate to reports
- **AI Insights** (Premium): Open AI assistant

### Sales Chart

- Daily sales trend (last 30 days)
- Hover over points for details
- Click to view detailed report

---

## Inventory Management

Manage your product catalog and stock levels.

### Adding Products

1. Click **Inventory** in sidebar
2. Click **"Add Product"** button
3. Fill in details:
   - **Name**: Product name (required)
   - **SKU**: Stock Keeping Unit (unique identifier)
   - **Barcode**: For scanner support
   - **Category**: Select from dropdown
   - **Selling Price**: Customer price
   - **Cost Price**: Your cost (for profit calculation)
   - **Stock Quantity**: Current stock level
   - **Reorder Level**: Alert threshold
   - **Unit**: pcs, kg, liters, etc.
4. Click **"Save"**

### Editing Products

1. Find product in list
2. Click **Edit** icon (pencil)
3. Modify fields
4. Click **"Save Changes"**

### Managing Categories

1. Go to **Inventory** → **Categories**
2. Click **"Add Category"**
3. Enter:
   - **Name**: Category name
   - **Description**: Optional details
4. Click **"Save"**

### Stock Adjustments

**Increase Stock** (receiving inventory):
1. Find product
2. Click **"Adjust Stock"**
3. Select **"Increase"**
4. Enter quantity and reason
5. Click **"Save"**

**Decrease Stock** (wastage, theft):
1. Same as above, select **"Decrease"**

**Note**: Regular sales automatically decrease stock.

### Search & Filters

- **Search Bar**: Type product name, SKU, or barcode
- **Category Filter**: Show products in specific category
- **Low Stock Toggle**: Show only low-stock items
- **Active/Inactive**: Toggle product visibility

---

## Billing & Sales (POS)

Process sales transactions at the point of sale.

### Creating a Sale

1. Click **Billing** in sidebar
2. **Add Products**:
   - Search by name/SKU/barcode
   - Click product to add to cart
   - Or scan barcode (if hardware connected)

3. **Adjust Quantities**:
   - Click +/- buttons
   - Or type quantity directly

4. **Apply Discount** (optional):
   - Enter discount amount in "Discount" field
   - Applied to total before tax

5. **Select Payment Method**:
   - Cash
   - Card
   - Mobile Money
   - Other

6. **Review Total**:
   - Subtotal: Sum of items
   - Tax: Calculated from settings
   - Discount: Subtracted
   - Grand Total: Final amount

7. **Complete Sale**:
   - Click **"Complete Sale"** button
   - Invoice number generated automatically
   - Print receipt (if printer connected)

### Sale Receipt

After completing sale:
- **Invoice Number**: Format `INV-YYYYMMDD-XXXX`
- **Print**: Send to receipt printer
- **Email**: Send to customer (if email provided)
- **New Sale**: Start fresh transaction

### Viewing Sales History

1. Go to **Billing** → **History**
2. View all completed sales
3. Click sale to view details
4. Search by invoice number, customer, or date

### Refunds/Voids

**Note**: Refund feature requires manager/admin role

1. Find sale in history
2. Click **"Void"** or **"Refund"**
3. Enter reason
4. Confirm action
5. Stock automatically adjusted

---

## Customer Management

Track customer information for sales history.

### Adding Customers

1. Go to **Customers** (in sidebar or during sale)
2. Click **"Add Customer"**
3. Fill in:
   - **Name**: Customer name (required)
   - **Email**: For receipts
   - **Phone**: Contact number
   - **Address**: Optional
4. Click **"Save"**

### Linking Customers to Sales

During checkout:
1. Click **"Select Customer"** dropdown
2. Choose existing customer or create new
3. Complete sale as normal
4. Sale is linked to customer record

### Customer History

1. Go to **Customers**
2. Click on customer name
3. View:
   - Total purchases
   - Purchase history
   - Last purchase date
   - Total spent

---

## Suppliers & Purchases (Standard+)

*Available in Standard and Premium tiers only*

### Adding Suppliers

1. Click **Suppliers** in sidebar
2. Click **"Add Supplier"**
3. Fill in:
   - **Name**: Supplier business name
   - **Contact Person**: Representative name
   - **Email**: Supplier email
   - **Phone**: Contact number
   - **Address**: Physical address
4. Click **"Save"**

### Creating Purchase Orders

1. Click **Purchases** → **"New Purchase"**
2. Select **Supplier** from dropdown
3. **Add Products**:
   - Click **"Add Item"**
   - Select product
   - Enter quantity
   - Enter unit cost
4. Review total
5. **Status**:
   - **Pending**: Order placed, not received
   - **Received**: Stock updated
6. Click **"Create Purchase"**

### Receiving Stock

When shipment arrives:
1. Go to **Purchases** → **Pending**
2. Find purchase order
3. Click **"Mark as Received"**
4. Stock automatically updated
5. Cost prices updated (if changed)

---

## Reports

Generate business intelligence reports.

### Sales Report (All Tiers)

**Access**: Reports → Sales Report

**Filters**:
- Date Range: From - To
- Payment Method: All, Cash, Card, etc.
- Customer: Specific customer or all

**Data Shown**:
- Total Revenue
- Number of Sales
- Average Sale Value
- Tax Collected
- Discounts Given
- Top 10 Products

**Export**: PDF, Excel (coming soon)

### Product Report (Standard+)

**Access**: Reports → Product Report

Shows per-product performance:
- Units Sold
- Revenue Generated
- Stock Status
- Profit Margin

### Monthly Report (Standard+)

**Access**: Reports → Monthly Report

Month-by-month comparison:
- Revenue trends
- Sales count
- Top performing months
- Year-over-year growth

### Profit & Loss (Premium)

**Access**: Reports → P&L Report

Comprehensive financial analysis:
- Total Revenue
- Cost of Goods Sold (COGS)
- Gross Profit
- Profit Margin %
- Purchase Costs

**Note**: Uses snapshotted cost prices for accurate historical P&L.

---

## AI Features (Premium)

*Available in Premium tier only*

### AI Sales Forecasting

**Access**: AI Insights → Forecast

**Features**:
- Predict sales for next 7, 14, or 30 days
- Based on historical data (last 365 days)
- Confidence scores provided
- Visual trend chart
- Day-by-day predictions

**Usage**:
1. Select prediction horizon (days)
2. Click **"Generate Forecast"**
3. View predictions and confidence scores
4. Export forecast data

**Requirements**:
- Minimum 30 days of sales history
- AI model downloaded (see admin guide)

### AI Natural Language Queries

**Access**: AI Insights → Ask AI

**Examples**:
- "What are my top selling products this month?"
- "Show me products with low stock"
- "How is my profit margin trending?"
- "Which categories generate the most revenue?"

**Usage**:
1. Type your question in plain English
2. Click **"Ask"**
3. AI analyzes your data and responds
4. Follow-up questions supported

**Limitations**:
- Responses based on available data only
- Cannot modify data (read-only)
- Best for analytical queries

---

## Settings

Configure system preferences and business settings.

### General Settings (Admin Only)

**Access**: Settings → General

**Options**:
- **Business Name**: Appears on receipts
- **Business Logo**: Upload image (PNG/JPG)
- **Tax Rate**: Default tax percentage
- **Currency**: USD, EUR, GBP, etc.

### User Management (Admin Only)

**Access**: Settings → Users

**Actions**:
- **Add User**: Create new user account
- **Edit User**: Modify user details or password
- **Disable User**: Temporarily disable access
- **Delete User**: Permanently remove user

**Password Requirements**:
- Minimum 8 characters
- Mix of letters and numbers (recommended)
- Change every 90 days (recommended)

### Backup & Restore (Standard+)

**Access**: Settings → System → Backup

**Create Backup**:
1. Click **"Create Backup"**
2. Choose location to save
3. Backup file: `mbas-backup-YYYYMMDD.db`
4. Store securely (contains all business data)

**Restore Backup**:
1. Click **"Restore Backup"**
2. Select backup file
3. **WARNING**: This will overwrite current data
4. Confirm action
5. Application restarts

**Best Practices**:
- Backup daily (end of business day)
- Store backups off-site (cloud, external drive)
- Test restores periodically

### License Information

**Access**: Settings → About

View:
- License Tier (Basic/Standard/Premium)
- Licensee Name
- Expiry Date (if applicable)
- Enabled Features

---

## Keyboard Shortcuts

### Global

- `Ctrl + /`: Quick search
- `Ctrl + K`: Open command palette
- `Ctrl + Shift + L`: Logout
- `Escape`: Close modal/dialog

### Navigation

- `Alt + D`: Dashboard
- `Alt + I`: Inventory
- `Alt + B`: Billing (POS)
- `Alt + R`: Reports
- `Alt + S`: Settings

### In POS (Billing)

- `F1`: New sale
- `F2`: Search products
- `F3`: Add customer
- `Enter`: Complete sale
- `Escape`: Cancel/clear cart

---

## Tips & Best Practices

### Daily Operations

1. **Morning**: Review low stock alerts
2. **Throughout Day**: Process sales via POS
3. **End of Day**: Create backup, review sales report

### Weekly Tasks

1. Review sales trends
2. Check inventory levels
3. Place purchase orders for low stock
4. Review profit margins

### Monthly Tasks

1. Generate monthly report
2. Analyze P&L (Premium)
3. Review AI forecasts (Premium)
4. Update pricing if needed
5. Archive old data (if database large)

### Security

- Change passwords regularly
- Don't share login credentials
- Log out when leaving workstation
- Backup data daily
- Keep license file secure

---

## Frequently Asked Questions

**Q: Can I use MBAS offline?**
A: Yes! MBAS is 100% offline. No internet required.

**Q: How do I upgrade from Basic to Standard/Premium?**
A: Contact your vendor for a new license file. Replace the license and restart.

**Q: Can multiple users work simultaneously?**
A: Yes, on the same computer (different logins) or via network setup.

**Q: What happens if I lose my license file?**
A: Contact your vendor with your business name to get a replacement.

**Q: Can I export data to Excel?**
A: Reports can be exported to PDF. Excel export is planned for future release.

**Q: How much data can MBAS handle?**
A: Tested with 100,000+ sales records. Performance remains excellent.

---

## Getting Support

If you need help:

1. Check this manual first
2. See **Admin Guide** for advanced topics
3. Contact your license vendor
4. Email: support@mbas.local (if available)

When reporting issues, include:
- MBAS version (Settings → About)
- License tier
- Screenshots of error
- Steps to reproduce

---

**MBAS User Manual v1.0**
Last Updated: 2026-04-23
