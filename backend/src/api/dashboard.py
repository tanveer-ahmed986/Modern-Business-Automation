from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func, desc, col
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from pydantic import BaseModel
import time

from src.core.db import get_session
from src.core.auth import get_current_user
from src.core.timeutils import local_day_utc_bounds, local_today, local_range_utc_bounds, local_date_key
from src.models.core import User, UserRole, Settings
from src.models.sales import Sale, SaleItem, SaleStatus
from src.models.inventory import Product, Category
from src.models.sales import Customer

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# ---------------------------------------------------------------------------
# Server-side metrics cache (avoids running 5 aggregation queries per visit)
# ---------------------------------------------------------------------------
_metrics_cache: dict = {"data": None, "ts": 0.0, "date": ""}
_METRICS_TTL = 10  # seconds – short enough to feel fresh, long enough to absorb page switches

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
def get_dashboard_metrics(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Return cached metrics if fresh (absorbs rapid page switches without hitting DB)
    now = time.monotonic()
    today_str = str(local_today())
    if (
        _metrics_cache["data"]
        and (now - _metrics_cache["ts"]) < _METRICS_TTL
        and _metrics_cache["date"] == today_str
    ):
        return _metrics_cache["data"]

    # Get currency from settings
    settings = session.get(Settings, 1)
    currency = settings.currency if settings else "USD"

    # Today's range: the BUSINESS-LOCAL calendar day converted to UTC bounds
    # (timestamps are stored as naive UTC; comparing them against a local
    # date boundary shifted "today" by the UTC offset)
    today_start, today_end = local_day_utc_bounds()

    # Combined query: sales today total + count in one query
    today_stats = session.execute(
        select(
            func.coalesce(func.sum(Sale.grand_total), 0),
            func.count(Sale.id)
        ).where(
            Sale.created_at >= today_start,
            Sale.created_at < today_end,
            Sale.status == SaleStatus.COMPLETED
        )
    ).one()
    total_sales_today = today_stats[0] or Decimal("0.0")
    total_orders_today = today_stats[1] or 0

    # Combined query: low stock count + total customers in one round-trip
    low_stock_count = session.exec(
        select(func.count(Product.id)).where(
            Product.stock_quantity <= Product.low_stock_threshold,
            Product.is_active == True
        )
    ).one() or 0

    total_customers = session.exec(select(func.count(Customer.id))).one() or 0

    # Recent sales with LEFT JOIN to customer (eliminates N+1 loop)
    recent_sales_rows = session.execute(
        select(Sale.id, Sale.grand_total, Sale.created_at, Sale.status, Customer.name)
        .outerjoin(Customer, Sale.customer_id == Customer.id)
        .order_by(desc(Sale.created_at))
        .limit(5)
    ).all()
    recent_sales = [
        RecentSale(
            id=r[0],
            customer_name=r[4] or "Walk-in",
            grand_total=r[1],
            created_at=r[2],
            status=r[3]
        )
        for r in recent_sales_rows
    ]

    # Top Products (By Quantity Sold)
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
            value=f"{currency} {total_sales_today:,.2f}",
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
    
    result = DashboardMetrics(
        cards=cards,
        recent_sales=recent_sales,
        top_products=top_products,
        low_stock_count=low_stock_count
    )

    # Cache the result so the next page-switch returns instantly
    _metrics_cache["data"] = result
    _metrics_cache["ts"] = time.monotonic()
    _metrics_cache["date"] = today_str

    return result


# ---------------------------------------------------------------------------
# Trends: last 30 local days of revenue + payment-method breakdown, for the
# dashboard charts. Cached the same way as /metrics.
# ---------------------------------------------------------------------------
_TRENDS_DAYS = 30
_trends_cache: dict = {"data": None, "ts": 0.0, "date": ""}

class DailyRevenuePoint(BaseModel):
    date: str  # YYYY-MM-DD, business-local day
    revenue: Decimal

class PaymentMethodTotal(BaseModel):
    method: str
    total: Decimal
    count: int

class DashboardTrends(BaseModel):
    daily_revenue: List[DailyRevenuePoint]
    payment_breakdown: List[PaymentMethodTotal]

@router.get("/trends", response_model=DashboardTrends)
def get_dashboard_trends(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    now = time.monotonic()
    today_str = str(local_today())
    if (
        _trends_cache["data"]
        and (now - _trends_cache["ts"]) < _METRICS_TTL
        and _trends_cache["date"] == today_str
    ):
        return _trends_cache["data"]

    start, end = local_range_utc_bounds(None, None, default_days=_TRENDS_DAYS - 1)

    rows = session.execute(
        select(Sale.created_at, Sale.grand_total, Sale.payment_method).where(
            Sale.created_at >= start,
            Sale.created_at < end,
            Sale.status == SaleStatus.COMPLETED,
        )
    ).all()

    # Pre-seed every local day in the window so the chart has no gaps on
    # days with zero sales.
    today = local_today()
    revenue_by_day: dict = {
        (today - timedelta(days=offset)).isoformat(): Decimal("0.0")
        for offset in range(_TRENDS_DAYS - 1, -1, -1)
    }
    payment_totals: dict = {}

    for created_at, grand_total, payment_method in rows:
        day_key = datetime.strptime(local_date_key(created_at), "%Y%m%d").date().isoformat()
        if day_key in revenue_by_day:
            revenue_by_day[day_key] += grand_total

        bucket = payment_totals.setdefault(payment_method, {"total": Decimal("0.0"), "count": 0})
        bucket["total"] += grand_total
        bucket["count"] += 1

    result = DashboardTrends(
        daily_revenue=[
            DailyRevenuePoint(date=day, revenue=revenue) for day, revenue in revenue_by_day.items()
        ],
        payment_breakdown=[
            PaymentMethodTotal(method=method, total=v["total"], count=v["count"])
            for method, v in sorted(payment_totals.items(), key=lambda kv: kv[1]["total"], reverse=True)
        ],
    )

    _trends_cache["data"] = result
    _trends_cache["ts"] = time.monotonic()
    _trends_cache["date"] = today_str

    return result
