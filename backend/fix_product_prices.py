"""Fix selling prices for existing products."""
from src.core.db import engine
from sqlmodel import Session, select
from src.models.inventory import Product
from decimal import Decimal

def fix_prices():
    session = Session(engine)

    # Mapping of product IDs/barcodes to correct selling prices
    price_fixes = {
        "LAPTOP001": Decimal("1200.00"),
        "MOUSE001": Decimal("25.00"),
        "CABLE001": Decimal("10.00"),
        "KEYB001": Decimal("95.00"),
        "MONITOR001": Decimal("400.00"),
        "WEBCAM001": Decimal("75.00"),
        "BAG001": Decimal("35.00"),
        "SSD001": Decimal("130.00")
    }

    print("Updating product selling prices...")

    for barcode, selling_price in price_fixes.items():
        product = session.exec(
            select(Product).where(Product.barcode == barcode)
        ).first()

        if product:
            product.selling_price = selling_price
            session.add(product)
            print(f"  [FIXED] {product.name}: ${selling_price}")
        else:
            print(f"  [SKIP] Product with barcode {barcode} not found")

    session.commit()

    # Verify
    print("\n[SUCCESS] All product prices updated!")
    print("\nCurrent products:")
    products = session.exec(select(Product)).all()
    for p in products:
        print(f"  {p.id}. {p.name} - Selling: ${p.selling_price}, Cost: ${p.cost_price}, Stock: {p.stock_quantity}")

    session.close()

if __name__ == "__main__":
    fix_prices()
