from typing import Optional
from sqlmodel import Session
from src.models.inventory import Product
from src.models.stock import StockMovement, StockMovementReason


def record_stock_movement(
    session: Session,
    product: Product,
    change: int,
    reason: StockMovementReason,
    user_id: Optional[int] = None,
    reference_type: Optional[str] = None,
    reference_id: Optional[int] = None,
    note: Optional[str] = None,
) -> StockMovement:
    """Append a ledger row for a stock change that has ALREADY been applied
    to `product.stock_quantity`. Call within the same transaction as the
    quantity change so the ledger and the stock level commit (or roll back)
    together."""
    movement = StockMovement(
        product_id=product.id,
        change=change,
        quantity_after=product.stock_quantity,
        reason=reason,
        reference_type=reference_type,
        reference_id=reference_id,
        user_id=user_id,
        note=note,
    )
    session.add(movement)
    return movement
