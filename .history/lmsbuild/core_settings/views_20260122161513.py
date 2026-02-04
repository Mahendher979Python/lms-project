from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import AdminSettings


@login_required
def admin_settings_view(request):
    """
    GLOBAL ADMIN SETTINGS PAGE
    - Only ONE settings object (Singleton)
    - Used by entire LMS
    """

    if request.user.role != "admin":
        return render(request, "403.html")

    settings = AdminSettings.get()

    if request.method == "POST":
        # ================= GENERAL =================
        settings.site_name = request.POST.get("site_name")
        settings.maintenance_mode = True if request.POST.get("maintenance_mode") else False

        # ================= USER =================
        settings.allow_self_registration = True if request.POST.get("allow_self_registration") else False
        settings.default_user_role = request.POST.get("default_user_role")

        # ================= ATTENDANCE =================
        settings.attendance_enabled = True if request.POST.get("attendance_enabled") else False
        settings.gps_required = True if request.POST.get("gps_required") else False
        settings.gps_radius_meters = request.POST.get("gps_radius_meters")
        settings.half_day_hours = request.POST.get("half_day_hours")
        settings.attendance_approval_required = True if request.POST.get("attendance_approval_required") else False

        # ================= REPORTS =================
        settings.reports_enabled = True if request.POST.get("reports_enabled") else False
        settings.allow_excel_export = True if request.POST.get("allow_excel_export") else False

        settings.save()
        messages.success(request, "Settings updated successfully")

        return redirect("admin_settings")

    return render(
        request,
        "core_settings/settings.html",
        {"settings": settings}
    )
