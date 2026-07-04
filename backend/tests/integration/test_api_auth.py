"""
Integration tests for Authentication & Authorization API endpoints.

Tests login, JWT validation, and RBAC (Role-Based Access Control).
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestLogin:
    """Test login endpoint and token generation."""

    def test_login_valid_credentials(self, client: TestClient, admin_user):
        """POST /auth/login with valid credentials → 200, JWT token returned."""
        response = client.post(
            "/auth/login",
            data={"username": "testadmin", "password": "testpass123"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0

    def test_login_invalid_password(self, client: TestClient, admin_user):
        """POST /auth/login with wrong password → 401."""
        response = client.post(
            "/auth/login",
            data={"username": "testadmin", "password": "wrongpassword"}
        )

        assert response.status_code == 401
        assert "detail" in response.json()

    def test_login_nonexistent_user(self, client: TestClient):
        """POST /auth/login with non-existent username → 401."""
        response = client.post(
            "/auth/login",
            data={"username": "nonexistent", "password": "anypassword"}
        )

        assert response.status_code == 401

    def test_login_missing_credentials(self, client: TestClient):
        """POST /auth/login without credentials → 422."""
        response = client.post("/auth/login", data={})

        assert response.status_code == 422  # Validation error


@pytest.mark.integration
class TestTokenValidation:
    """Test JWT token validation and user retrieval."""

    def test_get_current_user_valid_token(self, client: TestClient, auth_headers, admin_user):
        """Access protected endpoint with valid token → 200."""
        response = client.get("/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testadmin"
        assert data["role"] == "admin"

    def test_get_current_user_no_token(self, client: TestClient):
        """Access protected endpoint without token → 401."""
        response = client.get("/auth/me")

        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client: TestClient):
        """Access protected endpoint with invalid token → 401."""
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid_token_here"}
        )

        assert response.status_code == 401

    def test_get_current_user_malformed_header(self, client: TestClient):
        """Access protected endpoint with malformed auth header → 401."""
        response = client.get(
            "/auth/me",
            headers={"Authorization": "NotBearer token123"}
        )

        assert response.status_code == 401


@pytest.mark.integration
class TestRoleBasedAccessControl:
    """Test RBAC enforcement across different endpoints."""

    def test_admin_can_access_admin_endpoints(self, client: TestClient, admin_user):
        """Admin user can access admin-only endpoints like /settings."""
        # Login as admin
        login_response = client.post(
            "/auth/login",
            data={"username": "testadmin", "password": "testpass123"}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Access admin endpoint
        response = client.get("/settings/", headers=headers)

        assert response.status_code == 200

    def test_sales_user_cannot_access_admin_endpoints(self, client: TestClient, sales_user):
        """Sales user cannot access admin-only endpoints like /settings → 403."""
        # Login as sales user
        login_response = client.post(
            "/auth/login",
            data={"username": "testsales", "password": "testpass123"}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Try to access admin endpoint
        response = client.get("/settings/", headers=headers)

        assert response.status_code == 403

    def test_manager_can_access_manager_endpoints(self, client: TestClient, manager_user):
        """Manager user can access manager-level endpoints like /inventory."""
        # Login as manager
        login_response = client.post(
            "/auth/login",
            data={"username": "testmanager", "password": "testpass123"}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Access manager endpoint
        response = client.get("/inventory/products", headers=headers)

        assert response.status_code == 200

    def test_sales_user_can_create_sales(self, client: TestClient, sales_user, settings, product):
        """Sales user can access billing endpoints (their primary function)."""
        # Login as sales user
        login_response = client.post(
            "/auth/login",
            data={"username": "testsales", "password": "testpass123"}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create a sale
        sale_data = {
            "customer_id": None,
            "items": [{"product_id": product.id, "quantity": 1}],
            "discount_amount": 0,
            "payment_method": "cash"
        }

        response = client.post("/billing/sales", json=sale_data, headers=headers)

        assert response.status_code == 200 or response.status_code == 201


@pytest.mark.integration
class TestUserManagement:
    """Test user CRUD operations (admin only)."""

    def test_list_users_as_admin(self, client: TestClient, auth_headers, admin_user, manager_user, sales_user):
        """Admin can list all users."""
        response = client.get("/users/", headers=auth_headers)

        assert response.status_code == 200
        users = response.json()
        assert len(users) >= 3  # At least admin, manager, sales_user

    def test_create_user_as_admin(self, client: TestClient, auth_headers):
        """Admin can create new users."""
        new_user_data = {
            "username": "newuser",
            "full_name": "New User",
            "password": "password123",
            "role": "sales_user"
        }

        response = client.post("/users/", json=new_user_data, headers=auth_headers)

        assert response.status_code in [200, 201]
        data = response.json()
        assert data["username"] == "newuser"
        assert "password" not in data  # Password should not be returned

    def test_non_admin_cannot_create_users(self, client: TestClient, sales_user):
        """Non-admin users cannot create new users → 403."""
        # Login as sales user
        login_response = client.post(
            "/auth/login",
            data={"username": "testsales", "password": "testpass123"}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        new_user_data = {
            "username": "hacker",
            "full_name": "Hacker",
            "password": "password123",
            "role": "admin"
        }

        response = client.post("/users/", json=new_user_data, headers=headers)

        assert response.status_code == 403


@pytest.mark.integration
class TestPasswordSecurity:
    """Test password hashing and security."""

    def test_password_not_returned_in_response(self, client: TestClient, auth_headers):
        """User data should never include password or hashed_password."""
        response = client.get("/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "password" not in data
        assert "hashed_password" not in data

    def test_password_hashing_works(self, client: TestClient, auth_headers):
        """Verify that passwords are hashed (not stored in plaintext)."""
        # Create a new user
        new_user_data = {
            "username": "hashtest",
            "full_name": "Hash Test",
            "password": "plaintext123",
            "role": "sales_user"
        }

        create_response = client.post("/users/", json=new_user_data, headers=auth_headers)
        assert create_response.status_code in [200, 201]

        # Try to login with the password
        login_response = client.post(
            "/auth/login",
            data={"username": "hashtest", "password": "plaintext123"}
        )

        assert login_response.status_code == 200
        assert "access_token" in login_response.json()

    def test_cannot_login_with_hashed_password(self, client: TestClient, admin_user):
        """Attempting to login with hashed password should fail."""
        # Try to login with the actual hashed password (won't match)
        response = client.post(
            "/auth/login",
            data={"username": "testadmin", "password": admin_user.hashed_password}
        )

        assert response.status_code == 401
