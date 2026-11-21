from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum


class StockMovementReason(str, Enum):
    SALE = "sale"              # stock out via a completed sale
    REFUND = "refund"          # stock back in via a refunded sale
    PURCHASE = "purchase"      # stock in via a received purchase
    ADJUSTMENT = "adjustment"  # manual correction by Admin/Manager
    INITIAL = "initial"        # opening stock when the product is created


class StockMovement(SQLModel, table=True):
    """Append-only audit ledger: one row per stock quantity change.

    `change` is signed (+in / -out); `quantity_after` snapshots the product's
    stock level after the change so history is reconstructable even if rows
    are filtered.
    """
    __tablename__ = "stock_movements"

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id", index=True)
    change: int                       # signed quantity delta
    quantity_after: int               # stock level after applying the change
    reason: StockMovementReason = Field(index=True)
    reference_type: Optional[str] = Field(default=None)   # e.g. "sale", "purchase"
    reference_id: Optional[int] = Field(default=None)     # id of the sale/purchase
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    note: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class StockMovementRead(SQLModel):
    id: int
    product_id: int
    change: int
    quantity_after: int
    reason: StockMovementReason
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    user_id: Optional[int] = None
    note: Optional[str] = None
    created_at: datetime


class InvoiceSequence(SQLModel, table=True):
    """Per-local-day invoice counter.

    Incremented inside the same transaction as the Sale insert, so SQLite's
    single-writer lock serializes concurrent sales and numbers can never
    collide (the old implementation counted existing rows, which raced).
    """
    __tablename__ = "invoice_sequences"

    date_key: str = Field(primary_key=True)  # business-local YYYYMMDD
    next_seq: int = Field(default=1)
