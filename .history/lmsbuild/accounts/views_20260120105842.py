from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404

from courses.models import Course
from django.contrib import messages
from .models import User, TrainerProfile
from .decorators import admin_required


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
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, TrainerProfile
from .decorators import admin_required


# ================= TRAINER LIST =================


@admin_required
def trainer_list(request):
    trainers = User.objects.filter(role='trainer').select_related('trainerprofile')
    return render(request, 'accounts/admin/trainers/list.html', {
        'trainers': trainers
    })





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


# ================= TRAINER EDIT =================
@admin_required
def trainer_edit(request, id):
    trainer = get_object_or_404(User, id=id, role='trainer')
    profile = get_object_or_404(TrainerProfile, user=trainer)

    if request.method == "POST":
        trainer.username = request.POST['username']
        trainer.mobile = request.POST['mobile']
        trainer.is_active = 'is_active' in request.POST
        trainer.save()

        profile.qualification = request.POST['qualification']
        profile.designation = request.POST['designation']
        profile.experience = request.POST['experience']
        profile.save()

        messages.success(request, "Trainer updated successfully ✨")
        return redirect('trainer_list')

    return render(request, 'accounts/admin/trainers/edit.html', {
        'trainer': trainer,
        'profile': profile
    })


# ================= TRAINER DELETE (SOFT DELETE) =================
@admin_required
def trainer_delete(request, id):
    trainer = get_object_or_404(User, id=id, role='trainer')
    trainer.is_active = False
    trainer.save()

    messages.warning(request, "Trainer deactivated successfully ⚠️")
    return redirect('trainer_list')
