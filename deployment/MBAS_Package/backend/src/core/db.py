from sqlmodel import create_engine, SQLModel, Session, text
import os

# Import all models to ensure they are registered with SQLModel.metadata
from src.models.core import User, Settings
from src.models.inventory import Category, Product
from src.models.sales import Customer, Sale, SaleItem
from src.models.purchases import Supplier, Purchase, PurchaseItem, SupplierPayment
from src.models.ai_analytics import AIAnalytics

# Database file path (local SQLite)
DB_FILE = "mbas_database.db"
DB_URL = f"sqlite:///{DB_FILE}"

# Create engine with check_same_thread=False for SQLite compatibility with FastAPI
engine = create_engine(
    DB_URL, 
    connect_args={"check_same_thread": False},
    echo=False # Set to True for debugging SQL queries
)

def init_db():
    """Initialize database and create tables."""
    SQLModel.metadata.create_all(engine)
    
    # Optional: Enable WAL mode for better concurrency in SQLite
    with Session(engine) as session:
        # Enable WAL mode
        session.exec(text("PRAGMA journal_mode=WAL;"))
        
        # Create FTS5 virtual table for product search
        session.exec(text("""
            CREATE VIRTUAL TABLE IF NOT EXISTS products_fts USING fts5(
                id UNINDEXED,
                name,
                barcode,
                content='products',
                content_rowid='id'
            );
        """))
        
        # Create triggers to keep products_fts in sync
        # 1. After Insert
        session.exec(text("""
            CREATE TRIGGER IF NOT EXISTS products_after_insert AFTER INSERT ON products BEGIN
                INSERT INTO products_fts(rowid, id, name, barcode) 
                VALUES (new.id, new.id, new.name, new.barcode);
            END;
        """))
        
        # 2. After Update
        session.exec(text("""
            CREATE TRIGGER IF NOT EXISTS products_after_update AFTER UPDATE ON products BEGIN
                INSERT INTO products_fts(products_fts, rowid, id, name, barcode) VALUES('delete', old.id, old.id, old.name, old.barcode);
                INSERT INTO products_fts(rowid, id, name, barcode) VALUES (new.id, new.id, new.name, new.barcode);
            END;
        """))
        
        # 3. After Delete
        session.exec(text("""
            CREATE TRIGGER IF NOT EXISTS products_after_delete AFTER DELETE ON products BEGIN
                INSERT INTO products_fts(products_fts, rowid, id, name, barcode) VALUES('delete', old.id, old.id, old.name, old.barcode);
            END;
        """))
        
        session.commit()

def get_session():
    """Dependency for FastAPI endpoints to get a DB session."""
    with Session(engine) as session:
        yield session
