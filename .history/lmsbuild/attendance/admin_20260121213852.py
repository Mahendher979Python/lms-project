from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "date",
        "login_time",
        "logout_time",
        "status",
        "marked_by",
    )

    list_filter = (
        "role",
        "status",
        "date",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    ordering = ("-date",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("User Info", {
            "fields": ("user", "role", "date")
        }),
        ("Attendance Info", {
            "fields": ("login_time", "logout_time", "status")
        }),
        ("System Info", {
            "fields": ("marked_by", "created_at", "updated_at")
        }),
    )

    def save_model(self, request, obj, form, change):
        # If admin edits attendance
        if change:
            obj.marked_by = "admin"
        super().save_model(request, obj, form, change)
