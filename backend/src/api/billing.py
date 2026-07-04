from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, or_, func
from sqlalchemy.orm import selectinload
from src.core.db import get_session
from src.core.auth import get_current_user
from src.models.core import User
from src.models.sales import (
    Sale, SaleCreate, SaleRead,
    Customer, CustomerCreate, CustomerRead,
    SaleItem
)
from src.services.sale_service import SaleService

router = APIRouter(prefix="/billing", tags=["billing"])

# --- Sales Endpoints ---

@router.post("/sales", response_model=SaleRead)
def create_sale(
    sale_in: SaleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Process a new sale and deduct stock."""
    try:
        sale = SaleService.create_sale(session, sale_in, current_user.id)
        session.commit()
        session.refresh(sale)
        return sale
    except HTTPException as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/sales")
def list_sales(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page (max 200)"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all sales with pagination.

    Returns paginated results with metadata.
    Default: 50 items per page, sorted by most recent first.
    """
    # Count total sales
    total_count = session.exec(select(func.count(Sale.id))).one()

    # Calculate pagination
    offset = (page - 1) * page_size
    total_pages = (total_count + page_size - 1) // page_size

    # Get paginated sales
    statement = (
        select(Sale)
        .options(selectinload(Sale.items), selectinload(Sale.customer))
        .order_by(Sale.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    sales = session.exec(statement).all()

    return {
        "items": sales,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "total_pages": total_pages
        }
    }

@router.get("/sales/{sale_id}", response_model=SaleRead)
def get_sale(
    sale_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get details of a specific sale including items."""
    sale = session.get(Sale, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    return sale

# --- Customer Endpoints ---

@router.post("/customers", response_model=CustomerRead)
def create_customer(
    customer_in: CustomerCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new customer."""
    db_customer = Customer.from_orm(customer_in)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer

@router.get("/customers", response_model=List[CustomerRead])
def list_customers(
    search: Optional[str] = None,
    limit: int = Query(default=200, le=500),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List customers with optional search by name or phone."""
    statement = select(Customer)
    if search:
        statement = statement.where(
            or_(
                Customer.name.contains(search),
                Customer.phone.contains(search)
            )
        )
    customers = session.exec(statement.limit(limit)).all()
    return customers
