from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q

from .models import User



def home(request):
    return render(request, "home.html")
# =================================================
# LOGIN
# =================================================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(
                Q(username=username) | Q(email=username)
            )
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "account/login.html")


# =================================================
# LOGOUT
# =================================================
@login_required
def logout_view(request):
    logout(request)
    return redirect("account/login")


# =================================================
# DASHBOARD REDIRECT (ROLE BASED)
# =================================================
@login_required
def dashboard(request):
    if request.user.role == "admin":
        return redirect("admin_dashboard")
    elif request.user.role == "trainer":
        return redirect("trainer_dashboard")
    elif request.user.role == "student":
        return redirect("student_dashboard")
    else:
        return HttpResponseForbidden("Invalid role")


# =================================================
# ADMIN DASHBOARD
# =================================================
@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Access Denied")

    context = {
        "users_count": User.objects.count(),
        "trainers_count": User.objects.filter(role="trainer").count(),
        "students_count": User.objects.filter(role="student").count(),
    }
    return render(request, "admin/dashboard.html", context)


# =================================================
# TRAINER DASHBOARD
# =================================================
@login_required
def trainer_dashboard(request):
    if request.user.role != "trainer":
        return HttpResponseForbidden("Access Denied")

    courses = Course.objects.filter(trainer=request.user)

    context = {
        "courses": courses,
        "courses_count": courses.count(),
        "assignments_count": 0,
        "submissions_count": 0,
        "attendance_percentage": 0,
    }
    return render(request, "trainer/dashboard.html", context)


# =================================================
# STUDENT DASHBOARD
# =================================================
@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return HttpResponseForbidden("Access Denied")

    return render(request, "student/dashboard.html")
