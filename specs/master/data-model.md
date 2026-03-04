# Data Model: Modern Business Automation System (MBAS)

## Core Database: SQLite (SQLModel/SQLAlchemy 2.0)

### User Management
**Table: `users`**
- `id`: `int` (PK)
- `username`: `str` (Unique, Index)
- `password_hash`: `str` (BCrypt)
- `role`: `str` (Admin, Manager, SalesUser)
- `is_active`: `bool` (Default: True)

### Business Settings & Feature Toggles
**Table: `settings`**
- `id`: `int` (PK)
- `business_name`: `str`
- `logo_path`: `str` (Local file path)
- `address`: `str`
- `phone`: `str`
- `currency_symbol`: `str`
- `tax_percentage`: `decimal`
- `invoice_footer`: `str`
- `package_type`: `str` (Basic, Standard, Premium)
- `feature_flags`: `json` (Dictionary of module/feature toggles)

### Inventory
**Table: `categories`**
- `id`: `int` (PK)
- `name`: `str` (Unique)

**Table: `products`**
- `id`: `int` (PK)
- `name`: `str` (Index)
- `category_id`: `int` (FK -> categories.id)
- `barcode`: `str` (Unique, Index)
- `cost_price`: `decimal`
- `selling_price`: `decimal`
- `stock_quantity`: `int`
- `low_stock_threshold`: `int`
- `is_active`: `bool` (Default: True)

**Virtual Table: `products_fts` (FTS5)**
- `product_id`: `int`
- `name`: `str`
- `barcode`: `str`

### Sales & Customers
**Table: `customers`**
- `id`: `int` (PK)
- `name`: `str`
- `phone`: `str`
- `address`: `str`

**Table: `sales`**
- `id`: `int` (PK)
- `invoice_number`: `str` (Unique, Index)
- `date`: `datetime` (Index)
- `customer_id`: `int` (FK -> customers.id, Optional)
- `user_id`: `int` (FK -> users.id)
- `subtotal`: `decimal`
- `tax_amount`: `decimal`
- `discount_amount`: `decimal`
- `total_amount`: `decimal`
- `payment_method`: `str` (Cash, Card, Other)

**Table: `sale_items`**
- `id`: `int` (PK)
- `sale_id`: `int` (FK -> sales.id)
- `product_id`: `int` (FK -> products.id)
- `quantity`: `int`
- `selling_price`: `decimal` (Price at time of sale)
- `cost_price`: `decimal` (Cost at time of sale for profit calculation)

### Suppliers & Purchases (Standard/Premium)
**Table: `suppliers`**
- `id`: `int` (PK)
- `name`: `str`
- `phone`: `str`
- `address`: `str`
- `opening_balance`: `decimal`

**Table: `purchases`**
- `id`: `int` (PK)
- `invoice_number`: `str`
- `supplier_id`: `int` (FK -> suppliers.id)
- `date`: `datetime`
- `total_amount`: `decimal`

**Table: `purchase_items`**
- `id`: `int` (PK)
- `purchase_id`: `int` (FK -> purchases.id)
- `product_id`: `int` (FK -> products.id)
- `quantity`: `int`
- `cost_price`: `decimal`

**Table: `supplier_payments`**
- `id`: `int` (PK)
- `supplier_id`: `int` (FK -> suppliers.id)
- `date`: `datetime`
- `amount`: `decimal`

### AI & Analytics (Premium)
**Table: `ai_analytics`**
- `id`: `int` (PK)
- `type`: `str` (Prediction, Insight)
- `entity_id`: `int` (Optional, links to Product, etc.)
- `metric_name`: `str`
- `value`: `decimal`
- `prediction_date`: `datetime`
- `generated_at`: `datetime`

## State Transitions & Validation Rules

1. **Sale Execution (Atomic Transaction):**
    - Record Sale and SaleItems.
    - Subtract Product stock_quantity.
    - Update Customer balance (if credit sale).
2. **Purchase Execution (Atomic Transaction):**
    - Record Purchase and PurchaseItems.
    - Add Product stock_quantity.
    - Update Supplier balance.
3. **RBAC Logic:**
    - SalesUser cannot view `cost_price` in `products` or `sale_items`.
    - SalesUser cannot access `suppliers`, `purchases`, or `ai_analytics`.
4. **Package Toggles:**
    - If `package_type` == 'Basic', `suppliers` and `purchases` tables are locked at the API level.
