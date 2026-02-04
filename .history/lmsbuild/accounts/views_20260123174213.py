from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string

from .decorators import admin_required
from .models import User, Student, TeacherProfile
from .forms import StudentCreateForm, StudentUpdateForm
from courses.models import Course

from django.shortcuts import render, redirect, get_object_or_404



# ==================================================
# 🔐 ROLE BASED DECORATOR
# ==================================================
def role_required(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            # Admin / Superadmin full access
            if request.user.is_superuser or request.user.role == "admin":
                return view_func(request, *args, **kwargs)

            if request.user.role != role:
                return redirect("login")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# ==================================================
# 🏠 HOME
# ==================================================
def home(request):
    return render(request, "accounts/home.html")


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

            if user.is_superuser or user.role == "admin":
                return redirect("admin_dashboard")
            elif user.role == "trainer":
                return redirect("trainer_dashboard")
            elif user.role == "student":
                return redirect("student_dashboard")

        return render(request, "accounts/login.html", {
            "error": "Invalid username or password"
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
    trainer_profile = request.user.teacherprofile

    courses = Course.objects.filter(
        trainer=trainer_profile
    ).order_by("-created_at")

    students_count = Student.objects.filter(
        trainer=trainer_profile
    ).count()

    context = {
        "courses": courses,
        "courses_count": courses.count(),
        "students_count": students_count,
        "assignments_count": 0,
        "submissions_count": 0,
    }

    return render(request, "accounts/trainer/dashboard.html", context)


# ==================================================
# 🎓 STUDENT DASHBOARD
# ==================================================
@login_required
@role_required("student")
def student_dashboard(request):
    return render(request, "accounts/student/dashboard.html")


# ==================================================
# 👨‍🏫 ADMIN – TRAINER MANAGEMENT
# ==================================================
@admin_required
def trainer_list(request):
    trainers = TeacherProfile.objects.select_related("user")
    return render(request, "accounts/admin/trainers/list.html", {
        "trainers": trainers
    })


import uuid

@admin_required
def trainer_create(request):
    if request.method == "POST":
        username = request.POST["username"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("trainer_create")

        user = User.objects.create_user(
            username=username,
            password=request.POST["password"],
            role="trainer",
            mobile=request.POST.get("mobile"),
            is_active=True
        )

        TeacherProfile.objects.create(
            user=user,
            emp_id=f"EMP-{uuid.uuid4().hex[:6].upper()}",
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
            return redirect("trainer_edit", id=trainer_user.id)

        if profile:
            profile.emp_id = emp_id
            profile.subject = subject
            profile.save()
        else:
            TeacherProfile.objects.create(
                user=trainer_user,
                emp_id=emp_id,
                subject=subject
            )

        messages.success(request, "Trainer updated successfully")
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

    messages.warning(request, "Trainer deactivated successfully")
    return redirect("trainer_list")


# ==================================================
# 👨‍🎓 ADMIN – STUDENT LIST
# ==================================================
@admin_required
def admin_students(request):
    students = Student.objects.select_related("user","trainer","trainer__user")
    return render(request,"accounts/admin/students/list.html",{"students":students})

# ==================================================
# ➕ ADMIN – ADD STUDENT
# ==================================================
def admin_add_student(request):
    trainers = TeacherProfile.objects.select_related("user")
    form = StudentCreateForm(request.POST or None)

    if request.method=="POST" and form.is_valid():
        trainer = get_object_or_404(TeacherProfile,id=request.POST["trainer"])
        password = get_random_string(8)

        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=password,
            role="student"
        )

        student = form.save(commit=False)
        student.user = user
        student.trainer = trainer
        student.save()

        messages.success(request,"Student created successfully")
        return redirect("admin_students")

    return render(request,"accounts/admin/students/add.html",{
        "form":form,"trainers":trainers
    })

# ==================================================
# ✏️ ADMIN – EDIT STUDENT
# ==================================================
@admin_required
def admin_edit_student(request,id):
    student = get_object_or_404(Student,id=id)
    trainers = TeacherProfile.objects.select_related("user")

    form = StudentUpdateForm(request.POST or None,instance=student,initial={
        "username":student.user.username,
        "email":student.user.email
    })

    if request.method=="POST" and form.is_valid():
        student.user.username = form.cleaned_data["username"]
        student.user.email = form.cleaned_data["email"]

        if form.cleaned_data.get("password"):
            student.user.set_password(form.cleaned_data["password"])

        student.trainer = get_object_or_404(
            TeacherProfile,id=request.POST["trainer"]
        )

        student.user.save()
        student.save()

        messages.success(request,"Student updated")
        return redirect("admin_students")

    return render(request,"accounts/admin/students/edit.html",{
        "form":form,"student":student,"trainers":trainers
    })


# ==================================================
# ❌ ADMIN – DELETE (SOFT)
# ==================================================
@admin_required
def admin_delete_student(request,id):
    student = get_object_or_404(Student,id=id)
    student.user.is_active = False
    student.user.save()
    messages.warning(request,"Student deactivated")
    return redirect("admin_students")
# ==================================================
# 👨‍🏫 TRAINER – VIEW OWN STUDENTS ONLY
# ==================================================
@login_required
@role_required("trainer")
def trainer_students(request):
    students = Student.objects.filter(
        trainer=request.user.teacherprofile
    ).select_related("user")

    return render(request, "accounts/trainer/students/list.html", {
        "students": students
    })


# ==================================================
# 👥 ADMIN – USER LIST & DETAIL
# ==================================================
@admin_required
def admin_user_list(request):
    users = User.objects.all().order_by("id")
    return render(request, "accounts/admin/user/list.html", {
        "users": users
    })


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

