from django.contrib import admin
from django.urls import include, path


class CustomAdminSite(admin.AdminSite):
    site_header = "Custom Site Header"
    site_title = "Custom Site Title"


custom_admin_site = CustomAdminSite(name="custom_admin")

urlpatterns = [
    path("", include("django_admin_branding.urls")),
    path("admin/", admin.site.urls),
    path("custom-admin/", custom_admin_site.urls),
]
