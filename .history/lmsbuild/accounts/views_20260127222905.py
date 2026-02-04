from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import Student, TeacherProfile, Batch
from .decorators import admin_required
from django.db import IntegrityError
import uuid


User = get_user_model()

# ==================================================
# 🏠 HOME
# ==================================================

def home(request):
    return render(request, "accounts/home.html")


# ==================================================
# 🔐 ROLE DECORATORS
# ==================================================

def role_required(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if request.user.role != role:
                return redirect("login")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def admin_required(view_func):
    return role_required("admin")(view_func)

# ==================================================
# AUTH
# ==================================================

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)

            if user.role == "admin":
                return redirect("admin_dashboard")
            if user.role == "trainer":
                return redirect("trainer_dashboard")
            if user.role == "student":
                return redirect("student_dashboard")

        messages.error(request, "Invalid login")

    return render(request, "accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

# ==================================================
# DASHBOARDS
# ==================================================

@login_required
@admin_required
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

# ==================================================
# TRAINERS # ADMIN  CRUD
# ==================================================

@admin_required
def admin_add_trainer(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        mobile = request.POST.get("mobile")
        subject = request.POST.get("subject")

        if not username:
            messages.error(request, "Username required")
            return redirect("admin_add_trainer")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("admin_add_trainer")

        try:
            password = "Trainer@" + uuid.uuid4().hex[:4]

            user = User.objects.create_user(
                username=username,
                password=password,
                role="trainer",
                mobile=mobile,
                is_active=True
            )

            TeacherProfile.objects.create(
                user=user,
                emp_id="EMP-" + uuid.uuid4().hex[:6].upper(),
                subject=subject
            )

            messages.success(request, f"Trainer created. Password: {password}")
            return redirect("trainer_list")

        except IntegrityError:
            messages.error(request, "Error creating trainer")
            return redirect("admin_add_trainer")

    return render(request, "accounts/admin/trainers/add.html")


# ==================================================
# STUDENTS
# ==================================================

@admin_required
def admin_students(request):
    students=Student.objects.select_related("user","trainer","batch")
    return render(request,"accounts/admin/students/list.html",{"students":students})

# ---------- ADD STUDENT ----------

@admin_required
def admin_add_student(request):

    trainers = TeacherProfile.objects.select_related("user")
    batches = Batch.objects.select_related("trainer")

    if request.method=="POST":

        trainer = get_object_or_404(TeacherProfile,id=request.POST["trainer"])
        batch = get_object_or_404(Batch,id=request.POST["batch"],trainer=trainer)

        password=get_random_string(8)

        user=User.objects.create_user(
            username=request.POST["username"],
            password=password,
            role="student",
            is_active=True
        )

        Student.objects.create(
            user=user,
            trainer=trainer,
            batch=batch,
            roll_no="STD-"+uuid.uuid4().hex[:6].upper()
        )

        messages.success(request,f"Password : {password}")
        return redirect("admin_students")

    return render(request,"accounts/admin/students/add.html",{
        "trainers":trainers,
        "batches":batches
    })

# ---------- EDIT STUDENT ----------

@admin_required
def admin_edit_student(request,id):

    student=get_object_or_404(Student,id=id)
    trainers=TeacherProfile.objects.select_related("user")
    batches=Batch.objects.all()

    if request.method=="POST":

        student.user.username=request.POST["username"]

        if request.POST.get("password"):
            student.user.set_password(request.POST["password"])

        student.user.is_active="is_active" in request.POST
        student.user.save()

        student.trainer=get_object_or_404(TeacherProfile,id=request.POST["trainer"])
        student.batch=get_object_or_404(Batch,id=request.POST["batch"])
        student.save()

        return redirect("admin_students")

    return render(request,"accounts/admin/students/edit.html",{
        "student":student,
        "trainers":trainers,
        "batches":batches
    })

@admin_required
def admin_delete_student(request,id):
    s=get_object_or_404(Student,id=id)
    s.user.is_active=False
    s.user.save()
    return redirect("admin_students")














# ==================================================
# ADMIN → USERS
# ==================================================
@admin_required
def admin_user_list(request):
    users = User.objects.all().order_by("id")
    return render(request, "accounts/admin/user/list.html", {"users": users})


@admin_required
def admin_user_view(request, id):
    user = get_object_or_404(User, id=id)
    teacher_profile = TeacherProfile.objects.filter(user=user).first()
    student_profile = Student.objects.filter(user=user).first()

    return render(request, "accounts/admin/user/user.html", {
        "user": user,
        "teacher_profile": teacher_profile,
        "student_profile": student_profile
    })