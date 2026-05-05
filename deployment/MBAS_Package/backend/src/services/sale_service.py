from typing import List, Optional
from decimal import Decimal
from sqlmodel import Session, select, func
from fastapi import HTTPException, status
from src.models.sales import Sale, SaleItem, SaleCreate, SaleStatus
from src.models.inventory import Product
from src.models.core import Settings
from datetime import datetime

class SaleService:
    @staticmethod
    def _generate_invoice_number(session: Session) -> str:
        """Generate a unique invoice number in format INV-YYYYMMDD-XXXX"""
        today = datetime.utcnow().strftime("%Y%m%d")

        # Find the last invoice of today
        statement = select(func.count(Sale.id)).where(
            Sale.invoice_number.like(f"INV-{today}-%")
        )
        count = session.exec(statement).first() or 0

        # Generate new invoice number with zero-padded sequence
        sequence = str(count + 1).zfill(4)
        return f"INV-{today}-{sequence}"

    @staticmethod
    def create_sale(session: Session, sale_in: SaleCreate, user_id: int) -> Sale:
        # 0. Generate unique invoice number
        invoice_number = SaleService._generate_invoice_number(session)

        # 1. Get settings for tax calculation
        settings = session.get(Settings, 1)
        tax_rate = Decimal(str(settings.tax_rate / 100)) if settings else Decimal("0.0")

        # 2. Prepare items and check stock
        sale_items: List[SaleItem] = []
        total_amount = Decimal("0.0")

        for item_in in sale_in.items:
            product = session.get(Product, item_in.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with ID {item_in.product_id} not found"
                )
            
            if not product.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product {product.name} is not active"
                )

            if product.stock_quantity < item_in.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for {product.name}. Available: {product.stock_quantity}, Requested: {item_in.quantity}"
                )

            # Deduct stock
            product.stock_quantity -= item_in.quantity
            product.updated_at = datetime.utcnow()
            session.add(product)

            # Calculate subtotal
            subtotal = product.selling_price * item_in.quantity
            total_amount += subtotal

            # Create sale item record (snapshotting data including cost_price for profit calc)
            sale_item = SaleItem(
                product_id=product.id,
                product_name=product.name,
                quantity=item_in.quantity,
                unit_price=product.selling_price,
                cost_price=product.cost_price,  # CRITICAL: Snapshot cost_price at time of sale
                subtotal=subtotal
            )
            sale_items.append(sale_item)

        # 3. Final calculations
        tax_amount = total_amount * tax_rate
        grand_total = (total_amount + tax_amount) - sale_in.discount_amount

        # 4. Create Sale with unique invoice number
        db_sale = Sale(
            invoice_number=invoice_number,  # CRITICAL: Auto-generated unique invoice number
            customer_id=sale_in.customer_id,
            user_id=user_id,
            total_amount=total_amount,
            tax_amount=tax_amount,
            discount_amount=sale_in.discount_amount,
            grand_total=grand_total,
            payment_method=sale_in.payment_method,
            status=SaleStatus.COMPLETED
        )
        
        session.add(db_sale)
        session.flush() # Get sale ID

        # 5. Save items
        for item in sale_items:
            item.sale_id = db_sale.id
            session.add(item)

        # No need for explicit commit if used within a transaction context manager
        return db_sale
