import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import now

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

    # Read JSON sent from JS
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

    # If already exists but login missing
    if not created and attendance.login_time is None:
        attendance.login_time = now()
        attendance.latitude = lat
        attendance.longitude = lng
        attendance.save()

    return JsonResponse({
        "status": "logged_in",
        "latitude": lat,
        "longitude": lng
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
        return JsonResponse({"status": "logged_out"})
    except Attendance.DoesNotExist:
        return JsonResponse(
            {"error": "Login not found"},
            status=400
        )
