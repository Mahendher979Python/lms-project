from django.contrib import admin
from .models import AdminSettings, TrainerSettings

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



@admin.register(TrainerSettings)
class TrainerSettingsAdmin(admin.ModelAdmin):
    """
    Trainer Global Settings (Singleton)
    """

    list_display = (
        "approval_required",
        "can_create_courses",
        "attendance_mandatory",
        "payment_enabled",
        "updated_at",
    )

    fieldsets = (
        ("Profile Settings", {
            "fields": (
                "approval_required",
                "profile_editable",
            )
        }),

        ("Course Permissions", {
            "fields": (
                "can_create_courses",
                "course_approval_required",
                "max_courses",
                "can_edit_published_course",
                "can_delete_course",
            )
        }),

        ("Attendance Rules", {
            "fields": (
                "attendance_mandatory",
                "daily_work_hours",
                "late_login_minutes",
                "auto_mark_absent",
                "attendance_approval_required",
                "can_edit_own_attendance",
            )
        }),

        ("Leave Settings", {
            "fields": (
                "leave_module_enabled",
                "max_leaves_per_month",
                "leave_approval_required",
            )
        }),

        ("Payment / Payroll", {
            "fields": (
                "payment_enabled",
                "payment_type",
                "hourly_rate",
                "monthly_salary",
                "minimum_hours_for_payment",
            )
        }),

        ("Reports & Access", {
            "fields": (
                "can_view_student_attendance",
                "can_export_reports",
            )
        }),

        ("Security", {
            "fields": (
                "two_factor_auth",
                "ip_restriction_enabled",
            )
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
