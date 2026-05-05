# MBAS - Modern Business Automation System
## Complete User Manual

### Version 1.0 | 2026

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Getting Started](#2-getting-started)
3. [System Overview](#3-system-overview)
4. [Core Features](#4-core-features)
   - 4.1 [Dashboard](#41-dashboard)
   - 4.2 [Inventory Management](#42-inventory-management)
   - 4.3 [Billing & Point of Sale (POS)](#43-billing--point-of-sale-pos)
   - 4.4 [Suppliers Management](#44-suppliers-management)
   - 4.5 [Purchase Orders](#45-purchase-orders)
   - 4.6 [Reports & Analytics](#46-reports--analytics)
   - 4.7 [User Management](#47-user-management)
   - 4.8 [Backup & Restore](#48-backup--restore)
   - 4.9 [Settings & Configuration](#49-settings--configuration)
5. [Business-Specific Guides](#5-business-specific-guides)
   - 5.1 [Restaurant & Food Service](#51-restaurant--food-service)
   - 5.2 [Medical Store & Pharmacy](#52-medical-store--pharmacy)
   - 5.3 [Grocery & Supermarket](#53-grocery--supermarket)
   - 5.4 [Retail Clothing Store](#54-retail-clothing-store)
   - 5.5 [Electronics Shop](#55-electronics-shop)
   - 5.6 [Hardware & Construction Supplies](#56-hardware--construction-supplies)
6. [User Roles & Permissions](#6-user-roles--permissions)
7. [Troubleshooting](#7-troubleshooting)
8. [Frequently Asked Questions (FAQ)](#8-frequently-asked-questions-faq)

---

## 1. Introduction

### What is MBAS?

**MBAS (Modern Business Automation System)** is a comprehensive, offline-first business management solution designed for small to medium-sized businesses. It helps you manage inventory, process sales, track purchases, generate reports, and make data-driven decisions - all without requiring an internet connection.

### Key Benefits

- ✅ **100% Offline** - Works without internet connectivity
- ✅ **Multi-Industry** - Suitable for retail, pharmacy, grocery, restaurants, and more
- ✅ **Complete Solution** - Inventory, billing, purchasing, and reporting in one system
- ✅ **User-Friendly** - Intuitive interface designed for non-technical users
- ✅ **Secure** - Role-based access control to protect your business data
- ✅ **Fast** - Quick product search, instant billing, real-time stock updates
- ✅ **Flexible Invoicing** - Thermal receipt and A4 invoice printing options

### System Requirements

**Minimum Requirements:**
- Operating System: Windows 10 or later
- Processor: Intel Core i3 or equivalent
- RAM: 4 GB
- Storage: 5 GB free space
- Display: 1366x768 resolution

**Recommended:**
- Operating System: Windows 11
- Processor: Intel Core i5 or higher
- RAM: 8 GB
- Storage: 10 GB free space
- Display: 1920x1080 resolution
- Printer: Thermal receipt printer (58mm/80mm) or standard A4 printer

---

## 2. Getting Started

### 2.1 First-Time Setup

**Step 1: Install MBAS**
1. Run the `MBAS_Setup.msi` installer
2. Follow the installation wizard
3. Choose installation directory (default: `C:\Program Files\MBAS`)
4. Complete installation

**Step 2: Launch Application**
1. Double-click the MBAS desktop icon
2. The application will start and initialize the database on first run
3. Wait for the login screen to appear

**Step 3: First Login**
1. **Default Credentials:**
   - Username: `admin`
   - Password: `admin123`
2. Click "Login" button
3. **IMPORTANT:** Change your password immediately after first login

**Step 4: Change Default Password**
1. Click on your username at the bottom of the sidebar
2. Select "Change Password"
3. Enter current password: `admin123`
4. Enter new password (minimum 8 characters)
5. Confirm new password
6. Click "Save"

### 2.2 Initial Configuration

**Configure Business Settings:**

1. Click **"Settings"** in the sidebar
2. Update the following information:
   - **Business Name:** Your store/business name
   - **Address:** Complete business address
   - **Phone Number:** Contact number
   - **Email:** Business email address
   - **Tax Rate:** Default tax percentage (e.g., 15%)
   - **Currency Symbol:** Your local currency (e.g., USD, PKR, INR)
3. Click **"Save Settings"**

**Set Up First Category:**

1. Go to **"Inventory"** → **"Categories"**
2. Click **"Add Category"** button
3. Enter category name (e.g., "Electronics", "Medicines", "Food Items")
4. Click **"Create"**

**Add Your First Product:**

1. Go to **"Inventory"** → **"Products"**
2. Click **"Add Product"** button
3. Fill in product details:
   - Product Name
   - Barcode/SKU (if available)
   - Category
   - Cost Price (what you pay supplier)
   - Selling Price (what customer pays)
   - Stock Quantity (initial stock)
   - Low Stock Threshold (alert level)
4. Click **"Save Product"**

---

## 3. System Overview

### 3.1 User Interface Layout

The MBAS interface consists of three main sections:

**1. Left Sidebar (Navigation)**
- Dashboard
- Inventory
- Billing
- Suppliers
- Purchases
- Reports
- Users (Admin only)
- Backup (Admin only)
- Settings (Admin only)
- Sign Out

**2. Main Content Area**
- Displays the current module/page
- Contains forms, tables, and action buttons
- Shows real-time data and updates

**3. User Profile Section (Bottom of Sidebar)**
- Shows currently logged-in user
- Role indicator (Admin/Manager/Sales)
- Sign out option

### 3.2 Navigation Tips

- **Click sidebar items** to switch between modules
- **Use search bars** for quick product/customer lookup
- **Keyboard shortcuts:**
  - `Alt+S` - Focus on search in Billing page
  - `F5` - Refresh current page
  - `Ctrl+P` - Print (when on invoice page)

---

## 4. Core Features

### 4.1 Dashboard

**Purpose:** Get a quick overview of your business performance.

**What You See:**
- **Total Sales Today:** Today's revenue
- **Total Products:** Number of products in inventory
- **Low Stock Items:** Products below threshold
- **Total Customers:** Number of registered customers

**Recent Activities:**
- Latest sales transactions
- Recent stock updates
- Low stock alerts

**How to Use:**
1. Login to MBAS
2. Dashboard appears automatically
3. View key metrics at a glance
4. Click on metrics to drill down to detailed reports

---

### 4.2 Inventory Management

**Purpose:** Manage your product catalog and track stock levels.

#### 4.2.1 Managing Categories

**Add New Category:**
1. Go to **Inventory** → **Categories** tab
2. Click **"Add Category"**
3. Enter category name
4. Click **"Save"**

**Edit Category:**
1. Find the category in the list
2. Click **"Edit"** icon
3. Update name
4. Click **"Save"**

**Delete Category:**
1. Click **"Delete"** icon next to category
2. Confirm deletion
   - **Note:** Cannot delete if products are assigned to it

**Example Categories by Business Type:**
- **Pharmacy:** Medicines, Surgical Items, Medical Equipment, Supplements
- **Grocery:** Fresh Produce, Dairy, Beverages, Snacks, Household
- **Restaurant:** Appetizers, Main Course, Beverages, Desserts
- **Electronics:** Mobile Phones, Laptops, Accessories, Home Appliances

#### 4.2.2 Managing Products

**Add New Product:**

1. Click **"Inventory"** in sidebar
2. Click **"Add Product"** button
3. Fill in the form:

   **Basic Information:**
   - **Product Name:** Full descriptive name
   - **Barcode:** Enter or scan barcode (unique identifier)
   - **Category:** Select from dropdown

   **Pricing:**
   - **Cost Price:** What you paid to supplier
   - **Selling Price:** What customer pays
   - **Margin:** Automatically calculated

   **Stock Management:**
   - **Current Stock:** Initial quantity
   - **Low Stock Threshold:** Alert when below this number
   - **Unit:** piece, kg, liter, box, etc.

4. Click **"Save Product"**

**Search Products:**
1. Use the search bar at top
2. Type product name or barcode
3. Results appear instantly using fast search (FTS5)

**Edit Product:**
1. Find product in list
2. Click **"Edit"** button
3. Update any field
4. Click **"Save"**

**Delete Product:**
1. Click **"Delete"** button next to product
2. Confirm deletion
   - **Note:** Be careful - this removes all history

**View Low Stock Items:**
1. Products below threshold show in red/orange
2. Check dashboard for low stock count
3. Use Reports → Inventory Report for detailed view

---

### 4.3 Billing & Point of Sale (POS)

**Purpose:** Process customer sales quickly and efficiently.

#### 4.3.1 Complete Sales Transaction (Step-by-Step)

**Step 1: Navigate to Billing**
1. Click **"Billing"** in sidebar
2. POS interface opens

**Step 2: Search and Add Products**
1. Click in the **search box** (or press Alt+S)
2. Type product name or scan barcode
3. Dropdown shows matching products with:
   - Product name
   - Barcode
   - Price
   - Stock availability
4. Click on product to add to cart

**Step 3: Adjust Quantities**
1. Product appears in "Current Sale Items" table
2. Use **+/−** buttons to adjust quantity
3. Or click on quantity number and type directly
4. Subtotal updates automatically

**Step 4: Remove Items (if needed)**
1. Click **trash icon** next to item
2. Item removed from cart

**Step 5: Select Customer (Optional)**
1. In **"Customer Details"** section on right
2. Type customer name or phone in search box
3. Select existing customer from dropdown
4. Or click **"Add [name]"** to create new customer
5. Leave blank for walk-in sales

**Step 6: Choose Payment Method**
1. In **"Payment & Summary"** section
2. Select one of:
   - **Cash** - Physical cash payment
   - **Card** - Credit/debit card
   - **Transfer** - Bank/mobile transfer
   - **Credit** - Account/credit payment

**Step 7: Apply Discount (if applicable)**
1. See **"Discount"** field in summary
2. Enter discount amount (e.g., 50 for $50 off)
3. Total updates automatically

**Step 8: Review Summary**
- **Subtotal:** Sum of all items
- **Tax (%):** Applied automatically
- **Discount:** If entered
- **Total:** Final amount to collect

**Step 9: Complete Sale**
1. Verify total amount
2. Click **"Complete Sale"** button at bottom
3. Wait for confirmation message

**Step 10: Print Invoice**
1. "Sale Completed!" screen appears
2. Choose print format:
   - **"Print Receipt (Thermal)"** - For walk-in customers (small paper roll)
   - **"Print Invoice (A4)"** - For business customers (full page)
3. Click appropriate print button
4. Invoice prints

**Step 11: Start New Sale**
1. Click **"New Sale"** button
2. Returns to empty billing screen
3. Ready for next customer

#### 4.3.2 Invoice Details

**Thermal Receipt Includes:**
- Business name
- Date and invoice number
- Customer name (if selected)
- Items with quantities and prices
- Subtotal, tax, discount
- **YOU SAVED** amount (if discount applied)
- Grand total
- Payment method
- Thank you message

**A4 Invoice Includes:**
- Professional header with business name
- Invoice number and date
- Bill to (customer details)
- Itemized table with descriptions
- Subtotal, tax breakdown
- Discount and savings highlighted
- Grand total in large font
- Payment method
- Footer with thank you note

---

### 4.4 Suppliers Management

**Purpose:** Maintain a database of your suppliers for purchase tracking.

#### 4.4.1 Add New Supplier

1. Click **"Suppliers"** in sidebar
2. Click **"Add Supplier"** button
3. Fill in details:
   - **Supplier Name:** Company/person name
   - **Contact Person:** Representative name
   - **Phone Number:** Contact number
   - **Email:** Email address
   - **Address:** Full address
4. Click **"Save Supplier"**

#### 4.4.2 View Supplier History

1. Find supplier in list
2. Click on supplier name
3. View:
   - All purchase orders from this supplier
   - Total amount spent
   - Outstanding balance (if any)
   - Payment history

#### 4.4.3 Edit Supplier

1. Click **"Edit"** icon next to supplier
2. Update information
3. Click **"Save"**

---

### 4.5 Purchase Orders

**Purpose:** Record stock purchases from suppliers and auto-update inventory.

#### 4.5.1 Create Purchase Order (Step-by-Step)

**Step 1: Navigate to Purchases**
1. Click **"Purchases"** → **"New Purchase"**

**Step 2: Select Supplier**
1. Click **"Supplier"** dropdown
2. Select supplier from list
3. Or leave blank for direct/cash purchase

**Step 3: Enter Reference Number (Optional)**
1. Enter supplier's invoice number
2. Example: "INV-SUP-2024-001"
3. Helps track supplier invoices

**Step 4: Add Products to Purchase**
1. Click in **"Search products"** box
2. Type product name or barcode
3. Click product from dropdown to add
4. Product appears in purchase items table

**Step 5: Set Quantity and Cost Price**
1. **Quantity:** Enter number of units purchased
2. **Cost Price:** Enter price you paid per unit
   - This updates the product's cost price
   - Future profit calculations use this cost

**Step 6: Add More Products**
1. Repeat Step 4-5 for all items in purchase
2. Subtotals calculate automatically

**Step 7: Add Additional Charges (if any)**
1. **Tax Amount:** Enter any tax paid
2. **Discount Amount:** Enter supplier discount received

**Step 8: Enter Payment Details**
1. **Amount Paid:** How much you paid now
2. Remaining balance tracked automatically

**Step 9: Add Notes (Optional)**
1. Enter any special notes
2. Example: "Bulk order discount applied"

**Step 10: Review Order Summary**
- Check all items, quantities, prices
- Verify total amount

**Step 11: Record Purchase**
1. Click **"Record Purchase"** button
2. System will:
   - ✅ Add stock to inventory automatically
   - ✅ Update product cost prices
   - ✅ Record purchase in history
   - ✅ Update supplier balance
3. Confirmation message appears

**Step 12: View or Print Purchase Record**
1. Purchase saved successfully
2. Stock quantities updated
3. Navigate to Inventory to verify new stock

#### 4.5.2 View Purchase History

1. Go to **"Purchases"**
2. View all previous purchases
3. Filter by:
   - Supplier
   - Date range
   - Status (received/pending)
4. Click on purchase to see details

---

### 4.6 Reports & Analytics

**Purpose:** Generate insights and make data-driven decisions.

#### 4.6.1 Available Reports

**1. Sales Report**
- Daily/Weekly/Monthly/Custom date range
- Total sales revenue
- Number of transactions
- Average transaction value
- Top-selling products
- Sales by payment method

**How to Generate:**
1. Go to **"Reports"**
2. Select **"Sales Report"**
3. Choose date range
4. Click **"Generate"**
5. View on screen or export to PDF/Excel

**2. Inventory Report**
- Current stock levels
- Stock value (at cost price)
- Stock value (at selling price)
- Low stock items
- Out of stock items
- Overstock items

**3. Profit & Loss Report (P&L)**
- Total revenue
- Cost of goods sold (COGS)
- Gross profit
- Profit margin %
- Net profit/loss
- Breakdown by product category

**How to Read P&L:**
```
Revenue (Sales):           $10,000
- COGS (Cost):            - $6,000
= Gross Profit:            $4,000
Gross Margin:              40%
```

**4. Purchase Report**
- Total purchases by date range
- Spending by supplier
- Most purchased items
- Average purchase cost

**5. Customer Report**
- Top customers by revenue
- Customer purchase frequency
- Customer lifetime value
- New vs returning customers

#### 4.6.2 Export Reports

1. Generate any report
2. Click **"Export"** button
3. Choose format:
   - **PDF** - For printing/sharing
   - **Excel** - For further analysis
4. File downloads to your computer

---

### 4.7 User Management

**Purpose:** Control who can access the system and what they can do.

#### 4.7.1 User Roles

**Administrator (Admin)**
- Full system access
- Can manage users
- Can access all reports
- Can modify settings
- Can perform backups

**Manager**
- Can manage inventory
- Can process sales
- Can view most reports
- Can manage suppliers/purchases
- Cannot modify settings or users

**Sales User**
- Can process sales only
- Can view product prices
- Cannot see cost prices
- Cannot access inventory/purchase management
- Limited reporting access

#### 4.7.2 Add New User

1. Go to **"Users"** (Admin only)
2. Click **"Add User"** button
3. Fill in details:
   - **Full Name**
   - **Username** (for login)
   - **Email**
   - **Password** (user can change later)
   - **Role** (Admin/Manager/Sales)
4. Click **"Create User"**

#### 4.7.3 Edit User

1. Find user in list
2. Click **"Edit"** icon
3. Update details
4. Cannot change username (security)
5. Click **"Save"**

#### 4.7.4 Deactivate User

1. Find user in list
2. Click **"Deactivate"** button
3. User cannot login but data preserved
4. Can reactivate later if needed

---

### 4.8 Backup & Restore

**Purpose:** Protect your business data from loss.

#### 4.8.1 Create Backup

**Manual Backup:**
1. Go to **"Backup"** (Admin only)
2. Click **"Create Backup"**
3. Choose backup location:
   - Local drive (C:, D:)
   - External USB drive (recommended)
   - Network drive
4. Enter backup name (auto-generates with date)
5. Click **"Start Backup"**
6. Wait for completion (30 seconds - 5 minutes)
7. Confirmation message with backup location

**Automatic Backups:**
- System creates daily backup automatically
- Stored in: `C:\ProgramData\MBAS\Backups`
- Last 7 days retained automatically

**Backup Best Practices:**
- ✅ Backup daily (end of business day)
- ✅ Store backups on external drive
- ✅ Keep multiple backup copies
- ✅ Test restore process monthly
- ✅ Store one backup offsite (home/bank locker)

#### 4.8.2 Restore from Backup

**⚠️ WARNING:** Restore will replace current data!

1. Go to **"Backup"** → **"Restore"** tab
2. Click **"Browse"** to select backup file
3. Backup file format: `MBAS_Backup_YYYY-MM-DD.db`
4. Select the backup file
5. Review backup information:
   - Backup date
   - File size
   - Number of records
6. Click **"Restore Database"**
7. Confirm warning dialog
8. System will:
   - Stop current operations
   - Replace database
   - Restart application
9. Login again after restart
10. Verify data restored correctly

---

### 4.9 Settings & Configuration

**Purpose:** Customize system for your business needs.

#### 4.9.1 Business Settings

**Update Business Information:**
1. Go to **"Settings"**
2. **Business Details** section:
   - Business Name
   - Address
   - Phone Number
   - Email
   - Tax ID (optional)
3. Click **"Save"**

**Tax Configuration:**
1. **Default Tax Rate:** Enter percentage (e.g., 15 for 15%)
2. Applied automatically to all sales
3. Can override per transaction if needed

**Currency Settings:**
1. **Currency Symbol:** USD, PKR, INR, EUR, etc.
2. Displays throughout system
3. No currency conversion (single currency only)

#### 4.9.2 Invoice Customization

**Invoice Footer Text:**
1. Edit "Thank you" message
2. Add business slogan/tagline
3. Add return policy text
4. Add contact information

**Invoice Numbering:**
- Auto-generated format: `INV-YYYYMMDD-XXXX`
- Example: `INV-20260425-0001`
- Cannot be customized (ensures uniqueness)

---

## 5. Business-Specific Guides

### 5.1 Restaurant & Food Service

#### 5.1.1 Initial Setup

**Categories to Create:**
- Appetizers
- Soups & Salads
- Main Course
- Rice & Breads
- Beverages
- Desserts
- Extras (Sauces, Sides)

**Adding Menu Items:**

1. **Product Name:** Use dish names
   - Example: "Chicken Tikka Masala"
   - Example: "Vegetable Spring Rolls (3pcs)"

2. **Barcode/SKU:** Use custom codes
   - Format: `MENU-001`, `MENU-002`
   - Or use category codes: `APP-001` (Appetizer 1)

3. **Cost Price:** Ingredient cost
   - Calculate total ingredient cost
   - Example: $3.50 in ingredients

4. **Selling Price:** Menu price
   - Example: $8.99

5. **Stock Quantity:**
   - For prepared items: Daily preparation count
   - For made-to-order: Set to 9999 (unlimited)
   - Update daily for limited items

6. **Unit:** Use "plate" or "serving"

#### 5.1.2 Daily Operations

**Morning Setup:**
1. Go to Inventory
2. Update stock for daily specials
3. Mark out-of-stock items as "0"

**Taking Orders:**
1. Open Billing
2. Search dish name
3. Add to cart
4. Adjust quantity for multiple servings
5. Customer name optional (table number in notes)
6. Process payment
7. Print kitchen receipt (thermal)

**End of Day:**
1. Update inventory for remaining items
2. Generate Sales Report
3. Create backup
4. Review best-selling items

#### 5.1.3 Tips for Restaurants

- **Use Categories Wisely:** Helps servers find items quickly
- **Update Prices Regularly:** Seasonal pricing adjustments
- **Track Waste:** Reduce stock for items not selling
- **Special Offers:** Use discount feature for happy hours
- **Customer Names:** Track regular customers for loyalty

**Example Products:**
```
Product: Grilled Chicken Burger
Barcode: MAIN-015
Category: Main Course
Cost: $2.50
Price: $6.99
Stock: 9999 (made to order)
Unit: serving
```

---

### 5.2 Medical Store & Pharmacy

#### 5.2.1 Initial Setup

**Categories to Create:**
- Tablets & Capsules
- Syrups & Liquids
- Injections
- Surgical Items
- Medical Equipment
- Baby Care
- Personal Care
- Vitamins & Supplements

**Adding Medicines:**

1. **Product Name:** Generic + Brand name
   - Example: "Paracetamol 500mg (Panadol)"
   - Example: "Amoxicillin 250mg Syrup"

2. **Barcode:** Use manufacturer barcode
   - Scan from medicine box
   - Or use batch number

3. **Cost Price:** Wholesale price per unit

4. **Selling Price:** MRP or retail price

5. **Stock Quantity:** Number of strips/boxes/bottles

6. **Low Stock Threshold:** Important for medicines
   - Set based on monthly usage
   - Example: If 20 strips/month, set threshold to 10

7. **Additional Info (in description):**
   - Salt composition
   - Manufacturer name
   - Expiry date
   - Storage instructions

#### 5.2.2 Managing Expiry Dates

**Track Expiry:**
1. Add expiry date in product description
2. Create category: "Near Expiry"
3. Move products 3 months before expiry
4. Offer discounts to clear stock

**Batch Management:**
1. Use barcode for different batches
2. Example: `MED-PARA-500-BATCH-A`
3. Update cost price per batch

#### 5.2.3 Prescription Management

**Selling Prescription Medicines:**
1. Take customer name and phone
2. Add customer to system
3. Note prescription number in sale notes
4. Process sale as normal
5. Attach prescription copy to invoice

**Scheduled Drugs:**
- Track separately using customer notes
- Record prescription details
- Maintain register manually (compliance)

#### 5.2.4 Daily Operations

**Opening:**
1. Check low stock alerts
2. Receive deliveries (use Purchase module)
3. Update stock immediately

**During Day:**
1. Fast billing using barcode scan
2. Suggest alternatives for out-of-stock
3. Track customer purchases for follow-ups

**Closing:**
1. Generate Sales Report
2. Check inventory levels
3. Plan next day orders
4. Backup data

#### 5.2.5 Tips for Pharmacies

- **Barcode Scanning:** Essential for speed
- **Stock Alerts:** Set higher thresholds for critical medicines
- **Supplier Management:** Track medicine sources
- **Customer Database:** Important for prescription refills
- **Regular Audits:** Match physical stock weekly

**Example Products:**
```
Product: Paracetamol 500mg (Panadol) - 10 Tablets
Barcode: 8964000123456
Category: Tablets & Capsules
Cost: $1.20 per strip
Price: $2.00 per strip
Stock: 50 strips
Threshold: 15 strips
Description: Fever & pain relief | Mfg: GSK | Exp: 12/2026
```

---

### 5.3 Grocery & Supermarket

#### 5.3.1 Initial Setup

**Categories to Create:**
- Fresh Produce (Fruits, Vegetables)
- Dairy & Eggs
- Bakery
- Beverages
- Snacks & Confectionery
- Cooking Essentials (Oil, Spices, Flour)
- Household Items
- Personal Care
- Frozen Foods
- Canned & Packaged Foods

**Adding Grocery Items:**

1. **Product Name:** Brand + Item + Size
   - Example: "Coca Cola 1.5L Bottle"
   - Example: "Basmati Rice 5kg (Super Brand)"

2. **Barcode:** Scan from product

3. **Cost Price:** Per unit wholesale price

4. **Selling Price:** MRP

5. **Stock Quantity:**
   - For individual items: Number of units
   - For bulk items: Number of bags/boxes

6. **Unit:** Select appropriate
   - piece, kg, liter, dozen, box, pack

#### 5.3.2 Handling Perishables

**Fresh Produce:**
1. Set low stock threshold to minimum
2. Update stock daily
3. Use discount feature for items nearing expiry
4. Remove expired items from system

**Dairy Products:**
1. Track expiry in description
2. First-in-first-out (FIFO) manually
3. Daily stock checks

#### 5.3.3 Bulk Sales

**Selling by Weight:**
1. Product name: "Wheat Flour (per kg)"
2. Price: Per kg rate
3. At billing, enter exact quantity
   - Customer wants 3.5 kg
   - Enter quantity: 3.5
   - Total calculates automatically

**Bundle Offers:**
1. Create combo product
   - Example: "Tea Combo Pack (Tea + Sugar + Milk)"
2. Set discounted price
3. Note bundle contents in description

#### 5.3.4 Daily Operations

**Morning:**
1. Receive stock from suppliers
2. Record purchases in system
3. Update shelf prices if changed
4. Mark out-of-stock items

**Peak Hours:**
1. Fast checkout using barcode scanner
2. Multiple cashiers (separate login per user)
3. Quick cash handling

**Evening:**
1. Count cash
2. Match with sales report
3. Note any discrepancies
4. Stock check for fast-moving items

#### 5.3.5 Tips for Grocery Stores

- **Barcode Scanner:** Must-have for speed
- **Multiple Cashiers:** Create separate user accounts
- **Promotions:** Use discount field for special offers
- **Stock Rotation:** Update costs regularly
- **Supplier Tracking:** Essential for tracing products

**Example Products:**
```
Product: Coca Cola 1.5L Bottle
Barcode: 5449000000996
Category: Beverages
Cost: $0.80 per bottle
Price: $1.20 per bottle
Stock: 120 bottles
Threshold: 24 bottles
Unit: piece
```

---

### 5.4 Retail Clothing Store

#### 5.4.1 Initial Setup

**Categories to Create:**
- Men's Wear
  - Shirts
  - Pants
  - T-Shirts
  - Jeans
- Women's Wear
  - Tops
  - Dresses
  - Bottoms
- Kids Wear
- Accessories
- Footwear

**Adding Clothing Items:**

1. **Product Name:** Item + Size + Color
   - Example: "Men's Cotton Shirt - Blue - L"
   - Example: "Kids T-Shirt - Red - 8Y"

2. **Barcode:** Custom or manufacturer
   - Format: `MEN-SHIRT-BLUE-L-001`

3. **Cost Price:** Wholesale price per piece

4. **Selling Price:** Retail price

5. **Stock Quantity:** Number of pieces

**Size & Color Variations:**

**Option 1: Separate Products**
- Create one product per size/color combination
- Example:
  - "Men's Shirt - Blue - S"
  - "Men's Shirt - Blue - M"
  - "Men's Shirt - Blue - L"

**Option 2: SKU System**
- Use barcode to differentiate
- Base name: "Men's Formal Shirt"
- SKU: `SHIRT-BLUE-S`, `SHIRT-BLUE-M`, `SHIRT-BLUE-L`

#### 5.4.2 Seasonal Sales

**End of Season Clearance:**
1. Select old season items
2. Update selling prices (reduced)
3. Use discount feature at billing
4. Track sale performance

**New Collection:**
1. Create new category: "New Arrivals"
2. Add products
3. Premium pricing
4. Move to regular after 2-3 months

#### 5.4.3 Daily Operations

**Customer Service:**
1. Search by item type
2. Check size availability instantly
3. Suggest alternatives if out of stock
4. Add customer to database for future offers

**Returns & Exchange:**
1. Note in invoice notes: "Exchange within 7 days"
2. For exchange:
   - Create new sale
   - Add discount equal to returned item price
   - Note: "Exchange for INV-XXXX"

#### 5.4.4 Tips for Clothing Stores

- **Organized Categories:** Makes searching easier
- **Stock by Size:** Track popular sizes
- **Customer Database:** SMS for new arrivals
- **Seasonal Planning:** Clear old stock before new season
- **Bulk Purchasing:** Use purchase module for supplier orders

---

### 5.5 Electronics Shop

#### 5.5.1 Initial Setup

**Categories to Create:**
- Mobile Phones
- Laptops & Computers
- Accessories
  - Chargers
  - Cases
  - Screen Guards
  - Cables
- Home Appliances
- Cameras & Photography
- Gaming
- Audio Equipment

**Adding Electronics:**

1. **Product Name:** Brand + Model + Specifications
   - Example: "Samsung Galaxy S24 - 256GB - Black"
   - Example: "Dell XPS 15 - i7 - 16GB RAM - 512GB SSD"

2. **Barcode:** IMEI for phones, Serial for laptops

3. **Cost Price:** Purchase price

4. **Selling Price:** MRP or competitive price

5. **Stock Quantity:**
   - For phones: Individual IMEI tracking
   - For accessories: Quantity count

6. **Warranty Info:** Add in description
   - Manufacturer warranty period
   - Service center details

#### 5.5.2 Serial Number Tracking

**For High-Value Items:**
1. Use barcode field for IMEI/Serial
2. Create one product entry per unit
3. Example:
   - "iPhone 15 Pro - IMEI: 123456789012345"
4. Mark as sold after billing

**For Stock Items:**
- Accessories tracked by quantity
- No individual serial tracking needed

#### 5.5.3 Managing Returns & Warranty

**Dead on Arrival (DOA):**
1. Customer brings back within 7 days
2. Check invoice number
3. Verify product condition
4. Exchange or refund process:
   - New sale with zero payment (exchange)
   - Or manual refund tracking

**Warranty Claims:**
1. Keep warranty card with invoice
2. Note in system: "Warranty valid till: [date]"
3. Direct customer to service center
4. Track in customer notes

#### 5.5.4 Tips for Electronics

- **Detailed Descriptions:** Specs matter for search
- **Supplier Management:** Track authorized dealers
- **Price Updates:** Frequent price changes
- **Customer Follow-up:** For accessories purchases
- **Insurance:** Offer with high-value items

---

### 5.6 Hardware & Construction Supplies

#### 5.6.1 Initial Setup

**Categories to Create:**
- Cement & Sand
- Steel & Iron
- Electrical Items
- Plumbing
- Paints & Brushes
- Tools
- Safety Equipment
- Tiles & Flooring

**Adding Hardware Items:**

1. **Product Name:** Material + Size/Grade
   - Example: "Cement 50kg Bag (Brand A)"
   - Example: "Steel Rod 10mm - per kg"

2. **Barcode:** Custom SKU

3. **Cost Price:** Per unit/kg cost

4. **Selling Price:** Market rate

5. **Unit:** bag, kg, piece, meter, box

#### 5.6.2 Bulk & Retail Sales

**Selling by Weight/Length:**
1. Price per kg/meter
2. Enter quantity at billing
   - Customer needs 15.5 meters
   - Enter: 15.5
3. Auto-calculation

**Contractor Accounts:**
1. Create contractor as customer
2. Track all purchases
3. Monthly billing option (credit sales)
4. Generate customer report for statements

#### 5.6.3 Daily Operations

**Large Orders:**
1. Use Purchase Order feature
2. Prepare delivery challan
3. Print A4 invoice with itemized list
4. Get signature on delivery

**Stock Receiving:**
1. Record in Purchase module
2. Match delivery with purchase order
3. Update inventory immediately

#### 5.6.4 Tips for Hardware Stores

- **Unit Conversion:** Keep calculator handy
- **Supplier Relationships:** Critical for pricing
- **Delivery Tracking:** Note in invoice/sale
- **Credit Management:** Monitor customer balances
- **Seasonal Demand:** Stock accordingly

---

## 6. User Roles & Permissions

### 6.1 Role Comparison

| Feature | Admin | Manager | Sales User |
|---------|-------|---------|------------|
| Dashboard | ✅ Full | ✅ Full | ✅ Limited |
| Process Sales | ✅ | ✅ | ✅ |
| View Selling Prices | ✅ | ✅ | ✅ |
| View Cost Prices | ✅ | ✅ | ❌ |
| Manage Inventory | ✅ | ✅ | ❌ |
| Add/Edit Products | ✅ | ✅ | ❌ |
| View Suppliers | ✅ | ✅ | ❌ |
| Create Purchases | ✅ | ✅ | ❌ |
| View All Reports | ✅ | ✅ | ❌ |
| View P&L Report | ✅ | ✅ | ❌ |
| Manage Users | ✅ | ❌ | ❌ |
| System Settings | ✅ | ❌ | ❌ |
| Backup/Restore | ✅ | ❌ | ❌ |

### 6.2 Best Practices

**For Admins:**
- Create separate accounts for each staff member
- Never share admin password
- Regularly review user activity
- Disable accounts for departed staff

**For Managers:**
- Review daily sales reports
- Monitor inventory levels
- Manage supplier relationships
- Train sales staff

**For Sales Users:**
- Focus on customer service
- Accurate billing
- Report issues to manager
- Keep workstation secure

---

## 7. Troubleshooting

### 7.1 Common Issues

**Problem: Cannot Login**

**Solution:**
1. Verify username and password (case-sensitive)
2. Check Caps Lock is OFF
3. Try default credentials if first time: admin/admin123
4. Contact administrator to reset password

**Problem: Product Not Found in Search**

**Solution:**
1. Check spelling
2. Try partial name
3. Use barcode instead
4. Verify product exists in Inventory
5. Check if product is marked inactive

**Problem: "Out of Stock" Error During Sale**

**Solution:**
1. Check actual inventory level
2. Update stock if incorrect
3. Use Purchase module to add stock
4. Or proceed with backorder (note in sales notes)

**Problem: Printer Not Printing**

**Solution:**
1. Check printer is ON and connected
2. Check paper loaded
3. Test print from Windows
4. Reinstall printer driver
5. Try different USB port
6. Check printer selected in print dialog

**Problem: Slow Performance**

**Solution:**
1. Close other applications
2. Restart MBAS
3. Restart computer
4. Check database size (go to Backup)
5. If > 2GB, consider archiving old data
6. Run Windows disk cleanup

**Problem: Database Error**

**Solution:**
1. Exit MBAS completely
2. Restart application
3. If persists, restore from latest backup
4. Contact support

**Problem: Cannot Create Backup**

**Solution:**
1. Check destination drive has space (min 500MB)
2. Verify write permissions on destination
3. Try different backup location
4. Close MBAS and restart as Administrator

---

## 8. Frequently Asked Questions (FAQ)

### 8.1 General Questions

**Q: Does MBAS require internet connection?**
A: No, MBAS works 100% offline. No internet needed.

**Q: Can I use MBAS on multiple computers?**
A: Yes, but each installation has separate database. For shared data, manual backup/restore or network database required.

**Q: How many products can I add?**
A: Unlimited. System tested with 100,000+ products.

**Q: Can I customize invoice design?**
A: Limited customization available in Settings. Full customization requires development.

**Q: Is my data secure?**
A: Yes, data stored locally on your computer. Use Windows user accounts and MBAS user roles for security.

**Q: Can I import products from Excel?**
A: Currently not available. Products must be added individually or via API (custom development).

### 8.2 Sales & Billing

**Q: Can I edit a completed sale?**
A: No, sales are final once completed. This ensures data integrity. For corrections, create a new sale with negative quantities (return) and then create correct sale.

**Q: How do I handle returns?**
A: Create new sale with negative quantity and discount equal to returned amount. Note original invoice number.

**Q: Can I pause a sale and resume later?**
A: Not currently. Complete sale or clear cart to start over.

**Q: How do I apply percentage discount?**
A: Calculate discount amount manually and enter in discount field. Example: 10% off $100 = enter $10 discount.

### 8.3 Inventory

**Q: How often should I update stock?**
A: Update immediately after receiving stock (via Purchase module) and daily for perishables.

**Q: What happens when stock reaches zero?**
A: System prevents sale if stock insufficient. Update stock or allow overselling (not recommended).

**Q: Can I transfer stock between categories?**
A: Yes, edit product and change category.

**Q: How do I track product expiry?**
A: Add expiry date in product description. Create "Near Expiry" category and move products manually.

### 8.4 Reports

**Q: How far back do reports go?**
A: Reports show all historical data from system installation.

**Q: Can I schedule automatic reports?**
A: Not currently. Generate manually as needed.

**Q: How do I share reports?**
A: Export to PDF or Excel and email/print.

### 8.5 Backup & Data

**Q: How often should I backup?**
A: Daily, at end of business day. Automatic backups run daily.

**Q: Where are backups stored?**
A: Manual backups: Your chosen location
Automatic backups: C:\ProgramData\MBAS\Backups

**Q: Can I backup to cloud?**
A: Yes, backup to local folder synced with Dropbox/Google Drive.

**Q: How do I transfer data to new computer?**
A: 1. Create backup on old computer
2. Install MBAS on new computer
3. Restore backup on new computer

---

## Appendix A: Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Alt+S | Focus on search (Billing page) |
| F5 | Refresh current page |
| Ctrl+P | Print (on invoice page) |
| Esc | Close dialog/modal |
| Enter | Submit form/Confirm |
| Tab | Move to next field |

---

## Appendix B: File Locations

**Database:**
- Location: `C:\ProgramData\MBAS\mbas_database.db`
- Size: Grows with data (typical: 50-500MB)

**Automatic Backups:**
- Location: `C:\ProgramData\MBAS\Backups\`
- Retention: Last 7 days

**Logs:**
- Location: `C:\ProgramData\MBAS\Logs\`
- Used for troubleshooting

---

## Appendix C: Support & Contact

**Documentation:**
- User Manual (this document)
- Video Tutorials: [Coming Soon]
- Knowledge Base: [Coming Soon]

**Technical Support:**
- Email: support@mbas.local
- Phone: [Your Support Number]
- Hours: Monday-Friday, 9 AM - 6 PM

**Updates:**
- Check for updates: Help → Check for Updates
- Release notes: [Version History]

---

## Appendix D: Glossary

**Terms:**
- **SKU:** Stock Keeping Unit - Unique product identifier
- **COGS:** Cost of Goods Sold - How much you paid for items sold
- **P&L:** Profit & Loss - Financial summary showing profit
- **POS:** Point of Sale - Where sales transactions occur
- **Inventory:** Stock of products available for sale
- **Thermal Printer:** Small receipt printer using heat-sensitive paper
- **A4 Invoice:** Full-page invoice on standard printer paper
- **FIFO:** First In First Out - Sell oldest stock first
- **MRP:** Maximum Retail Price - Price printed on product

---

**End of User Manual**

*Version 1.0 - April 2026*
*© 2026 Modern Business Automation System. All rights reserved.*
