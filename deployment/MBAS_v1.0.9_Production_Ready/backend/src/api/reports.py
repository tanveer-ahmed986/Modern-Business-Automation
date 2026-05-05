from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from ..core.db import get_session
from ..core.auth import get_current_user
from ..core.features import check_feature
from ..models.core import User, UserRole
from ..models.sales import Sale
from ..services.report_service import ReportService
from ..core.export import ExportUtility

router = APIRouter(prefix="/reports", tags=["reports"])

def get_admin_or_manager(current_user: User = Depends(get_current_user)):
    """Ensures the user has high enough privileges for reports."""
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access reports."
        )
    return current_user

@router.get("/sales")
def get_sales_report(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_or_manager)
):
    """
    Returns a summary of sales performance within the specified date range.
    Defaults to the last 30 days if no range provided.
    """
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=30)
        
    return ReportService.get_sales_report(session, start_date, end_date)

@router.get("/profit-loss")
def get_profit_loss_report(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_or_manager),
    has_premium: bool = Depends(check_feature("premium_reports"))
):
    """
    Premium feature: Returns a P&L overview for the specified range.
    """
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=30)
        
    return ReportService.get_profit_loss_report(session, start_date, end_date)

@router.get("/export/sales")
def export_sales_csv(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_or_manager)
):
    """
    Exports all sales records in the given range to CSV.
    """
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=30)
        
    from sqlmodel import between
    query = select(Sale).where(between(Sale.created_at, start_date, end_date))
    sales = session.exec(query).all()
    
    # Flatten data for CSV
    export_data = []
    for s in sales:
        export_data.append({
            "id": s.id,
            "created_at": s.created_at,
            "total_amount": s.total_amount,
            "tax_amount": s.tax_amount,
            "discount_amount": s.discount_amount,
            "grand_total": s.grand_total,
            "payment_method": s.payment_method,
            "status": s.status
        })
        
    return ExportUtility.to_csv(export_data, f"sales_report_{start_date.date()}_{end_date.date()}")

