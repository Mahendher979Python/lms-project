from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from functools import wraps

# 🔐 ROLE DECORATOR (MUST BE ON TOP)
def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.role != role:
                return redirect("login")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def home(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔴 ROLE BASED REDIRECT
            if user.role == "admin":
                return redirect("/admin/")
            elif user.role == "trainer":
                return redirect("trainer_dashboard")
            elif user.role == "student":
                return redirect("student_dashboard")
        else:
            return render(request, "accounts/login.html", {
                "error": "Invalid credentials"
            })

    return render(request, "accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
@role_required("admin")
def admin_dashboard(request):
    return render(request, "accounts/admin/dashboard.html")

@login_required
@role_required("admin")
def admin_dashboard(request):
    return render(request, "accounts/admin/dashboard.html")

@login_required
@role_required("trainer")
def trainer_dashboard(request):
    return render(request, "accounts/trainer/dashboard.html")

@login_required
@role_required("student")
def student_dashboard(request):
    return render(request, "accounts/student/dashboard.html")

def redirect_by_role(user):
    if user.role == "admin":
        return redirect("/admin/")
    elif user.role == "trainer":
        return redirect("trainer_dashboard")
    elif user.role == "student":
        return redirect("student_dashboard")
