from django.urls import path

from .views import FaviconView

urlpatterns = [
    path("favicon.ico", FaviconView.as_view(), name="admin-branding-favicon"),
]
