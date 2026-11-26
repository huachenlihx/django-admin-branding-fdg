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


class ThemeToggleTests(TestCase):
    """The branding override must keep Django's theme toggle on the login page."""

    def test_login_page_has_theme_toggle(self):
        response = self.client.get("/admin/login/")
        self.assertContains(response, 'class="theme-toggle"')

    @override_settings(ADMIN_BRANDING={"SITE_HEADER": "Acme Admin"})
    def test_toggle_present_with_custom_header(self):
        response = self.client.get("/admin/login/")
        self.assertContains(response, "Acme Admin")
        self.assertContains(response, 'class="theme-toggle"')


class LoginFooterTests(TestCase):
    """An optional footer must be restricted to the admin login page."""

    @override_settings(ADMIN_BRANDING={})
    def test_no_footer_by_default(self):
        response = self.client.get("/admin/login/")
        self.assertNotContains(response, 'class="fdg-admin-footer"')

    @override_settings(ADMIN_BRANDING={"FOOTER_LINES": []})
    def test_empty_footer_is_hidden(self):
        response = self.client.get("/admin/login/")
        self.assertNotContains(response, 'class="fdg-admin-footer"')

    @override_settings(ADMIN_BRANDING={
        "FOOTER_LINES": [
            "© 2026 Example Ltd.",
            'Built by <a href="https://example.com/"><strong>Example</strong></a>',
            "Third line",
        ],
    })
    def test_footer_lines_and_trusted_html(self):
        response = self.client.get("/admin/login/")
        self.assertContains(response, 'class="fdg-admin-footer"')
        self.assertContains(response, "© 2026 Example Ltd.")
        self.assertContains(response, '<a href="https://example.com/"><strong>Example</strong></a>', html=False)
        self.assertContains(response, "Third line")
        self.assertContains(response, 'class="fdg-admin-footer-line"', count=3)
        self.assertContains(response, 'var(--header-bg, #417690)')
        self.assertContains(response, 'var(--header-color, #fff)')

    @override_settings(ADMIN_BRANDING={
        "FOOTER_LINES": ["Company footer"],
        "FOOTER_BACKGROUND_COLOR": "#123456",
        "FOOTER_TEXT_COLOR": "#ffffff",
    })
    def test_explicit_footer_colors(self):
        response = self.client.get("/admin/login/")
        self.assertContains(response, 'background-color: #123456; color: #ffffff;')

    @override_settings(ADMIN_BRANDING={"FOOTER_LINES": ["Public login only"]})
    def test_authenticated_admin_has_no_footer(self):
        user = get_user_model().objects.create_superuser(
            username="footer-admin", email="footer@example.com", password="test-password-123"
        )
        self.client.force_login(user)
        response = self.client.get("/admin/")
        self.assertNotContains(response, "Public login only")
        self.assertNotContains(response, 'class="fdg-admin-footer"')
