from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from decimal import Decimal
from enum import Enum

class PurchaseStatus(str, Enum):
    ORDERED = "ordered"
    RECEIVED = "received"
    CANCELLED = "cancelled"

class PaymentStatus(str, Enum):
    PAID = "paid"
    PARTIAL = "partial"
    UNPAID = "unpaid"

class SupplierBase(SQLModel):
    name: str = Field(index=True, unique=True)
    contact_person: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    balance: Decimal = Field(default=0.0)

class Supplier(SupplierBase, table=True):
    __tablename__ = "suppliers"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    purchases: List["Purchase"] = Relationship(back_populates="supplier")

class SupplierCreate(SupplierBase):
    pass

class SupplierRead(SupplierBase):
    id: int
    created_at: datetime

class SupplierUpdate(SQLModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    balance: Optional[Decimal] = None

class PurchaseBase(SQLModel):
    supplier_id: Optional[int] = Field(default=None, foreign_key="suppliers.id")
    user_id: int = Field(foreign_key="user.id")
    reference_number: Optional[str] = Field(default=None, index=True)
    total_amount: Decimal = Field(default=0.0)
    tax_amount: Decimal = Field(default=0.0)
    discount_amount: Decimal = Field(default=0.0)
    grand_total: Decimal = Field(default=0.0)
    paid_amount: Decimal = Field(default=0.0)
    status: PurchaseStatus = Field(default=PurchaseStatus.RECEIVED)
    payment_status: PaymentStatus = Field(default=PaymentStatus.PAID)
    notes: Optional[str] = Field(default=None)

class Purchase(PurchaseBase, table=True):
    __tablename__ = "purchases"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    supplier: Optional[Supplier] = Relationship(back_populates="purchases")
    items: List["PurchaseItem"] = Relationship(back_populates="purchase")

class PurchaseItemBase(SQLModel):
    purchase_id: Optional[int] = Field(default=None, foreign_key="purchases.id")
    product_id: Optional[int] = Field(default=None, foreign_key="products.id")
    product_name: str
    quantity: int = Field(default=1)
    cost_price: Decimal = Field(default=0.0)
    subtotal: Decimal = Field(default=0.0)

class PurchaseItem(PurchaseItemBase, table=True):
    __tablename__ = "purchase_items"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    purchase: Optional[Purchase] = Relationship(back_populates="items")

class PurchaseItemCreate(SQLModel):
    product_id: int
    quantity: int
    cost_price: Decimal

class PurchaseCreate(SQLModel):
    supplier_id: Optional[int] = None
    reference_number: Optional[str] = None
    items: List[PurchaseItemCreate]
    tax_amount: Decimal = Decimal("0.0")
    discount_amount: Decimal = Decimal("0.0")
    paid_amount: Decimal = Decimal("0.0")
    notes: Optional[str] = None

class PurchaseRead(PurchaseBase):
    id: int
    created_at: datetime
    items: List[PurchaseItem] = []
    supplier: Optional[SupplierRead] = None
