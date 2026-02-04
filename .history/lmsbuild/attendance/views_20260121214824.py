from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Attendance

from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)   # 🔥 SIGNAL TRIGGERS HERE
            return redirect("student_dashboard")

    return render(request, "accounts/login.html")

from django.contrib.auth import logout

def user_logout(request):
    logout(request)   # 🔥 logout signal triggers
    return redirect("login")

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
