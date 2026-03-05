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
        """
        # Base query for sales within range
        query = select(Sale).where(between(Sale.created_at, start_date, end_date))
        sales = db.exec(query).all()
        
        total_revenue = sum((sale.grand_total for sale in sales), Decimal("0.0"))
        total_tax = sum((sale.tax_amount for sale in sales), Decimal("0.0"))
        total_discount = sum((sale.discount_amount for sale in sales), Decimal("0.0"))
        sale_count = len(sales)
        
        # Breakdown by payment method
        payment_methods = {}
        for sale in sales:
            pm = sale.payment_method.value
            payment_methods[pm] = payment_methods.get(pm, Decimal("0.0")) + sale.grand_total
            
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
        # 1. Total Sales Revenue
        sales_query = select(Sale).where(
            and_(
                between(Sale.created_at, start_date, end_date),
                Sale.status == "completed"
            )
        )
        sales = db.exec(sales_query).all()
        total_revenue = sum((sale.grand_total for sale in sales), Decimal("0.0"))
        
        # 2. COGS (Cost of Goods Sold)
        # We calculate this by joining SaleItem with Product to get the current cost_price.
        # Note: In a more mature system, we'd store the cost_price in SaleItem at transaction time.
        cogs_query = (
            select(
                func.sum(SaleItem.quantity * Product.cost_price).label("total_cogs")
            )
            .join(Sale)
            .join(Product, SaleItem.product_id == Product.id)
            .where(
                and_(
                    between(Sale.created_at, start_date, end_date),
                    Sale.status == "completed"
                )
            )
        )
        total_cogs = db.exec(cogs_query).one() or Decimal("0.0")
        
        # 3. Total Purchases (Cash Outflow)
        purchases_query = select(Purchase).where(
            and_(
                between(Purchase.created_at, start_date, end_date),
                Purchase.status == "received"
            )
        )
        purchases = db.exec(purchases_query).all()
        total_purchases = sum((p.grand_total for p in purchases), Decimal("0.0"))
        
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
