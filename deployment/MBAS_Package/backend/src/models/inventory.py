from typing import Optional, List, Any
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from pydantic import field_validator
from decimal import Decimal

class CategoryBase(SQLModel):
    name: str = Field(index=True, unique=True)

class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    products: List["Product"] = Relationship(back_populates="category")

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int

class ProductBase(SQLModel):
    name: str = Field(index=True)
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    barcode: str = Field(index=True, unique=True)
    selling_price: float = Field(default=0.0)  # Changed from Decimal to float
    stock_quantity: int = Field(default=0)
    low_stock_threshold: int = Field(default=5)
    is_active: bool = Field(default=True)

class Product(ProductBase, table=True):
    __tablename__ = "products"
    id: Optional[int] = Field(default=None, primary_key=True)
    cost_price: float = Field(default=0.0)  # Changed from Decimal to float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    category: Optional[Category] = Relationship(back_populates="products")

    @field_validator('selling_price', 'cost_price', mode='before')
    @classmethod
    def convert_decimal_to_float(cls, v: Any) -> float:
        """Convert Decimal values from database to float."""
        if isinstance(v, Decimal):
            return float(v)
        return float(v) if v is not None else 0.0

class ProductCreate(ProductBase):
    cost_price: float = Field(default=0.0)

class ProductRead(SQLModel):
    """Standard view for Sales users (excludes cost_price)."""
    id: int
    name: str
    category_id: Optional[int] = None
    barcode: str
    selling_price: float
    stock_quantity: int
    low_stock_threshold: int
    is_active: bool
    category: Optional[CategoryRead] = None
    created_at: datetime
    updated_at: datetime

class ProductReadAdmin(ProductRead):
    """Admin/Manager view (includes cost_price)."""
    cost_price: float

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    barcode: Optional[str] = None
    cost_price: Optional[float] = None
    selling_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    is_active: Optional[bool] = None
