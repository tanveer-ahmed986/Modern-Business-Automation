from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

from backend.src.core.db import get_session
from backend.src.models.core import User, UserRole
from backend.src.models.purchases import (
    Supplier, SupplierCreate, SupplierRead, SupplierUpdate
)
from backend.src.core.auth import get_current_user

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

def check_manager_role(current_user: User = Depends(get_current_user)):
    """Dependency to ensure the current user has ADMIN or MANAGER role."""
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation restricted to Managers and Administrators"
        )
    return current_user

@router.get("", response_model=List[SupplierRead])
def get_suppliers(
    session: Session = Depends(get_session),
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Retrieve all suppliers."""
    return session.exec(select(Supplier)).all()

@router.post("", response_model=SupplierRead)
def create_supplier(
    *,
    session: Session = Depends(get_session),
    supplier_in: SupplierCreate,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Create a new supplier."""
    db_supplier = Supplier.from_orm(supplier_in)
    session.add(db_supplier)
    session.commit()
    session.refresh(db_supplier)
    return db_supplier

@router.get("/{id}", response_model=SupplierRead)
def get_supplier(
    *,
    session: Session = Depends(get_session),
    id: int,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Retrieve a single supplier by ID."""
    db_supplier = session.get(Supplier, id)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

@router.put("/{id}", response_model=SupplierRead)
def update_supplier(
    *,
    session: Session = Depends(get_session),
    id: int,
    supplier_in: SupplierUpdate,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Update a supplier."""
    db_supplier = session.get(Supplier, id)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    update_data = supplier_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_supplier, key, value)
    
    session.add(db_supplier)
    session.commit()
    session.refresh(db_supplier)
    return db_supplier

@router.delete("/{id}")
def delete_supplier(
    *,
    session: Session = Depends(get_session),
    id: int,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Delete a supplier."""
    db_supplier = session.get(Supplier, id)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
        
    # Check if supplier has purchases
    if db_supplier.purchases:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete supplier that has associated purchases"
        )
        
    session.delete(db_supplier)
    session.commit()
    return {"message": "Supplier deleted successfully"}
