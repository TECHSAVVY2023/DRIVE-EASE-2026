from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Accounts, AdminActivityLog


class AssignAccountRoleTests(APITestCase):
    def setUp(self):
        self.admin = Accounts.objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            password="test-password",
            is_staff=True,
        )
        self.user = Accounts.objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="test-password",
        )
        self.url = reverse(
            "account-assign-role",
            kwargs={"user_id": self.user.pk},
        )

    def test_admin_can_assign_admin_role(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {"role": "Admin"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(
            AdminActivityLog.objects.filter(
                admin=self.admin,
                target_type="user",
                target_id=str(self.user.pk),
            ).exists()
        )

    def test_regular_user_cannot_assign_roles(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            reverse(
                "account-assign-role",
                kwargs={"user_id": self.admin.pk},
            ),
            {"role": "User"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_admin_cannot_assign_super_admin_role(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {"role": "Super Admin"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_super_admin_can_assign_super_admin_role(self):
        super_admin = Accounts.objects.create_superuser(
            username="owner@example.com",
            email="owner@example.com",
            password="test-password",
        )
        self.client.force_authenticate(super_admin)

        response = self.client.patch(
            self.url,
            {"role": "Super Admin"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)

    def test_admin_cannot_change_own_role(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            reverse(
                "account-assign-role",
                kwargs={"user_id": self.admin.pk},
            ),
            {"role": "User"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class LogoutTests(APITestCase):
    def setUp(self):
        self.user = Accounts.objects.create_user(
            username="logout@example.com",
            email="logout@example.com",
            password="test-password",
        )
        self.url = reverse("auth-logout")

    def test_logout_blacklists_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies[settings.JWT_REFRESH_COOKIE_NAME] = str(refresh)

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(
            BlacklistedToken.objects.filter(token__jti=refresh["jti"]).exists()
        )

    def test_logout_is_safe_without_a_valid_token(self):
        self.client.cookies[settings.JWT_REFRESH_COOKIE_NAME] = "not-a-token"
        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RefreshCookieTests(APITestCase):
    def setUp(self):
        self.user = Accounts.objects.create_user(
            username="refresh@example.com",
            email="refresh@example.com",
            password="test-password",
        )
        self.url = reverse("token-refresh")

    def test_refresh_uses_httponly_cookie_and_rotates_it(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies[settings.JWT_REFRESH_COOKIE_NAME] = str(refresh)

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertNotIn("refresh", response.data)

        cookie = response.cookies[settings.JWT_REFRESH_COOKIE_NAME]
        self.assertTrue(cookie["httponly"])
        self.assertEqual(cookie["path"], settings.JWT_REFRESH_COOKIE_PATH)
        self.assertNotEqual(cookie.value, str(refresh))

    def test_refresh_token_in_request_body_is_rejected(self):
        refresh = RefreshToken.for_user(self.user)

        response = self.client.post(
            self.url,
            {"refresh": str(refresh)},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_rejects_unapproved_browser_origin(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies[settings.JWT_REFRESH_COOKIE_NAME] = str(refresh)

        response = self.client.post(
            self.url,
            {},
            format="json",
            HTTP_ORIGIN="https://attacker.example",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
