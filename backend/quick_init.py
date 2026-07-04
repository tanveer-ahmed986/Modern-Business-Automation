"""Quick database initialization using minimal imports."""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import sys

# Add src to path to import security module
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.security import get_password_hash

def init_database():
    """Initialize database with SQL directly."""
    db_path = Path("mbas_database.db")

    # Remove existing database
    if db_path.exists():
        db_path.unlink()
        print(f"[*] Removed existing database")

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    print("[*] Creating database tables...")

    # Create all tables (extracted from SQLModel definitions)
    cursor.executescript("""
        -- Settings table
        CREATE TABLE settings (
            id INTEGER PRIMARY KEY,
            business_name VARCHAR NOT NULL,
            address TEXT,
            phone VARCHAR,
            email VARCHAR,
            tax_rate FLOAT NOT NULL DEFAULT 15.0,
            currency_symbol VARCHAR NOT NULL DEFAULT 'PKR',
            feature_flags JSON NOT NULL
        );

        -- User table
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR NOT NULL UNIQUE,
            email VARCHAR NOT NULL UNIQUE,
            full_name VARCHAR NOT NULL,
            hashed_password VARCHAR NOT NULL,
            role VARCHAR NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        );

        -- Category table
        CREATE TABLE category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR NOT NULL UNIQUE,
            description TEXT
        );

        -- Product table
        CREATE TABLE product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR NOT NULL,
            sku VARCHAR UNIQUE,
            category_id INTEGER,
            cost_price FLOAT NOT NULL,
            selling_price FLOAT NOT NULL,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            reorder_level INTEGER DEFAULT 10,
            barcode VARCHAR UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES category(id)
        );

        -- Customer table
        CREATE TABLE customer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR NOT NULL,
            phone VARCHAR,
            email VARCHAR,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Supplier table
        CREATE TABLE supplier (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR NOT NULL,
            contact_person VARCHAR,
            phone VARCHAR,
            email VARCHAR,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Sale table
        CREATE TABLE sale (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number VARCHAR NOT NULL UNIQUE,
            customer_id INTEGER,
            user_id INTEGER NOT NULL,
            sale_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            subtotal FLOAT NOT NULL,
            discount_amount FLOAT DEFAULT 0.0,
            tax_amount FLOAT NOT NULL,
            total_amount FLOAT NOT NULL,
            payment_method VARCHAR DEFAULT 'cash',
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customer(id),
            FOREIGN KEY (user_id) REFERENCES user(id)
        );

        -- SaleItem table
        CREATE TABLE saleitem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price FLOAT NOT NULL,
            cost_price FLOAT NOT NULL,
            total_price FLOAT NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sale(id),
            FOREIGN KEY (product_id) REFERENCES product(id)
        );

        -- Purchase table
        CREATE TABLE purchase (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            po_number VARCHAR NOT NULL UNIQUE,
            supplier_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            purchase_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            total_amount FLOAT NOT NULL,
            status VARCHAR DEFAULT 'pending',
            notes TEXT,
            FOREIGN KEY (supplier_id) REFERENCES supplier(id),
            FOREIGN KEY (user_id) REFERENCES user(id)
        );

        -- PurchaseItem table
        CREATE TABLE purchaseitem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price FLOAT NOT NULL,
            total_price FLOAT NOT NULL,
            FOREIGN KEY (purchase_id) REFERENCES purchase(id),
            FOREIGN KEY (product_id) REFERENCES product(id)
        );

        -- AI Analytics table
        CREATE TABLE ai_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analytic_type VARCHAR NOT NULL,
            metric_name VARCHAR NOT NULL,
            metric_value FLOAT NOT NULL,
            confidence_score FLOAT,
            insights TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP
        );
    """)

    print("[+] Tables created successfully")

    # Insert default settings with Premium features
    feature_flags = json.dumps({
        "inventory": True,
        "billing": True,
        "customers": True,
        "dashboard": True,
        "suppliers": True,
        "purchases": True,
        "backup_restore": True,
        "advanced_reports": True,
        "premium_reports": True,
        "ai_assistant": True,
        "ai_forecasting": True
    })

    cursor.execute("""
        INSERT INTO settings (id, business_name, tax_rate, currency_symbol, feature_flags)
        VALUES (?, ?, ?, ?, ?)
    """, (1, "MBAS Test Store", 15.0, "PKR", feature_flags))

    print("[+] Default settings created")

    # Insert default admin user
    hashed_pw = get_password_hash("admin123")
    cursor.execute("""
        INSERT INTO user (username, email, full_name, hashed_password, role, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("admin", "admin@mbas.local", "System Administrator", hashed_pw, "ADMIN", 1))

    print("[+] Admin user created (username: admin, password: admin123)")

    # Insert sample categories
    categories = [
        ("Electronics", "Electronic items and gadgets"),
        ("Groceries", "Food and grocery items"),
        ("Clothing", "Apparel and accessories"),
        ("Stationery", "Office and school supplies"),
    ]

    for name, desc in categories:
        cursor.execute("INSERT INTO category (name, description) VALUES (?, ?)", (name, desc))

    print(f"[+] Created {len(categories)} categories")

    # Insert sample products
    products = [
        ("Samsung Galaxy Phone", "ELEC-001", 1, 45000.00, 55000.00, 25, 5, "8801234567890", "Latest Samsung smartphone"),
        ("HP Laptop", "ELEC-002", 1, 75000.00, 90000.00, 10, 3, "8801234567891", "HP 15-inch laptop with 8GB RAM"),
        ("Rice (5kg bag)", "GROC-001", 2, 800.00, 1000.00, 100, 20, "8801234567892", "Premium basmati rice"),
        ("Cooking Oil (1L)", "GROC-002", 2, 400.00, 500.00, 50, 15, "8801234567893", "Pure vegetable cooking oil"),
        ("Men's T-Shirt", "CLOT-001", 3, 500.00, 800.00, 50, 10, "8801234567894", "Cotton casual t-shirt"),
        ("Notebook A4", "STAT-001", 4, 50.00, 80.00, 200, 50, "8801234567895", "200-page ruled notebook"),
    ]

    for product in products:
        cursor.execute("""
            INSERT INTO product (name, sku, category_id, cost_price, selling_price,
                               stock_quantity, reorder_level, barcode, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, product)

    print(f"[+] Created {len(products)} sample products")

    # Insert sample customers
    customers = [
        ("Walk-in Customer", None, None, None),
        ("Ahmed Khan", "0300-1234567", "ahmed@example.com", "Lahore, Pakistan"),
        ("Fatima Ali", "0301-7654321", "fatima@example.com", "Karachi, Pakistan"),
    ]

    for customer in customers:
        cursor.execute("""
            INSERT INTO customer (name, phone, email, address)
            VALUES (?, ?, ?, ?)
        """, customer)

    print(f"[+] Created {len(customers)} sample customers")

    # Insert sample suppliers
    suppliers = [
        ("Tech Distributors", "Imran Hassan", "0300-1111111", "tech@supplier.com", "Islamabad"),
        ("Food Wholesalers", "Sara Ahmed", "0301-2222222", "food@supplier.com", "Faisalabad"),
    ]

    for supplier in suppliers:
        cursor.execute("""
            INSERT INTO supplier (name, contact_person, phone, email, address)
            VALUES (?, ?, ?, ?, ?)
        """, supplier)

    print(f"[+] Created {len(suppliers)} sample suppliers")

    conn.commit()
    conn.close()

    print("\n" + "="*70)
    print("DATABASE INITIALIZATION COMPLETE!")
    print("="*70)
    print("\n✓ Database file: mbas.db")
    print("✓ All tables created")
    print("✓ Sample data inserted")
    print("\nDefault Login Credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nYou can now start the backend server:")
    print("  cd backend")
    print("  python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload")
    print("="*70)

if __name__ == "__main__":
    init_database()
