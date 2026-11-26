# Django Admin Branding FDG

**Distribution:** `django-admin-branding-fdg`  
**Python import:** `django_admin_branding`  
**Version:** `0.2.0`  
**License:** MIT

Customize the look of Django's built-in admin without copying branding templates between projects. Configure the admin header, browser title, a logo above the login form, a favicon, and an optional HTML footer on the admin login page in one `ADMIN_BRANDING` setting.

**Features**

- Custom admin site header and browser-tab title.
- Optional logo on the admin login page, with configurable alt text and maximum width.
- Favicon links on admin pages and an optional `/favicon.ico` redirect.
- Static-file paths, absolute paths, and external/CDN URLs for images.
- Optional multi-line HTML footer on the login page with header-matching theme colors by default.
- No extra runtime dependencies beyond Django.

## Requirements

- Python 3.10 or newer.
- Django 5.2 or newer, subject to the Python requirements of the installed Django version.

The package declares support for Django 5.2, 6.0, and 6.1. Choose a Django version compatible with your Python version.

## Quick start

**1. Install**

```bash
python -m pip install django-admin-branding-fdg
```

The distribution name has the `-fdg` suffix, but the Python import and Django app name remain `django_admin_branding`.

**2. Configure `settings.py`**

Place `django_admin_branding` **before** `django.contrib.admin` so that Django finds this package's admin templates first. Keep your other installed apps and existing settings.

```python
INSTALLED_APPS = [
    "django_admin_branding",  # must be before django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # ...your other apps...
]

ADMIN_BRANDING = {
    "SITE_HEADER": "My Company Administration",
    "SITE_TITLE": "My Company Admin",
    "LOGIN_LOGO": "images/logo.png",
    "LOGIN_LOGO_ALT": "My Company",
    "LOGIN_LOGO_MAX_WIDTH": "220px",
    "FAVICON": "images/favicon.png",
    # Optional login-page footer: omit or leave empty to hide it.
    "FOOTER_LINES": [
        "© 2026 My Company | London, ON, Canada",
        'Website Development by <a href="https://example.com/">My Company</a>',
    ],
    # Optional; omit to follow Django's admin header colors in light/dark mode.
    # "FOOTER_BACKGROUND_COLOR": "#417690",
    # "FOOTER_TEXT_COLOR": "#ffffff",
}

# If images are in your project-level static/ directory:
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
```

`BASE_DIR` in this example is the `pathlib.Path` value normally defined by Django's project template. If your images are already in an installed app's `static/` folder, you do not need to add `STATICFILES_DIRS`.

**3. Configure `urls.py`**

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("django_admin_branding.urls")),  # optional /favicon.ico endpoint
    path("admin/", admin.site.urls),
    # ...your other routes...
]
```

The URL include is **optional**: favicon `<link>` tags on admin pages work without it. Include it if you also want requests for `/favicon.ico` redirected to your configured favicon. Without a configured `FAVICON`, that endpoint responds with HTTP 404. It uses a temporary HTTP 302 redirect so browser caches are less likely to pin an outdated destination.

**4. Add your images**

For the example above, place the files here:

```text
myproject/
├── manage.py
├── static/
│   └── images/
│       ├── logo.png
│       └── favicon.png
└── ...
```

Start your application and visit `/admin/login/` to see the branding. Every `ADMIN_BRANDING` key is optional; with no overrides, Django's usual admin header/title are used, and no extra logo or favicon is shown.

## Configuration reference

| Setting | Default | Purpose |
| --- | --- | --- |
| `SITE_HEADER` | Django admin site's `site_header` | Text in the admin header |
| `SITE_TITLE` | Django admin site's `site_title` | Text appended to the page title in the browser tab |
| `LOGIN_LOGO` | `None` | Image displayed above the admin login form |
| `LOGIN_LOGO_ALT` | Site header fallback | Accessible alternative text for the logo |
| `LOGIN_LOGO_MAX_WIDTH` | `"220px"` | CSS `max-width` for the login logo |
| `FAVICON` | `None` | Icon URL used in admin `<link>` tags and by `/favicon.ico` |
| `FOOTER_LINES` | `[]` | Ordered list of footer lines displayed on the **login page only**; each entry may contain trusted HTML (e.g. `<a>`, `<strong>`) |
| `FOOTER_BACKGROUND_COLOR` | Unset | Footer background; by default uses `var(--header-bg, #417690)` and follows Django's light/dark theme |
| `FOOTER_TEXT_COLOR` | Unset | Footer text color; by default uses `var(--header-color, #fff)` and follows Django's light/dark theme |

Example with only a header and title:

```python
ADMIN_BRANDING = {
    "SITE_HEADER": "Operations Portal",
    "SITE_TITLE": "Operations Admin",
}
```

### Optional login-page footer

Set `FOOTER_LINES` to a list of strings. **One list item produces one line**, rendered in its own `<div>`, so HTML links, bold text, and other inline markup can be included. The footer appears on the Django admin **login page only**; it is not shown on authenticated admin pages. When `FOOTER_LINES` is omitted or empty, no custom footer is displayed.

```python
ADMIN_BRANDING = {
    "FOOTER_LINES": [
        "© 2026 My Company | London, ON, Canada",
        'Website Development by <a href="https://example.com/" target="_blank" rel="noopener noreferrer"><strong>My Company</strong></a>',
    ],
}
```

By default, the background and text color inherit Django's header color variables, including dark-mode changes. Set `FOOTER_BACKGROUND_COLOR` and/or `FOOTER_TEXT_COLOR` to CSS color values (such as `"#417690"`) only when you need to override them; a fixed override will no longer automatically follow the theme.

**Security:** Footer strings are rendered as **trusted HTML**. Only put HTML you control in `ADMIN_BRANDING`; never pass untrusted input, visitor content, or database fields into `FOOTER_LINES` without sanitization.

### Supported image locations

**Project static files:** set `LOGIN_LOGO` or `FAVICON` to a path relative to your staticfiles finders, such as `"images/logo.png"`. Django resolves the path using its `{% static %}` mechanism, including configured hashed/static storage URLs.

**App static files:** `myapp/static/images/logo.png` in an installed Django app can be referenced as `"images/logo.png"` (assuming no duplicate conflicting filename).

**Uploaded media or absolute paths:** values beginning with `/` are passed through, e.g. `"/media/branding/logo.png"`. Your app/server must serve that URL; the package does not manage media uploads.

**CDN or external URLs:** full `https://...`, `http://...`, protocol-relative `//...`, and `data:` URLs are also passed through unchanged. Use trusted image sources; prefer HTTPS for production.

For static paths, avoid supplying `static/` as part of the setting: use `"images/logo.png"`, not `"static/images/logo.png"`.

## Production deployment

The package doesn't serve image assets itself. Configure production static file hosting as you normally would for Django admin (for example, a web server, WhiteNoise, or a supported cloud storage backend).

```bash
python manage.py collectstatic --noinput
```

Check that the logo and favicon URLs load in a browser after deployment. If an image URL is under `/media/`, media serving must be configured separately from Django staticfiles. Also check that `/favicon.ico` is not intercepted by a web server route if you have enabled the optional redirect.

## Troubleshooting

**Branding is not appearing:** Check that `django_admin_branding` precedes `django.contrib.admin` in `INSTALLED_APPS`. A project-level `templates/admin/base_site.html` or `templates/admin/login.html` can override the package's versions; other admin-customization packages may also conflict.

**Logo or favicon is broken:** Verify the configured path matches a file discoverable by Django staticfiles. You can inspect it with `python manage.py findstatic images/logo.png`. In production, check your collected static assets and storage/CDN configuration; check `/media/` paths separately.

**Browser still shows an older favicon:** Browsers cache icons aggressively. Verify the new image URL, try a fresh browser session, and consider a versioned favicon filename. The optional `/favicon.ico` endpoint uses HTTP 302 (rather than a permanent redirect), but it cannot control browser icon caching.

**`/favicon.ico` responds with 404:** Add the optional URL include and set `ADMIN_BRANDING["FAVICON"]`. If the web server serves `/favicon.ico` directly, configure that server route appropriately.

**A custom `AdminSite` has different header text:** When `SITE_HEADER` or `SITE_TITLE` is unset, the templates use the current admin site's context value. Setting these options overrides that fallback.

## Project links

- Source repository: [GitHub](https://github.com/huachenlihx/django-admin-branding-fdg)
- Issues and feature requests: [GitHub Issues](https://github.com/huachenlihx/django-admin-branding-fdg/issues)

## Contact

**Email:** `huachenlihx@gmail.com`

## License

This project is licensed under the **MIT License**. See the [LICENSE](https://github.com/huachenlihx/django-admin-branding-fdg/blob/main/LICENSE) file for the full license text.
