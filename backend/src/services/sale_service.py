from typing import List
from decimal import Decimal, ROUND_HALF_UP
from sqlmodel import Session, select, text
from fastapi import HTTPException, status
from src.models.sales import Sale, SaleItem, SaleCreate, SaleStatus
from src.models.inventory import Product
from src.models.core import Settings
from src.models.stock import StockMovementReason
from src.services.stock_service import record_stock_movement
from src.core.timeutils import local_date_key
from datetime import datetime

_TWO_PLACES = Decimal("0.01")


def money(value) -> Decimal:
    """Convert any numeric to a Decimal rounded to 2 dp (HALF_UP) —
    the single rounding rule for all invoice amounts."""
    return Decimal(str(value)).quantize(_TWO_PLACES, rounding=ROUND_HALF_UP)


class SaleService:
    @staticmethod
    def _generate_invoice_number(session: Session) -> str:
        """Allocate the next invoice number (INV-YYYYMMDD-XXXX) from the
        per-day sequence table, atomically.

        The UPSERT acquires SQLite's write lock immediately, so concurrent
        sales are serialized by busy_timeout and each transaction reads back
        the sequence value it allocated. The UNIQUE constraint on
        sales.invoice_number remains as a safety net. The date key uses the
        business-local day so numbering rolls over at local midnight.
        """
        date_key = local_date_key()
        session.execute(
            text(
                "INSERT INTO invoice_sequences (date_key, next_seq) VALUES (:k, 2) "
                "ON CONFLICT(date_key) DO UPDATE SET next_seq = next_seq + 1"
            ),
            {"k": date_key},
        )
        seq = session.execute(
            text("SELECT next_seq - 1 FROM invoice_sequences WHERE date_key = :k"),
            {"k": date_key},
        ).scalar_one()
        return f"INV-{date_key}-{str(seq).zfill(4)}"

    @staticmethod
    def create_sale(session: Session, sale_in: SaleCreate, user_id: int) -> Sale:
        if not sale_in.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A sale must contain at least one item",
            )

        # 0. Allocate unique invoice number (same transaction as the sale)
        invoice_number = SaleService._generate_invoice_number(session)

        # 1. Get settings for tax calculation
        settings = session.get(Settings, 1)
        tax_rate = Decimal(str(settings.tax_rate)) / Decimal("100") if settings else Decimal("0")

        # 2. Prepare items and check stock
        sale_items: List[SaleItem] = []
        touched_products: List[tuple] = []  # (product, qty) for ledger entries
        total_amount = Decimal("0.00")

        for item_in in sale_in.items:
            if item_in.quantity <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Item quantity must be a positive integer",
                )

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
            touched_products.append((product, item_in.quantity))

            # Money math: quantized Decimals only (snapshot prices at sale time)
            unit_price = money(product.selling_price)
            cost_price = money(product.cost_price)
            subtotal = money(unit_price * item_in.quantity)
            total_amount += subtotal

            sale_item = SaleItem(
                product_id=product.id,
                product_name=product.name,
                quantity=item_in.quantity,
                unit_price=unit_price,
                cost_price=cost_price,  # snapshot for accurate historical profit
                subtotal=subtotal
            )
            sale_items.append(sale_item)

        # 3. Final calculations — consistent 2 dp rounding at each money step
        tax_amount = money(total_amount * tax_rate)
        discount = money(sale_in.discount_amount)
        if discount < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Discount cannot be negative",
            )
        grand_total = money(total_amount + tax_amount - discount)

        # 4. Create Sale
        db_sale = Sale(
            invoice_number=invoice_number,
            customer_id=sale_in.customer_id,
            user_id=user_id,
            total_amount=total_amount,
            tax_amount=tax_amount,
            discount_amount=discount,
            grand_total=grand_total,
            payment_method=sale_in.payment_method,
            status=SaleStatus.COMPLETED
        )

        session.add(db_sale)
        session.flush()  # Get sale ID

        # 5. Save items + stock ledger entries referencing the sale
        for item in sale_items:
            item.sale_id = db_sale.id
            session.add(item)
        for product, qty in touched_products:
            record_stock_movement(
                session, product,
                change=-qty,
                reason=StockMovementReason.SALE,
                user_id=user_id,
                reference_type="sale",
                reference_id=db_sale.id,
            )

        # Caller commits (keeps sequence, sale, items, and ledger atomic)
        return db_sale

    @staticmethod
    def refund_sale(session: Session, sale_id: int, user_id: int) -> Sale:
        """Full refund: restore stock for every item, write ledger entries,
        and mark the sale REFUNDED. Runs in the caller's transaction."""
        sale = session.get(Sale, sale_id)
        if not sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sale not found"
            )
        if sale.status != SaleStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only completed sales can be refunded (current status: {sale.status})"
            )

        items = session.exec(
            select(SaleItem).where(SaleItem.sale_id == sale_id)
        ).all()

        for item in items:
            if item.product_id is None:
                continue
            product = session.get(Product, item.product_id)
            if not product:
                # Product row was removed historically — stock cannot be
                # restored, but the refund still proceeds (ledger skips it).
                continue
            product.stock_quantity += item.quantity
            product.updated_at = datetime.utcnow()
            session.add(product)
            record_stock_movement(
                session, product,
                change=item.quantity,
                reason=StockMovementReason.REFUND,
                user_id=user_id,
                reference_type="sale",
                reference_id=sale.id,
                note=f"Refund of invoice {sale.invoice_number}",
            )

        sale.status = SaleStatus.REFUNDED
        session.add(sale)
        return sale
