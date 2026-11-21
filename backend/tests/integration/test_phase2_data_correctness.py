"""
Phase 2 (system-overhaul) tests: refund flow, soft-delete products,
stock movement ledger, invoice sequence, money rounding, timezone bounds.
"""

import pytest
from datetime import date, datetime, timedelta
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlmodel import select

from src.models.inventory import Product
from src.models.stock import StockMovement, InvoiceSequence
from src.services.sale_service import money
from src.core.timeutils import local_day_utc_bounds, local_range_utc_bounds, local_date_key


# ---------------------------------------------------------------------------
# Money rounding
# ---------------------------------------------------------------------------
@pytest.mark.financial
class TestMoneyRounding:
    def test_two_decimal_quantization(self):
        assert money("10.005") == Decimal("10.01")   # HALF_UP
        assert money("10.004") == Decimal("10.00")
        assert money(10) == Decimal("10.00")
        assert money(0.1 + 0.2) == Decimal("0.30")   # float noise collapsed

    def test_sale_amounts_are_quantized(self, session, settings, admin_user, product):
        from src.models.sales import SaleCreate, SaleItemCreate
        from src.services.sale_service import SaleService

        settings.tax_rate = 17.0
        product.selling_price = 99.99
        session.add(settings)
        session.add(product)
        session.commit()

        sale = SaleService.create_sale(
            session,
            SaleCreate(items=[SaleItemCreate(product_id=product.id, quantity=3)]),
            admin_user.id,
        )
        session.commit()

        assert sale.total_amount == Decimal("299.97")
        assert sale.tax_amount == Decimal("50.99")    # 50.9949 -> 50.99
        assert sale.grand_total == Decimal("350.96")


# ---------------------------------------------------------------------------
# Invoice sequence
# ---------------------------------------------------------------------------
@pytest.mark.financial
class TestInvoiceSequenceTable:
    def test_sequence_row_tracks_allocations(self, session, settings, admin_user, product):
        from src.models.sales import SaleCreate, SaleItemCreate
        from src.services.sale_service import SaleService

        for _ in range(3):
            SaleService.create_sale(
                session,
                SaleCreate(items=[SaleItemCreate(product_id=product.id, quantity=1)]),
                admin_user.id,
            )
        session.commit()

        row = session.get(InvoiceSequence, local_date_key())
        assert row is not None
        assert row.next_seq == 4  # three allocated, next is 4


# ---------------------------------------------------------------------------
# Refund flow (API)
# ---------------------------------------------------------------------------
@pytest.mark.integration
class TestRefundFlow:
    def _make_sale(self, client, auth_headers, product, qty=2):
        resp = client.post(
            "/billing/sales",
            json={
                "customer_id": None,
                "items": [{"product_id": product.id, "quantity": qty}],
                "discount_amount": 0,
                "payment_method": "cash",
            },
            headers=auth_headers,
        )
        assert resp.status_code == 200
        return resp.json()

    def test_refund_restores_stock_and_marks_sale(
        self, client: TestClient, auth_headers, settings, product, session
    ):
        initial_stock = product.stock_quantity
        sale = self._make_sale(client, auth_headers, product, qty=2)

        session.refresh(product)
        assert product.stock_quantity == initial_stock - 2

        resp = client.post(f"/billing/sales/{sale['id']}/refund", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["status"] == "refunded"

        session.refresh(product)
        assert product.stock_quantity == initial_stock

        # Ledger: one 'sale' entry and one 'refund' entry
        movements = session.exec(
            select(StockMovement).where(StockMovement.product_id == product.id)
        ).all()
        reasons = sorted(m.reason.value for m in movements)
        assert reasons == ["refund", "sale"]

    def test_refund_twice_rejected(self, client, auth_headers, settings, product):
        sale = self._make_sale(client, auth_headers, product)
        assert client.post(f"/billing/sales/{sale['id']}/refund", headers=auth_headers).status_code == 200
        resp = client.post(f"/billing/sales/{sale['id']}/refund", headers=auth_headers)
        assert resp.status_code == 400

    def test_refund_requires_manager_role(
        self, client, settings, product, sales_user, session, admin_user, auth_headers
    ):
        sale = self._make_sale(client, auth_headers, product)

        login = client.post(
            "/auth/login", data={"username": "testsales", "password": "testpass123"}
        )
        sales_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        resp = client.post(f"/billing/sales/{sale['id']}/refund", headers=sales_headers)
        assert resp.status_code == 403

    def test_refund_nonexistent_sale(self, client, auth_headers, settings):
        resp = client.post("/billing/sales/99999/refund", headers=auth_headers)
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Soft delete
# ---------------------------------------------------------------------------
@pytest.mark.integration
class TestSoftDeleteProducts:
    def test_unreferenced_product_hard_deleted(self, client, auth_headers, session, category):
        resp = client.post(
            "/inventory/products",
            json={
                "name": "Throwaway",
                "barcode": "THROW-1",
                "category_id": category.id,
                "selling_price": 10,
                "cost_price": 5,
                "stock_quantity": 4,
                "low_stock_threshold": 1,
            },
            headers=auth_headers,
        )
        pid = resp.json()["id"]

        resp = client.delete(f"/inventory/products/{pid}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["soft_deleted"] is False
        assert session.get(Product, pid) is None

    def test_sold_product_soft_deleted(
        self, client, auth_headers, settings, product, session
    ):
        # Sell it so it becomes referenced
        sale_resp = client.post(
            "/billing/sales",
            json={
                "customer_id": None,
                "items": [{"product_id": product.id, "quantity": 1}],
                "discount_amount": 0,
                "payment_method": "cash",
            },
            headers=auth_headers,
        )
        assert sale_resp.status_code == 200

        resp = client.delete(f"/inventory/products/{product.id}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["soft_deleted"] is True

        session.refresh(product)
        assert product.is_active is False  # still exists, deactivated

        # Historical sale data intact
        sale_id = sale_resp.json()["id"]
        detail = client.get(f"/billing/sales/{sale_id}", headers=auth_headers)
        assert detail.status_code == 200
        assert detail.json()["items"][0]["product_id"] == product.id

    def test_inactive_product_hidden_from_pos_search(
        self, client, auth_headers, settings, product, session
    ):
        product.is_active = False
        session.add(product)
        session.commit()

        # Default search (POS) hides it
        resp = client.get(
            "/inventory/products/search",
            params={"query": product.barcode},
            headers=auth_headers,
        )
        assert resp.json()["pagination"]["total_count"] == 0

        # Inventory-management search can still find it
        resp = client.get(
            "/inventory/products/search",
            params={"query": product.barcode, "include_inactive": True},
            headers=auth_headers,
        )
        assert resp.json()["pagination"]["total_count"] == 1

    def test_product_list_active_filter(self, client, auth_headers, session, category):
        for i, active in enumerate([True, True, False]):
            session.add(Product(
                name=f"Filter-{i}", barcode=f"FLT-{i}", category_id=category.id,
                selling_price=10, cost_price=5, stock_quantity=1,
                low_stock_threshold=1, is_active=active,
            ))
        session.commit()

        all_resp = client.get("/inventory/products", headers=auth_headers)
        active_resp = client.get(
            "/inventory/products", params={"is_active": True}, headers=auth_headers
        )
        assert all_resp.json()["pagination"]["total_count"] == 3
        assert active_resp.json()["pagination"]["total_count"] == 2


# ---------------------------------------------------------------------------
# Timezone helpers
# ---------------------------------------------------------------------------
class TestTimeutils:
    def test_day_bounds_cover_24h(self):
        start, end = local_day_utc_bounds(date(2026, 11, 12))
        assert end - start == timedelta(days=1)

    def test_range_bounds_inclusive_of_both_days(self):
        start, end = local_range_utc_bounds(date(2026, 11, 1), date(2026, 11, 2))
        assert end - start == timedelta(days=2)

    def test_default_range_is_31_local_days(self):
        start, end = local_range_utc_bounds(None, None)
        assert end - start == timedelta(days=31)  # 30 back + today inclusive

    def test_bounds_are_naive_utc(self):
        start, end = local_day_utc_bounds()
        assert start.tzinfo is None and end.tzinfo is None

    def test_date_key_format(self):
        key = local_date_key()
        assert len(key) == 8 and key.isdigit()
