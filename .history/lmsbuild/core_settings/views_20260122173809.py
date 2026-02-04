from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from core_settings.models import AdminSettings, TrainerSettings

#================================
# Admin Settings View
#================================
@login_required
def admin_settings_view(request):
    """
    LMS Admin Global Settings Page
    """

    if request.user.role != "admin":
        return render(request, "403.html")

    settings = AdminSettings.get()

    if request.method == "POST":

        # -------- GENERAL --------
        settings.site_name = request.POST.get("site_name")
        settings.maintenance_mode = bool(request.POST.get("maintenance_mode"))

        # -------- USER --------
        settings.allow_self_registration = bool(request.POST.get("allow_self_registration"))
        settings.default_user_role = request.POST.get("default_user_role")

        # -------- ATTENDANCE --------
        settings.attendance_enabled = bool(request.POST.get("attendance_enabled"))
        settings.gps_required = bool(request.POST.get("gps_required"))
        settings.gps_radius_meters = request.POST.get("gps_radius_meters") or 100
        settings.half_day_hours = request.POST.get("half_day_hours") or 4
        settings.attendance_approval_required = bool(
            request.POST.get("attendance_approval_required")
        )

        # -------- REPORTS --------
        settings.reports_enabled = bool(request.POST.get("reports_enabled"))
        settings.allow_excel_export = bool(request.POST.get("allow_excel_export"))

        settings.save()
        messages.success(request, "Admin settings updated successfully")

        return redirect("admin_settings")

    return render(
        request,
        "core_settings/settings.html",
        {"settings": settings}
    )

#================================
# Trainer Settings View
#================================
@login_required
def trainer_settings_view(request):
    """
    Admin – Trainer Global Settings Page
    """

    if request.user.role != "admin":
        return render(request, "403.html")

    settings = TrainerSettings.get()

    if request.method == "POST":

        # ========= PROFILE =========
        settings.approval_required = bool(request.POST.get("approval_required"))
        settings.profile_editable = bool(request.POST.get("profile_editable"))

        # ========= COURSE =========
        settings.can_create_courses = bool(request.POST.get("can_create_courses"))
        settings.course_approval_required = bool(
            request.POST.get("course_approval_required")
        )
        settings.max_courses = request.POST.get("max_courses")
        settings.can_edit_published_course = bool(
            request.POST.get("can_edit_published_course")
        )
        settings.can_delete_course = bool(
            request.POST.get("can_delete_course")
        )

        # ========= ATTENDANCE =========
        settings.attendance_mandatory = bool(request.POST.get("attendance_mandatory"))
        settings.daily_work_hours = request.POST.get("daily_work_hours")
        settings.late_login_minutes = request.POST.get("late_login_minutes")
        settings.auto_mark_absent = bool(request.POST.get("auto_mark_absent"))
        settings.attendance_approval_required = bool(
            request.POST.get("attendance_approval_required")
        )
        settings.can_edit_own_attendance = bool(
            request.POST.get("can_edit_own_attendance")
        )

        # ========= LEAVE =========
        settings.leave_module_enabled = bool(
            request.POST.get("leave_module_enabled")
        )
        settings.max_leaves_per_month = request.POST.get(
            "max_leaves_per_month"
        )
        settings.leave_approval_required = bool(
            request.POST.get("leave_approval_required")
        )

        # ========= PAYMENT =========
        settings.payment_enabled = bool(request.POST.get("payment_enabled"))
        settings.payment_type = request.POST.get("payment_type")
        settings.hourly_rate = request.POST.get("hourly_rate") or None
        settings.monthly_salary = request.POST.get("monthly_salary") or None
        settings.minimum_hours_for_payment = request.POST.get(
            "minimum_hours_for_payment"
        )

        # ========= REPORTS =========
        settings.can_view_student_attendance = bool(
            request.POST.get("can_view_student_attendance")
        )
        settings.can_export_reports = bool(
            request.POST.get("can_export_reports")
        )

        # ========= SECURITY =========
        settings.two_factor_auth = bool(request.POST.get("two_factor_auth"))
        settings.ip_restriction_enabled = bool(
            request.POST.get("ip_restriction_enabled")
        )

        settings.save()
        messages.success(request, "Trainer settings updated successfully")
        return redirect("trainer_settings")

    return render(
        request,
        "core_settings/trainer_settings.html",
        {"settings": settings}
    )

#================================
# Student Settings View
#================================

@login_required
def student_settings_view(request):
    """
    ADMIN – Student Global Settings
    Controls student behaviour across the LMS
    """

    # 🔒 Admin-only access
    if request.user.role != "admin":
        return render(request, "403.html")

    # Singleton settings
    settings = AdminSettings.get()

    if request.method == "POST":

        # =========================
        # APPROVAL SETTINGS
        # =========================
        settings.student_approval_required = (
            "student_approval_required" in request.POST
        )

        # =========================
        # COURSE RULES
        # =========================
        settings.max_courses_per_student = request.POST.get(
            "max_courses_per_student"
        )
        settings.allow_course_preview = (
            "allow_course_preview" in request.POST
        )

        # =========================
        # ATTENDANCE RULES
        # =========================
        settings.student_attendance_required_percent = request.POST.get(
            "student_attendance_required_percent"
        )

        # =========================
        # AUTO BLOCK RULES
        # =========================
        settings.auto_block_student_inactive_days = request.POST.get(
            "auto_block_student_inactive_days"
        )

        settings.save()
        messages.success(request, "Student settings updated successfully")

        return redirect("student_settings")

    return render(
        request,
        "core_settings/student_settings.html",
        {
            "settings": settings
        }
    )

