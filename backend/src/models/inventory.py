from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
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
    selling_price: Decimal = Field(default=0.0)
    stock_quantity: int = Field(default=0)
    low_stock_threshold: int = Field(default=5)
    is_active: bool = Field(default=True)

class Product(ProductBase, table=True):
    __tablename__ = "products"
    id: Optional[int] = Field(default=None, primary_key=True)
    cost_price: Decimal = Field(default=0.0) # Admin/Manager only field
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    category: Optional[Category] = Relationship(back_populates="products")

class ProductCreate(ProductBase):
    cost_price: Decimal = Field(default=0.0)

class ProductRead(ProductBase):
    """Standard view for Sales users (excludes cost_price)."""
    id: int
    category: Optional[CategoryRead] = None
    created_at: datetime
    updated_at: datetime

class ProductReadAdmin(ProductRead):
    """Admin/Manager view (includes cost_price)."""
    cost_price: Decimal

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    barcode: Optional[str] = None
    cost_price: Optional[Decimal] = None
    selling_price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    is_active: Optional[bool] = None
