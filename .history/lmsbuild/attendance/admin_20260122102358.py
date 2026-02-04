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

    list_filter = ("role", "status", "date")
    search_fields = ("user__username",)
    ordering = ("-date",)

    readonly_fields = ("total_work_hours",)

    fieldsets = (
        ("User Info", {
            "fields": ("user", "role", "status")
        }),
        ("Time Info", {
            "fields": ("date", "login_time", "logout_time", "total_work_hours")
        }),
        ("System Info", {
            "fields": ("marked_by",)
        }),
    )
