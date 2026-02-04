from django.contrib import admin
from .models import AdminSettings

# Register your models here.
@admin.register(AdminSettings)
class AdminSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
