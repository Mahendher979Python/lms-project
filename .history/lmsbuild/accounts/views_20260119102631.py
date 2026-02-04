from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from functools import wraps
from courses.models import Course

from .forms import AdminCreateUserForm


# ==================================================
# 🔐 ROLE BASED DECORATOR
# ==================================================
def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            if request.user.role != role:
                return redirect("login")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# ==================================================
# 🏠 HOME
# ==================================================
# views.py
from django.shortcuts import render

def home(request):
    # Dummy logic to get notification count
    # Replace this with your actual Notification model query
    notif_count = 0
    if request.user.is_authenticated:
        # Example: notif_count = Notification.objects.filter(user=request.user, is_read=False).count()
        notif_count = 3  # Testing kosam 3 ani pettanu

    context = {
        'notification_count': notif_count
    }
    return render(request, "accounts/home.html")


# ==================================================
# 👤 ADMIN CREATE USER
# ==================================================
@login_required
@role_required("admin")
def admin_create_user(request):
    if request.method == "POST":
        form = AdminCreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")
        else:
            print(form.errors)   # 🔥 ADD THIS
    else:
        form = AdminCreateUserForm()

    return render(request, "accounts/admin/create_user.html", {"form": form})


# ==================================================
# 🔑 LOGIN
# ==================================================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.role == "admin":
                return redirect("admin_dashboard")
            elif user.role == "trainer":
                return redirect("trainer_dashboard")
            elif user.role == "student":
                return redirect("student_dashboard")

        return render(request, "accounts/login.html", {
            "error": "Invalid credentials"
        })

    return render(request, "accounts/login.html")


# ==================================================
# 🚪 LOGOUT
# ==================================================
def user_logout(request):
    logout(request)
    return redirect("login")


# ==================================================
# 🧑‍💼 ADMIN DASHBOARD
# ==================================================
@login_required
@role_required("admin")
def admin_dashboard(request):
    return render(request, "accounts/admin/dashboard.html")


# ==================================================
# 👨‍🏫 TRAINER DASHBOARD
# ==================================================
@login_required
@role_required("trainer")
def trainer_dashboard(request):
    user = request.user

    courses = Course.objects.filter(trainer=user).order_by("-created_at")

    context = {
        "courses": courses,
        "courses_count": courses.count(),
        "assignments_count": 0,     # future use
        "submissions_count": 0,     # future use
        "attendance_percentage": 0  # future use
    }

    return render(request, "accounts/trainer/dashboard.html", context)

# ==================================================
# 🎓 STUDENT DASHBOARD
# ==================================================
@login_required
@role_required("student")
def student_dashboard(request):
    return render(request, "accounts/student/dashboard.html")
