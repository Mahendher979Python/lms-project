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
        "total_work_hours",
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
        "total_work_hours",
    )

    fieldsets = (
        ("User Info", {
            "fields": ("user", "role", "status")
        }),
        ("Attendance Time", {
            "fields": ("date", "login_time", "logout_time", "total_work_hours")
        }),
        ("Location", {
            "fields": ("latitude", "longitude")
        }),
        ("System", {
            "fields": ("marked_by",)
        }),
    )
