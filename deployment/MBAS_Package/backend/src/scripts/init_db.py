import sys
from pathlib import Path

# Add backend/src to path for direct script execution
backend_src = Path(__file__).parent.parent
if str(backend_src) not in sys.path:
    sys.path.insert(0, str(backend_src))

from sqlmodel import Session, select
from src.core.db import engine, init_db
from src.models.core import User, UserRole, Settings
from src.core.security import get_password_hash
from src.models.license import get_tier_features

def bootstrap():
    """Initial system setup: Create tables, default settings, and admin user."""
    print("[*] Initializing MBAS Database...")
    init_db()

    with Session(engine) as session:
        # 1. Ensure singleton Settings exist
        statement = select(Settings).where(Settings.id == 1)
        settings = session.exec(statement).first()
        if not settings:
            print("[+] Creating default system settings...")

            # Try to load license features, fallback to Basic tier
            try:
                from src.core.license import LicenseValidator
                _script_dir = Path(__file__).resolve().parent  # backend/src/scripts/
                _src_dir = _script_dir.parent                  # backend/src/
                _backend_dir = _src_dir.parent                 # backend/
                _project_dir = _backend_dir.parent             # project root

                # Find license file
                license_path = None
                for candidate in [
                    _project_dir / "mbas.license",
                    _backend_dir / "mbas.license",
                    Path("mbas.license"),
                ]:
                    if candidate.exists():
                        license_path = candidate
                        break

                # Find public key
                public_key_path = None
                for candidate in [
                    _src_dir / "embedded" / "public_key.pem",
                    _backend_dir / "src" / "embedded" / "public_key.pem",
                    Path("backend/src/embedded/public_key.pem"),
                ]:
                    if candidate.exists():
                        public_key_path = candidate
                        break

                if license_path and license_path.exists() and public_key_path and public_key_path.exists():
                    validator = LicenseValidator(str(license_path), str(public_key_path))
                    license_data = validator.validate()
                    business_name = license_data.licensee
                    feature_flags = license_data.features.model_dump()
                    print(f"[+] Loaded {license_data.tier.upper()} license for: {business_name}")
                else:
                    print("[!] No license found, using Basic tier defaults")
                    business_name = "MBAS Demo Store"
                    feature_flags = get_tier_features("basic").model_dump()
            except Exception as e:
                print(f"[!] License validation failed: {e}")
                print("[!] Using Basic tier defaults")
                business_name = "MBAS Demo Store"
                feature_flags = get_tier_features("basic").model_dump()

            settings = Settings(
                id=1,
                business_name=business_name,
                tax_rate=0.0,
                feature_flags=feature_flags
            )
            session.add(settings)

        # 2. Ensure default Admin user exists
        statement = select(User).where(User.username == "admin")
        admin = session.exec(statement).first()
        if not admin:
            print("[+] Creating default administrator account...")
            admin = User(
                username="admin",
                full_name="System Administrator",
                role=UserRole.ADMIN,
                hashed_password=get_password_hash("admin123") # Default password
            )
            session.add(admin)

        session.commit()

    print("[SUCCESS] System initialized successfully.")

if __name__ == "__main__":
    bootstrap()
