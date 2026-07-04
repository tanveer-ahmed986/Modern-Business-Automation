"""
Unit tests for Report Service - Financial Reporting (100% coverage required).

These tests verify accurate profit/loss calculations and reporting logic.
"""

import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from src.services.report_service import ReportService
from src.services.sale_service import SaleService
from src.models.sales import SaleCreate, SaleItemCreate, PaymentMethod, SaleStatus
from src.models.inventory import Product


@pytest.mark.financial
class TestProfitLossCalculation:
    """Test P&L calculation accuracy."""

    def test_profit_loss_basic_calculation(self, session, settings, admin_user, product):
        """Sale: price=150, cost=100, quantity=1 → profit=50, margin=33.3%."""
        # Set product prices
        product.selling_price = 150.0
        product.cost_price = 100.0
        session.add(product)
        session.commit()

        # Set 0% tax for simpler calculation
        settings.tax_rate = 0.0
        session.add(settings)
        session.commit()

        # Create sale
        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )
        sale = SaleService.create_sale(session, sale_in, admin_user.id)

        # Generate P&L report
        start_date = datetime.utcnow() - timedelta(days=1)
        end_date = datetime.utcnow() + timedelta(days=1)

        report = ReportService.get_profit_loss_report(session, start_date, end_date)

        # Verify calculations
        assert report["revenue"] == Decimal("150.0")
        assert report["cogs"] == Decimal("100.0")
        assert report["gross_profit"] == Decimal("50.0")

    def test_profit_loss_multiple_sales(self, session, settings, admin_user, sample_products):
        """Multiple sales should aggregate correctly in P&L."""
        settings.tax_rate = 0.0
        session.add(settings)
        session.commit()

        # Create multiple sales
        for i, product in enumerate(sample_products[:3]):
            sale_in = SaleCreate(
                customer_id=None,
                items=[SaleItemCreate(product_id=product.id, quantity=2)],
                discount_amount=0,
                payment_method=PaymentMethod.CASH
            )
            SaleService.create_sale(session, sale_in, admin_user.id)

        # Generate P&L report
        start_date = datetime.utcnow() - timedelta(days=1)
        end_date = datetime.utcnow() + timedelta(days=1)

        report = ReportService.get_profit_loss_report(session, start_date, end_date)

        # Calculate expected values
        expected_revenue = sum(p.selling_price * 2 for p in sample_products[:3])
        expected_cogs = sum(p.cost_price * 2 for p in sample_products[:3])
        expected_profit = expected_revenue - expected_cogs

        assert float(report["revenue"]) == pytest.approx(float(expected_revenue), rel=1e-2)
        assert float(report["cogs"]) == pytest.approx(float(expected_cogs), rel=1e-2)
        assert float(report["gross_profit"]) == pytest.approx(float(expected_profit), rel=1e-2)


@pytest.mark.financial
class TestCOGSAccuracy:
    """Test COGS (Cost of Goods Sold) uses snapshotted costs."""

    def test_cogs_uses_snapshotted_costs(self, session, settings, admin_user, product):
        """Verify P&L uses SaleItem.cost_price, not current Product.cost_price."""
        # Original cost
        product.cost_price = 100.0
        product.selling_price = 150.0
        session.add(product)
        session.commit()

        settings.tax_rate = 0.0
        session.add(settings)
        session.commit()

        # Create sale with original cost
        sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )
        SaleService.create_sale(session, sale_in, admin_user.id)

        # CHANGE product cost AFTER sale
        product.cost_price = 120.0
        session.add(product)
        session.commit()

        # Generate P&L report
        start_date = datetime.utcnow() - timedelta(days=1)
        end_date = datetime.utcnow() + timedelta(days=1)

        report = ReportService.get_profit_loss_report(session, start_date, end_date)

        # COGS should use ORIGINAL cost (100), not new cost (120)
        assert report["cogs"] == Decimal("100.0")
        assert report["gross_profit"] == Decimal("50.0")  # 150 - 100

    def test_cogs_with_cost_changes_over_time(self, session, settings, admin_user, product):
        """Multiple sales with cost changes should track each sale's cost correctly."""
        settings.tax_rate = 0.0
        session.add(settings)
        session.commit()

        product.selling_price = 150.0

        # Sale 1 with cost=100
        product.cost_price = 100.0
        session.add(product)
        session.commit()
        sale1_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )
        SaleService.create_sale(session, sale1_in, admin_user.id)
        session.refresh(product)

        # Sale 2 with cost=110 (cost increased)
        product.cost_price = 110.0
        session.add(product)
        session.commit()
        sale2_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )
        SaleService.create_sale(session, sale2_in, admin_user.id)

        # Generate P&L report
        start_date = datetime.utcnow() - timedelta(days=1)
        end_date = datetime.utcnow() + timedelta(days=1)

        report = ReportService.get_profit_loss_report(session, start_date, end_date)

        # COGS should be 100 + 110 = 210
        assert report["cogs"] == Decimal("210.0")
        # Revenue should be 150 * 2 = 300
        assert report["revenue"] == Decimal("300.0")
        # Gross profit should be 300 - 210 = 90
        assert report["gross_profit"] == Decimal("90.0")


@pytest.mark.financial
class TestSalesReportDateFiltering:
    """Test sales report date range filtering."""

    def test_sales_report_includes_only_date_range(self, session, settings, admin_user, product):
        """Filter 2026-04-01 to 2026-04-30, verify only April sales included."""
        settings.tax_rate = 0.0
        session.add(settings)
        session.commit()

        # Create sale in March (should be excluded)
        sale_march_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )
        sale_march = SaleService.create_sale(session, sale_march_in, admin_user.id)
        # Manually set created_at to March
        sale_march.created_at = datetime(2026, 3, 15)
        session.add(sale_march)
        session.commit()

        session.refresh(product)

        # Create sale in April (should be included)
        sale_april_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=2)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )
        sale_april = SaleService.create_sale(session, sale_april_in, admin_user.id)
        sale_april.created_at = datetime(2026, 4, 15)
        session.add(sale_april)
        session.commit()

        session.refresh(product)

        # Create sale in May (should be excluded)
        sale_may_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=product.id, quantity=3)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )
        sale_may = SaleService.create_sale(session, sale_may_in, admin_user.id)
        sale_may.created_at = datetime(2026, 5, 15)
        session.add(sale_may)
        session.commit()

        # Generate report for April only
        start_date = datetime(2026, 4, 1)
        end_date = datetime(2026, 4, 30, 23, 59, 59)

        report = ReportService.get_sales_report(session, start_date, end_date)

        # Only April sale should be included (2 items * price)
        assert report["summary"]["sale_count"] == 1
        expected_revenue = product.selling_price * 2
        assert float(report["summary"]["total_revenue"]) == pytest.approx(float(expected_revenue), rel=1e-2)

    def test_empty_date_range_returns_zero(self, session, settings):
        """Date range with no sales should return zero values."""
        # Query a date range with no sales
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2020, 1, 31)

        report = ReportService.get_sales_report(session, start_date, end_date)

        assert report["summary"]["total_revenue"] == Decimal("0.0")
        assert report["summary"]["sale_count"] == 0


@pytest.mark.financial
class TestReportAggregations:
    """Test report aggregation calculations."""

    def test_payment_method_breakdown(self, session, settings, admin_user, sample_products):
        """Sales should be correctly grouped by payment method."""
        settings.tax_rate = 0.0
        session.add(settings)
        session.commit()

        # Cash sale
        cash_sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=sample_products[0].id, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CASH
        )
        SaleService.create_sale(session, cash_sale_in, admin_user.id)

        # Card sale
        card_sale_in = SaleCreate(
            customer_id=None,
            items=[SaleItemCreate(product_id=sample_products[1].id, quantity=1)],
            discount_amount=0,
            payment_method=PaymentMethod.CARD
        )
        SaleService.create_sale(session, card_sale_in, admin_user.id)

        # Generate report
        start_date = datetime.utcnow() - timedelta(days=1)
        end_date = datetime.utcnow() + timedelta(days=1)

        report = ReportService.get_sales_report(session, start_date, end_date)

        # Check payment method breakdown
        assert "cash" in report["payment_methods"]
        assert "card" in report["payment_methods"]
        assert float(report["payment_methods"]["cash"]) == pytest.approx(float(sample_products[0].selling_price), rel=1e-2)
        assert float(report["payment_methods"]["card"]) == pytest.approx(float(sample_products[1].selling_price), rel=1e-2)

    def test_top_products_ranking(self, session, settings, admin_user, sample_products):
        """Top products should be ranked by quantity sold."""
        settings.tax_rate = 0.0
        session.add(settings)
        session.commit()

        # Sell different quantities of each product
        for i, product in enumerate(sample_products[:3]):
            quantity = 10 - i  # 10, 9, 8
            sale_in = SaleCreate(
                customer_id=None,
                items=[SaleItemCreate(product_id=product.id, quantity=quantity)],
                discount_amount=0,
                payment_method=PaymentMethod.CASH
            )
            SaleService.create_sale(session, sale_in, admin_user.id)

        # Generate report
        start_date = datetime.utcnow() - timedelta(days=1)
        end_date = datetime.utcnow() + timedelta(days=1)

        report = ReportService.get_sales_report(session, start_date, end_date)

        # Check top products are in descending order
        top_products = report["top_products"]
        assert len(top_products) >= 3
        assert top_products[0]["quantity"] >= top_products[1]["quantity"]
        assert top_products[1]["quantity"] >= top_products[2]["quantity"]
