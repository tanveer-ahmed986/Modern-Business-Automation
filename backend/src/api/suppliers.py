from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from decimal import Decimal

from src.core.db import get_session
from src.models.core import User, UserRole
from src.models.purchases import (
    Supplier, SupplierCreate, SupplierRead, SupplierUpdate,
    SupplierPayment, SupplierPaymentCreate, SupplierPaymentRead,
    Purchase
)
from src.core.auth import get_current_user

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
    
    update_data = supplier_in.model_dump(exclude_unset=True)
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
        
    # Check if supplier has purchases (count query avoids loading all purchases)
    purchase_count = session.exec(
        select(func.count(Purchase.id)).where(Purchase.supplier_id == id)
    ).one()
    if purchase_count > 0:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete supplier that has associated purchases"
        )
        
    session.delete(db_supplier)
    session.commit()
    return {"message": "Supplier deleted successfully"}


# --- SUPPLIER PAYMENTS ---

@router.get("/{id}/payments", response_model=List[SupplierPaymentRead])
def get_supplier_payments(
    *,
    session: Session = Depends(get_session),
    id: int,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Retrieve all payments made to a supplier."""
    db_supplier = session.get(Supplier, id)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    payments = session.exec(
        select(SupplierPayment)
        .where(SupplierPayment.supplier_id == id)
        .order_by(SupplierPayment.payment_date.desc())
    ).all()
    return payments


@router.post("/{id}/payments", response_model=SupplierPaymentRead)
def record_supplier_payment(
    *,
    session: Session = Depends(get_session),
    id: int,
    payment_in: SupplierPaymentCreate,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Record a payment to a supplier and reduce their outstanding balance."""
    db_supplier = session.get(Supplier, id)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    if payment_in.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment amount must be greater than zero"
        )

    # Record the payment
    db_payment = SupplierPayment(
        supplier_id=id,
        amount=payment_in.amount,
        payment_method=payment_in.payment_method,
        reference_number=payment_in.reference_number,
        notes=payment_in.notes
    )
    session.add(db_payment)

    # Reduce supplier balance
    db_supplier.balance = max(Decimal("0"), Decimal(str(db_supplier.balance)) - Decimal(str(payment_in.amount)))
    session.add(db_supplier)

    session.commit()
    session.refresh(db_payment)
    return db_payment


@router.get("/{id}/ledger")
def get_supplier_ledger(
    *,
    session: Session = Depends(get_session),
    id: int,
    current_user: User = Depends(check_manager_role)
) -> Any:
    """Get full supplier ledger: purchases, payments, and balance summary."""
    db_supplier = session.get(Supplier, id)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    # SQL-level aggregation for totals (replaces Python sum loops)
    purchase_totals = session.execute(
        select(
            func.coalesce(func.sum(Purchase.grand_total), 0),
            func.coalesce(func.sum(Purchase.paid_amount), 0)
        ).where(Purchase.supplier_id == id)
    ).one()
    total_purchased = float(purchase_totals[0])
    total_paid_on_purchases = float(purchase_totals[1])

    payment_total = session.execute(
        select(func.coalesce(func.sum(SupplierPayment.amount), 0))
        .where(SupplierPayment.supplier_id == id)
    ).scalar()
    total_payments = float(payment_total)

    total_paid = total_paid_on_purchases + total_payments
    outstanding_balance = float(db_supplier.balance)

    # Fetch recent purchases (limited to 50 for performance)
    purchases = session.exec(
        select(Purchase)
        .where(Purchase.supplier_id == id)
        .order_by(Purchase.created_at.desc())
        .limit(50)
    ).all()

    # Fetch recent payments (limited to 50 for performance)
    payments = session.exec(
        select(SupplierPayment)
        .where(SupplierPayment.supplier_id == id)
        .order_by(SupplierPayment.payment_date.desc())
        .limit(50)
    ).all()

    return {
        "supplier": {
            "id": db_supplier.id,
            "name": db_supplier.name,
            "balance": outstanding_balance
        },
        "summary": {
            "total_purchased": round(total_purchased, 2),
            "total_paid": round(total_paid, 2),
            "outstanding_balance": round(outstanding_balance, 2)
        },
        "purchases": [
            {
                "id": p.id,
                "reference_number": p.reference_number,
                "grand_total": float(p.grand_total),
                "paid_amount": float(p.paid_amount),
                "payment_status": p.payment_status,
                "created_at": p.created_at.isoformat()
            }
            for p in purchases
        ],
        "payments": [
            {
                "id": pay.id,
                "amount": float(pay.amount),
                "payment_method": pay.payment_method,
                "reference_number": pay.reference_number,
                "notes": pay.notes,
                "payment_date": pay.payment_date.isoformat()
            }
            for pay in payments
        ]
    }
