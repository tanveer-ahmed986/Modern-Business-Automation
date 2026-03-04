from typing import List, Optional
from decimal import Decimal
from sqlmodel import Session, select
from fastapi import HTTPException, status
from backend.src.models.purchases import (
    Purchase, PurchaseItem, PurchaseCreate, 
    PurchaseStatus, PaymentStatus, Supplier
)
from backend.src.models.inventory import Product
from datetime import datetime

class PurchaseService:
    @staticmethod
    def create_purchase(session: Session, purchase_in: PurchaseCreate, user_id: int) -> Purchase:
        # 1. Verify Supplier
        supplier = None
        if purchase_in.supplier_id:
            supplier = session.get(Supplier, purchase_in.supplier_id)
            if not supplier:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Supplier with ID {purchase_in.supplier_id} not found"
                )

        # 2. Prepare items and update stock
        purchase_items: List[PurchaseItem] = []
        total_amount = Decimal("0.0")

        for item_in in purchase_in.items:
            product = session.get(Product, item_in.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with ID {item_in.product_id} not found"
                )

            # Increase stock
            product.stock_quantity += item_in.quantity
            # Update cost price to the latest purchase price
            product.cost_price = item_in.cost_price
            product.updated_at = datetime.utcnow()
            session.add(product)

            # Calculate subtotal
            subtotal = item_in.cost_price * item_in.quantity
            total_amount += subtotal

            # Create purchase item record
            purchase_item = PurchaseItem(
                product_id=product.id,
                product_name=product.name,
                quantity=item_in.quantity,
                cost_price=item_in.cost_price,
                subtotal=subtotal
            )
            purchase_items.append(purchase_item)

        # 3. Final calculations
        grand_total = (total_amount + purchase_in.tax_amount) - purchase_in.discount_amount
        
        # Determine payment status
        payment_status = PaymentStatus.PAID
        if purchase_in.paid_amount == 0:
            payment_status = PaymentStatus.UNPAID
        elif purchase_in.paid_amount < grand_total:
            payment_status = PaymentStatus.PARTIAL
        elif purchase_in.paid_amount > grand_total:
             # Overpayment could happen, but we'll treat as PAID for now
             payment_status = PaymentStatus.PAID

        # 4. Update Supplier Balance
        if supplier:
            unpaid_balance = grand_total - purchase_in.paid_amount
            supplier.balance += unpaid_balance
            session.add(supplier)

        # 5. Create Purchase
        db_purchase = Purchase(
            supplier_id=purchase_in.supplier_id,
            user_id=user_id,
            reference_number=purchase_in.reference_number,
            total_amount=total_amount,
            tax_amount=purchase_in.tax_amount,
            discount_amount=purchase_in.discount_amount,
            grand_total=grand_total,
            paid_amount=purchase_in.paid_amount,
            status=PurchaseStatus.RECEIVED,
            payment_status=payment_status,
            notes=purchase_in.notes
        )
        
        session.add(db_purchase)
        session.flush()

        # 6. Save items
        for item in purchase_items:
            item.purchase_id = db_purchase.id
            session.add(item)

        return db_purchase
