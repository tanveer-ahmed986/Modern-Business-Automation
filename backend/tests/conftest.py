"""
Pytest configuration and shared fixtures for MBAS tests.
"""

import sys
from pathlib import Path
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient

# Add backend/src to path for imports
backend_src = Path(__file__).parent.parent / "src"
if str(backend_src) not in sys.path:
    sys.path.insert(0, str(backend_src))

from src.main import app
from src.core.db import get_session
from src.models.core import User, UserRole, Settings
from src.models.inventory import Product, Category
from src.models.sales import Sale, SaleItem
from src.models.purchases import Purchase, PurchaseItem, Supplier
from src.core.security import get_password_hash


@pytest.fixture(name="engine")
def engine_fixture():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="file_engine")
def file_engine_fixture(tmp_path):
    """File-based SQLite engine with WAL + busy_timeout, mirroring production.

    Required for concurrency/isolation tests: the in-memory StaticPool engine
    shares ONE connection across threads, which hides real locking behavior.
    """
    from sqlalchemy import event

    db_path = tmp_path / "test_mbas.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False, "timeout": 5.0},
    )

    @event.listens_for(engine, "connect")
    def _set_pragmas(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA busy_timeout=5000;")
        cursor.close()

    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(name="session")
def session_fixture(engine):
    """Create a database session for testing."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a FastAPI test client with database session override."""
    def get_session_override():
        return session

    # Reset the dashboard's module-level metrics cache so results from one
    # test's database never leak into another test within the cache TTL.
    from src.api import dashboard as dashboard_module
    dashboard_module._metrics_cache.update({"data": None, "ts": 0.0, "date": ""})
    dashboard_module._trends_cache.update({"data": None, "ts": 0.0, "date": ""})

    # Reset the login rate-limiter and the user-identity cache: both are
    # module-level and otherwise leak failed-attempt counts / stale user
    # objects across tests that reuse the same usernames (e.g. "testadmin").
    from src.api import auth as auth_api_module
    from src.core import auth as auth_core_module
    auth_api_module._failed_attempts.clear()
    with auth_core_module._user_cache_lock:
        auth_core_module._user_cache.clear()

    # Reset the license validator singleton so one test's simulated license
    # (see the `premium_license` fixture) never leaks into the next test.
    from src.core import license as license_module
    license_module._license_validator = None

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
    license_module._license_validator = None


@pytest.fixture(name="settings")
def settings_fixture(session: Session):
    """Create default system settings."""
    settings = Settings(
        id=1,
        business_name="Test Store",
        tax_rate=15.0,
        currency="USD",
        feature_flags={
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
            "ai_forecasting": True,
        }
    )
    session.add(settings)
    session.commit()
    session.refresh(settings)
    return settings


@pytest.fixture(name="admin_user")
def admin_user_fixture(session: Session):
    """Create an admin user for testing."""
    user = User(
        username="testadmin",
        full_name="Test Administrator",
        role=UserRole.ADMIN,
        hashed_password=get_password_hash("testpass123")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="manager_user")
def manager_user_fixture(session: Session):
    """Create a manager user for testing."""
    user = User(
        username="testmanager",
        full_name="Test Manager",
        role=UserRole.MANAGER,
        hashed_password=get_password_hash("testpass123")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="sales_user")
def sales_user_fixture(session: Session):
    """Create a sales user for testing."""
    user = User(
        username="testsales",
        full_name="Test Sales User",
        role=UserRole.SALES,
        hashed_password=get_password_hash("testpass123")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(client: TestClient, admin_user: User):
    """Get authentication headers for admin user."""
    response = client.post(
        "/auth/login",
        data={"username": "testadmin", "password": "testpass123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class _FakeLicenseInfo:
    """Minimal duck-typed stand-in for LicenseData — avoids needing a real
    RSA-signed fixture file just to simulate 'a premium license is active'
    for tests of the license-derived feature gate (core/features.py)."""
    def __init__(self, features, expiry_date=None):
        self.features = features
        self.expiry_date = expiry_date


class _FakeLicenseValidator:
    def __init__(self, info: _FakeLicenseInfo):
        self._info = info

    def get_license_info(self):
        return self._info


@pytest.fixture
def premium_license():
    """Simulate an active, valid premium license for the duration of a test."""
    from src.core import license as license_module
    from src.models.license import get_tier_features

    validator = _FakeLicenseValidator(_FakeLicenseInfo(get_tier_features("premium")))
    license_module.set_license_validator(validator)
    yield validator
    license_module.set_license_validator(None)


@pytest.fixture(name="category")
def category_fixture(session: Session):
    """Create a test category."""
    category = Category(name="Test Category")
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@pytest.fixture(name="product")
def product_fixture(session: Session, category: Category):
    """Create a test product with stock."""
    product = Product(
        name="Test Product",
        barcode="1234567890",
        category_id=category.id,
        selling_price=150.0,
        cost_price=100.0,
        stock_quantity=50,
        low_stock_threshold=10
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@pytest.fixture(name="supplier")
def supplier_fixture(session: Session):
    """Create a test supplier."""
    supplier = Supplier(
        name="Test Supplier",
        contact_person="John Doe",
        email="supplier@example.com",
        phone="123-456-7890",
        address="123 Supplier St"
    )
    session.add(supplier)
    session.commit()
    session.refresh(supplier)
    return supplier


@pytest.fixture
def sample_products(session: Session, category: Category):
    """Create multiple products for testing."""
    products = [
        Product(
            name=f"Product {i}",
            barcode=f"BAR{i:07d}",
            category_id=category.id,
            selling_price=100.0 + (i * 10),
            cost_price=50.0 + (i * 5),
            stock_quantity=100 - i,
            low_stock_threshold=10
        )
        for i in range(1, 6)
    ]
    for product in products:
        session.add(product)
    session.commit()
    for product in products:
        session.refresh(product)
    return products
