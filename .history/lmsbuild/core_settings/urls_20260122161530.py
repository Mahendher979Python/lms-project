from django.urls import path
from .views import admin_settings_view

urlpatterns = [
    path("admin/settings/", admin_settings_view, name="admin_settings"),
]
