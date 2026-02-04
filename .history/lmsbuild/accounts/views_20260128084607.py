from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import Post, Student, TeacherProfile, Batch
from .decorators import admin_required
from django.db import IntegrityError
import uuid
from django.db.models import Count, Q
from .models import Course,Post, Student, TeacherProfile, Batch, User


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


# Access` control decorators for trainer and student`
from django.http import HttpResponseForbidden

def trainer_only(view):
    def wrap(request,*args,**kwargs):
        if request.user.role == "trainer":
            return view(request,*args,**kwargs)
        return HttpResponseForbidden("Not allowed")
    return wrap


def student_only(view):
    def wrap(request,*args,**kwargs):
        if request.user.role == "student":
            return view(request,*args,**kwargs)
        return HttpResponseForbidden("Not allowed")
    return wrap

@login_required
@trainer_only
def trainer_profile(request):

    trainer = request.user.teacher_profile

    return render(request,"trainer/profile.html",{
        "trainer":trainer
    })


# ==================================================
# DASHBOARDS
# ==================================================

@login_required
@admin_required
def admin_dashboard(request):

    trainers = TeacherProfile.objects.select_related("user")
    students = Student.objects.select_related("user", "trainer", "batch")
    batches = Batch.objects.all()

    total_trainers = trainers.count()
    total_students = students.count()
    total_batches = batches.count()

    # Batch wise students
    batch_stats = students.values("batch__name").annotate(count=Count("id"))

    return render(request, "accounts/admin/dashboard.html", {
        "total_trainers": total_trainers,
        "total_students": total_students,
        "total_batches": total_batches,
        "trainers": trainers,
        "students": students,
        "batch_stats": batch_stats,
    })

@login_required
@trainer_only
def trainer_dashboard(request):

    trainer = request.user.teacher_profile

    courses = Course.objects.filter(trainer=trainer)
    posts = Post.objects.filter(trainer=trainer)

    return render(request,"accounts/trainer/dashboard.html",{
        "courses":courses,
        "posts":posts
    })

@login_required
@student_only
def student_dashboard(request):
    student = request.user.student
    courses = Course.objects.filter(trainer=student.trainer)
    posts = Post.objects.filter(trainer=student.trainer)

    return render(request,"accounts/student/dashboard.html",{
        "courses":courses,
        "posts":posts
    })


from .models import Student

@login_required
@trainer_only
def trainer_students(request):

    trainer = request.user.teacher_profile

    students = Student.objects.filter(trainer=trainer)

    return render(request,"accounts/trainer/students.html",{
        "students":students
    })






# ==================================================
# TRAINERS # ADMIN  CRUD
# ==================================================

# ---------- LIST TRAINERS ----------
@admin_required
def trainer_list(request):

    # Fetch trainer profiles with users
    trainers = TeacherProfile.objects.select_related("user").all()

    return render(request, "accounts/admin/trainers/list.html", {
        "trainers": trainers
    })

# ---------- ADD TRAINER ----------
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

# ---------- EDIT TRAINER ----------
@admin_required
def admin_edit_trainer(request, id):

    trainer_user = get_object_or_404(User, id=id, role="trainer")
    profile = get_object_or_404(TeacherProfile, user=trainer_user)

    if request.method == "POST":

        # Username
        trainer_user.username = request.POST.get("username")

        # Mobile
        trainer_user.mobile = request.POST.get("mobile")

        # Optional password reset
        password = request.POST.get("password")
        if password:
            trainer_user.set_password(password)

        # Active / Inactive
        trainer_user.is_active = request.POST.get("is_active") == "on"

        trainer_user.save()

        # Profile update
        profile.subject = request.POST.get("subject")
        profile.save()

        messages.success(request, "Trainer updated successfully")
        return redirect("trainer_list")

    return render(request, "accounts/admin/trainers/edit.html", {
        "trainer": trainer_user,
        "profile": profile
    })

# ---------- DELETE TRAINER ----------
@admin_required
def trainer_delete(request, id):

    trainer_user = get_object_or_404(User, id=id, role="trainer")

    trainer_user.is_active = False
    trainer_user.save()

    messages.warning(request, "Trainer deactivated successfully")

    return redirect("trainer_list")

# ==================================================
# STUDENTS
# ==================================================

#================Student List ================
@admin_required
def admin_students(request):

    students = Student.objects.select_related(
        "user",
        "trainer",
        "trainer__user",
        "batch"
    )

    return render(request, "accounts/admin/students/list.html", {
        "students": students
    })

#================Student add ===============
@admin_required
def admin_add_student(request):

    trainers = User.objects.filter(role="trainer")
    batches = Batch.objects.all()

    if request.method == "POST":

        username = request.POST.get("username")
        trainer_id = request.POST.get("trainer")
        batch_id = request.POST.get("batch")

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username exists")
            return redirect("admin_add_student")

        password = get_random_string(8)

        user = User.objects.create_user(
            username=username,
            password=password,
            role="student",
            is_active=True
        )

        # IMPORTANT FIX
        trainer_user = User.objects.get(id=trainer_id)
        trainer_profile = TeacherProfile.objects.get(user=trainer_user)

        Student.objects.create(
            user=user,
            trainer=trainer_profile,
            batch=Batch.objects.get(id=batch_id),
            roll_no="STD-"+uuid.uuid4().hex[:6].upper(),
            is_active=True
        )

        messages.success(request,"Student created")
        return redirect("admin_students")

    return render(request,"accounts/admin/students/add.html",{
        "trainers":trainers,
        "batches":batches
    })

# -================Student Edit ================
@admin_required
def admin_edit_student(request,id):

    student = Student.objects.get(id=id)
    trainers = User.objects.filter(role="trainer")
    batches = Batch.objects.all()

    if request.method=="POST":

        student.user.username = request.POST.get("username")

        password = request.POST.get("password")
        if password:
            student.user.set_password(password)

        student.user.is_active = request.POST.get("is_active")=="on"
        student.user.save()

        # FIX
        trainer_user = User.objects.get(id=request.POST.get("trainer"))
        student.trainer = TeacherProfile.objects.get(user=trainer_user)

        student.batch = Batch.objects.get(id=request.POST.get("batch"))

        student.save()

        messages.success(request,"Student updated")
        return redirect("admin_students")

    return render(request,"accounts/admin/students/edit.html",{
        "student":student,
        "trainers":trainers,
        "batches":batches
    })

# =================Student Delete =================
@admin_required
def admin_delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    # Soft delete (deactivate user)
    student.user.is_active = False
    student.user.save()

    messages.warning(request, "Student deactivated successfully")

    return redirect("admin_students")









# ==================================================
# ADMIN → USERS
# ==================================================


@admin_required
def admin_user_list(request):

    admin_user = request.user

    trainers = TeacherProfile.objects.select_related("user")
    students = Student.objects.select_related("user", "trainer", "batch")

    total_trainers = trainers.count()
    total_students = students.count()

    # Batch wise students
    batch_stats = students.values("batch__name").annotate(count=Count("id"))

    return render(request, "accounts/admin/user/user_deails.html", {
        "admin": admin_user,
        "trainers": trainers,
        "students": students,
        "total_trainers": total_trainers,
        "total_students": total_students,
        "batch_stats": batch_stats
    })
