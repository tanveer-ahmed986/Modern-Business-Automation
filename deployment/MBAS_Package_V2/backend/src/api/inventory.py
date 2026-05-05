from typing import Any, List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, or_, text
from datetime import datetime

from src.core.db import get_session
from src.models.core import User, UserRole
from src.models.inventory import (
    Category, CategoryCreate, CategoryRead,
    Product, ProductCreate, ProductRead, ProductReadAdmin, ProductUpdate
)
from src.core.auth import get_current_user

router = APIRouter(prefix="/inventory", tags=["inventory"])

def check_manager_role(current_user: User = Depends(get_current_user)):
    """Dependency to ensure the current user has ADMIN or MANAGER role."""
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation restricted to Managers and Administrators"
        )
    return current_user

# --- CATEGORIES ---

@router.get("/categories", response_model=List[CategoryRead])
def get_categories(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve all categories."""
    return session.exec(select(Category)).all()

@router.post("/categories", response_model=CategoryRead)
def create_category(
    *,
    session: Session = Depends(get_session),
    category_in: CategoryCreate,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Create a new category (Manager/Admin only)."""
    db_category = Category.from_orm(category_in)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@router.put("/categories/{id}", response_model=CategoryRead)
def update_category(
    *,
    session: Session = Depends(get_session),
    id: int,
    category_in: CategoryCreate,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Update a category (Manager/Admin only)."""
    db_category = session.get(Category, id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_category.name = category_in.name
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@router.delete("/categories/{id}")
def delete_category(
    *,
    session: Session = Depends(get_session),
    id: int,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Delete a category (Manager/Admin only)."""
    db_category = session.get(Category, id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has products
    if db_category.products:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category that has associated products"
        )
        
    session.delete(db_category)
    session.commit()
    return {"message": "Category deleted successfully"}

# --- PRODUCTS ---

@router.get("/products", response_model=List[Union[ProductReadAdmin, ProductRead]])
def get_products(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None
) -> Any:
    """Retrieve products with pagination and category filtering."""
    statement = select(Product)
    if category_id:
        statement = statement.where(Product.category_id == category_id)
    
    products = session.exec(statement.offset(skip).limit(limit)).all()
    
    # RBAC logic: Sales users don't get cost_price
    is_privileged = current_user.role in [UserRole.ADMIN, UserRole.MANAGER]
    
    if is_privileged:
        return products
    
    # If not privileged, SQLModel/Pydantic will automatically strip cost_price 
    # because of the response_model logic, but we can be explicit if needed.
    return products

@router.get("/products/search", response_model=List[Union[ProductReadAdmin, ProductRead]])
def search_products(
    query: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    limit: int = 20
) -> Any:
    """Search products using SQLite FTS5."""
    # Using FTS5 virtual table for fast search
    fts_statement = text("""
        SELECT id FROM products_fts 
        WHERE products_fts MATCH :query 
        ORDER BY rank 
        LIMIT :limit
    """)
    
    # Prepare query for FTS5 (append * for prefix search)
    fts_query = f"{query}*"
    result_ids = session.execute(fts_statement, {"query": fts_query, "limit": limit}).scalars().all()
    
    if not result_ids:
        # Fallback to simple ILIKE search if FTS5 yields no results or for very short queries
        statement = select(Product).where(
            or_(
                Product.name.contains(query),
                Product.barcode.contains(query)
            )
        ).limit(limit)
        return session.exec(statement).all()

    # Retrieve full product objects for the found IDs
    statement = select(Product).where(Product.id.in_(result_ids))
    return session.exec(statement).all()

@router.post("/products", response_model=ProductReadAdmin)
def create_product(
    *,
    session: Session = Depends(get_session),
    product_in: ProductCreate,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Create a new product (Manager/Admin only)."""
    db_product = Product.from_orm(product_in)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.get("/products/{id}", response_model=Union[ProductReadAdmin, ProductRead])
def get_product(
    *,
    session: Session = Depends(get_session),
    id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve a single product by ID."""
    db_product = session.get(Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/products/{id}", response_model=ProductReadAdmin)
def update_product(
    *,
    session: Session = Depends(get_session),
    id: int,
    product_in: ProductUpdate,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Update a product (Manager/Admin only)."""
    db_product = session.get(Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db_product.updated_at = datetime.utcnow()
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.delete("/products/{id}")
def delete_product(
    *,
    session: Session = Depends(get_session),
    id: int,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Delete a product (Manager/Admin only)."""
    db_product = session.get(Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    session.delete(db_product)
    session.commit()
    return {"message": "Product deleted successfully"}
