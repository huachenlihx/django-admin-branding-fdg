"""Additional regression coverage for Django admin branding."""

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from django_admin_branding.conf import get, resolve_url


class ConfigurationTests(TestCase):
    @override_settings(ADMIN_BRANDING={})
    def test_unknown_option_rejected(self):
        with self.assertRaises(KeyError):
            get("UNKNOWN_SETTING")

    @override_settings(ADMIN_BRANDING={"LOGIN_LOGO_MAX_WIDTH": "180px"})
    def test_configured_option(self):
        self.assertEqual(get("LOGIN_LOGO_MAX_WIDTH"), "180px")

    def test_url_variants(self):
        self.assertEqual(resolve_url(None), "")
        self.assertEqual(resolve_url(""), "")
        self.assertEqual(resolve_url("images/logo.png"), "/static/images/logo.png")
        for value in (
            "/media/logo.png",
            "https://cdn.example.com/logo.png",
            "//cdn.example.com/logo.png",
            "data:image/png;base64,AAAA",
        ):
            with self.subTest(value=value):
                self.assertEqual(resolve_url(value), value)


class AuthenticatedAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username="branding-admin", email="admin@example.com", password="test-password-123"
        )

    @override_settings(ADMIN_BRANDING={
        "SITE_HEADER": "Branded Administration",
        "SITE_TITLE": "Branded Browser Title",
        "FAVICON": "images/favicon.png",
    })
    def test_authenticated_admin_index(self):
        self.client.force_login(self.user)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn("Branded Administration", html)
        self.assertIn("Branded Browser Title", html)
        self.assertIn('href="/static/images/favicon.png"', html)

    @override_settings(ADMIN_BRANDING={})
    def test_custom_admin_site_fallback(self):
        self.client.force_login(self.user)
        response = self.client.get("/custom-admin/")
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn("Custom Site Header", html)
        self.assertIn("Custom Site Title", html)

    @override_settings(ADMIN_BRANDING={"FAVICON": "/media/site-icon.ico"})
    def test_media_favicon_redirect_not_permanent(self):
        response = self.client.get("/favicon.ico")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/media/site-icon.ico")
