"""
Integration tests for Phase 3 (security & licensing hardening):
- /auth/login no longer leaks hashed_password and enforces rate limiting
- get_current_user rejects deactivated users and no longer accepts a
  token via query parameter
- feature flags are derived from the license, not the mutable settings row
- /system/restore rejects path traversal and unknown filenames
- forced password change on the bootstrap admin account
"""

import os
import pytest
from fastapi.testclient import TestClient

from src.core.security import get_password_hash
from src.models.core import User, UserRole


@pytest.mark.integration
class TestLoginHardening:
    def test_login_response_never_leaks_hashed_password(self, client: TestClient, admin_user):
        response = client.post(
            "/auth/login",
            data={"username": "testadmin", "password": "testpass123"}
        )
        assert response.status_code == 200
        body = response.json()
        assert "hashed_password" not in body
        assert "hashed_password" not in body["user"]
        assert body["user"]["username"] == "testadmin"
        assert "must_change_password" in body

    def test_login_rate_limited_after_repeated_failures(self, client: TestClient, session):
        user = User(
            username="lockout_target",
            full_name="Lockout Target",
            role=UserRole.SALES,
            hashed_password=get_password_hash("correct-password"),
        )
        session.add(user)
        session.commit()

        for _ in range(5):
            r = client.post(
                "/auth/login",
                data={"username": "lockout_target", "password": "wrong"}
            )
            assert r.status_code == 401

        # 6th attempt, even with the CORRECT password, is locked out.
        r = client.post(
            "/auth/login",
            data={"username": "lockout_target", "password": "correct-password"}
        )
        assert r.status_code == 429

    def test_token_query_param_no_longer_authenticates(self, client: TestClient, auth_headers):
        token = auth_headers["Authorization"].split(" ")[1]
        response = client.get(f"/auth/me?token={token}")
        assert response.status_code == 401

    def test_inactive_user_rejected(self, client: TestClient, session, auth_headers):
        user = User(
            username="deactivate_me",
            full_name="Soon Inactive",
            role=UserRole.SALES,
            hashed_password=get_password_hash("testpass123"),
        )
        session.add(user)
        session.commit()

        login = client.post(
            "/auth/login",
            data={"username": "deactivate_me", "password": "testpass123"}
        )
        assert login.status_code == 200
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        # Confirm the token works before deactivation.
        assert client.get("/auth/me", headers=headers).status_code == 200

        user.is_active = False
        session.add(user)
        session.commit()

        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401


@pytest.mark.integration
class TestForcedPasswordChange:
    def test_admin_reset_forces_password_change(self, client: TestClient, auth_headers, sales_user):
        """When an admin resets another user's password, that user must
        change it on their next login."""
        response = client.put(
            f"/users/{sales_user.id}",
            json={
                "username": sales_user.username,
                "full_name": sales_user.full_name,
                "role": "sales",
                "is_active": True,
                "password": "admin-reset-password123",
            },
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["must_change_password"] is True

        login = client.post(
            "/auth/login",
            data={"username": sales_user.username, "password": "admin-reset-password123"}
        )
        assert login.status_code == 200
        assert login.json()["must_change_password"] is True

    def test_self_service_change_password_clears_flag(self, client: TestClient, session):
        user = User(
            username="first_login_user",
            full_name="First Login",
            role=UserRole.SALES,
            hashed_password=get_password_hash("temp-password123"),
            must_change_password=True,
        )
        session.add(user)
        session.commit()

        login = client.post(
            "/auth/login",
            data={"username": "first_login_user", "password": "temp-password123"}
        )
        assert login.json()["must_change_password"] is True
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        response = client.post(
            "/users/me/change-password",
            json={"current_password": "temp-password123", "new_password": "new-strong-password123"},
            headers=headers,
        )
        assert response.status_code == 200

        relogin = client.post(
            "/auth/login",
            data={"username": "first_login_user", "password": "new-strong-password123"}
        )
        assert relogin.status_code == 200
        assert relogin.json()["must_change_password"] is False

    def test_change_password_rejects_wrong_current_password(self, client: TestClient, auth_headers):
        response = client.post(
            "/users/me/change-password",
            json={"current_password": "not-the-real-password", "new_password": "whatever12345"},
            headers=auth_headers,
        )
        assert response.status_code == 401


@pytest.mark.integration
class TestLicenseDerivedFeatureFlags:
    def test_premium_feature_denied_without_license(self, client: TestClient, auth_headers, settings, session):
        response = client.get(
            "/reports/profit-loss?start_date=2026-01-01&end_date=2026-12-31",
            headers=auth_headers,
        )
        assert response.status_code == 403

    def test_premium_feature_allowed_with_premium_license(self, client: TestClient, auth_headers, settings, premium_license):
        response = client.get(
            "/reports/profit-loss?start_date=2026-01-01&end_date=2026-12-31",
            headers=auth_headers,
        )
        assert response.status_code == 200


@pytest.mark.integration
class TestRestoreBackupHardening:
    def test_restore_rejects_path_traversal_filename(self, client: TestClient, auth_headers, premium_license):
        response = client.post(
            "/system/restore",
            params={"backup_filename": "../../../../windows/system32/config"},
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_restore_rejects_unknown_filename(self, client: TestClient, auth_headers, premium_license):
        response = client.post(
            "/system/restore",
            params={"backup_filename": "nonexistent_backup.db"},
            headers=auth_headers,
        )
        assert response.status_code == 404
