"""Settings access. Configure with ``ADMIN_BRANDING = {...}`` in settings.py."""
from django.conf import settings
from django.templatetags.static import static

DEFAULTS = {
    # Text shown in the header bar (falls back to admin.site.site_header)
    "SITE_HEADER": None,
    # Text appended to the browser tab title (falls back to admin.site.site_title)
    "SITE_TITLE": None,
    # Image shown between the header and the login form.
    # A static path ("images/logo.png"), an absolute URL, or a "/media/..." path.
    "LOGIN_LOGO": None,
    "LOGIN_LOGO_ALT": None,  # defaults to SITE_HEADER
    "LOGIN_LOGO_MAX_WIDTH": "220px",
    # Favicon: same rules as LOGIN_LOGO. Used for <link rel="icon"> and /favicon.ico
    "FAVICON": None,
}


def get(name):
    if name not in DEFAULTS:
        raise KeyError(f"Unknown ADMIN_BRANDING option: {name!r}")
    user = getattr(settings, "ADMIN_BRANDING", None) or {}
    return user.get(name, DEFAULTS[name])


def resolve_url(value):
    """Turn a static path or an absolute URL into a usable URL (\"\" if unset)."""
    if not value:
        return ""
    if value.startswith(("http://", "https://", "//", "/", "data:")):
        return value
    return static(value)
