from sqlmodel import Session, select
from backend.src.core.db import engine, init_db
from backend.src.models.core import User, UserRole, Settings
from backend.src.core.security import get_password_hash

def bootstrap():
    """Initial system setup: Create tables, default settings, and admin user."""
    print("🚀 Initializing MBAS Database...")
    init_db()
    
    with Session(engine) as session:
        # 1. Ensure singleton Settings exist
        statement = select(Settings).where(Settings.id == 1)
        settings = session.exec(statement).first()
        if not settings:
            print("📦 Creating default system settings...")
            settings = Settings(
                id=1,
                business_name="MBAS Demo Store",
                tax_rate=0.0,
                feature_flags={
                    "inventory": True,
                    "billing": True,
                    "dashboard": True,
                    "reports": False,    # Standard/Premium
                    "ai_assistant": False # Premium
                }
            )
            session.add(settings)
        
        # 2. Ensure default Admin user exists
        statement = select(User).where(User.username == "admin")
        admin = session.exec(statement).first()
        if not admin:
            print("🔑 Creating default administrator account...")
            admin = User(
                username="admin",
                full_name="System Administrator",
                role=UserRole.ADMIN,
                hashed_password=get_password_hash("admin123") # Default password
            )
            session.add(admin)
        
        session.commit()
    
    print("✅ System initialized successfully.")

if __name__ == "__main__":
    bootstrap()
