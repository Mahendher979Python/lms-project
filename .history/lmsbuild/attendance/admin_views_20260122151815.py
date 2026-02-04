import json
import openpyxl
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Attendance


# =========================================================
# ADMIN – ATTENDANCE LIST + FILTERS
# =========================================================
@login_required
def admin_attendance_list(request):
    if request.user.role != "admin":
        return render(request, "403.html")

    attendance_list = Attendance.objects.select_related("user")

    # ---------- FILTERS ----------
    role = request.GET.get("role")
    status = request.GET.get("status")
    from_date = request.GET.get("from")
    to_date = request.GET.get("to")

    if role:
        attendance_list = attendance_list.filter(role=role)

    if status:
        attendance_list = attendance_list.filter(status=status)

    if from_date and to_date:
        attendance_list = attendance_list.filter(
            date__range=[from_date, to_date]
        )

    attendance_list = attendance_list.order_by("-date", "-login_time")

    return render(
        request,
        "attendance/admin/attendance_list.html",
        {
            "attendance_list": attendance_list
        }
    )


# =========================================================
# ADMIN – MONTHLY REPORT
# =========================================================
@login_required
def admin_monthly_report(request):
    if request.user.role != "admin":
        return render(request, "403.html")

    month = request.GET.get("month")  # YYYY-MM
    data = []

    if month:
        year, m = month.split("-")
        data = Attendance.objects.filter(
            date__year=year,
            date__month=m,
            status__in=["Approved", "Present"]
        ).values(
            "user__username",
            "role"
        ).annotate(
            total_days=Count("id")
        ).order_by("role", "user__username")

    return render(
        request,
        "attendance/admin/attendance_reports.html",
        {"data": data}
    )


# =========================================================
# ADMIN – EXPORT TO EXCEL
# =========================================================
@login_required
def admin_attendance_export(request):
    if request.user.role != "admin":
        return render(request, "403.html")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Attendance"

    ws.append([
        "Username",
        "Role",
        "Date",
        "Login Time",
        "Logout Time",
        "Total Hours",
        "Status",
        "Marked By",
    ])

    records = Attendance.objects.select_related("user").order_by("-date")

    for a in records:
        ws.append([
            a.user.username,
            a.role,
            a.date.strftime("%Y-%m-%d"),
            a.login_time.strftime("%H:%M") if a.login_time else "",
            a.logout_time.strftime("%H:%M") if a.logout_time else "",
            a.total_work_hours or "00:00",
            a.status,
            a.marked_by,
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="attendance.xlsx"'
    wb.save(response)

    return response


# =========================================================
# ADMIN – APPROVE ATTENDANCE
# =========================================================
@login_required
def admin_attendance_approve(request, pk):
    if request.user.role != "admin":
        return render(request, "403.html")

    attendance = get_object_or_404(Attendance, pk=pk)
    attendance.status = "Approved"
    attendance.marked_by = "admin"
    attendance.save()

    messages.success(request, "Attendance approved")
    return redirect("admin_attendance_list")


# =========================================================
# ADMIN – REJECT ATTENDANCE
# =========================================================
@login_required
def admin_attendance_reject(request, pk):
    if request.user.role != "admin":
        return render(request, "403.html")

    attendance = get_object_or_404(Attendance, pk=pk)
    attendance.status = "Rejected"
    attendance.marked_by = "admin"
    attendance.save()

    messages.success(request, "Attendance rejected")
    return redirect("admin_attendance_list")


# =========================================================
# ADMIN – CREATE ATTENDANCE
# =========================================================
@login_required
def admin_attendance_create(request):
    if request.user.role != "admin":
        return render(request, "403.html")

    if request.method == "POST":
        user_id = request.POST.get("user")
        role = request.POST.get("role")
        status = request.POST.get("status")
        date = datetime.strptime(
            request.POST.get("date"), "%Y-%m-%d"
        ).date()

        login_time = logout_time = None

        if request.POST.get("login_time"):
            login_time = datetime.strptime(
                request.POST.get("login_time"), "%Y-%m-%dT%H:%M"
            ).time()

        if request.POST.get("logout_time"):
            logout_time = datetime.strptime(
                request.POST.get("logout_time"), "%Y-%m-%dT%H:%M"
            ).time()

        attendance = Attendance.objects.create(
            user_id=user_id,
            role=role,
            date=date,
            login_time=login_time,
            logout_time=logout_time,
            status=status,
            marked_by="admin",
        )

        attendance.calculate_work_hours()
        attendance.save()

        messages.success(request, "Attendance created successfully")
        return redirect("admin_attendance_list")

    return render(request, "attendance/admin/attendance_form.html")


# =========================================================
# ADMIN – EDIT ATTENDANCE
# =========================================================
@login_required
def admin_attendance_edit(request, pk):
    if request.user.role != "admin":
        return render(request, "403.html")

    attendance = get_object_or_404(Attendance, pk=pk)

    if request.method == "POST":
        attendance.status = request.POST.get("status")

        if request.POST.get("login_time"):
            attendance.login_time = datetime.strptime(
                request.POST.get("login_time"), "%Y-%m-%dT%H:%M"
            ).time()

        if request.POST.get("logout_time"):
            attendance.logout_time = datetime.strptime(
                request.POST.get("logout_time"), "%Y-%m-%dT%H:%M"
            ).time()

        attendance.marked_by = "admin"
        attendance.calculate_work_hours()
        attendance.save()

        messages.success(request, "Attendance updated successfully")
        return redirect("admin_attendance_list")

    return render(
        request,
        "attendance/admin/attendance_form.html",
        {"attendance": attendance}
    )


# =========================================================
# ADMIN – DELETE ATTENDANCE
# =========================================================
@login_required
def admin_attendance_delete(request, pk):
    if request.user.role != "admin":
        return render(request, "403.html")

    attendance = get_object_or_404(Attendance, pk=pk)

    if request.method == "POST":
        attendance.delete()
        messages.success(request, "Attendance deleted")
        return redirect("admin_attendance_list")

    return render(
        request,
        "attendance/admin/attendance_confirm_delete.html",
        {"attendance": attendance}
    )
