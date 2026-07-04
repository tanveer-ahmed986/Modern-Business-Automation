from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload
from datetime import datetime

from src.core.db import get_session
from src.models.core import User, UserRole
from src.models.purchases import (
    Purchase, PurchaseCreate, PurchaseRead
)
from src.services.purchase_service import PurchaseService
from src.core.auth import get_current_user

router = APIRouter(prefix="/purchases", tags=["purchases"])

def check_manager_role(current_user: User = Depends(get_current_user)):
    """Dependency to ensure the current user has ADMIN or MANAGER role."""
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation restricted to Managers and Administrators"
        )
    return current_user

@router.get("")
def get_purchases(
    session: Session = Depends(get_session),
    current_user: User = Depends(check_manager_role),
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page (max 200)"),
    supplier_id: Optional[int] = None
) -> Any:
    """Retrieve all purchases with pagination and optional supplier filtering.

    Returns paginated results with metadata.
    Default: 50 items per page, sorted by most recent first.
    """
    # Build query
    statement = (
        select(Purchase)
        .options(selectinload(Purchase.items), selectinload(Purchase.supplier))
        .order_by(Purchase.created_at.desc())
    )
    count_statement = select(func.count(Purchase.id))

    if supplier_id:
        statement = statement.where(Purchase.supplier_id == supplier_id)
        count_statement = count_statement.where(Purchase.supplier_id == supplier_id)

    # Get total count
    total_count = session.exec(count_statement).one()

    # Calculate pagination
    offset = (page - 1) * page_size
    total_pages = (total_count + page_size - 1) // page_size

    # Get paginated items
    purchases = session.exec(statement.offset(offset).limit(page_size)).all()

    return {
        "items": purchases,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "total_pages": total_pages
        }
    }

@router.post("", response_model=PurchaseRead)
def create_purchase(
    *,
    session: Session = Depends(get_session),
    purchase_in: PurchaseCreate,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Create a new purchase and update stock."""
    try:
        db_purchase = PurchaseService.create_purchase(
            session=session,
            purchase_in=purchase_in,
            user_id=current_user.id
        )
        session.commit()
        session.refresh(db_purchase)
        return db_purchase
    except HTTPException as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{id}", response_model=PurchaseRead)
def get_purchase(
    *,
    session: Session = Depends(get_session),
    id: int,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Retrieve a single purchase by ID."""
    db_purchase = session.get(Purchase, id)
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase
