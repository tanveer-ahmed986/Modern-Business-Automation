"""
Create default admin user for MBAS
Run this script to initialize the database and create admin user
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from sqlmodel import Session, create_engine, SQLModel, select
from passlib.context import CryptContext

# Import models
from src.models.core import User, Settings, UserRole

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_database():
    """Initialize database and create default admin user"""

    # Create database
    database_path = backend_path / "database" / "mbas_database.db"
    database_path.parent.mkdir(parents=True, exist_ok=True)

    engine = create_engine(f"sqlite:///{database_path}")

    # Create all tables
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("✓ Tables created")

    with Session(engine) as session:
        # Check if admin exists
        statement = select(User).where(User.username == "admin")
        existing_admin = session.exec(statement).first()

        if existing_admin:
            print("\n⚠ Admin user already exists!")
            print(f"  Username: {existing_admin.username}")
            print(f"  Role: {existing_admin.role}")
            return

        # Create admin user
        print("\nCreating default admin user...")
        hashed_password = pwd_context.hash("admin123")

        admin_user = User(
            username="admin",
            full_name="System Administrator",
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
            is_active=True
        )

        session.add(admin_user)

        # Create default settings
        print("Creating default settings...")
        settings = Settings(
            id=1,
            company_name="My Business",
            currency="USD",
            tax_rate=0.0,
            feature_flags={}
        )

        session.add(settings)
        session.commit()

        print("\n" + "="*60)
        print("  ✓ DATABASE INITIALIZED SUCCESSFULLY!")
        print("="*60)
        print("\nDefault Admin Credentials:")
        print(f"  Username: admin")
        print(f"  Password: admin123")
        print("\n⚠ IMPORTANT: Change the password after first login!")
        print("  Settings → Users → Edit admin → Change password")
        print("\n" + "="*60)

if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ ERROR: Failed to initialize database")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
