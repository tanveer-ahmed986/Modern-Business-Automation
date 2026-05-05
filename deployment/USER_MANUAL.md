# MBAS User Manual
## Modern Business Automation System - Complete User Guide

**Version**: 1.0.7
**Last Updated**: April 28, 2026
**Target Audience**: End Users, Business Owners, Sales Staff, Managers

---

## 📑 Table of Contents

1. [Getting Started](#getting-started)
2. [Core Features Overview](#core-features-overview)
3. [User Roles & Permissions](#user-roles--permissions)
4. [Industry-Specific Usage Guides](#industry-specific-usage-guides)
   - [Pharmacy & Medical Supplies](#1-pharmacy--medical-supplies)
   - [Electronics & Mobile Shop](#2-electronics--mobile-shop)
   - [Restaurant & Cafe](#3-restaurant--cafe)
   - [Retail Shop & Boutique](#4-retail-shop--boutique)
   - [Hardware & Building Materials](#5-hardware--building-materials)
   - [Grocery Store & Supermarket](#6-grocery-store--supermarket)
   - [Wholesale & Distribution](#7-wholesale--distribution)
   - [Auto Parts & Service](#8-auto-parts--service)
5. [Module-by-Module Guide](#module-by-module-guide)
6. [Common Tasks & Workflows](#common-tasks--workflows)
7. [Reports & Analytics](#reports--analytics)
8. [Best Practices](#best-practices)
9. [FAQ & Tips](#faq--tips)

---

## 🚀 Getting Started

### First Login

1. **Launch MBAS**
   - Double-click the "MBAS" desktop icon
   - Wait 3-5 seconds for system tray icon to appear
   - Browser opens automatically to login page

2. **Login Credentials**
   ```
   Username: admin
   Password: admin123
   ```
   ⚠️ **Change password immediately after first login!**

3. **Initial Setup Wizard**
   - Enter business name and details
   - Upload your business logo
   - Set currency (USD, EUR, INR, etc.)
   - Configure tax rates
   - Create user accounts

### Understanding the Interface

```
┌─────────────────────────────────────────────────────────────┐
│  🏢 MBAS                          Admin ▼  🔔  ⚙️  🚪       │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                   │
│  📊 Dashboard                                                │
│  💰 Billing    ← Main Navigation (Left Sidebar)             │
│  📦 Inventory                                                │
│  📈 Reports              Main Content Area                  │
│  👥 Customers            (Your work happens here)           │
│  🏭 Suppliers                                                │
│  ⚙️ Settings                                                 │
│                                                              │
└──────────┴──────────────────────────────────────────────────┘
```

### Navigation Tips

- **Sidebar Menu**: Main navigation (always visible)
- **Command Palette**: Press `Ctrl+K` for quick search
- **Breadcrumbs**: Shows your current location
- **User Menu**: Top-right corner (profile, settings, logout)

---

## 🎯 Core Features Overview

### Available in All Packages (Basic, Standard, Premium)

| Feature | Description | Who Uses It |
|---------|-------------|-------------|
| **Point of Sale (POS)** | Fast invoice generation with barcode support | Sales staff |
| **Inventory Management** | Product catalog with search and categories | All users |
| **Customer Database** | Customer details and purchase history | Sales & managers |
| **User Roles** | Admin, Manager, Sales User permissions | Admins |
| **Daily Reports** | Sales summary and stock alerts | Managers |
| **Custom Branding** | Logo, colors, invoice templates | Admins |

### Standard Package Features

| Feature | Description |
|---------|-------------|
| **Supplier Management** | Vendor database and payment tracking |
| **Purchase Orders** | Stock replenishment and cost tracking |
| **Advanced Reports** | Profit/loss, inventory valuation, trends |
| **Backup & Restore** | Automated data protection |

### Premium Package Features

| Feature | Description |
|---------|-------------|
| **AI Sales Forecasting** | Predict future sales based on history |
| **AI Inventory Optimization** | Smart reorder point recommendations |
| **Natural Language Queries** | Ask questions in plain English |

---

## 👥 User Roles & Permissions

### 👨‍💼 Administrator (Full Access)

**Can Do**:
- ✅ All system functions
- ✅ Settings and configuration
- ✅ User management
- ✅ View cost prices and profit margins
- ✅ Financial reports
- ✅ Backup and restore
- ✅ AI features (Premium)

**Typical Users**: Business owner, IT manager

### 👔 Manager (Operations)

**Can Do**:
- ✅ Point of sale
- ✅ Inventory management
- ✅ Supplier and purchase orders
- ✅ Sales reports
- ❌ Cannot change settings
- ❌ Cannot view detailed profit margins
- ❌ Cannot manage users

**Typical Users**: Store manager, operations lead

### 🛒 Sales User (Basic POS)

**Can Do**:
- ✅ Point of sale only
- ✅ View products (selling price only)
- ✅ Create invoices
- ✅ Customer management
- ❌ Cannot see cost prices
- ❌ Cannot access reports
- ❌ Cannot manage inventory

**Typical Users**: Cashiers, sales staff, front desk

---

## 🏥 Industry-Specific Usage Guides

### 1. Pharmacy & Medical Supplies

#### Quick Setup for Pharmacy

1. **Configure Business Settings**
   ```
   Business Type: Pharmacy
   Currency: Your local currency
   Tax Rate: As per local regulations (e.g., 5% GST for medicines)
   ```

2. **Product Categories**
   - Prescription Medicines
   - Over-the-Counter (OTC)
   - Vitamins & Supplements
   - Personal Care
   - Medical Devices
   - Baby Care
   - Health Monitoring

3. **Essential Product Fields**
   - **Product Name**: Paracetamol 500mg
   - **Generic Name**: Acetaminophen (use in description)
   - **Batch Number**: Use "Supplier Invoice" field
   - **Expiry Date**: Use "Notes" field
   - **Manufacturer**: Use "Supplier" field
   - **MRP/Retail Price**: Selling price
   - **Schedule/Class**: Use "Category" field (e.g., Schedule H)

#### Daily Pharmacy Workflow

**Morning Routine**:
1. Login as Manager or Admin
2. Check **Dashboard** for:
   - Low stock alerts
   - Expiring items (check notes)
   - Yesterday's sales summary
3. Review pending supplier payments

**Sales Process**:
1. Customer presents prescription
2. Search product by name or scan barcode
3. Check stock availability
4. Add to cart
5. Apply customer details (for prescription records)
6. Generate invoice
7. Print or email to customer

**Inventory Management**:
1. Go to **Inventory → Products**
2. Filter by category (e.g., "Expiring Soon")
3. Update stock levels after supplier delivery
4. Mark expired products (reduce quantity to zero)
5. Use **Purchase Orders** to restock

**End-of-Day**:
1. Generate **Sales Report** (daily)
2. Count cash drawer and match with system
3. Review pending prescriptions
4. Backup data (automatic in Standard/Premium)

#### Pharmacy-Specific Tips

- **Prescription Tracking**: Use customer notes to record doctor name and prescription number
- **Expiry Management**: Set up weekly review schedule
- **Controlled Substances**: Mark as separate category for auditing
- **Insurance Claims**: Export sales reports for insurance submissions
- **Stock Rotation**: Use FIFO (First In, First Out) - manually track in notes

#### Sample Pharmacy Products

```
Product: Amoxicillin 250mg Capsules
Category: Prescription Medicines
Supplier: PharmaCo Distributors
Cost Price: ₹2.50 per capsule
Selling Price: ₹3.00 per capsule
Stock: 500 capsules
Reorder Level: 100 capsules
Notes: Schedule H, Batch: AMX2024Q2, Exp: 12/2025
```

---

### 2. Electronics & Mobile Shop

#### Quick Setup for Electronics Shop

1. **Configure Business Settings**
   ```
   Business Type: Electronics Retail
   Currency: Your local currency
   Tax Rate: 18% GST (India) or applicable rate
   Warranty Period: Configure per product
   ```

2. **Product Categories**
   - Mobile Phones
   - Laptops & Computers
   - Accessories (cables, chargers, cases)
   - Audio (headphones, speakers)
   - Smart Watches & Wearables
   - Gaming Consoles
   - Home Appliances

3. **Essential Product Fields**
   - **Product Name**: iPhone 15 Pro 128GB Black
   - **Model Number**: Use description field
   - **IMEI/Serial**: Track in customer invoice notes
   - **Warranty**: Use product notes (e.g., "1 year Apple warranty")
   - **Brand**: Use in product name or category
   - **Specifications**: Use description field

#### Daily Electronics Shop Workflow

**Sales Process**:
1. Customer inquires about product
2. Search by brand/model
3. Check current stock
4. Show price to customer
5. Add to cart (may include accessories)
6. **Record IMEI/Serial Number** in invoice notes
7. Apply warranty information
8. Generate invoice
9. Provide printed invoice + warranty card

**Mobile Phone Sales (Specific)**:
1. Verify product is in stock
2. **Record IMEI** before sale:
   - Add to invoice notes
   - Keep record for warranty claims
3. Offer accessories (case, screen protector, charger)
4. Explain warranty terms
5. Activate if required
6. Customer signature on invoice (optional)

**Accessory Bundle Sales**:
1. Search for main product (e.g., "iPhone 15")
2. Add to cart
3. Add suggested accessories:
   - Protective case
   - Screen protector
   - Fast charger
   - Earphones
4. Apply bundle discount (manual price adjustment)
5. Generate combined invoice

**Inventory Management**:
1. Track high-value items separately
2. Update stock immediately after sale
3. Use **Suppliers** module for brand-wise tracking
4. Record model-specific details in product notes
5. Set reorder alerts for fast-moving items

**Returns & Warranty Claims**:
1. Search customer invoice by date or number
2. Verify IMEI matches
3. Check warranty period (in notes)
4. Process return:
   - Adjust inventory (+1 stock)
   - Create credit note (negative invoice)
5. Forward to supplier if under warranty

#### Electronics-Specific Tips

- **IMEI Tracking**: Always record IMEI/Serial in invoice notes for phones, laptops, tablets
- **Combo Offers**: Create "bundle" products or add multiple items to cart
- **Price Fluctuation**: Update prices regularly (weekly for mobiles)
- **Demo Units**: Mark as separate category with "-DEMO" suffix
- **Extended Warranty**: Add as separate product (service item)

#### Sample Electronics Products

```
Product: Samsung Galaxy S24 Ultra 256GB
Category: Mobile Phones → Samsung
Supplier: Samsung India
Cost Price: ₹89,000
Selling Price: ₹1,04,999
Stock: 5 units
Reorder Level: 2 units
Description: 6.8" Dynamic AMOLED, Snapdragon 8 Gen 3, 12GB RAM
Notes: 1 year manufacturer warranty, IMEI tracked on invoice
```

---

### 3. Restaurant & Cafe

#### Quick Setup for Restaurant

1. **Configure Business Settings**
   ```
   Business Type: Restaurant / Cafe
   Currency: Your local currency
   Tax Rate: 5% (Food Tax) or 18% (AC Restaurant)
   Invoice Prefix: TBL (Table) or ORD (Order)
   ```

2. **Product Categories** (Menu Items)
   - Appetizers / Starters
   - Main Course (Veg / Non-Veg)
   - Breads & Rice
   - Beverages (Hot / Cold)
   - Desserts
   - Combo Meals
   - Specials / Chef's Choice

3. **Essential Product Fields**
   - **Item Name**: Butter Chicken
   - **Category**: Main Course → Non-Veg
   - **Cost Price**: Ingredient cost (for profit tracking)
   - **Selling Price**: Menu price
   - **Availability**: Use stock quantity (set to 999 for always available)
   - **Ingredients**: Use description field

#### Daily Restaurant Workflow

**Opening Routine**:
1. Login as Manager
2. Review **Dashboard**:
   - Yesterday's sales
   - Popular items
   - Low stock alerts (ingredients)
3. Update menu availability (mark items as out of stock)

**Taking Orders (POS)**:
1. Select table number (use customer name field: "Table 5")
2. Search menu items by name
3. Add items to cart with quantity
4. Add special instructions (use invoice notes)
5. Review order with customer
6. Generate invoice
7. Print KOT (Kitchen Order Ticket) - use invoice print
8. Print customer bill

**Quick Order Flow**:
```
Waiter → MBAS POS → Add Items → Generate Invoice →
Print KOT → Kitchen → Prepare → Serve →
Customer Payment → Close Invoice
```

**Managing Menu Items**:
1. Go to **Inventory → Products**
2. Add new dish:
   - Name, category, price
   - Set stock to 999 (unlimited) for regular items
   - Set actual stock for limited daily specials
3. Mark seasonal items (use notes)
4. Update prices for daily specials

**Combo Meals**:
1. Create combo as single product:
   ```
   Product: Lunch Combo 1
   Price: ₹299
   Description: 2 Rotis, Dal Makhani, Jeera Rice, Salad, Raita
   ```
2. Or add individual items with discount

**End-of-Day**:
1. Generate **Sales Report**
2. Reconcile cash and card payments
3. Review top-selling items
4. Plan next day's specials
5. Update ingredient stock (if tracked)

#### Restaurant-Specific Tips

- **Table Management**: Use customer name field for table numbers
- **Split Bills**: Generate separate invoices for same table
- **Takeaway**: Use "TAKEAWAY" in customer name
- **Online Orders**: Use "SWIGGY-Order123" or "ZOMATO-Order456" format
- **Kotations**: Print invoice as KOT (Kitchen Order Ticket)
- **Chef Specials**: Create daily special products with date in name
- **Happy Hours**: Manually adjust prices during specific hours

#### Sample Restaurant Products

```
Product: Paneer Butter Masala
Category: Main Course → Vegetarian
Cost Price: ₹85 (ingredient cost)
Selling Price: ₹220
Stock: 999 (always available)
Description: Cottage cheese in rich tomato gravy with butter
Notes: Serves 2, Preparation time: 15 mins
```

```
Product: Chef's Special Biryani (Today)
Category: Specials
Cost Price: ₹120
Selling Price: ₹350
Stock: 20 (limited quantity)
Description: Hyderabadi Dum Biryani with raita and salan
Notes: Available only today - April 28, 2026
```

---

### 4. Retail Shop & Boutique

#### Quick Setup for Retail Shop

1. **Configure Business Settings**
   ```
   Business Type: Retail / Boutique
   Currency: Your local currency
   Tax Rate: 12% or 18% GST (clothing)
   Seasonal Sales: Configure discount periods
   ```

2. **Product Categories**
   - Men's Clothing
   - Women's Clothing
   - Kids Wear
   - Accessories
   - Footwear
   - Seasonal Collection
   - Sale Items

3. **Essential Product Fields**
   - **Product Name**: Cotton Kurta - Blue - L
   - **Size/Variant**: Include in product name
   - **Color**: Include in product name or use separate products
   - **Brand**: Use in product name or category
   - **Material**: Use description
   - **Season**: Use category (Summer 2026, Winter 2025)

#### Daily Boutique Workflow

**Morning Routine**:
1. Review new arrivals
2. Check pending customer orders
3. Review low stock in popular sizes
4. Update sale pricing for clearance

**Sales Process**:
1. Customer browses shop
2. Customer selects items
3. Search products in MBAS
4. Check available sizes (use product name variants)
5. Add to cart
6. Apply discounts if applicable
7. Generate invoice
8. Pack items
9. Customer payment

**Managing Fashion Inventory**:
1. **Size Variants**: Create separate products
   ```
   - Cotton Kurta Blue - S
   - Cotton Kurta Blue - M
   - Cotton Kurta Blue - L
   - Cotton Kurta Blue - XL
   ```

2. **Color Variants**: Create separate products or use description
   ```
   - Cotton Kurta - Blue - L
   - Cotton Kurta - Red - L
   - Cotton Kurta - Green - L
   ```

3. **Stock Management**:
   - Update stock after each sale
   - Track popular sizes
   - Reorder fast-moving items

**Seasonal Sales**:
1. Identify end-of-season stock
2. Create "Sale" category
3. Update prices (manual reduction)
4. Mark original price in description
5. Track clearance items

**Custom Orders**:
1. Create customer record with contact
2. Add order details in customer notes
3. Create pending invoice (save as draft)
4. When ready, complete invoice
5. Customer pickup notification

#### Retail-Specific Tips

- **Size Management**: Use product name for sizes (e.g., "Shirt-Blue-M", "Shirt-Blue-L")
- **Loyalty Programs**: Track in customer notes
- **Alterations**: Add as service product (₹50 - Alteration Service)
- **Exchange/Return**: Create negative invoice, add replacement
- **Seasonal Clearance**: Update prices manually for sale items
- **Gift Wrapping**: Add as additional product

#### Sample Retail Products

```
Product: Designer Saree - Silk - Red
Category: Women's Clothing → Sarees
Supplier: Nalli Silks
Cost Price: ₹2,500
Selling Price: ₹4,999
Stock: 3 units
Description: Pure silk saree with golden border work
Notes: Wedding collection, Hand wash only
```

```
Product: Men's Formal Shirt - White - 40
Category: Men's Clothing → Shirts
Cost Price: ₹450
Selling Price: ₹999
Stock: 5 units
Description: Premium cotton formal shirt, full sleeves
Notes: Size: 40, Available sizes: 38, 40, 42, 44
```

---

### 5. Hardware & Building Materials

#### Quick Setup for Hardware Shop

1. **Configure Business Settings**
   ```
   Business Type: Hardware / Building Materials
   Currency: Your local currency
   Tax Rate: 18% GST (most items)
   Units: Piece, Kg, Meter, Bag, Bundle
   ```

2. **Product Categories**
   - Cement & Concrete
   - Steel & Iron
   - Electrical Items
   - Plumbing & Sanitary
   - Paints & Coatings
   - Tools & Equipment
   - Fasteners (Nuts, Bolts, Screws)
   - Wood & Timber

3. **Essential Product Fields**
   - **Product Name**: ACC Cement - 50kg Bag
   - **Unit of Measure**: Use in name (Kg, Meter, Piece)
   - **Grade/Specification**: Use description
   - **Brand**: Use in product name
   - **Bulk Pricing**: Manage through manual discounts

#### Daily Hardware Shop Workflow

**Sales Process**:
1. Customer provides shopping list
2. Search each item
3. Check stock availability
4. Add to cart with quantity
5. For bulk orders: Apply discount manually
6. Verify total with customer
7. Generate invoice
8. Arrange loading if large order

**Bulk Sales**:
```
Customer orders: 100 bags of cement

1. Search: "ACC Cement 50kg"
2. Add to cart: Quantity = 100
3. Retail price: ₹400/bag = ₹40,000
4. Apply bulk discount: 5% = ₹38,000
5. Generate invoice
6. Arrange truck delivery
```

**Inventory Management**:
1. Track large quantities
2. Update stock after sales
3. Use **Purchase Orders** for supplier orders
4. Monitor fast-moving items (cement, steel)
5. Track seasonal demand (monsoon items)

**Contractor Sales**:
1. Create contractor as customer
2. Generate invoice for project
3. Track multiple invoices per project (use customer notes)
4. Provide monthly statement (use Reports)
5. Manage credit payments (track in supplier ledger - workaround)

#### Hardware-Specific Tips

- **Unit Pricing**: Clearly mention unit in product name (₹40/kg, ₹500/meter)
- **Bulk Discounts**: Apply manual discount at checkout
- **Heavy Items**: Note delivery charges in invoice notes
- **Project Tracking**: Use customer name as "ProjectName-ContractorName"
- **Seasonal Stock**: Plan for monsoon (waterproofing), summer (coolers)
- **Cutting Services**: Add as service product (₹50 - Glass Cutting)

#### Sample Hardware Products

```
Product: TMT Steel Rod - 12mm - Per Kg
Category: Steel & Iron
Supplier: Tata Steel
Cost Price: ₹55/kg
Selling Price: ₹62/kg
Stock: 5000 kg
Reorder Level: 1000 kg
Description: Fe 500D grade, 12mm diameter
Notes: Sold by weight, standard length: 12 meters
```

```
Product: Berger Weather Coat - 20L - White
Category: Paints & Coatings
Cost Price: ₹2,800
Selling Price: ₹3,500
Stock: 15 buckets
Description: Exterior emulsion, weather resistant
Notes: Coverage: 140-160 sq.ft per liter
```

---

### 6. Grocery Store & Supermarket

#### Quick Setup for Grocery Store

1. **Configure Business Settings**
   ```
   Business Type: Grocery / Supermarket
   Currency: Your local currency
   Tax Rate: 5% (essential items) or 12% (packaged goods)
   Barcode Scanner: Enable for faster checkout
   ```

2. **Product Categories**
   - Fresh Produce (Fruits & Vegetables)
   - Dairy & Eggs
   - Bakery
   - Beverages
   - Snacks & Confectionery
   - Staples (Rice, Flour, Pulses)
   - Personal Care
   - Household Items

3. **Essential Product Fields**
   - **Product Name**: Amul Milk - Full Cream - 1L
   - **Weight/Volume**: Include in name
   - **MRP**: Selling price
   - **Barcode**: Use product SKU or barcode field
   - **Expiry Tracking**: Use notes

#### Daily Grocery Store Workflow

**Opening Routine**:
1. Update fresh produce prices (daily rates)
2. Check expiring items (review notes)
3. Remove out-of-stock items from display
4. Review yesterday's sales

**Fast Checkout (POS)**:
1. Customer brings items to counter
2. Scan barcode or search by name
3. Quick add to cart:
   - Amul Milk 1L (Qty: 2)
   - Bread (Qty: 1)
   - Rice 5kg (Qty: 1)
4. Display total to customer
5. Generate invoice
6. Print receipt
7. Next customer

**Express Billing Tips**:
- Use barcode scanner for packaged goods
- Use quick search (Ctrl+K) for common items
- Keep frequently sold items favorited
- Train staff on keyboard shortcuts

**Managing Perishables**:
1. Daily pricing updates for vegetables
2. Mark items near expiry in notes
3. Apply discounts for near-expiry items
4. Remove expired items from stock

**Bulk Customer Orders**:
1. Create customer account (for monthly billing)
2. Generate invoice
3. Track credit payments in customer notes
4. Provide monthly statement

#### Grocery-Specific Tips

- **Daily Price Changes**: Update vegetable/fruit prices every morning
- **Barcode Scanning**: Use SKU field for barcode integration
- **Loose Items**: Create products by weight (Rice - Per Kg)
- **Offers**: Create combo products (Milk + Bread Combo)
- **Loyalty Cards**: Track points in customer notes
- **Home Delivery**: Mark "Delivery - CustomerName" in invoice notes

#### Sample Grocery Products

```
Product: Tomato - Per Kg
Category: Fresh Produce → Vegetables
Cost Price: ₹25/kg (updated daily)
Selling Price: ₹30/kg
Stock: 100 kg
Notes: Today's rate: April 28, Fresh stock
```

```
Product: Amul Butter - 100g
Category: Dairy
Supplier: Amul Distributors
Cost Price: ₹45
Selling Price: ₹50
Stock: 50 units
Barcode: 8901430009014
Notes: MRP: ₹50, Exp: Check on pack
```

---

### 7. Wholesale & Distribution

#### Quick Setup for Wholesale Business

1. **Configure Business Settings**
   ```
   Business Type: Wholesale / Distribution
   Currency: Your local currency
   Tax Rate: 18% GST (B2B sales)
   Credit Terms: 30/60/90 days
   ```

2. **Product Categories**
   - By product line or by manufacturer
   - FMCG Products
   - Electronics Wholesale
   - Textile Wholesale
   - Industrial Supplies

3. **Essential Features**
   - **Bulk Pricing**: Track wholesale vs retail prices
   - **Credit Management**: Use customer notes for credit limits
   - **B2B Invoices**: Include GST details
   - **Supplier Management**: Track purchase orders

#### Daily Wholesale Workflow

**Order Processing**:
1. Receive order from retailer (phone/email/visit)
2. Create customer account (if new)
3. Search products and add to cart
4. Apply wholesale pricing (may need manual adjustment)
5. Check credit limit (manual check in customer notes)
6. Generate invoice with GST details
7. Arrange delivery
8. Track payment due date

**Large Order Example**:
```
Retailer orders:
- 10 cartons of Soap (120 pieces each)
- 5 cartons of Shampoo (60 bottles each)
- 20 cartons of Detergent (30 packs each)

1. Add each product with carton quantity
2. Apply wholesale rate
3. Calculate GST
4. Generate B2B invoice
5. Delivery challan (print invoice as delivery note)
```

**Credit Management**:
1. Set credit limit in customer notes
2. Before creating invoice, check:
   - Outstanding invoices (use Reports → Customer Sales)
   - Credit limit
   - Payment history
3. If limit exceeded, request payment first

**Supplier Purchase Orders**:
1. Go to **Purchases** module
2. Create new purchase order
3. Add products with quantities
4. Track order status
5. When stock arrives, update inventory
6. Record supplier payment

#### Wholesale-Specific Tips

- **Carton/Box Pricing**: Create products as "per carton" or "per box"
- **Minimum Order Quantity**: Mention in product notes
- **Bulk Discounts**: Tiered pricing (manual adjustment)
- **GST Invoices**: Ensure all details for B2B compliance
- **Delivery Tracking**: Use invoice notes for truck/delivery details
- **Credit Control**: Strict monitoring of outstanding payments

#### Sample Wholesale Products

```
Product: Dove Soap - 100g - Carton (120 pcs)
Category: FMCG → Personal Care
Supplier: HUL Distributors
Cost Price: ₹2,400 (₹20/piece)
Wholesale Price: ₹2,880 (₹24/piece)
Retail MRP: ₹30/piece
Stock: 50 cartons
MOQ: 5 cartons
Notes: 120 pieces per carton, GST 18%
```

---

### 8. Auto Parts & Service

#### Quick Setup for Auto Parts Shop

1. **Configure Business Settings**
   ```
   Business Type: Auto Parts & Accessories
   Currency: Your local currency
   Tax Rate: 28% GST (auto parts in India)
   Warranty: Track per product
   ```

2. **Product Categories**
   - Engine Parts
   - Brake System
   - Suspension & Steering
   - Electrical Components
   - Filters (Oil, Air, Fuel)
   - Batteries
   - Tyres & Wheels
   - Accessories
   - Lubricants & Fluids

3. **Essential Product Fields**
   - **Part Number**: Use in product name
   - **Vehicle Compatibility**: Use description
   - **OEM vs Aftermarket**: Use category
   - **Warranty Period**: Use notes

#### Daily Auto Parts Workflow

**Sales Process**:
1. Customer provides vehicle details + required part
2. Search by part number or name
3. Verify compatibility (check description)
4. Check stock
5. Advise on installation (if service available)
6. Add to cart
7. Include warranty information in invoice notes
8. Generate invoice

**Service Integration**:
```
Customer needs: Oil change service

Products:
1. Engine Oil - 5L (₹1,200)
2. Oil Filter (₹300)
3. Labor - Oil Change Service (₹500)

Total Invoice: ₹2,000
```

**Managing Part Numbers**:
- Create products with full part number
- Use description for vehicle compatibility
- Example: "Brake Pad Set - BP1234 (Honda City 2018-2023)"

**Warranty Tracking**:
1. Record warranty period in product notes
2. Include warranty terms in invoice notes
3. Keep customer contact for follow-up
4. Track warranty claims (use customer notes)

#### Auto Parts-Specific Tips

- **Part Numbers**: Always include in product name for easy search
- **Compatibility Charts**: Maintain in product descriptions
- **Service Products**: Create "labor" products (₹500 - Brake Service)
- **Battery Exchange**: Track old battery return (discount on invoice)
- **Tyre Installation**: Add as service product
- **Bulk Mechanic Sales**: Create mechanic as customer for tracking

#### Sample Auto Parts Products

```
Product: Engine Oil - Castrol GTX - 5W-30 - 5L
Category: Lubricants & Fluids
Supplier: Castrol India
Cost Price: ₹1,800
Selling Price: ₹2,200
Stock: 30 units
Description: Suitable for petrol engines, API SN, ACEA A3/B4
Notes: 5000 km or 6 months warranty
```

```
Product: Brake Pad Set - BP8945 - Maruti Swift
Category: Brake System → Brake Pads
Part Number: BP8945
Cost Price: ₹650
Selling Price: ₹950
Stock: 15 sets
Description: Front brake pads for Maruti Swift (2018-2023)
Notes: 10,000 km warranty, Installation available
```

---

## 📚 Module-by-Module Guide

### 📊 Dashboard

**Purpose**: Quick overview of business performance

**Key Metrics**:
- **Total Sales Today**: Real-time sales amount
- **Invoices Generated**: Count of bills
- **Top Selling Products**: Best performers
- **Low Stock Alerts**: Items to reorder
- **Recent Transactions**: Latest invoices

**How to Use**:
1. Login and view dashboard (default landing page)
2. Review key metrics at a glance
3. Click on alerts for more details
4. Use quick actions for common tasks

**Best For**: Daily morning review, quick health check

---

### 💰 Billing (Point of Sale)

**Purpose**: Generate customer invoices quickly

**Step-by-Step Billing**:

1. **Start New Invoice**
   - Click "New Invoice" or "Billing" in sidebar
   - Blank invoice screen appears

2. **Add Products**
   - **Method 1**: Search by name
     - Type product name in search box
     - Select from dropdown
     - Press Enter or click Add

   - **Method 2**: Barcode scan
     - Click barcode input field
     - Scan product barcode
     - Product added automatically

   - **Method 3**: Browse products
     - Click "Browse Products" button
     - Select category
     - Click on product to add

3. **Adjust Quantities**
   - Click quantity field next to product
   - Enter new quantity
   - Price updates automatically

4. **Add Customer (Optional but Recommended)**
   - Search existing customer by name/phone
   - Or click "Add New Customer"
   - Enter customer details
   - Save customer

5. **Apply Discounts (If Applicable)**
   - Click on discount field
   - Enter discount percentage or amount
   - Total updates automatically

6. **Review Total**
   - **Subtotal**: Before tax and discount
   - **Discount**: Amount reduced
   - **Tax**: GST or sales tax
   - **Grand Total**: Final amount to pay

7. **Generate Invoice**
   - Click "Generate Invoice" button
   - Invoice number assigned automatically
   - Format: `INV-20260428-0001`

8. **Print or Email**
   - Click "Print" for paper receipt
   - Click "Email" to send to customer
   - Or click "Download PDF"

**Quick Tips**:
- Use keyboard shortcuts: `Ctrl+K` for quick search
- Press `F9` to quickly generate invoice
- Use Tab to navigate between fields
- Double-click product to edit quantity

---

### 📦 Inventory (Product Management)

**Purpose**: Manage product catalog and stock levels

**Adding New Product**:

1. Click **Inventory** → **Products** → **Add New Product**

2. Fill in product details:
   ```
   Product Name: *Required* (e.g., "iPhone 15 Pro 128GB")
   Category: Select from dropdown
   SKU/Barcode: Optional (for scanning)

   Pricing:
   - Cost Price: What you pay supplier
   - Selling Price: What customer pays
   - Profit Margin: Auto-calculated

   Stock:
   - Current Stock: Available quantity
   - Reorder Level: Alert when stock falls below this

   Supplier: Select default supplier

   Description: Product details, specifications
   Notes: Internal notes (expiry, warranty, etc.)
   ```

3. Click **Save Product**

**Editing Existing Product**:
1. Search for product
2. Click on product name
3. Edit any field
4. Click "Update Product"

**Adjusting Stock**:
1. Find product in inventory list
2. Click "Adjust Stock" button
3. Enter new quantity
4. Add reason (optional): "Received supplier delivery"
5. Save adjustment

**Bulk Stock Update**:
1. When supplier delivery arrives
2. Go to **Purchases** → **New Purchase Order**
3. Add all products from delivery
4. Save purchase order
5. Stock updates automatically

**Categories Management**:
1. Click **Inventory** → **Categories**
2. Add new category or edit existing
3. Assign products to categories
4. Use for filtering and reports

---

### 👥 Customers

**Purpose**: Maintain customer database and purchase history

**Adding New Customer**:

1. Click **Customers** → **Add Customer**

2. Fill details:
   ```
   Customer Name: *Required*
   Phone Number: Contact number
   Email: For sending invoices
   Address: Delivery address

   Tax ID / GST Number: For B2B customers
   Credit Limit: Maximum outstanding allowed

   Notes: Loyalty points, preferences, etc.
   ```

3. Click **Save Customer**

**Customer Purchase History**:
1. Search for customer
2. Click on customer name
3. View all past invoices
4. See total purchases
5. Track payment history

**Customer Reports**:
1. Go to **Reports** → **Customer Reports**
2. Select customer
3. View date-wise purchases
4. Export to Excel/PDF

---

### 🏭 Suppliers (Standard/Premium)

**Purpose**: Manage vendor relationships and purchases

**Adding Supplier**:
1. Click **Suppliers** → **Add Supplier**
2. Enter supplier details:
   - Name, contact, address
   - Tax ID / GST number
   - Payment terms (30/60/90 days)
   - Credit limit
3. Save supplier

**Supplier Ledger**:
1. View all transactions with supplier
2. Track pending payments
3. See purchase history
4. Generate supplier statements

---

### 🛒 Purchases (Standard/Premium)

**Purpose**: Record stock purchases from suppliers

**Creating Purchase Order**:

1. Click **Purchases** → **New Purchase**

2. Select Supplier from dropdown

3. Add Products:
   - Search and select product
   - Enter quantity purchased
   - Enter cost price (per unit)
   - Add more products as needed

4. Review Purchase Details:
   - **Subtotal**: Total cost before tax
   - **Tax**: GST or purchase tax
   - **Total Amount**: Final payment to supplier

5. Payment Information:
   - **Payment Status**: Paid / Pending / Partial
   - **Amount Paid**: If paying now
   - **Payment Method**: Cash / Bank Transfer / Cheque

6. Click **Save Purchase Order**

**Stock Update**:
- When you save purchase order, stock automatically increases
- Check inventory to verify stock update

**Supplier Payment Tracking**:
1. Go to **Suppliers** → Select Supplier
2. View **Supplier Ledger**
3. See pending payments
4. Record payment when made

---

### 📈 Reports & Analytics

**Purpose**: Business insights and decision making

**Available Reports**:

1. **Sales Reports**
   - Daily/Weekly/Monthly/Yearly sales
   - Sales by product
   - Sales by category
   - Sales by customer
   - Salesperson performance

2. **Inventory Reports**
   - Current stock levels
   - Low stock alerts
   - Overstock items
   - Stock valuation
   - Inventory movement

3. **Profit & Loss** (Premium)
   - Revenue vs expenses
   - Profit margins by product
   - Profit margins by category
   - Monthly/yearly trends

4. **Financial Reports**
   - Outstanding payments (customers)
   - Payable to suppliers
   - Cash flow summary

**Generating Reports**:

1. Click **Reports** in sidebar

2. Select report type

3. Set date range:
   - Today
   - This Week
   - This Month
   - Custom Range (select start and end date)

4. Apply filters (optional):
   - Filter by category
   - Filter by customer
   - Filter by payment status

5. Click **Generate Report**

6. **Export Options**:
   - View on screen
   - Download PDF
   - Export to Excel
   - Print

**Premium: AI-Powered Insights**

1. **Sales Forecasting**:
   - Predicts next month's sales
   - Based on historical trends
   - Seasonal adjustments

2. **Inventory Optimization**:
   - Suggests optimal reorder quantities
   - Identifies slow-moving items
   - Recommends stock adjustments

3. **Natural Language Queries**:
   - Ask: "What were my top 5 products last month?"
   - Ask: "Which customers haven't purchased in 60 days?"
   - Get instant answers

---

### ⚙️ Settings

**Purpose**: Configure system and business preferences

**Business Information**:
1. Click **Settings** → **Business Info**
2. Update:
   - Business name
   - Address, phone, email
   - Tax ID / GST number
   - Currency (USD, EUR, INR, etc.)
   - Timezone

**Branding**:
1. **Logo Upload**:
   - Click "Upload Logo"
   - Select image file (PNG/JPG)
   - Logo appears on invoices

2. **Color Theme**:
   - Choose primary color
   - Choose accent color
   - Preview changes

**Invoice Settings**:
1. **Invoice Prefix**: Change from "INV" to custom prefix
2. **Tax Rates**: Set default tax percentage
3. **Payment Terms**: Net 30, Net 60, etc.
4. **Footer Text**: Terms and conditions, thank you note

**User Management** (Admin Only):
1. Click **Settings** → **Users**
2. **Add New User**:
   - Username
   - Email
   - Password
   - Role (Admin / Manager / Sales User)
3. **Edit User**: Change role or reset password
4. **Deactivate User**: Disable access without deleting

**Backup & Restore** (Standard/Premium):
1. **Manual Backup**:
   - Click "Create Backup"
   - Backup file saved to `backend/backups/`

2. **Automatic Backup**:
   - Enable daily/weekly auto-backup
   - Set backup retention period

3. **Restore**:
   - Select backup file
   - Click "Restore Database"
   - Confirm restoration

**Security Settings**:
1. **Change Password**:
   - Click user menu → Change Password
   - Enter current password
   - Enter new password (min 8 characters)
   - Confirm

2. **Session Timeout**:
   - Auto-logout after inactivity
   - Default: 30 minutes

---

## 🔄 Common Tasks & Workflows

### Task 1: Processing a Quick Sale

**Time**: 30 seconds

1. Click **Billing**
2. Search product: "Coke"
3. Select "Coca Cola 500ml" from dropdown
4. Press Enter (quantity defaults to 1)
5. Click **Generate Invoice**
6. Print receipt
7. Done!

---

### Task 2: Adding Stock After Supplier Delivery

**Time**: 2-3 minutes

1. Click **Purchases** → **New Purchase**
2. Select supplier: "ABC Distributors"
3. Add products received:
   - Product 1: Rice 25kg (Qty: 10 bags)
   - Product 2: Sugar 5kg (Qty: 20 bags)
4. Enter total amount paid: ₹5,000
5. Payment status: "Paid"
6. Click **Save Purchase**
7. Stock automatically updated
8. Verify in **Inventory**

---

### Task 3: End-of-Day Sales Report

**Time**: 1 minute

1. Click **Reports** → **Sales Reports**
2. Select "Today"
3. Click **Generate Report**
4. Review:
   - Total sales: ₹15,450
   - Invoices: 28
   - Top product: Coca Cola (15 units)
5. Export to PDF for records
6. Done!

---

### Task 4: Customer Purchase History Lookup

**Time**: 30 seconds

1. Click **Customers**
2. Search: "John Doe"
3. Click on customer name
4. View purchase history:
   - Last purchase: April 25, 2026
   - Total purchases: ₹45,800 (year-to-date)
   - Pending payment: ₹0
5. Done!

---

### Task 5: Setting Low Stock Alerts

**Time**: 1 minute per product

1. Click **Inventory** → **Products**
2. Search product: "Amul Milk 1L"
3. Click on product to edit
4. Set **Reorder Level**: 20 units
5. Click **Update Product**
6. When stock falls below 20, alert appears on dashboard
7. Done!

---

## 📊 Reports & Analytics Guide

### Understanding Key Metrics

**Gross Sales**: Total sales before discounts and returns
**Net Sales**: After discounts and returns
**Profit Margin**: (Selling Price - Cost Price) / Selling Price × 100
**Stock Turnover**: How many times stock is sold and replaced

### Best Reporting Practices

1. **Daily Review**:
   - Check dashboard every morning
   - Review yesterday's sales
   - Address low stock alerts

2. **Weekly Review**:
   - Sales trend analysis
   - Top 10 products
   - Slow-moving inventory

3. **Monthly Review**:
   - Profit & loss statement
   - Inventory valuation
   - Supplier payment reconciliation
   - Customer outstanding payments

4. **Quarterly Review**:
   - Seasonal trends
   - Category performance
   - Strategic inventory planning

---

## ✅ Best Practices

### Inventory Management

1. **Regular Stock Counts**: Physical verification weekly/monthly
2. **FIFO Method**: First In, First Out (for expiring products)
3. **Reorder Levels**: Set for all products to avoid stockouts
4. **Category Organization**: Logical grouping for easy search
5. **Accurate Cost Pricing**: Update cost prices when supplier prices change

### Billing & Invoicing

1. **Always Add Customer**: Builds valuable database
2. **Verify Before Generating**: Double-check quantities and prices
3. **Print/Email Immediately**: Professional customer service
4. **Daily Reconciliation**: Match physical cash with system
5. **Backup Invoices**: Keep PDF copies for tax purposes

### Security & Access Control

1. **Strong Passwords**: Minimum 8 characters, mix of letters/numbers/symbols
2. **Role-Based Access**: Give users only necessary permissions
3. **Regular Backups**: Daily automated backups (Standard/Premium)
4. **Logout When Not in Use**: Prevent unauthorized access
5. **Password Changes**: Update passwords quarterly

### Data Quality

1. **Complete Product Information**: All fields filled accurately
2. **Standardized Naming**: Consistent product name format
3. **Regular Data Cleanup**: Remove duplicate or obsolete products
4. **Customer Data Accuracy**: Verify phone/email at every transaction
5. **Supplier Updates**: Keep contact information current

---

## ❓ FAQ & Tips

### General Questions

**Q: Can I use MBAS without internet?**
A: Yes! MBAS is 100% offline. Internet only needed for first-time installation.

**Q: How many products can I add?**
A: Unlimited. SQLite database supports 100,000+ products efficiently.

**Q: Can multiple users work simultaneously?**
A: Yes, up to 5 concurrent users on the same network.

**Q: Is my data secure?**
A: Yes. All data stored locally on your computer. Passwords encrypted with BCrypt.

**Q: Can I customize invoice templates?**
A: Yes, in Settings → Invoice Settings. Upload logo, change colors, add footer text.

### Billing Questions

**Q: Can I edit an invoice after generation?**
A: No, invoices are immutable for accounting integrity. Create a new invoice or credit note for corrections.

**Q: How do I handle returns?**
A: Create a new invoice with negative quantity (or use credit note feature if available).

**Q: Can I apply discounts?**
A: Yes, at invoice level or product level. Enter percentage or flat amount.

**Q: What if I make a mistake in billing?**
A: For minor errors: Note in invoice. For major errors: Create corrected invoice and void the incorrect one (mark in notes).

### Inventory Questions

**Q: How do I track variants (sizes, colors)?**
A: Create separate products for each variant. Example: "Shirt Red L", "Shirt Red XL", "Shirt Blue L"

**Q: Can I import products from Excel?**
A: Not built-in yet. Manual entry or custom import script required.

**Q: How do I handle damaged/expired stock?**
A: Reduce stock quantity manually. Add reason in notes: "5 units damaged"

### Reporting Questions

**Q: Can I export reports to Excel?**
A: Yes, all reports have "Export to Excel" option.

**Q: What's the difference between Standard and Premium reports?**
A: Premium includes AI-powered forecasting, natural language queries, and advanced profit analysis.

**Q: How far back does data go?**
A: Unlimited. All historical data preserved unless manually deleted.

### Tips & Tricks

1. **Keyboard Shortcuts**:
   - `Ctrl+K`: Quick search (command palette)
   - `F9`: Generate invoice (on billing page)
   - `Esc`: Close dialogs/modals
   - `Tab`: Navigate form fields

2. **Fast Product Search**:
   - Type first few letters
   - Use product code/SKU for faster lookup
   - Barcode scanning (if hardware available)

3. **Backup Reminders**:
   - Set phone reminder for weekly backups
   - Copy backup file to USB/cloud storage
   - Test restore process quarterly

4. **Customer Service**:
   - Email invoices for professional touch
   - Keep customer purchase history for personalized service
   - Use customer notes for preferences

5. **Performance Optimization**:
   - Run VACUUM on database monthly (in Settings)
   - Archive old data yearly
   - Keep system updated

---

## 🎓 Training Recommendations

### For Administrators

- **Week 1**: System setup, settings configuration, user management
- **Week 2**: Inventory management, supplier setup, purchase orders
- **Week 3**: Reports and analytics, backup and restore
- **Week 4**: Advanced features, AI tools (Premium)

### For Managers

- **Day 1**: Navigation, dashboard overview
- **Day 2**: Billing and invoicing
- **Day 3**: Inventory management
- **Day 4**: Reports and daily tasks
- **Day 5**: Supplier and purchase orders

### For Sales Users

- **Day 1**: Login, navigation, dashboard
- **Day 2**: Product search and billing
- **Day 3**: Customer management
- **Day 4**: Practice and speed drills

---

## 📞 Support & Resources

### Help Documentation

- **Installation Guide**: `INSTALLATION_REQUIREMENTS_GUIDE.md`
- **System Preview**: `SYSTEM_PREVIEW.md`
- **Quick Start**: `README_FIRST.txt`

### Video Tutorials (If Available)

- Getting Started (10 mins)
- Billing Basics (5 mins)
- Inventory Management (15 mins)
- Reports & Analytics (10 mins)

### Community Support

- Contact your system administrator
- Refer to product documentation
- Check release notes for updates

---

## 🔄 Quick Reference Card

**Print this section for desk reference:**

```
┌─────────────────────────────────────────────────────────────┐
│                   MBAS QUICK REFERENCE                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🚀 START MBAS                                              │
│  Double-click "MBAS" desktop icon                           │
│                                                             │
│  🔐 DEFAULT LOGIN                                           │
│  Username: admin                                            │
│  Password: admin123                                         │
│                                                             │
│  ⚡ QUICK BILLING                                           │
│  1. Billing → Search Product → Add to Cart → Generate      │
│                                                             │
│  📦 ADD STOCK                                               │
│  1. Purchases → New Purchase → Add Products → Save         │
│                                                             │
│  📊 DAILY REPORT                                            │
│  1. Reports → Sales Reports → Today → Generate             │
│                                                             │
│  ⌨️ SHORTCUTS                                               │
│  Ctrl+K : Quick Search                                      │
│  F9     : Generate Invoice                                  │
│  Esc    : Close Dialog                                      │
│                                                             │
│  🆘 HELP                                                    │
│  Right-click MBAS tray icon → Health Check                 │
│  Or run: HEALTH_CHECK.bat                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**User Manual Version**: 1.0.7
**Last Updated**: April 28, 2026
**Total Pages**: 50+
**Status**: Production-Ready
**Next Review**: July 2026

---

**End of User Manual**

For technical installation details, refer to: `INSTALLATION_REQUIREMENTS_GUIDE.md`
