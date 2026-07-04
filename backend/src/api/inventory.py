from typing import Any, List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, or_, text, col, func
from sqlalchemy.orm import selectinload
from datetime import datetime

from src.core.db import get_session
from src.models.core import User, UserRole
from src.models.inventory import (
    Category, CategoryCreate, CategoryRead,
    Product, ProductCreate, ProductRead, ProductReadAdmin, ProductUpdate,
    PaginationMeta
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
    
    # Check if category has products (count query avoids loading all products)
    product_count = session.exec(
        select(func.count(Product.id)).where(Product.category_id == id)
    ).one()
    if product_count > 0:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category that has associated products"
        )
        
    session.delete(db_category)
    session.commit()
    return {"message": "Category deleted successfully"}

# --- PRODUCTS ---

@router.get("/products")
def get_products(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page (max 200)"),
    category_id: Optional[int] = None
) -> Any:
    """Retrieve products with pagination and category filtering.

    Returns paginated results with metadata.
    Default: 50 items per page.
    """
    # Build base query
    statement = select(Product).options(selectinload(Product.category))
    count_statement = select(func.count(Product.id))

    if category_id:
        statement = statement.where(Product.category_id == category_id)
        count_statement = count_statement.where(Product.category_id == category_id)

    # Get total count
    total_count = session.exec(count_statement).one()

    # Calculate pagination
    offset = (page - 1) * page_size
    total_pages = (total_count + page_size - 1) // page_size

    # Get paginated items
    products = session.exec(statement.offset(offset).limit(page_size)).all()

    return {
        "items": products,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "total_pages": total_pages
        }
    }

@router.get("/products/search")
def search_products(
    query: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page (max 100)")
) -> Any:
    """Search products using SQLite FTS5 with LIKE fallback.

    Returns paginated search results with metadata.
    """
    if not query or not query.strip():
        return {
            "items": [],
            "pagination": {
                "page": 1,
                "page_size": page_size,
                "total_count": 0,
                "total_pages": 0
            }
        }

    query = query.strip()

    # First try exact barcode match (fastest path for barcode scanners)
    exact_match = session.exec(
        select(Product).options(selectinload(Product.category)).where(Product.barcode == query)
    ).first()
    if exact_match:
        return {
            "items": [exact_match],
            "pagination": {
                "page": 1,
                "page_size": page_size,
                "total_count": 1,
                "total_pages": 1
            }
        }

    # Try FTS5 for text search (only for alphanumeric queries without special chars)
    fts_safe = query.replace('"', '').replace("'", "").replace('-', ' ')
    result_ids = []
    if fts_safe.strip():
        try:
            # Get all matching IDs first (for count)
            fts_statement = text("""
                SELECT id FROM products_fts
                WHERE products_fts MATCH :query
                ORDER BY rank
            """)
            fts_query = f'"{fts_safe}"*'
            all_ids = session.execute(
                fts_statement, {"query": fts_query}
            ).scalars().all()

            if all_ids:
                result_ids = all_ids
        except Exception:
            # FTS5 can fail on certain query patterns, fall through to LIKE
            result_ids = []

    if result_ids:
        total_count = len(result_ids)
        offset = (page - 1) * page_size
        total_pages = (total_count + page_size - 1) // page_size

        # Paginate the IDs
        paginated_ids = result_ids[offset:offset + page_size]

        statement = select(Product).options(selectinload(Product.category)).where(Product.id.in_(paginated_ids))
        items = session.exec(statement).all()

        return {
            "items": items,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": total_pages
            }
        }

    # Fallback to LIKE search (handles barcodes with special chars, partial matches)
    like_statement = select(Product).options(selectinload(Product.category)).where(
        or_(
            Product.name.contains(query),
            Product.barcode.contains(query)
        )
    )

    # Count total matches
    count_statement = select(func.count(Product.id)).where(
        or_(
            Product.name.contains(query),
            Product.barcode.contains(query)
        )
    )
    total_count = session.exec(count_statement).one()

    # Paginate
    offset = (page - 1) * page_size
    total_pages = (total_count + page_size - 1) // page_size
    items = session.exec(like_statement.offset(offset).limit(page_size)).all()

    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "total_pages": total_pages
        }
    }

@router.post("/products", response_model=ProductReadAdmin)
def create_product(
    *,
    session: Session = Depends(get_session),
    product_in: ProductCreate,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Create a new product (Manager/Admin only)."""
    # Check for duplicate product name (count avoids loading full row)
    existing = session.exec(
        select(func.count(Product.id)).where(Product.name == product_in.name)
    ).one()
    if existing > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A product with the name '{product_in.name}' already exists"
        )

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

    # Check for duplicate product name on update (count avoids loading full row)
    if "name" in update_data and update_data["name"] != db_product.name:
        existing = session.exec(
            select(func.count(Product.id)).where(Product.name == update_data["name"])
        ).one()
        if existing > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A product with the name '{update_data['name']}' already exists"
            )

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
