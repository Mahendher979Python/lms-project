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
        {"attendance_list": attendance_list}
    )
