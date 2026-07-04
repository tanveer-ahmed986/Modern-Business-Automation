from typing import List, Optional, Dict, Any
from sqlmodel import Session, select, func, between, and_
from datetime import datetime
from decimal import Decimal
from ..models.sales import Sale, SaleItem
from ..models.purchases import Purchase, PurchaseItem
from ..models.inventory import Product, Category
from ..core.features import is_feature_enabled

class ReportService:
    @staticmethod
    def get_sales_report(db: Session, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Retrieves a summary of sales performance within a given date range.
        Uses SQL aggregation instead of loading all rows into Python memory.
        """
        # Aggregate totals at the DB level (avoids loading all Sale rows)
        summary_row = db.execute(
            select(
                func.coalesce(func.sum(Sale.grand_total), 0),
                func.coalesce(func.sum(Sale.tax_amount), 0),
                func.coalesce(func.sum(Sale.discount_amount), 0),
                func.count(Sale.id),
            ).where(between(Sale.created_at, start_date, end_date))
        ).one()
        total_revenue = summary_row[0]
        total_tax = summary_row[1]
        total_discount = summary_row[2]
        sale_count = summary_row[3]

        # Breakdown by payment method (SQL aggregation)
        pm_rows = db.execute(
            select(Sale.payment_method, func.sum(Sale.grand_total))
            .where(between(Sale.created_at, start_date, end_date))
            .group_by(Sale.payment_method)
        ).all()
        payment_methods = {str(row[0]): row[1] for row in pm_rows}
            
        # Top products in this period
        product_query = (
            select(
                SaleItem.product_name,
                func.sum(SaleItem.quantity).label("total_quantity"),
                func.sum(SaleItem.subtotal).label("total_revenue")
            )
            .join(Sale)
            .where(between(Sale.created_at, start_date, end_date))
            .group_by(SaleItem.product_name)
            .order_by(func.sum(SaleItem.quantity).desc())
            .limit(10)
        )
        top_products = db.exec(product_query).all()
        
        # Sales by Category (Standard feature)
        category_query = (
            select(
                Category.name,
                func.sum(SaleItem.subtotal).label("total_revenue")
            )
            .join(Sale)
            .join(Product, SaleItem.product_id == Product.id)
            .join(Category, Product.category_id == Category.id)
            .where(between(Sale.created_at, start_date, end_date))
            .group_by(Category.name)
            .order_by(func.sum(SaleItem.subtotal).desc())
        )
        category_sales = db.exec(category_query).all()
        
        return {
            "summary": {
                "total_revenue": total_revenue,
                "total_tax": total_tax,
                "total_discount": total_discount,
                "sale_count": sale_count,
            },
            "payment_methods": payment_methods,
            "top_products": [
                {"name": name, "quantity": qty, "revenue": rev} 
                for name, qty, rev in top_products
            ],
            "category_sales": [
                {"name": name, "revenue": rev}
                for name, rev in category_sales
            ],
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            }
        }

    @staticmethod
    def get_profit_loss_report(db: Session, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Premium only: Calculates Gross Profit based on Sales and COGS.
        """
        # 1. Total Sales Revenue (SQL aggregation - avoids loading all rows)
        total_revenue = db.execute(
            select(func.coalesce(func.sum(Sale.grand_total), 0)).where(
                and_(
                    between(Sale.created_at, start_date, end_date),
                    Sale.status == "completed"
                )
            )
        ).scalar() or Decimal("0.0")
        
        # 2. COGS (Cost of Goods Sold)
        # CRITICAL FIX: Use snapshotted cost_price from SaleItem (not current Product cost_price)
        # This ensures accurate historical profit calculations even if cost_price changes
        cogs_query = (
            select(
                func.sum(SaleItem.quantity * SaleItem.cost_price).label("total_cogs")
            )
            .join(Sale)
            .where(
                and_(
                    between(Sale.created_at, start_date, end_date),
                    Sale.status == "completed"
                )
            )
        )
        total_cogs = db.exec(cogs_query).one() or Decimal("0.0")
        
        # 3. Total Purchases (SQL aggregation - avoids loading all rows)
        total_purchases = db.execute(
            select(func.coalesce(func.sum(Purchase.grand_total), 0)).where(
                and_(
                    between(Purchase.created_at, start_date, end_date),
                    Purchase.status == "received"
                )
            )
        ).scalar() or Decimal("0.0")
        
        gross_profit = total_revenue - total_cogs
        
        return {
            "revenue": total_revenue,
            "cogs": total_cogs,
            "gross_profit": gross_profit,
            "total_purchases": total_purchases,
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            }
        }
