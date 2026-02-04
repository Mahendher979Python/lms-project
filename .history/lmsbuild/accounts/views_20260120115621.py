from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from .decorators import admin_required
from django.contrib.auth import get_user_model
from accounts.models import StudentProfile, Course, TrainerProfile, User
from courses.models import Course

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


# ================= TRAINER EDIT =================
@admin_required
def trainer_edit(request, id):
    trainer = get_object_or_404(User, id=id, role='trainer')

    profile, created = TrainerProfile.objects.get_or_create(
        user=trainer,
        defaults={
            'qualification': 'N/A',
            'designation': 'Trainer',
            'experience': 0
        }
    )

    if request.method == "POST":
        trainer.username = request.POST['username']
        trainer.mobile = request.POST['mobile']
        trainer.is_active = 'is_active' in request.POST
        trainer.save()

        profile.qualification = request.POST['qualification']
        profile.designation = request.POST['designation']
        profile.experience = request.POST['experience']
        profile.save()

        messages.success(request, "Trainer updated successfully ✅")
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



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string

User = get_user_model()

# ===============================
# 1. LIST STUDENTS
# ===============================
@login_required
def admin_students(request):
    # Admin చెక్ (లేకపోతే Login కి పంపిస్తుంది)
    if not request.user.is_superuser and request.user.role != "admin":
        return redirect("login")

    # కేవలం స్టూడెంట్స్ ని మాత్రమే తీసుకురావాలి
    students = User.objects.filter(role="student").order_by('-date_joined')

    return render(request, "admin/student_admin/list.html", {
        "students": students
    })

# ===============================
# 2. ADD STUDENT (Auto Password)
# ===============================
# views.py లో ఈ మార్పులు చేయండి

@login_required
def admin_add_student(request):
    # ... (Permission checks same as before) ...

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        # ✅ Extra Fields from Form
        roll_no = request.POST.get("roll_no")
        phone = request.POST.get("phone")

        # 1. Check validations (Username/Email exist?)
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("admin_add_student")

        # 2. Create User (Authentication)
        password = get_random_string(8)
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password, 
            role="student"
        )

        # 3. ✅ Create Student Profile (Extra Details)
        Student.objects.create(
            user=user,
            roll_no=roll_no,
            phone=phone
        )

        # 4. Save session & Redirect
        request.session["new_student_password"] = password
        request.session["new_student_username"] = username
        
        messages.success(request, "Student created successfully")
        return redirect("admin_student_created")

    return render(request, "admin/student_admin/add_student.html")
# ===============================
# 3. SUCCESS PAGE (Show Password)
# ===============================
@login_required
def admin_student_created(request):
    # సెషన్ నుండి డేటా తీసి, వెంటనే డిలీట్ చేస్తుంది (Security కోసం)
    password = request.session.pop("new_student_password", None)
    username = request.session.pop("new_student_username", None)

    if not password:
        return redirect("admin_students")

    return render(request, "admin/student_admin/student_created.html", {
        "username": username,
        "password": password
    })

# ===============================
# 4. EDIT STUDENT
# ===============================
@login_required
def admin_edit_student(request, student_id):
    student = get_object_or_404(User, id=student_id, role="student")

    if request.method == "POST":
        student.username = request.POST["username"]
        student.email = request.POST["email"]
        # స్టేటస్ అప్‌డేట్
        status = request.POST.get("status")
        student.is_active = (status == "active")

        # పాస్‌వర్డ్ ఇస్తేనే అప్‌డేట్ చేయాలి
        new_password = request.POST.get("password")
        if new_password:
            student.set_password(new_password)

        student.save()
        messages.success(request, f"Student '{student.username}' updated!")
        return redirect("admin_students")

    return render(request, "admin/student_admin/edit_student.html", {
        "student": student
    })

# ===============================
# 5. DELETE STUDENT
# ===============================
@login_required
def admin_delete_student(request, student_id):
    student = get_object_or_404(User, id=student_id, role="student")
    student.delete()
    messages.success(request, "Student account deleted.")
    return redirect("admin_students")