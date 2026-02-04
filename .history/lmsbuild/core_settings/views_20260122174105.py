from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from core_settings.models import AdminSettings, TrainerSettings


# =====================================================
# ADMIN – GLOBAL LMS SETTINGS
# =====================================================
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
        settings.maintenance_mode = "maintenance_mode" in request.POST

        # -------- USER --------
        settings.allow_self_registration = "allow_self_registration" in request.POST
        settings.default_user_role = request.POST.get("default_user_role")

        # -------- ATTENDANCE --------
        settings.attendance_enabled = "attendance_enabled" in request.POST
        settings.gps_required = "gps_required" in request.POST
        settings.gps_radius_meters = request.POST.get("gps_radius_meters") or 100
        settings.half_day_hours = request.POST.get("half_day_hours") or 4
        settings.attendance_approval_required = (
            "attendance_approval_required" in request.POST
        )

        # -------- REPORTS --------
        settings.reports_enabled = "reports_enabled" in request.POST
        settings.allow_excel_export = "allow_excel_export" in request.POST

        settings.save()
        messages.success(request, "Admin settings updated successfully")
        return redirect("admin_settings")

    return render(
        request,
        "core_settings/settings.html",
        {"settings": settings}
    )


# =====================================================
# ADMIN – TRAINER GLOBAL SETTINGS
# =====================================================
@login_required
def trainer_settings_view(request):
    """
    Admin – Trainer Global Settings
    """

    if request.user.role != "admin":
        return render(request, "403.html")

    settings = TrainerSettings.get()

    if request.method == "POST":

        # PROFILE
        settings.approval_required = "approval_required" in request.POST
        settings.profile_editable = "profile_editable" in request.POST

        # COURSE
        settings.can_create_courses = "can_create_courses" in request.POST
        settings.course_approval_required = "course_approval_required" in request.POST
        settings.max_courses = request.POST.get("max_courses")
        settings.can_edit_published_course = (
            "can_edit_published_course" in request.POST
        )
        settings.can_delete_course = "can_delete_course" in request.POST

        # ATTENDANCE
        settings.attendance_mandatory = "attendance_mandatory" in request.POST
        settings.daily_work_hours = request.POST.get("daily_work_hours")
        settings.late_login_minutes = request.POST.get("late_login_minutes")
        settings.auto_mark_absent = "auto_mark_absent" in request.POST
        settings.attendance_approval_required = (
            "attendance_approval_required" in request.POST
        )
        settings.can_edit_own_attendance = (
            "can_edit_own_attendance" in request.POST
        )

        # LEAVE
        settings.leave_module_enabled = "leave_module_enabled" in request.POST
        settings.max_leaves_per_month = request.POST.get("max_leaves_per_month")
        settings.leave_approval_required = "leave_approval_required" in request.POST

        # PAYMENT
        settings.payment_enabled = "payment_enabled" in request.POST
        settings.payment_type = request.POST.get("payment_type")
        settings.hourly_rate = request.POST.get("hourly_rate") or None
        settings.monthly_salary = request.POST.get("monthly_salary") or None
        settings.minimum_hours_for_payment = request.POST.get(
            "minimum_hours_for_payment"
        )

        # REPORTS
        settings.can_view_student_attendance = (
            "can_view_student_attendance" in request.POST
        )
        settings.can_export_reports = "can_export_reports" in request.POST

        # SECURITY
        settings.two_factor_auth = "two_factor_auth" in request.POST
        settings.ip_restriction_enabled = "ip_restriction_enabled" in request.POST

        settings.save()
        messages.success(request, "Trainer settings updated successfully")
        return redirect("trainer_settings")

    return render(
        request,
        "core_settings/trainer_settings.html",
        {"settings": settings}
    )


# =====================================================
# ADMIN – STUDENT GLOBAL SETTINGS
# =====================================================
@login_required
def student_settings_view(request):
    """
    Admin – Student Global Settings
    """

    if request.user.role != "admin":
        return render(request, "403.html")

    settings = AdminSettings.get()

    if request.method == "POST":

        # APPROVAL
        settings.student_approval_required = (
            "student_approval_required" in request.POST
        )

        # COURSE RULES
        settings.max_courses_per_student = request.POST.get(
            "max_courses_per_student"
        )
        settings.allow_course_preview = "allow_course_preview" in request.POST

        # ATTENDANCE
        settings.student_attendance_required_percent = request.POST.get(
            "student_attendance_required_percent"
        )

        # AUTO BLOCK
        settings.auto_block_student_inactive_days = request.POST.get(
            "auto_block_student_inactive_days"
        )

        settings.save()
        messages.success(request, "Student settings updated successfully")
        return redirect("student_settings")

    return render(
        request,
        "core_settings/student_settings.html",
        {"settings": settings}
    )
