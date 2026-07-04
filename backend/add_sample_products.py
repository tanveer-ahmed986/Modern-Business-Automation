"""Add sample products to test the Purchase functionality."""
from src.core.db import engine
from sqlmodel import Session, select
from src.models.inventory import Product, Category
from decimal import Decimal

def add_sample_products():
    session = Session(engine)

    # Check if category exists
    category = session.exec(select(Category)).first()
    if not category:
        print("Creating default category...")
        category = Category(name="General")
        session.add(category)
        session.commit()
        session.refresh(category)

    print(f"Using category: {category.name} (ID: {category.id})")

    # Sample products
    sample_products = [
        {
            "name": "Laptop Dell XPS 15",
            "barcode": "LAPTOP001",
            "category_id": category.id,
            "cost_price": Decimal("800.00"),
            "selling_price": Decimal("1200.00"),
            "stock_quantity": 0,  # Will be added via purchase
            "low_stock_threshold": 5
        },
        {
            "name": "Wireless Mouse Logitech",
            "barcode": "MOUSE001",
            "category_id": category.id,
            "cost_price": Decimal("15.00"),
            "selling_price": Decimal("25.00"),
            "stock_quantity": 0,
            "low_stock_threshold": 20
        },
        {
            "name": "USB-C Cable",
            "barcode": "CABLE001",
            "category_id": category.id,
            "cost_price": Decimal("5.00"),
            "selling_price": Decimal("10.00"),
            "stock_quantity": 0,
            "low_stock_threshold": 50
        },
        {
            "name": "Mechanical Keyboard",
            "barcode": "KEYB001",
            "category_id": category.id,
            "cost_price": Decimal("60.00"),
            "selling_price": Decimal("95.00"),
            "stock_quantity": 0,
            "low_stock_threshold": 10
        },
        {
            "name": "27-inch Monitor",
            "barcode": "MONITOR001",
            "category_id": category.id,
            "cost_price": Decimal("250.00"),
            "selling_price": Decimal("400.00"),
            "stock_quantity": 0,
            "low_stock_threshold": 5
        },
        {
            "name": "Webcam HD 1080p",
            "barcode": "WEBCAM001",
            "category_id": category.id,
            "cost_price": Decimal("45.00"),
            "selling_price": Decimal("75.00"),
            "stock_quantity": 0,
            "low_stock_threshold": 15
        },
        {
            "name": "Laptop Bag",
            "barcode": "BAG001",
            "category_id": category.id,
            "cost_price": Decimal("20.00"),
            "selling_price": Decimal("35.00"),
            "stock_quantity": 0,
            "low_stock_threshold": 25
        },
        {
            "name": "External SSD 1TB",
            "barcode": "SSD001",
            "category_id": category.id,
            "cost_price": Decimal("80.00"),
            "selling_price": Decimal("130.00"),
            "stock_quantity": 0,
            "low_stock_threshold": 10
        }
    ]

    print("\nAdding products...")
    for product_data in sample_products:
        # Check if product already exists
        existing = session.exec(
            select(Product).where(Product.barcode == product_data["barcode"])
        ).first()

        if existing:
            print(f"  [SKIP] {product_data['name']} already exists")
            continue

        product = Product(**product_data)
        session.add(product)
        print(f"  [+] Added: {product_data['name']} (Cost: ${product_data['cost_price']}, Sale: ${product_data['selling_price']})")

    session.commit()

    # Verify
    total_products = len(session.exec(select(Product)).all())
    print(f"\n[SUCCESS] Total products in database: {total_products}")
    print("\nYou can now:")
    print("  1. Go to Purchases page")
    print("  2. Select the 'Chemical' supplier")
    print("  3. Search for products (e.g., 'laptop', 'mouse')")
    print("  4. Add them to cart and record a purchase")

    session.close()

if __name__ == "__main__":
    add_sample_products()
