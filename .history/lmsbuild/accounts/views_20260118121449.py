from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # 🔁 Auto redirect based on role
            if user.role == "admin":
                return redirect("admin_dashboard")
            elif user.role == "trainer":
                return redirect("trainer_dashboard")
            else:
                return redirect("student_dashboard")

        else:
            return render(request, "accounts/login.html", {"error": "Invalid credentials"})

    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return redirect("login")
    return render(request, "accounts/admin_dashboard.html")


@login_required
def trainer_dashboard(request):
    if request.user.role != "trainer":
        return redirect("login")
    return render(request, "accounts/trainer_dashboard.html")


@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return redirect("login")
    return render(request, "accounts/student_dashboard.html")
