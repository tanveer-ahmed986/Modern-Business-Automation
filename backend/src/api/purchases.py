from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

from backend.src.core.db import get_session
from backend.src.models.core import User, UserRole
from backend.src.models.purchases import (
    Purchase, PurchaseCreate, PurchaseRead
)
from backend.src.services.purchase_service import PurchaseService
from backend.src.core.auth import get_current_user

router = APIRouter(prefix="/purchases", tags=["purchases"])

def check_manager_role(current_user: User = Depends(get_current_user)):
    """Dependency to ensure the current user has ADMIN or MANAGER role."""
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation restricted to Managers and Administrators"
        )
    return current_user

@router.get("", response_model=List[PurchaseRead])
def get_purchases(
    session: Session = Depends(get_session),
    current_user: User = Depends(check_manager_role),
    supplier_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Retrieve all purchases with optional supplier filtering."""
    statement = select(Purchase)
    if supplier_id:
        statement = statement.where(Purchase.supplier_id == supplier_id)
    
    return session.exec(statement.offset(skip).limit(limit)).all()

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
