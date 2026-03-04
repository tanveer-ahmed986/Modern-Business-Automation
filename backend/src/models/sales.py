from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from decimal import Decimal
from enum import Enum

class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    TRANSFER = "transfer"
    CREDIT = "credit"

class SaleStatus(str, Enum):
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class CustomerBase(SQLModel):
    name: str = Field(index=True)
    phone: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)

class Customer(CustomerBase, table=True):
    __tablename__ = "customers"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    sales: List["Sale"] = Relationship(back_populates="customer")

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    created_at: datetime

class SaleBase(SQLModel):
    customer_id: Optional[int] = Field(default=None, foreign_key="customers.id")
    user_id: int = Field(foreign_key="user.id") # Link to the User who made the sale
    total_amount: Decimal = Field(default=0.0)
    tax_amount: Decimal = Field(default=0.0)
    discount_amount: Decimal = Field(default=0.0)
    grand_total: Decimal = Field(default=0.0)
    payment_method: PaymentMethod = Field(default=PaymentMethod.CASH)
    status: SaleStatus = Field(default=SaleStatus.COMPLETED)

class Sale(SaleBase, table=True):
    __tablename__ = "sales"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    customer: Optional[Customer] = Relationship(back_populates="sales")
    items: List["SaleItem"] = Relationship(back_populates="sale")

class SaleItemBase(SQLModel):
    sale_id: Optional[int] = Field(default=None, foreign_key="sales.id")
    product_id: Optional[int] = Field(default=None, foreign_key="products.id")
    product_name: str # Snapshot for historical data
    quantity: int = Field(default=1)
    unit_price: Decimal = Field(default=0.0) # Snapshot
    subtotal: Decimal = Field(default=0.0)

class SaleItem(SaleItemBase, table=True):
    __tablename__ = "sale_items"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    sale: Optional[Sale] = Relationship(back_populates="items")
    # We don't necessarily need a Relationship back to Product if we want to avoid complex circular imports,
    # but for SaleItem -> Product it might be useful.
    # product: Optional["Product"] = Relationship()

class SaleItemCreate(SQLModel):
    product_id: int
    quantity: int

class SaleCreate(SQLModel):
    customer_id: Optional[int] = None
    items: List[SaleItemCreate]
    payment_method: PaymentMethod = PaymentMethod.CASH
    discount_amount: Decimal = Decimal("0.0")

class SaleRead(SaleBase):
    id: int
    created_at: datetime
    items: List[SaleItem] = []
    customer: Optional[CustomerRead] = None
