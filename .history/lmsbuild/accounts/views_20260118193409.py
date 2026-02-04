from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.db.models import Q
from django.utils.crypto import get_random_string

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
