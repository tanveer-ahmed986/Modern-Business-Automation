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
from src.models.purchases import Purchase, PurchaseItem
from src.models.suppliers import Supplier
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

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


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
        role=UserRole.SALES_USER,
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


@pytest.fixture(name="category")
def category_fixture(session: Session):
    """Create a test category."""
    category = Category(name="Test Category", description="Test category for products")
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@pytest.fixture(name="product")
def product_fixture(session: Session, category: Category):
    """Create a test product with stock."""
    product = Product(
        name="Test Product",
        sku="TEST-001",
        barcode="1234567890",
        category_id=category.id,
        selling_price=150.0,
        cost_price=100.0,
        stock_quantity=50,
        reorder_level=10,
        unit="pcs"
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
            sku=f"SKU-{i:03d}",
            barcode=f"BAR{i:07d}",
            category_id=category.id,
            selling_price=100.0 + (i * 10),
            cost_price=50.0 + (i * 5),
            stock_quantity=100 - i,
            reorder_level=10,
            unit="pcs"
        )
        for i in range(1, 6)
    ]
    for product in products:
        session.add(product)
    session.commit()
    for product in products:
        session.refresh(product)
    return products
