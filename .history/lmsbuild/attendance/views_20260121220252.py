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
