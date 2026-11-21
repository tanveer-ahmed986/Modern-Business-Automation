"""
Integration tests for Billing/Sales API endpoints.

Tests sale creation, validation, and feature gating.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import select
from src.models.sales import Sale
from src.models.core import Settings


@pytest.mark.integration
class TestSaleCreation:
    """Test sale creation endpoint."""

    def test_create_sale_success(self, client: TestClient, auth_headers, settings, product):
        """POST /billing/sales with valid data → 200/201, invoice created."""
        sale_data = {
            "customer_id": None,
            "items": [
                {"product_id": product.id, "quantity": 2}
            ],
            "discount_amount": 10.0,
            "payment_method": "cash"
        }

        response = client.post("/billing/sales", json=sale_data, headers=auth_headers)

        assert response.status_code in [200, 201]
        data = response.json()
        assert "invoice_number" in data
        assert data["invoice_number"].startswith("INV-")
        assert "id" in data
        assert float(data["grand_total"]) > 0  # Decimals serialize as strings

    def test_create_sale_multiple_items(self, client: TestClient, auth_headers, settings, sample_products):
        """Sale with multiple items should calculate totals correctly."""
        sale_data = {
            "customer_id": None,
            "items": [
                {"product_id": sample_products[0].id, "quantity": 2},
                {"product_id": sample_products[1].id, "quantity": 3},
                {"product_id": sample_products[2].id, "quantity": 1},
            ],
            "discount_amount": 0,
            "payment_method": "card"
        }

        response = client.post("/billing/sales", json=sale_data, headers=auth_headers)

        assert response.status_code in [200, 201]
        data = response.json()
        assert len(data["items"]) == 3

        # Verify total calculation
        expected_total = (
            sample_products[0].selling_price * 2 +
            sample_products[1].selling_price * 3 +
            sample_products[2].selling_price * 1
        )
        # Account for tax (Decimals serialize as strings)
        assert float(data["total_amount"]) == pytest.approx(float(expected_total), rel=1e-2)

    def test_create_sale_insufficient_stock(self, client: TestClient, auth_headers, settings, product):
        """Sale with insufficient stock → 400."""
        product.stock_quantity = 2

        sale_data = {
            "customer_id": None,
            "items": [
                {"product_id": product.id, "quantity": 10}  # More than available
            ],
            "discount_amount": 0,
            "payment_method": "cash"
        }

        response = client.post("/billing/sales", json=sale_data, headers=auth_headers)

        assert response.status_code == 400
        assert "insufficient" in response.json()["detail"].lower()

    def test_create_sale_nonexistent_product(self, client: TestClient, auth_headers, settings):
        """Sale with non-existent product → 404."""
        sale_data = {
            "customer_id": None,
            "items": [
                {"product_id": 99999, "quantity": 1}
            ],
            "discount_amount": 0,
            "payment_method": "cash"
        }

        response = client.post("/billing/sales", json=sale_data, headers=auth_headers)

        assert response.status_code == 404

    def test_create_sale_without_auth(self, client: TestClient, settings, product):
        """POST /billing/sales without auth → 401."""
        sale_data = {
            "customer_id": None,
            "items": [{"product_id": product.id, "quantity": 1}],
            "discount_amount": 0,
            "payment_method": "cash"
        }

        response = client.post("/billing/sales", json=sale_data)

        assert response.status_code == 401


@pytest.mark.integration
class TestSaleRetrieval:
    """Test sale retrieval endpoints."""

    def test_list_sales(self, client: TestClient, auth_headers, settings, product):
        """GET /billing/sales returns list of sales."""
        # Create a sale first
        sale_data = {
            "customer_id": None,
            "items": [{"product_id": product.id, "quantity": 1}],
            "discount_amount": 0,
            "payment_method": "cash"
        }
        client.post("/billing/sales", json=sale_data, headers=auth_headers)

        # List sales (paginated response)
        response = client.get("/billing/sales", headers=auth_headers)

        assert response.status_code == 200
        body = response.json()
        assert isinstance(body["items"], list)
        assert len(body["items"]) > 0
        assert body["pagination"]["total_count"] >= 1
        # Each sale's own line items must survive serialization — a prior
        # bug silently dropped "items"/"customer" when the list endpoint's
        # response_model was a generic PaginatedResponse[SaleRead] wrapper.
        sale = body["items"][0]
        assert "items" in sale
        assert len(sale["items"]) == 1
        assert sale["items"][0]["product_id"] == product.id
        assert "customer" in sale

    def test_get_sale_by_id(self, client: TestClient, auth_headers, settings, product):
        """GET /billing/sales/{id} returns specific sale."""
        # Create a sale
        sale_data = {
            "customer_id": None,
            "items": [{"product_id": product.id, "quantity": 1}],
            "discount_amount": 0,
            "payment_method": "cash"
        }
        create_response = client.post("/billing/sales", json=sale_data, headers=auth_headers)
        sale_id = create_response.json()["id"]

        # Get sale by ID
        response = client.get(f"/billing/sales/{sale_id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sale_id
        assert "invoice_number" in data

    def test_get_nonexistent_sale(self, client: TestClient, auth_headers):
        """GET /billing/sales/{nonexistent_id} → 404."""
        response = client.get("/billing/sales/99999", headers=auth_headers)

        assert response.status_code == 404


@pytest.mark.integration
class TestSaleValidation:
    """Test sale data validation."""

    def test_create_sale_negative_quantity(self, client: TestClient, auth_headers, settings, product):
        """Sale with negative quantity → 422."""
        sale_data = {
            "customer_id": None,
            "items": [{"product_id": product.id, "quantity": -5}],
            "discount_amount": 0,
            "payment_method": "cash"
        }

        response = client.post("/billing/sales", json=sale_data, headers=auth_headers)

        assert response.status_code == 422

    def test_create_sale_negative_discount(self, client: TestClient, auth_headers, settings, product):
        """Sale with negative discount → 422."""
        sale_data = {
            "customer_id": None,
            "items": [{"product_id": product.id, "quantity": 1}],
            "discount_amount": -10.0,
            "payment_method": "cash"
        }

        response = client.post("/billing/sales", json=sale_data, headers=auth_headers)

        assert response.status_code == 422

    def test_create_sale_invalid_payment_method(self, client: TestClient, auth_headers, settings, product):
        """Sale with invalid payment method → 422."""
        sale_data = {
            "customer_id": None,
            "items": [{"product_id": product.id, "quantity": 1}],
            "discount_amount": 0,
            "payment_method": "invalid_method"
        }

        response = client.post("/billing/sales", json=sale_data, headers=auth_headers)

        assert response.status_code == 422

    def test_create_sale_empty_items(self, client: TestClient, auth_headers, settings):
        """Sale with empty items list → 422."""
        sale_data = {
            "customer_id": None,
            "items": [],
            "discount_amount": 0,
            "payment_method": "cash"
        }

        response = client.post("/billing/sales", json=sale_data, headers=auth_headers)

        assert response.status_code == 422


@pytest.mark.integration
class TestFeatureGating:
    """Test feature flag enforcement for billing features."""

    def test_billing_disabled_returns_403(self, client: TestClient, auth_headers, settings, product, session, monkeypatch):
        """Disable billing feature, verify endpoint returns 403.

        Feature flags are now derived from the license at runtime (see
        core/features.py) — settings.feature_flags is just a display mirror
        and is no longer read for enforcement, so the gate itself is
        exercised here by patching the authoritative flag source.
        """
        import src.core.features as features_module
        original_flags = features_module.get_effective_feature_flags()
        monkeypatch.setattr(
            features_module, "get_effective_feature_flags",
            lambda: {**original_flags, "billing": False}
        )

        sale_data = {
            "customer_id": None,
            "items": [{"product_id": product.id, "quantity": 1}],
            "discount_amount": 0,
            "payment_method": "cash"
        }

        response = client.post("/billing/sales", json=sale_data, headers=auth_headers)

        # Should be forbidden due to feature flag
        assert response.status_code == 403
        assert "not enabled" in response.json()["detail"].lower()

    def test_premium_reports_disabled_returns_403(self, client: TestClient, auth_headers, settings, session):
        """No license loaded -> falls back to the basic tier, which does not
        include premium_reports. Confirms the license-derived gate denies
        access by default rather than trusting the (now-ignored) settings row."""
        # Try to access P&L report (Premium feature)
        response = client.get(
            "/reports/profit-loss?start_date=2026-01-01&end_date=2026-12-31",
            headers=auth_headers
        )

        assert response.status_code == 403

    def test_settings_put_cannot_override_feature_flags(self, client: TestClient, auth_headers, settings, session):
        """A client cannot re-enable a premium feature by PUTting
        feature_flags through /settings/ (the historical licensing bypass).
        The field must be silently ignored on write."""
        payload = {
            **settings.model_dump(mode="json", exclude={"id", "created_at", "updated_at"}),
            "feature_flags": {**settings.feature_flags, "premium_reports": True},
        }
        response = client.put("/settings/", json=payload, headers=auth_headers)
        assert response.status_code == 200

        # The feature gate must still deny access — the write had no effect.
        report_response = client.get(
            "/reports/profit-loss?start_date=2026-01-01&end_date=2026-12-31",
            headers=auth_headers
        )
        assert report_response.status_code == 403


@pytest.mark.integration
class TestDashboardMetrics:
    """Test dashboard metrics endpoint."""

    def test_get_dashboard_metrics(self, client: TestClient, auth_headers, settings, product):
        """GET /dashboard/metrics returns aggregated metric cards."""
        # Create some sales first (product fixture starts with 50 in stock)
        for i in range(3):
            sale_data = {
                "customer_id": None,
                "items": [{"product_id": product.id, "quantity": 1}],
                "discount_amount": 0,
                "payment_method": "cash"
            }
            resp = client.post("/billing/sales", json=sale_data, headers=auth_headers)
            assert resp.status_code == 200

        response = client.get("/dashboard/metrics", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "cards" in data and len(data["cards"]) == 4
        assert "recent_sales" in data
        assert len(data["recent_sales"]) >= 3
        # Today's Revenue card reflects the completed sales
        revenue_card = data["cards"][0]
        assert revenue_card["title"] == "Today's Revenue"

    def test_get_dashboard_trends(self, client: TestClient, auth_headers, settings, product):
        """GET /dashboard/trends returns a 30-day revenue series (zero-filled)
        plus a payment-method breakdown reflecting completed sales."""
        sale_data = {
            "customer_id": None,
            "items": [{"product_id": product.id, "quantity": 1}],
            "discount_amount": 0,
            "payment_method": "card"
        }
        resp = client.post("/billing/sales", json=sale_data, headers=auth_headers)
        assert resp.status_code == 200

        response = client.get("/dashboard/trends", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data["daily_revenue"]) == 30
        # Today (the last point) must reflect the sale just created
        assert float(data["daily_revenue"][-1]["revenue"]) > 0
        assert any(p["method"] == "card" and p["count"] == 1 for p in data["payment_breakdown"])


@pytest.mark.integration
class TestInventoryIntegration:
    """Test inventory-related endpoints."""

    def test_create_product(self, client: TestClient, auth_headers, category):
        """POST /inventory/products creates new product (with INITIAL ledger entry)."""
        product_data = {
            "name": "New Product",
            "barcode": "9999999999",
            "category_id": category.id,
            "selling_price": 200.0,
            "cost_price": 120.0,
            "stock_quantity": 50,
            "low_stock_threshold": 10
        }

        response = client.post("/inventory/products", json=product_data, headers=auth_headers)

        assert response.status_code in [200, 201]
        data = response.json()
        assert data["name"] == "New Product"
        assert data["barcode"] == "9999999999"
        assert data["stock_quantity"] == 50

        # Opening stock must be recorded in the movement ledger
        movements = client.get(
            f"/inventory/products/{data['id']}/movements", headers=auth_headers
        )
        assert movements.status_code == 200
        items = movements.json()["items"]
        assert len(items) == 1
        assert items[0]["reason"] == "initial"
        assert items[0]["change"] == 50

    def test_list_products(self, client: TestClient, auth_headers, product):
        """GET /inventory/products returns paginated product list."""
        response = client.get("/inventory/products", headers=auth_headers)

        assert response.status_code == 200
        body = response.json()
        assert isinstance(body["items"], list)
        assert len(body["items"]) > 0
        assert body["pagination"]["total_count"] >= 1

    def test_update_product_stock(self, client: TestClient, auth_headers, product):
        """PUT /inventory/products/{id} updates stock and logs an adjustment."""
        update_data = {"stock_quantity": 100}

        response = client.put(f"/inventory/products/{product.id}", json=update_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["stock_quantity"] == 100

        # Manual stock change must appear in the ledger as an adjustment
        movements = client.get(
            f"/inventory/products/{product.id}/movements", headers=auth_headers
        )
        assert movements.status_code == 200
        items = movements.json()["items"]
        assert any(m["reason"] == "adjustment" and m["change"] == 50 for m in items)
