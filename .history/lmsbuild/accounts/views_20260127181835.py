from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
import uuid

from .models import TeacherProfile, Student
# from courses.models import Course   # optional

User = get_user_model()

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
# 🏠 HOME
# ==================================================

def home(request):
    return render(request, "accounts/home.html")


# ==================================================
# 🔑 LOGIN / LOGOUT
# ==================================================

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_superuser or user.role == "admin":
                return redirect("admin_dashboard")
            elif user.role == "trainer":
                return redirect("trainer_dashboard")
            elif user.role == "student":
                return redirect("student_dashboard")

        messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


# ==================================================
# 👑 ADMIN DASHBOARD
# ==================================================

@login_required
@admin_required
def admin_dashboard(request):
    return render(request, "accounts/admin/dashboard.html")


# ==================================================
# 👨‍🏫 TRAINER DASHBOARD
# ==================================================

@login_required
@role_required("trainer")
def trainer_dashboard(request):
    trainer_profile = request.user.teacherprofile

    students_count = Student.objects.filter(trainer=trainer_profile).count()

    context = {
        "students_count": students_count,
        # "courses": Course.objects.filter(trainer=trainer_profile)
    }
    return render(request, "accounts/trainer/dashboard.html", context)


# ==================================================
# 👨‍🎓 STUDENT DASHBOARD
# ==================================================

@login_required
@role_required("student")
def student_dashboard(request):
    return render(request, "accounts/student/dashboard.html")


# ==================================================
# 👑 ADMIN → TRAINER CRUD
# ==================================================

@admin_required
def trainer_list(request):
    trainers = TeacherProfile.objects.select_related("user")
    return render(request, "accounts/admin/trainers/list.html", {"trainers": trainers})


@admin_required
def trainer_create(request):
    if request.method == "POST":
        username = request.POST.get("username")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("trainer_create")

        user = User.objects.create_user(
            username=username,
            password=request.POST.get("password"),
            role="trainer",
            mobile=request.POST.get("mobile"),
            is_active=True
        )

        TeacherProfile.objects.create(
            user=user,
            emp_id="EMP-" + uuid.uuid4().hex[:6].upper(),
            subject=request.POST.get("subject", "General")
        )

        messages.success(request, "Trainer created successfully")
        return redirect("trainer_list")

    return render(request, "accounts/admin/trainers/create.html")


@admin_required
def trainer_edit(request, id):
    trainer_user = get_object_or_404(User, id=id, role="trainer")
    profile = TeacherProfile.objects.filter(user=trainer_user).first()

    if request.method == "POST":
        trainer_user.username = request.POST.get("username", trainer_user.username)
        trainer_user.mobile = request.POST.get("mobile", trainer_user.mobile)
        trainer_user.is_active = request.POST.get("is_active") == "on"
        trainer_user.save()

        emp_id = request.POST.get("emp_id")
        subject = request.POST.get("subject")

        if TeacherProfile.objects.filter(emp_id=emp_id).exclude(user=trainer_user).exists():
            messages.error(request, "Employee ID already exists")
            return redirect("trainer_edit", id=id)

        if profile:
            profile.emp_id = emp_id
            profile.subject = subject
            profile.save()
        else:
            TeacherProfile.objects.create(user=trainer_user, emp_id=emp_id, subject=subject)

        messages.success(request, "Trainer updated")
        return redirect("trainer_list")

    return render(request, "accounts/admin/trainers/edit.html", {
        "trainer": trainer_user,
        "profile": profile
    })


@admin_required
def trainer_delete(request, id):
    trainer = get_object_or_404(User, id=id, role="trainer")
    trainer.is_active = False
    trainer.save()
    messages.warning(request, "Trainer deactivated")
    return redirect("trainer_list")


# ==================================================
# 👑 ADMIN → STUDENT CRUD
# ==================================================

@admin_required
def admin_students(request):
    students = Student.objects.select_related("user", "trainer", "trainer__user")
    return render(request, "accounts/admin/students/list.html", {"students": students})


@admin_required
def admin_add_student(request):
    trainers = TeacherProfile.objects.select_related("user")

    if request.method == "POST":
        username = request.POST.get("username")
        trainer_id = request.POST.get("trainer")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username exists")
            return redirect("admin_add_student")

        trainer = get_object_or_404(TeacherProfile, id=trainer_id)

        user = User.objects.create_user(
            username=username,
            password=get_random_string(8),
            role="student",
            is_active=True
        )

        Student.objects.create(
            user=user,
            trainer=trainer
        )

        messages.success(request, "Student created")
        return redirect("admin_students")

    return render(request, "accounts/admin/students/add.html", {"trainers": trainers})


@admin_required
def admin_edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    trainers = TeacherProfile.objects.select_related("user")

    if request.method == "POST":
        student.user.username = request.POST.get("username", student.user.username)

        password = request.POST.get("password")
        if password:
            student.user.set_password(password)

        student.user.save()

        student.trainer = get_object_or_404(TeacherProfile, id=request.POST.get("trainer"))
        student.save()

        messages.success(request, "Student updated")
        return redirect("admin_students")

    return render(request, "accounts/admin/students/edit.html", {
        "student": student,
        "trainers": trainers
    })


@admin_required
def admin_delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.user.is_active = False
    student.user.save()
    messages.warning(request, "Student deactivated")
    return redirect("admin_students")


# ==================================================
# 👨‍🏫 TRAINER → OWN STUDENTS ONLY
# ==================================================

@login_required
@role_required("trainer")
def trainer_students(request):
    students = Student.objects.filter(
        trainer=request.user.teacherprofile
    ).select_related("user")

    return render(request, "accounts/trainer/students/list.html", {"students": students})


@login_required
@role_required("trainer")
def trainer_add_student(request):
    trainer = request.user.teacherprofile

    if request.method == "POST":
        username = request.POST.get("username")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username exists")
            return redirect("trainer_add_student")

        user = User.objects.create_user(
            username=username,
            password=request.POST.get("password"),
            role="student",
            is_active=True
        )

        Student.objects.create(user=user, trainer=trainer)

        messages.success(request, "Student added")
        return redirect("trainer_students")

    return render(request, "accounts/trainer/students/add.html")
