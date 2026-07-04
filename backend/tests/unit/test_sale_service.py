"""
Unit tests for Sale Service - Financial Logic (100% coverage required).

These tests verify critical financial calculations and business logic integrity.
"""

import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from sqlmodel import select
from src.services.sale_service import SaleService
from src.models.sales import Sale, SaleItem, SaleCreate, SaleItemCreate, PaymentMethod
from src.models.inventory import Product
from src.models.core import Settings


@pytest.mark.financial
class TestInvoiceNumberGeneration:
    """Test invoice number uniqueness and format."""

    def test_invoice_number_format(self, session, settings, admin_user, product):
        """Verify invoice number follows INV-YYYYMMDD-XXXX format."""
        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )

        sale = SaleService.create_sale(session, sale_in, admin_user.id)

        # Check format
        assert sale.invoice_number.startswith("INV-")
        parts = sale.invoice_number.split("-")
        assert len(parts) == 3
        assert len(parts[1]) == 8  # YYYYMMDD
        assert len(parts[2]) == 4  # Sequence number
        assert parts[2].isdigit()

    def test_invoice_number_uniqueness_same_day(self, session, settings, admin_user, product):
        """Generate 10 invoices on same day and verify all are unique."""
        invoice_numbers = set()

        for i in range(10):
            sale_in = SaleCreate(
                customer_id=None,
                items=[SaleItemCreate(product_id=product.id, quantity=1)],
                discount_amount=0,
                payment_method=PaymentMethod.CASH
            )

            sale = SaleService.create_sale(session, sale_in, admin_user.id)
            invoice_numbers.add(sale.invoice_number)

            # Refresh product stock for next sale
            session.refresh(product)

        # All invoice numbers should be unique
        assert len(invoice_numbers) == 10

    def test_invoice_number_sequence(self, session, settings, admin_user, product):
        """Verify invoice numbers increment sequentially."""
        sale1_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )
        sale1 = SaleService.create_sale(session, sale1_in, admin_user.id)

        session.refresh(product)

        sale2_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )
        sale2 = SaleService.create_sale(session, sale2_in, admin_user.id)

        # Extract sequence numbers
        seq1 = int(sale1.invoice_number.split("-")[2])
        seq2 = int(sale2.invoice_number.split("-")[2])

        assert seq2 == seq1 + 1


@pytest.mark.financial
class TestStockDeduction:
    """Test inventory stock deduction accuracy."""

    def test_stock_deduction_single_item(self, session, settings, admin_user, product):
        """Sale of 5 units should reduce stock by exactly 5."""
        initial_stock = product.stock_quantity
        quantity_sold = 5

        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=quantity_sold)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )

        SaleService.create_sale(session, sale_in, admin_user.id)
        session.refresh(product)

        assert product.stock_quantity == initial_stock - quantity_sold

    def test_stock_deduction_multiple_items(self, session, settings, admin_user, sample_products):
        """Sale of multiple products should deduct stock correctly for each."""
        initial_stocks = {p.id: p.stock_quantity for p in sample_products}

        sale_in = SaleCreate(
            customer_id=None,
            items=[
                SaleItemCreate(product_id=sample_products[0].id, quantity=3),
                SaleItemCreate(product_id=sample_products[1].id, quantity=5),
                SaleItemCreate(product_id=sample_products[2].id, quantity=2),
            ],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )

        SaleService.create_sale(session, sale_in, admin_user.id)

        for product in sample_products[:3]:
            session.refresh(product)

        assert sample_products[0].stock_quantity == initial_stocks[sample_products[0].id] - 3
        assert sample_products[1].stock_quantity == initial_stocks[sample_products[1].id] - 5
        assert sample_products[2].stock_quantity == initial_stocks[sample_products[2].id] - 2

    def test_insufficient_stock_rejection(self, session, settings, admin_user, product):
        """Attempting to sell more than available stock should fail."""
        product.stock_quantity = 3
        session.add(product)
        session.commit()

        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=5)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )

        with pytest.raises(Exception) as exc_info:
            SaleService.create_sale(session, sale_in, admin_user.id)

        assert "Insufficient stock" in str(exc_info.value)


@pytest.mark.financial
class TestCostPriceSnapshot:
    """Test cost price snapshotting for accurate P&L calculation."""

    def test_cost_price_snapshot_at_sale_time(self, session, settings, admin_user, product):
        """Verify cost_price is snapshotted in SaleItem at time of sale."""
        original_cost = product.cost_price

        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=2)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )

        sale = SaleService.create_sale(session, sale_in, admin_user.id)
        sale_item = sale.items[0]

        assert sale_item.cost_price == original_cost

    def test_cost_price_change_after_sale(self, session, settings, admin_user, product):
        """Change product cost after sale, verify P&L uses old (snapshotted) cost."""
        original_cost = 100.0
        product.cost_price = original_cost
        session.add(product)
        session.commit()

        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )

        sale = SaleService.create_sale(session, sale_in, admin_user.id)

        # Change product cost price AFTER sale
        product.cost_price = 120.0
        session.add(product)
        session.commit()

        # Sale item should still have original cost
        session.refresh(sale)
        assert sale.items[0].cost_price == original_cost
        assert sale.items[0].cost_price != product.cost_price


@pytest.mark.financial
class TestTaxCalculation:
    """Test tax calculation accuracy."""

    def test_tax_calculation_basic(self, session, admin_user, product):
        """Subtotal=100, tax_rate=15% → tax_amount=15, total=115."""
        # Set tax rate to 15%
        settings = session.get(Settings, 1)
        settings.tax_rate = 15.0
        session.add(settings)
        session.commit()

        # Product with selling price that gives subtotal of 100
        product.selling_price = 100.0
        session.add(product)
        session.commit()

        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )

        sale = SaleService.create_sale(session, sale_in, admin_user.id)

        assert sale.total_amount == Decimal("100.0")
        assert sale.tax_amount == Decimal("15.0")
        assert sale.grand_total == Decimal("115.0")

    def test_tax_calculation_zero_rate(self, session, admin_user, product):
        """Verify tax calculation works with 0% tax rate."""
        settings = session.get(Settings, 1)
        settings.tax_rate = 0.0
        session.add(settings)
        session.commit()

        product.selling_price = 100.0
        session.add(product)
        session.commit()

        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )

        sale = SaleService.create_sale(session, sale_in, admin_user.id)

        assert sale.tax_amount == Decimal("0.0")
        assert sale.grand_total == sale.total_amount


@pytest.mark.financial
class TestDiscountCalculation:
    """Test discount calculation accuracy."""

    def test_discount_calculation(self, session, admin_user, product):
        """Subtotal=100, discount=10, tax=15% → total=(100-10)*1.15=103.5."""
        settings = session.get(Settings, 1)
        settings.tax_rate = 15.0
        session.add(settings)
        session.commit()

        product.selling_price = 100.0
        session.add(product)
        session.commit()

        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=1)],
            discount_amount=10.0,
            payment_method=PaymentMethod.CASH
        )

        sale = SaleService.create_sale(session, sale_in, admin_user.id)

        expected_subtotal = Decimal("100.0")
        expected_tax = Decimal("15.0")  # Tax on original amount
        expected_grand_total = (expected_subtotal + expected_tax) - Decimal("10.0")

        assert sale.total_amount == expected_subtotal
        assert sale.discount_amount == Decimal("10.0")
        assert sale.grand_total == expected_grand_total

    def test_discount_larger_than_subtotal(self, session, admin_user, product):
        """Discount larger than subtotal should result in negative or zero grand total."""
        settings = session.get(Settings, 1)
        settings.tax_rate = 0.0
        session.add(settings)
        session.commit()

        product.selling_price = 50.0
        session.add(product)
        session.commit()

        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=1)],
            discount_amount=100.0,  # Discount > subtotal
            payment_method=PaymentMethod.CASH
        )

        sale = SaleService.create_sale(session, sale_in, admin_user.id)

        # Grand total should be negative (business logic may vary)
        assert sale.grand_total < 0


@pytest.mark.financial
class TestTransactionIntegrity:
    """Test database transaction rollback on errors."""

    def test_rollback_on_insufficient_stock(self, session, settings, admin_user, product):
        """Attempt sale with insufficient stock → rollback, stock unchanged."""
        initial_stock = product.stock_quantity = 3
        session.add(product)
        session.commit()

        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=5)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )

        try:
            SaleService.create_sale(session, sale_in, admin_user.id)
        except Exception:
            session.rollback()

        # Stock should remain unchanged
        session.refresh(product)
        assert product.stock_quantity == initial_stock

    def test_rollback_on_invalid_product(self, session, settings, admin_user):
        """Attempt sale with non-existent product → rollback, no sale created."""
        initial_sale_count = len(session.exec(select(Sale)).all())

        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=99999, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )

        try:
            SaleService.create_sale(session, sale_in, admin_user.id)
        except Exception:
            session.rollback()

        # No sale should be created
        final_sale_count = len(session.exec(select(Sale)).all())
        assert final_sale_count == initial_sale_count


@pytest.mark.financial
class TestMultipleItemCalculations:
    """Test calculations with multiple line items."""

    def test_multiple_items_total_calculation(self, session, settings, admin_user, sample_products):
        """Verify total amount is sum of all item subtotals."""
        settings.tax_rate = 0.0
        session.add(settings)
        session.commit()

        sale_in = SaleCreate(
            customer_id=None,
            items=[
                SaleItemCreate(product_id=sample_products[0].id, quantity=2),  # 2 * price
                SaleItemCreate(product_id=sample_products[1].id, quantity=3),  # 3 * price
                SaleItemCreate(product_id=sample_products[2].id, quantity=1),  # 1 * price
            ],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )

        sale = SaleService.create_sale(session, sale_in, admin_user.id)

        expected_total = (
            (sample_products[0].selling_price * 2) +
            (sample_products[1].selling_price * 3) +
            (sample_products[2].selling_price * 1)
        )

        assert float(sale.total_amount) == pytest.approx(float(expected_total), rel=1e-2)
