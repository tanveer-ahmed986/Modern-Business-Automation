from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func, desc
from typing import List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from pydantic import BaseModel

from src.core.db import get_session
from src.core.auth import get_current_user
from src.models.core import User, UserRole
from src.models.sales import Sale, SaleItem, SaleStatus
from src.models.inventory import Product, Category
from src.models.sales import Customer

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

class MetricCard(BaseModel):
    title: str
    value: str
    description: Optional[str] = None
    trend: Optional[float] = None # Percentage change
    icon: Optional[str] = None

class RecentSale(BaseModel):
    id: int
    customer_name: str
    grand_total: Decimal
    created_at: datetime
    status: str

class TopProduct(BaseModel):
    id: int
    name: str
    total_quantity: int
    total_revenue: Decimal

class DashboardMetrics(BaseModel):
    cards: List[MetricCard]
    recent_sales: List[RecentSale]
    top_products: List[TopProduct]
    low_stock_count: int

@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Today's Range
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    
    # 1. Total Sales Today
    sales_today_query = select(func.sum(Sale.grand_total)).where(
        Sale.created_at >= today_start,
        Sale.created_at <= today_end,
        Sale.status == SaleStatus.COMPLETED
    )
    total_sales_today = session.exec(sales_today_query).one() or Decimal("0.0")
    
    # 2. Total Orders Today
    orders_today_query = select(func.count(Sale.id)).where(
        Sale.created_at >= today_start,
        Sale.created_at <= today_end,
        Sale.status == SaleStatus.COMPLETED
    )
    total_orders_today = session.exec(orders_today_query).one() or 0
    
    # 3. Low Stock Count
    low_stock_query = select(func.count(Product.id)).where(
        Product.stock_quantity <= Product.low_stock_threshold,
        Product.is_active == True
    )
    low_stock_count = session.exec(low_stock_query).one() or 0
    
    # 4. Total Customers
    customers_query = select(func.count(Customer.id))
    total_customers = session.exec(customers_query).one() or 0
    
    # 5. Recent Sales
    recent_sales_query = select(Sale).order_by(desc(Sale.created_at)).limit(5)
    recent_sales_db = session.exec(recent_sales_query).all()
    recent_sales = []
    for s in recent_sales_db:
        customer_name = "Walk-in"
        if s.customer_id:
            customer = session.get(Customer, s.customer_id)
            if customer:
                customer_name = customer.name
        recent_sales.append(RecentSale(
            id=s.id,
            customer_name=customer_name,
            grand_total=s.grand_total,
            created_at=s.created_at,
            status=s.status
        ))
    
    # 6. Top Products (By Quantity Sold)
    top_products_query = (
        select(SaleItem.product_id, SaleItem.product_name, func.sum(SaleItem.quantity).label("total_qty"), func.sum(SaleItem.subtotal).label("total_rev"))
        .group_by(SaleItem.product_id, SaleItem.product_name)
        .order_by(desc("total_qty"))
        .limit(5)
    )
    top_products_db = session.exec(top_products_query).all()
    top_products = [
        TopProduct(id=p[0], name=p[1], total_quantity=p[2], total_revenue=p[3])
        for p in top_products_db
    ]
    
    # Construct Cards
    cards = [
        MetricCard(
            title="Today's Revenue",
            value=f"${total_sales_today:,.2f}",
            description="Total completed sales today",
            icon="DollarSign"
        ),
        MetricCard(
            title="Total Orders",
            value=str(total_orders_today),
            description="Completed orders today",
            icon="ShoppingCart"
        ),
        MetricCard(
            title="Total Customers",
            value=str(total_customers),
            description="Total registered customers",
            icon="Users"
        ),
        MetricCard(
            title="Low Stock Items",
            value=str(low_stock_count),
            description="Items below threshold",
            icon="AlertTriangle"
        )
    ]
    
    return DashboardMetrics(
        cards=cards,
        recent_sales=recent_sales,
        top_products=top_products,
        low_stock_count=low_stock_count
    )
