from typing import Optional
from sqlmodel import SQLModel, Field, JSON, Column
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    SALES = "sales"

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    full_name: Optional[str] = None
    role: UserRole = Field(default=UserRole.SALES)
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime

class Settings(SQLModel, table=True):
    """Core application settings for branding and tier control."""
    id: int = Field(default=1, primary_key=True)
    business_name: str = Field(default="My Business")
    business_logo_url: Optional[str] = None
    tax_rate: float = Field(default=0.0)
    currency: str = Field(default="USD")
    
    # Feature Toggles (Tier Management)
    # Stored as JSON to allow flexible toggling of Basic/Standard/Premium features
    feature_flags: dict = Field(default_factory=dict, sa_column=Column(JSON))
    
    updated_at: datetime = Field(default_factory=datetime.utcnow)
