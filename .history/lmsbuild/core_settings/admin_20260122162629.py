from django.contrib import admin
from .models import AdminSettings


@admin.register(AdminSettings)
class AdminSettingsAdmin(admin.ModelAdmin):
    """
    Admin Global Settings
    - Only ONE row allowed (Singleton)
    """

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ("site_name", "attendance_enabled", "maintenance_mode", "updated_at")
