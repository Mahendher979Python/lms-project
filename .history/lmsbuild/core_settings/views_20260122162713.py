from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from core_settings.models import AdminSettings


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
