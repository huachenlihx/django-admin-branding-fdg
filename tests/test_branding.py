from django.test import TestCase, override_settings

CFG = {
    "SITE_HEADER": "United Supermarket Administration",
    "SITE_TITLE": "United Admin",
    "LOGIN_LOGO": "images/logo.jpg",
    "FAVICON": "unitedicon_32.png",
}


class LoginPageTests(TestCase):
    @override_settings(ADMIN_BRANDING=CFG)
    def test_login_page_is_branded(self):
        html = self.client.get("/admin/login/?next=/admin/").content.decode()
        self.assertIn("United Supermarket Administration", html)
        self.assertIn('src="/static/images/logo.jpg"', html)
        self.assertIn("| United Admin</title>", html)
        self.assertIn('rel="icon" href="/static/unitedicon_32.png"', html)
        # logo sits between header and form
        self.assertLess(html.index("United Supermarket Administration"),
                        html.index("logo.jpg"))
        self.assertLess(html.index("logo.jpg"), html.index("<form"))

    @override_settings(ADMIN_BRANDING={})
    def test_defaults_fall_back_to_django(self):
        html = self.client.get("/admin/login/").content.decode()
        self.assertIn("Django administration", html)
        self.assertNotIn("<img", html)
        self.assertNotIn('rel="icon"', html)

    @override_settings(ADMIN_BRANDING={"LOGIN_LOGO": "https://cdn.example.com/a.png"})
    def test_absolute_url_not_staticified(self):
        html = self.client.get("/admin/login/").content.decode()
        self.assertIn('src="https://cdn.example.com/a.png"', html)


class FaviconViewTests(TestCase):
    @override_settings(ADMIN_BRANDING=CFG)
    def test_redirects(self):
        r = self.client.get("/favicon.ico")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r["Location"], "/static/unitedicon_32.png")

    @override_settings(ADMIN_BRANDING={})
    def test_404_when_unset(self):
        self.assertEqual(self.client.get("/favicon.ico").status_code, 404)
