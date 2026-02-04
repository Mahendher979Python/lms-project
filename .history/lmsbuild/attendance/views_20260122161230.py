import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages

from .models import Attendance
from courses.models import Course
from enrollments.models import Enrollment

import openpyxl
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseForbidden

from core_settings.decorators import attendance_required
from django.contrib.auth.decorators import login_required
from core_settings.decorators import attendance_required, maintenance_guard
from core_settings.services import validate_attendance_rules





# =========================================================
# STUDENT ATTENDANCE PAGE
# =========================================================

@login_required
def student_attendance(request):
    if request.user.role != "student":
        return render(request, "403.html")

    attendance_list = Attendance.objects.filter(
        user=request.user
    ).order_by("-date")

    attendance_today = Attendance.objects.filter(
        user=request.user,
        date=timezone.localdate()
    ).first()

    return render(
        request,
        "attendance/student/attendance_list.html",
        {
            "attendance_list": attendance_list,
            "attendance_today": attendance_today,
        }
    )


# =========================================================
# TRAINER ATTENDANCE PAGE
# =========================================================
@login_required
def trainer_attendance(request):
    if request.user.role != "trainer":
        return render(request, "403.html")

    my_attendance = Attendance.objects.filter(
        user=request.user
    ).order_by("-date")

    trainer_courses = Course.objects.filter(trainer=request.user)

    student_ids = Enrollment.objects.filter(
        course__in=trainer_courses
    ).values_list("student_id", flat=True)

    students_attendance = Attendance.objects.filter(
        user_id__in=student_ids,
        role="student"   # ✅ safety
    ).select_related("user").order_by("-date")

    return render(
        request,
        "attendance/trainer/attendance_list.html",
        {
            "my_attendance": my_attendance,
            "students_attendance": students_attendance,
        }
    )


# =========================================================
# ADMIN ATTENDANCE LIST
# =========================================================
@login_required
def admin_attendance_list(request):
    if request.user.role != "admin":
        return render(request, "403.html")

    attendance_list = Attendance.objects.select_related(
        "user"
    ).order_by("-date", "-login_time")

    return render(
        request,
        "attendance/admin/attendance_list.html",
        {
            "attendance_list": attendance_list
        }
    )


# =========================================================
# ADMIN CREATE ATTENDANCE
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
                request.POST.get("login_time"),
                "%Y-%m-%dT%H:%M"
            ).time()

        if request.POST.get("logout_time"):
            logout_time = datetime.strptime(
                request.POST.get("logout_time"),
                "%Y-%m-%dT%H:%M"
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

        messages.success(request, "Attendance added successfully")
        return redirect("admin_attendance_list")

    return render(request, "attendance/admin/attendance_form.html")


# =========================================================
# ADMIN UPDATE ATTENDANCE
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
                request.POST.get("login_time"),
                "%Y-%m-%dT%H:%M"
            ).time()

        if request.POST.get("logout_time"):
            attendance.logout_time = datetime.strptime(
                request.POST.get("logout_time"),
                "%Y-%m-%dT%H:%M"
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
# ADMIN DELETE ATTENDANCE
# =========================================================
@login_required
def admin_attendance_delete(request, pk):
    if request.user.role != "admin":
        return render(request, "403.html")

    attendance = get_object_or_404(Attendance, pk=pk)

    if request.method == "POST":
        attendance.delete()
        messages.success(request, "Attendance deleted successfully")
        return redirect("admin_attendance_list")

    return render(
        request,
        "attendance/admin/attendance_confirm_delete.html",
        {"attendance": attendance}
    )


# =========================================================
# STUDENT LOGIN (GPS)
# =========================================================

@login_required
def attendance_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        today = timezone.localdate()

        att, created = Attendance.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={
                "role": request.user.role,     # ✅ student / trainer
                "status": "Present",
                "marked_by": request.user.role # ✅ dynamic
            }
        )

        if not att.login_time:
            att.login_time = timezone.localtime().time()
            att.latitude = data.get("latitude")
            att.longitude = data.get("longitude")
            att.save()

        return JsonResponse({
            "login_time": att.login_time.strftime("%H:%M"),
            "lat": att.latitude,
            "lng": att.longitude
        })


# =========================================================
# STUDENT LOGOUT
# =========================================================
@login_required
def attendance_logout(request):
    if request.method == "POST":
        today = timezone.localdate()

        try:
            att = Attendance.objects.get(
                user=request.user,
                date=today
            )
            att.logout_time = timezone.localtime().time()
            att.marked_by = request.user.role
            att.save()
            return JsonResponse({"status": "ok"})
        except Attendance.DoesNotExist:
            return JsonResponse(
                {"error": "Attendance not found"},
                status=400
            )


# =========================================================
# Trainer ATTENDANCE PAGE Repeat (for reference)
# =========================================================

@login_required
def trainer_attendance_report(request):
    month = request.GET.get("month")
    data = []

    if month:
        y, m = month.split("-")
        data = Attendance.objects.filter(
            user=request.user,
            date__year=y,
            date__month=m,
            status__in=["Approved","Present"]
        ).values("user").annotate(total_days=Count("id"))

    return render(request,"attendance/trainer/attendance_reports.html",{"data":data})


@login_required
def student_attendance_report(request):
    month = request.GET.get("month")
    data = []

    if month:
        y, m = month.split("-")
        data = Attendance.objects.filter(
            user=request.user,
            date__year=y,
            date__month=m,
            status__in=["Approved","Present"]
        ).values("user").annotate(total_days=Count("id"))

    return render(request,"attendance/student/attendance_reports.html",{"data":data})


# =========================================================
# ADMIN – MONTHLY ATTENDANCE REPORT (ALL USERS)
# URL: /attendance/admin/report/
# =========================================================
@login_required
def admin_monthly_report(request):
    if request.user.role != "admin":
        return render(request, "403.html")

    month = request.GET.get("month")  # format: YYYY-MM
    report_data = []

    if month:
        year, m = month.split("-")

        report_data = Attendance.objects.filter(
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
        {
            "data": report_data,
            "month": month
        }
    )


# =========================================================
# ADMIN – EXPORT ATTENDANCE TO EXCEL (ALL USERS)
# URL: /attendance/admin/export/
# =========================================================
@login_required
def admin_attendance_export(request):
    if request.user.role != "admin":
        return render(request, "403.html")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Attendance Report"

    # ---- Header Row ----
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
    response["Content-Disposition"] = 'attachment; filename="attendance_report.xlsx"'

    wb.save(response)
    return response


#   settings
@login_required
@maintenance_guard          # 1️⃣ site check
@attendance_required        # 2️⃣ attendance ON/OFF
def attendance_login(request):
    data = json.loads(request.body)
    lat = data.get("latitude")
    lng = data.get("longitude")

    # 3️⃣ Time + GPS rules
    blocked = validate_attendance_rules(lat, lng)
    if blocked:
        return blocked

    today = timezone.localdate()

    att, created = Attendance.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={
            "role": request.user.role,
            "status": "Present",
            "marked_by": request.user.role
        }
    )

    if not att.login_time:
        att.login_time = timezone.localtime().time()
        att.latitude = lat
        att.longitude = lng
        att.save()

    return JsonResponse({"status": "login success"})
