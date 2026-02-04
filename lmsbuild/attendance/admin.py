from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    # ===== TABLE VIEW =====
    list_display = (
        "user",
        "role",
        "date",
        "login_time",
        "logout_time",
        "total_work_hours",
        "status",
        "marked_by",
    )

    # ===== FILTERS (Right side) =====
    list_filter = (
        "role",
        "status",
        "date",
        "marked_by",
    )

    # ===== SEARCH =====
    search_fields = (
        "user__username",
        "user__email",
    )

    # ===== ORDER =====
    ordering = ("-date",)

    # ===== READ ONLY FIELDS =====
    readonly_fields = (
        "total_work_hours",
    )

    # ===== FORM LAYOUT =====
    fieldsets = (
        ("User Info", {
            "fields": ("user", "role", "status", "marked_by")
        }),
        ("Attendance Time", {
            "fields": ("date", "login_time", "logout_time", "total_work_hours")
        }),
        ("Location (GPS)", {
            "fields": ("latitude", "longitude"),
        }),
    )

    # ===== AUTO CALCULATION SAFETY =====
    def save_model(self, request, obj, form, change):
        obj.calculate_work_hours()
        super().save_model(request, obj, form, change)
