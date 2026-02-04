from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.core.mail import send_mail
from django.contrib import messages
from courses.models import Course

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from accounts.decorators import admin_required

from .models import TrainerProfile, StudentProfile, StaffProfile
from courses.models import Course


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




# ======================================================
# ADMIN – USERS (BASIC USER MANAGEMENT)
# ======================================================
@login_required
@admin_required
def admin_users(request):
    users = User.objects.exclude(role="admin")
    return render(request, "accounts/admin/users/users_list.html", {
        "users": users
    })


@login_required
@admin_required
def admin_create_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("admin_create_user")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("admin_create_user")

        user = User.objects.create_user(
            username=username,
            email=email,
            password="Temp@123",   # later auto-generate
            role=role,
            is_active=True,
            is_staff=(role != "student")
        )

        messages.success(request, "User created successfully")
        return redirect("admin_users")

    return render(request, "accounts/admin/users/create_user.html")

# ADMIN EDIT USER
@login_required
@admin_required
def admin_edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.is_active = request.POST.get("status") == "active"

        password = request.POST.get("password")
        if password:
            user.set_password(password)

        user.save()
        messages.success(request, "User updated successfully")
        return redirect("admin_users")

    return render(request, "accounts/admin/users/user_edit.html", {
        "user": user
    })

# ADMIN DELETE  USER
@login_required
@admin_required
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted")
    return redirect("admin_users")


# ======================================================
# ADMIN – TRAINERS CRUD
# ======================================================

@login_required
@admin_required
def admin_trainer_list(request):
    trainers = TrainerProfile.objects.select_related("user")
    return render(request, "accounts/admin/trainers/list.html", {
        "trainers": trainers
    })

@login_required
@admin_required
def admin_trainer_create(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            password="Temp@123",
            role="trainer",
            is_staff=True
        )

        TrainerProfile.objects.create(
            user=user,
            employee_id=request.POST["employee_id"],
            first_name=request.POST["first_name"],
            surname=request.POST["surname"],
            qualification=request.POST["qualification"],
            designation=request.POST["designation"],
            phone=request.POST["phone"],
            address=request.POST["address"],
            joining_date=request.POST["joining_date"],
        )

        messages.success(request, "Trainer created")
        return redirect("admin_trainer_list")

    return render(request, "accounts/admin/trainers/create.html")


@login_required
@admin_required
def admin_trainer_edit(request, trainer_id):
    trainer = get_object_or_404(TrainerProfile, id=trainer_id)

    if request.method == "POST":
        trainer.first_name = request.POST["first_name"]
        trainer.surname = request.POST["surname"]
        trainer.qualification = request.POST["qualification"]
        trainer.designation = request.POST["designation"]
        trainer.phone = request.POST["phone"]
        trainer.address = request.POST["address"]
        trainer.joining_date = request.POST["joining_date"]
        trainer.save()

        messages.success(request, "Trainer updated")
        return redirect("admin_trainer_list")

    return render(request, "accounts/admin/trainers/edit.html", {
        "trainer": trainer
    })


# ======================================================
# ADMIN – STUDENTS CRUD
# ======================================================

@login_required
@admin_required
def admin_student_list(request):
    students = StudentProfile.objects.select_related("user")
    return render(request, "accounts/admin/students/list.html", {
        "students": students
    })


@login_required
@admin_required
def admin_student_create(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            password="Temp@123",
            role="student",
            is_staff=False
        )

        student = StudentProfile.objects.create(
            user=user,
            student_id=request.POST["student_id"],
            first_name=request.POST["first_name"],
            surname=request.POST["surname"],
            phone=request.POST["phone"],
            qualification=request.POST["qualification"],
            address=request.POST["address"],
        )

        student.courses.set(request.POST.getlist("courses"))

        messages.success(request, "Student created")
        return redirect("admin_student_list")

    courses = Course.objects.all()
    return render(request, "accounts/admin/students/create.html", {
        "courses": courses
    })


@login_required
@admin_required
def admin_student_edit(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)

    if request.method == "POST":
        student.first_name = request.POST["first_name"]
        student.surname = request.POST["surname"]
        student.phone = request.POST["phone"]
        student.qualification = request.POST["qualification"]
        student.address = request.POST["address"]
        student.save()

        student.courses.set(request.POST.getlist("courses"))

        messages.success(request, "Student updated")
        return redirect("admin_student_list")

    courses = Course.objects.all()
    return render(request, "accounts/admin/students/edit.html", {
        "student": student,
        "courses": courses
    })


# ======================================================
# ADMIN – STAFF CRUD
# ======================================================

@login_required
@admin_required
def admin_staff_list(request):
    staff = StaffProfile.objects.select_related("user")
    return render(request, "accounts/admin/staff/list.html", {
        "staff": staff
    })


@login_required
@admin_required
def admin_staff_create(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            password="Temp@123",
            role="staff",
            is_staff=True
        )

        StaffProfile.objects.create(
            user=user,
            employee_id=request.POST["employee_id"],
            first_name=request.POST["first_name"],
            surname=request.POST["surname"],
            designation=request.POST["designation"],
            phone=request.POST["phone"],
            address=request.POST["address"],
        )

        messages.success(request, "Staff created")
        return redirect("admin_staff_list")

    return render(request, "accounts/admin/staff/create.html")

def subscribe_email(request):
    if request.method == "POST":
        email = request.POST.get("email")

        subscriber, created = EmailSubscriber.objects.get_or_create(email=email)

        if created:
            send_mail(
                subject="New LMS Subscription",
                message=f"New user subscribed with email: {email}",
                from_email="yourgmail@gmail.com",
                recipient_list=["mahibanavath979@gmail.com"],
                fail_silently=False,
            )

            messages.success(request, "Subscribed successfully!")
        else:
            messages.info(request, "You are already subscribed.")

    return redirect("/")
