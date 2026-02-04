from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Attendance


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


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Attendance
from enrollments.models import Enrollment   # if you use enrollments


@login_required
def trainer_attendance(request):
    if request.user.role != "trainer":
        return render(request, "403.html")

    # Trainer own attendance
    my_attendance = Attendance.objects.filter(
        user=request.user
    ).order_by("-date")

    # Students under this trainer
    student_ids = Enrollment.objects.filter(
        course__trainer=request.user
    ).values_list("student_id", flat=True)

    students_attendance = Attendance.objects.filter(
        user_id__in=student_ids
    ).order_by("-date")

    return render(
        request,
        "attendance/trainer/attendance_list.html",
        {
            "my_attendance": my_attendance,
            "students_attendance": students_attendance,
        }
    )

from django.http import JsonResponse
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import Attendance


@login_required
def attendance_login(request):
    if request.method == "POST":
        lat = request.POST.get("latitude")
        lng = request.POST.get("longitude")

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

        return JsonResponse({"status": "logged_in"})


@login_required
def attendance_logout(request):
    if request.method == "POST":
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
            return JsonResponse({"error": "No login found"}, status=400)
