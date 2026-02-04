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
        user_id__in=student_ids
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
    ).order_by("-date")

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

        # date (YYYY-MM-DD)
        date = datetime.strptime(
            request.POST.get("date"), "%Y-%m-%d"
        ).date()

        login_time = None
        logout_time = None

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

        Attendance.objects.create(
            user_id=user_id,
            role=role,
            date=date,
            login_time=login_time,
            logout_time=logout_time,
            status=status,
            marked_by="admin",
        )

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
            att.save()
            return JsonResponse({"status": "ok"})
        except Attendance.DoesNotExist:
            return JsonResponse(
                {"error": "Attendance not found"},
                status=400
            )
