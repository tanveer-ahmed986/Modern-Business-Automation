from sqlmodel import create_engine, SQLModel, Session, text
from sqlalchemy import event
from sqlalchemy.pool import QueuePool
import os
from pathlib import Path

# Import all models to ensure they are registered with SQLModel.metadata
from src.models.core import User, Settings
from src.models.inventory import Category, Product
from src.models.sales import Customer, Sale, SaleItem
from src.models.purchases import Supplier, Purchase, PurchaseItem, SupplierPayment
from src.models.ai_analytics import AIAnalytics
from src.models.stock import StockMovement, InvoiceSequence

# Database file path - use ProgramData on Windows to avoid Program Files write restrictions
_DATA_DIR = Path(os.environ.get("MBAS_DATA_DIR", ""))
if not _DATA_DIR or not _DATA_DIR.is_absolute():
    _DATA_DIR = Path(os.environ.get("ProgramData", "C:\\ProgramData")) / "MBAS" / "data"

_DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_FILE = str(_DATA_DIR / "mbas_database.db")
DB_URL = f"sqlite:///{DB_FILE}"

# ---------------------------------------------------------------------------
# Connection pool strategy: QueuePool(5+5) with WAL concurrency
# ---------------------------------------------------------------------------
# WAL mode allows any number of concurrent readers plus one writer, so a
# pool of persistent connections is safe and keeps SQLite's page cache warm.
#
# The previous pool_size=1 + max_overflow=2 capped the app at 3 concurrent
# queries. A page navigation fires 2-4 parallel GETs (plus service-worker
# revalidations before the SW fix), so the 4th query waited pool_timeout
# seconds and then failed with a 500 — the axios retry/backoff on top of
# that is what users experienced as a multi-second "hang" on tab switches.
#
# Write serialization is handled where it belongs: SQLite's own write lock
# with busy_timeout=5000 queues concurrent writers instead of erroring.
# ---------------------------------------------------------------------------
engine = create_engine(
    DB_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 5.0,              # DBAPI-level lock wait (matches busy_timeout)
    },
    poolclass=QueuePool,
    pool_size=5,                     # Persistent connections (warm page cache, parallel reads)
    max_overflow=5,                  # Up to 10 total under burst
    pool_timeout=10,                 # Wait max 10s for a connection
    pool_pre_ping=True,              # Verify connection is alive before checkout
    pool_recycle=3600,               # Recycle every 60 minutes
    echo=False,
)

@event.listens_for(engine, "connect")
def _set_sqlite_pragmas(dbapi_conn, connection_record):
    """Apply performance PRAGMAs once per pooled connection (NOT per request).
    The persistent pool connection keeps these settings and its page cache alive."""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.execute("PRAGMA cache_size=-65536;")        # 64 MB page cache (stays warm in pool)
    cursor.execute("PRAGMA temp_store=MEMORY;")
    cursor.execute("PRAGMA mmap_size=67108864;")        # 64 MB memory-mapped I/O
    cursor.execute("PRAGMA busy_timeout=5000;")         # Queue concurrent writers (WAL single-writer)
    cursor.execute("PRAGMA wal_autocheckpoint=1000;")   # Checkpoint every 1000 pages
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

def _ensure_column(session: Session, table: str, column: str, ddl_type: str, default_sql: str) -> None:
    """Additively add a column to an existing table if missing.

    SQLModel.metadata.create_all() only creates missing TABLES, not missing
    COLUMNS on tables that already exist in a customer's deployed database.
    Alembic adoption is deferred to Phase 5, so new columns on existing
    tables are migrated here with a plain idempotent ALTER TABLE.
    """
    existing = {row[1] for row in session.exec(text(f"PRAGMA table_info({table});")).all()}
    if column not in existing:
        session.exec(text(f"ALTER TABLE {table} ADD COLUMN {column} {ddl_type} DEFAULT {default_sql};"))

def init_db():
    """Initialize database and create tables."""
    SQLModel.metadata.create_all(engine)

    # Additive column migrations for existing databases (new tables are
    # handled by create_all above; this covers new columns on old tables).
    with Session(engine) as session:
        _ensure_column(session, "user", "must_change_password", "BOOLEAN", "0")
        session.commit()

    # Ensure critical performance indexes exist on existing databases.
    # CREATE INDEX IF NOT EXISTS is safe to run on every startup.
    with Session(engine) as session:
        _indexes = [
            "CREATE INDEX IF NOT EXISTS ix_sales_created_at ON sales(created_at);",
            "CREATE INDEX IF NOT EXISTS ix_sales_status ON sales(status);",
            # Compound index for dashboard queries that filter by date + status
            "CREATE INDEX IF NOT EXISTS ix_sales_created_status ON sales(created_at, status);",
            "CREATE INDEX IF NOT EXISTS ix_sale_items_sale_id ON sale_items(sale_id);",
            "CREATE INDEX IF NOT EXISTS ix_sale_items_product_id ON sale_items(product_id);",
            "CREATE INDEX IF NOT EXISTS ix_purchases_supplier_id ON purchases(supplier_id);",
            "CREATE INDEX IF NOT EXISTS ix_purchases_created_at ON purchases(created_at);",
            "CREATE INDEX IF NOT EXISTS ix_supplier_payments_supplier_id ON supplier_payments(supplier_id);",
            "CREATE INDEX IF NOT EXISTS ix_products_is_active ON products(is_active);",
            # Foreign key indexes for JOIN performance
            "CREATE INDEX IF NOT EXISTS ix_sales_customer_id ON sales(customer_id);",
            "CREATE INDEX IF NOT EXISTS ix_sales_user_id ON sales(user_id);",
            "CREATE INDEX IF NOT EXISTS ix_purchases_user_id ON purchases(user_id);",
            "CREATE INDEX IF NOT EXISTS ix_purchase_items_purchase_id ON purchase_items(purchase_id);",
            "CREATE INDEX IF NOT EXISTS ix_purchase_items_product_id ON purchase_items(product_id);",
            # Product name index for duplicate checks
            "CREATE INDEX IF NOT EXISTS ix_products_name ON products(name);",
            # Product barcode index for exact-match search
            "CREATE INDEX IF NOT EXISTS ix_products_barcode ON products(barcode);",
            # Stock ledger: per-product history queries sorted by time
            "CREATE INDEX IF NOT EXISTS ix_stock_movements_product_created ON stock_movements(product_id, created_at);",
        ]
        for idx_sql in _indexes:
            session.exec(text(idx_sql))
        session.commit()

    # PRAGMAs are applied automatically via the connect event.
    with Session(engine) as session:
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
        session.exec(text("""
            CREATE TRIGGER IF NOT EXISTS products_after_insert AFTER INSERT ON products BEGIN
                INSERT INTO products_fts(rowid, id, name, barcode)
                VALUES (new.id, new.id, new.name, new.barcode);
            END;
        """))
        session.exec(text("""
            CREATE TRIGGER IF NOT EXISTS products_after_update AFTER UPDATE ON products BEGIN
                INSERT INTO products_fts(products_fts, rowid, id, name, barcode) VALUES('delete', old.id, old.id, old.name, old.barcode);
                INSERT INTO products_fts(rowid, id, name, barcode) VALUES (new.id, new.id, new.name, new.barcode);
            END;
        """))
        session.exec(text("""
            CREATE TRIGGER IF NOT EXISTS products_after_delete AFTER DELETE ON products BEGIN
                INSERT INTO products_fts(products_fts, rowid, id, name, barcode) VALUES('delete', old.id, old.id, old.name, old.barcode);
            END;
        """))

        session.commit()

def get_session():
    """Dependency for FastAPI endpoints to get a DB session."""
    session = Session(engine, expire_on_commit=False)
    try:
        yield session
    finally:
        session.close()

def cleanup_connections():
    """Cleanup database connections and dispose of the connection pool."""
    engine.dispose()
