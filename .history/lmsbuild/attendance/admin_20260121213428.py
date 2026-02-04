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

    list_filter = ("role", "status", "date")
    search_fields = ("user__username",)
