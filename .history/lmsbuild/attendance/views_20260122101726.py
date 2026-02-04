import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.timezone import now
from django.contrib import messages

from .models import Attendance
from courses.models import Course
from enrollments.models import Enrollment


# ================= STUDENT ATTENDANCE PAGE =================
@login_required
def student_attendance(request):
    if request.user.role != "student":
        return render(request, "403.html")

    attendance_list = Attendance.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(
        request,
        "attendance/student/attendance_list.html",
        {
            "attendance_list": attendance_list
        }
    )


# ================= TRAINER ATTENDANCE PAGE =================
@login_required
def trainer_attendance(request):
    if request.user.role != "trainer":
        return render(request, "403.html")

    # Trainer own attendance
    my_attendance = Attendance.objects.filter(
        user=request.user
    ).order_by("-date")

    # Trainer courses
    trainer_courses = Course.objects.filter(
        trainer=request.user
    )

    # Students enrolled in trainer courses
    student_ids = Enrollment.objects.filter(
        course__in=trainer_courses
    ).values_list("student_id", flat=True)

    # Students attendance
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


# ================= ATTENDANCE LOGIN (GPS) =================
@login_required
def attendance_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body.decode("utf-8"))
    lat = data.get("latitude")
    lng = data.get("longitude")

    today = now().date()

    attendance, created = Attendance.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={
            "role": request.user.role,
            "login_time": now(),
            "latitude": lat,
            "longitude": lng,
            "status": "present",
            "marked_by": "system",
        }
    )

    # If record exists but login_time missing
    if not created and attendance.login_time is None:
        attendance.login_time = now()
        attendance.latitude = lat
        attendance.longitude = lng
        attendance.save()

    return JsonResponse({
        "success": True,
        "login_time": attendance.login_time.strftime("%H:%M:%S")
    })


# ================= ATTENDANCE LOGOUT =================
@login_required
def attendance_logout(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    today = now().date()

    try:
        attendance = Attendance.objects.get(
            user=request.user,
            date=today
        )
        attendance.logout_time = now()
        attendance.save()

        return JsonResponse({
            "success": True,
            "logout_time": attendance.logout_time.strftime("%H:%M:%S"),
            "work_hours": str(attendance.total_work_hours)
        })

    except Attendance.DoesNotExist:
        return JsonResponse(
            {"error": "Attendance login not found"},
            status=400
        )


# ================= ADMIN ATTENDANCE LIST =================
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


# ================= ADMIN CREATE ATTENDANCE =================
from datetime import datetime



@login_required
def admin_attendance_create(request):
    if request.user.role != "admin":
        return render(request, "403.html")

    if request.method == "POST":
        user_id = request.POST.get("user")
        role = request.POST.get("role")
        status = request.POST.get("status")

        # 🔥 FIX: convert date string → date object
        date_str = request.POST.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        login_raw = request.POST.get("login_time")
        logout_raw = request.POST.get("logout_time")

        login_time = None
        logout_time = None

        if login_raw:
            login_time = datetime.strptime(login_raw, "%Y-%m-%dT%H:%M").time()

        if logout_raw:
            logout_time = datetime.strptime(logout_raw, "%Y-%m-%dT%H:%M").time()

        Attendance.objects.create(
            user_id=user_id,
            role=role,
            date=date,              # ✅ date object
            login_time=login_time,  # ✅ time object
            logout_time=logout_time,
            status=status,
            marked_by="admin",
        )

        messages.success(request, "Attendance added successfully")
        return redirect("admin_attendance_list")

    return render(request, "attendance/admin/attendance_form.html")

# ================= ADMIN UPDATE ATTENDANCE =================
@login_required
def admin_attendance_edit(request, pk):
    if request.user.role != "admin":
        return render(request, "403.html")

    attendance = get_object_or_404(Attendance, pk=pk)

    if request.method == "POST":
        attendance.status = request.POST.get("status")
        attendance.login_time = request.POST.get("login_time") or None
        attendance.logout_time = request.POST.get("logout_time") or None
        attendance.marked_by = "admin"
        attendance.save()

        messages.success(request, "Attendance updated successfully")
        return redirect("admin_attendance_list")

    return render(
        request,
        "attendance/admin/attendance_form.html",
        {
            "attendance": attendance
        }
    )


# ================= ADMIN DELETE ATTENDANCE =================
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
        {
            "attendance": attendance
        }
    )
