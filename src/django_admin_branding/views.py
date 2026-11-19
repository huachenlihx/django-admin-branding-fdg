from django.http import Http404
from django.views.generic.base import RedirectView

from . import conf


class FaviconView(RedirectView):
    """Redirect /favicon.ico to the configured ADMIN_BRANDING["FAVICON"]."""

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        url = conf.resolve_url(conf.get("FAVICON"))
        if not url:
            raise Http404("No favicon configured.")
        return url
