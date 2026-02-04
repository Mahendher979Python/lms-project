from sre_constants import IN
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from .decorators import admin_required
from django.contrib.auth import get_user_model
from accounts.models import Student,  User
from courses.models import Course
from .forms import StudentCreateForm, StudentUpdateForm
from django.utils.crypto import get_random_string
User = get_user_model()


# ==================================================
# 🔐 ROLE BASED DECORATOR (ADMIN SAFE)
# ==================================================
def role_required(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            # 🔥 allow admin everywhere
            if request.user.is_superuser:
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

        if user is not None:
            login(request, user)
        
            # 🔥 SUPERUSER FIRST
            if user.is_superuser:
                return redirect("admin_dashboard")

            if user.role == "admin":
                return redirect("admin_dashboard")
            elif user.role == "trainer":
                return redirect("trainer_dashboard")
            elif user.role == "student":
                return redirect("student_dashboard")
            print("LOGIN:", user.username, user.role, user.is_superuser)

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
    user = request.user

    courses = Course.objects.filter(trainer=user).order_by("-created_at")

    context = {
        "courses": courses,
        "courses_count": courses.count(),
        "assignments_count": 0,
        "submissions_count": 0,
        "attendance_percentage": 0,
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
# 🧑‍🏫 TRAINER LIST
# ==================================================

# ================= TRAINER LIST =================
@admin_required
def trainer_list(request):
    trainers = (
        User.objects
        .filter(role='trainer')
        .select_related('trainerprofile')
        .order_by('id')
    )

    return render(request, 'accounts/admin/trainers/list.html', {
        'trainers': trainers
    })


# ================= TRAINER CREATE =================
@admin_required
def trainer_create(request):
    if request.method == "POST":
        username = request.POST['username']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('trainer_create')

        user = User.objects.create_user(
            username=username,
            password=request.POST['password'],
            role='trainer',
            mobile=request.POST['mobile'],
            is_active=True
        )

        TrainerProfile.objects.get_or_create(
            user=user,
            defaults={
                'qualification': request.POST['qualification'],
                'designation': request.POST['designation'],
                'experience': request.POST['experience'],
            }
        )

        messages.success(request, f"Trainer '{username}' added successfully ✅")
        return redirect('trainer_list')

    return render(request, 'accounts/admin/trainers/create.html')


@login_required
def trainer_edit(request, id):
    trainer = get_object_or_404(User, id=id, role="trainer")

    # Try to fetch profile safely
    profile = TrainerProfile.objects.filter(user=trainer).first()

    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        department = request.POST.get("department")

        # 🔒 Check emp_id uniqueness EXCEPT current trainer
        if TrainerProfile.objects.filter(emp_id=emp_id).exclude(user=trainer).exists():
            messages.error(request, "Employee ID already exists!")
            return redirect("trainer_edit", id=trainer.id)

        if profile:
            # UPDATE
            profile.emp_id = emp_id
            profile.department = department
            profile.save()
        else:
            # CREATE only if not exists
            TrainerProfile.objects.create(
                user=trainer,
                emp_id=emp_id,
                department=department
            )

        messages.success(request, "Trainer updated successfully")
        return redirect("trainer_list")

    return render(request, "accounts/admin/trainers/edit.html", {
        "trainer": trainer,
        "profile": profile
    })


# ================= TRAINER DELETE (SOFT DELETE) =================
@admin_required
def trainer_delete(request, id):
    trainer = get_object_or_404(User, id=id, role='trainer')
    trainer.is_active = False
    trainer.save()

    messages.warning(request, "Trainer deactivated successfully ⚠️")
    return redirect('trainer_list')

# ==================================================
# 🧑‍🎓 STUDENTS MANAGEMENT FOR ADMIN
# ==================================================
# ===============================
# LIST STUDENTS
# ===============================
@login_required
def admin_students(request):
    students = Student.objects.select_related("user").all()
    return render(request, "accounts/admin/students/list.html", {
        "students": students
    })


# ===============================
# ADD STUDENT
# ===============================
@login_required
def admin_add_student(request):
    form = StudentCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("admin_add_student")

        password = get_random_string(8)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role="student"
        )

        student = form.save(commit=False)
        student.user = user
        student.save()

        request.session["student_username"] = username
        request.session["student_password"] = password

        messages.success(request, "Student created successfully")
        return redirect("admin_student_created")

    return render(request, "accounts/admin/students/add.html", {
        "form": form
    })


# ===============================
# SUCCESS PAGE
# ===============================
@login_required
def admin_student_created(request):
    username = request.session.pop("student_username", None)
    password = request.session.pop("student_password", None)

    if not password:
        return redirect("admin_students")

    return render(request, "accounts/admin/students/create.html", {
        "username": username,
        "password": password
    })


# ===============================
# EDIT STUDENT
# ===============================
@login_required
def admin_edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    user = student.user
    form = StudentUpdateForm(request.POST or None, instance=student, initial={
        "username": student.user.username,
        "email": student.user.email,
        "status": "active" if student.user.is_active else "inactive"
    })

    if request.method == "POST" and form.is_valid():
        user.username = form.cleaned_data["username"]
        user.email = form.cleaned_data["email"]
        user.is_active = form.cleaned_data["status"] == "active"

        password = form.cleaned_data.get("password")
        if password:
            user.set_password(password)

        user.save()
        form.save()

        messages.success(request, "Student updated successfully")
        return redirect("admin_students")

    return render(request, "accounts/admin/students/edit.html", {
        "form": form,
        "student": student
    })


# ===============================
# DELETE / DEACTIVATE STUDENT
# ===============================
@login_required
def admin_delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.user.is_active = False
    student.user.save()

    messages.warning(request, "Student deactivated successfully ⚠️")
    return redirect("admin_students")



@login_required
def admin_user_list(request):
    users = User.objects.all()
    return render(request, "accounts/admin/user/list.html", {
        "users": users
    })



@login_required
def admin_user_view(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, "accounts/admin/user/user.html", {
        "user": user
    })
