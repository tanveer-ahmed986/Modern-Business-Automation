"""
Simple database initialization script that can be run independently.
"""
import sys
from pathlib import Path

# Add backend/src to Python path
backend_dir = Path(__file__).parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

from sqlmodel import Session, select
from core.db import engine, init_db
from models.core import User, UserRole, Settings, Category
from models.inventory import Product
from core.security import get_password_hash
from models.license import get_tier_features

def main():
    """Initialize database with default data."""
    print("[*] Initializing MBAS Database...")

    # Create all tables
    init_db()
    print("[+] Database tables created")

    with Session(engine) as session:
        # 1. Create default settings
        statement = select(Settings).where(Settings.id == 1)
        settings = session.exec(statement).first()

        if not settings:
            print("[+] Creating default system settings...")

            # Load license features (Premium tier for testing)
            try:
                from core.license import LicenseValidator
                license_path = Path("../mbas.license")
                public_key_path = Path("src/embedded/public_key.pem")

                if license_path.exists() and public_key_path.exists():
                    validator = LicenseValidator(str(license_path), str(public_key_path))
                    license_data = validator.validate()
                    business_name = license_data.licensee
                    feature_flags = license_data.features.model_dump()
                    print(f"[+] Loaded {license_data.tier.upper()} license for: {business_name}")
                else:
                    print("[!] No license found, using Premium tier defaults for testing")
                    business_name = "MBAS Test Store"
                    feature_flags = get_tier_features("premium").model_dump()
            except Exception as e:
                print(f"[!] License validation failed: {e}")
                print("[!] Using Premium tier defaults for testing")
                business_name = "MBAS Test Store"
                feature_flags = get_tier_features("premium").model_dump()

            settings = Settings(
                id=1,
                business_name=business_name,
                tax_rate=15.0,  # 15% default tax
                currency_symbol="PKR",
                feature_flags=feature_flags
            )
            session.add(settings)
            session.commit()
            print(f"[+] Settings created: {business_name}")
        else:
            print(f"[+] Settings already exist: {settings.business_name}")

        # 2. Create default admin user
        statement = select(User).where(User.username == "admin")
        admin = session.exec(statement).first()

        if not admin:
            print("[+] Creating default admin user...")
            admin = User(
                username="admin",
                email="admin@mbas.local",
                full_name="System Administrator",
                hashed_password=get_password_hash("admin123"),  # Default password
                role=UserRole.ADMIN,
                is_active=True
            )
            session.add(admin)
            session.commit()
            print("[+] Admin user created (username: admin, password: admin123)")
        else:
            print(f"[+] Admin user already exists: {admin.username}")

        # 3. Create sample categories
        statement = select(Category)
        categories = session.exec(statement).all()

        if not categories:
            print("[+] Creating sample categories...")
            sample_categories = [
                Category(name="Electronics", description="Electronic items and gadgets"),
                Category(name="Groceries", description="Food and grocery items"),
                Category(name="Clothing", description="Apparel and accessories"),
                Category(name="Stationery", description="Office and school supplies"),
            ]
            for cat in sample_categories:
                session.add(cat)
            session.commit()
            print(f"[+] Created {len(sample_categories)} categories")
        else:
            print(f"[+] {len(categories)} categories already exist")

        # 4. Create sample products
        statement = select(Product)
        products = session.exec(statement).all()

        if not products:
            print("[+] Creating sample products...")

            # Get categories for assignment
            electronics = session.exec(select(Category).where(Category.name == "Electronics")).first()
            groceries = session.exec(select(Category).where(Category.name == "Groceries")).first()

            sample_products = [
                Product(
                    name="Samsung Galaxy Phone",
                    sku="ELEC-001",
                    category_id=electronics.id if electronics else None,
                    cost_price=45000.00,
                    selling_price=55000.00,
                    stock_quantity=25,
                    reorder_level=5,
                    barcode="8801234567890",
                    description="Latest Samsung smartphone"
                ),
                Product(
                    name="HP Laptop",
                    sku="ELEC-002",
                    category_id=electronics.id if electronics else None,
                    cost_price=75000.00,
                    selling_price=90000.00,
                    stock_quantity=10,
                    reorder_level=3,
                    barcode="8801234567891",
                    description="HP 15-inch laptop with 8GB RAM"
                ),
                Product(
                    name="Rice (5kg bag)",
                    sku="GROC-001",
                    category_id=groceries.id if groceries else None,
                    cost_price=800.00,
                    selling_price=1000.00,
                    stock_quantity=100,
                    reorder_level=20,
                    barcode="8801234567892",
                    description="Premium basmati rice"
                ),
                Product(
                    name="Cooking Oil (1L)",
                    sku="GROC-002",
                    category_id=groceries.id if groceries else None,
                    cost_price=400.00,
                    selling_price=500.00,
                    stock_quantity=50,
                    reorder_level=15,
                    barcode="8801234567893",
                    description="Pure vegetable cooking oil"
                ),
            ]

            for product in sample_products:
                session.add(product)
            session.commit()
            print(f"[+] Created {len(sample_products)} sample products")
        else:
            print(f"[+] {len(products)} products already exist")

    print("\n" + "="*60)
    print("DATABASE INITIALIZATION COMPLETE!")
    print("="*60)
    print("\nDefault Login Credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nBackend API: http://127.0.0.1:8000")
    print("API Docs: http://127.0.0.1:8000/docs")
    print("="*60)

if __name__ == "__main__":
    main()
