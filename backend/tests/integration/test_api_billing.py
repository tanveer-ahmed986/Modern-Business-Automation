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
        assert data["grand_total"] > 0

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
        # Account for tax
        assert data["total_amount"] == pytest.approx(float(expected_total), rel=1e-2)

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

        # List sales
        response = client.get("/billing/sales", headers=auth_headers)

        assert response.status_code == 200
        sales = response.json()
        assert isinstance(sales, list)
        assert len(sales) > 0

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

    def test_billing_disabled_returns_403(self, client: TestClient, auth_headers, settings, product, session):
        """Disable billing feature, verify endpoint returns 403."""
        # Disable billing feature
        settings.feature_flags["billing"] = False
        session.add(settings)
        session.commit()

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
        """Disable premium_reports feature, verify P&L endpoint returns 403."""
        # Disable premium reports
        settings.feature_flags["premium_reports"] = False
        session.add(settings)
        session.commit()

        # Try to access P&L report (Premium feature)
        response = client.get(
            "/reports/profit-loss?start_date=2026-01-01&end_date=2026-12-31",
            headers=auth_headers
        )

        assert response.status_code == 403


@pytest.mark.integration
class TestDashboardMetrics:
    """Test dashboard metrics endpoint."""

    def test_get_dashboard_metrics(self, client: TestClient, auth_headers, settings, product):
        """GET /dashboard/metrics returns aggregated metrics."""
        # Create some sales first
        for i in range(3):
            sale_data = {
                "customer_id": None,
                "items": [{"product_id": product.id, "quantity": 1}],
                "discount_amount": 0,
                "payment_method": "cash"
            }
            client.post("/billing/sales", json=sale_data, headers=auth_headers)
            # Refresh product stock for next sale
            from src.core.db import get_session
            with get_session() as sess:
                from src.models.inventory import Product
                p = sess.get(Product, product.id)
                p.stock_quantity += 1
                sess.add(p)
                sess.commit()

        response = client.get("/dashboard/metrics", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "total_sales" in data or "revenue" in data


@pytest.mark.integration
class TestInventoryIntegration:
    """Test inventory-related endpoints."""

    def test_create_product(self, client: TestClient, auth_headers, category):
        """POST /inventory/products creates new product."""
        product_data = {
            "name": "New Product",
            "sku": "NEW-001",
            "barcode": "9999999999",
            "category_id": category.id,
            "selling_price": 200.0,
            "cost_price": 120.0,
            "stock_quantity": 50,
            "reorder_level": 10,
            "unit": "pcs"
        }

        response = client.post("/inventory/products", json=product_data, headers=auth_headers)

        assert response.status_code in [200, 201]
        data = response.json()
        assert data["name"] == "New Product"
        assert data["sku"] == "NEW-001"

    def test_list_products(self, client: TestClient, auth_headers, product):
        """GET /inventory/products returns product list."""
        response = client.get("/inventory/products", headers=auth_headers)

        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert len(products) > 0

    def test_update_product_stock(self, client: TestClient, auth_headers, product):
        """PUT /inventory/products/{id} updates product stock."""
        update_data = {
            "name": product.name,
            "sku": product.sku,
            "category_id": product.category_id,
            "selling_price": product.selling_price,
            "cost_price": product.cost_price,
            "stock_quantity": 100,  # Updated stock
            "reorder_level": product.reorder_level,
            "unit": product.unit
        }

        response = client.put(f"/inventory/products/{product.id}", json=update_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["stock_quantity"] == 100
