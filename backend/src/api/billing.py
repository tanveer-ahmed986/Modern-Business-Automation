from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, or_, func
from sqlalchemy.orm import selectinload
from src.core.db import get_session
from src.core.auth import get_current_user
from src.models.core import User, UserRole
from src.models.sales import (
    Sale, SaleCreate, SaleRead,
    Customer, CustomerCreate, CustomerRead,
    SaleItem
)
from src.services.sale_service import SaleService
from src.core.features import check_feature

router = APIRouter(prefix="/billing", tags=["billing"])

def check_manager_role(current_user: User = Depends(get_current_user)):
    """Refunds are restricted to Managers and Administrators."""
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation restricted to Managers and Administrators"
        )
    return current_user

# --- Sales Endpoints ---

@router.post("/sales", response_model=SaleRead)
def create_sale(
    sale_in: SaleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _billing_enabled: bool = Depends(check_feature("billing"))
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

    # Materialize each row as a SaleRead instance (not raw ORM objects)
    # before returning: without a declared response_model, FastAPI's
    # jsonable_encoder serializes plain pydantic model instances correctly,
    # but round-tripping SaleRead through a generic PaginatedResponse[SaleRead]
    # response_model silently drops the items/customer relationship fields
    # (a SQLModel + pydantic-generics serialization quirk) — this sidesteps it.
    return {
        "items": [SaleRead.model_validate(s) for s in sales],
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

@router.post("/sales/{sale_id}/refund", response_model=SaleRead)
def refund_sale(
    sale_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(check_manager_role)
):
    """Refund a completed sale: restores stock (with ledger entries) and
    marks the sale REFUNDED. Manager/Admin only."""
    try:
        sale = SaleService.refund_sale(session, sale_id, current_user.id)
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
