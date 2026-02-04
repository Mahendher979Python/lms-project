from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from .models import StudentProfile, TrainerProfile, AdminProfile


# -----------------------------
# COMMON PROFILE VIEW (SELF)
# -----------------------------
@login_required
def profile_view(request):
    user = request.user

    if user.role == "student":
        profile, _ = StudentProfile.objects.get_or_create(user=user)
        return render(request, "profiles/student_profile.html", {"profile": profile})

    elif user.role == "trainer":
        profile, _ = TrainerProfile.objects.get_or_create(
            user=user,
            defaults={"qualification": "", "experience_years": 0, "expertise": ""},
        )
        return render(request, "profiles/trainer_profile.html", {"profile": profile})

    elif user.role in ["admin", "superadmin"]:
        profile, _ = AdminProfile.objects.get_or_create(user=user)
        return render(request, "profiles/admin_profile.html", {"profile": profile})

    return redirect("login")


# -----------------------------
# ADMIN ONLY – STUDENT LIST
# -----------------------------
@login_required
def admin_student_list(request):
    if request.user.role not in ["admin", "superadmin"]:
        return HttpResponseForbidden("Access Denied")

    students = StudentProfile.objects.select_related("user").all()
    return render(
        request,
        "profiles/admin_student_list.html",
        {"students": students},
    )


# -----------------------------
# ADMIN ONLY – TRAINER LIST
# -----------------------------
@login_required
def admin_trainer_list(request):
    if request.user.role not in ["admin", "superadmin"]:
        return HttpResponseForbidden("Access Denied")

    trainers = TrainerProfile.objects.select_related("user").all()
    return render(
        request,
        "profiles/admin_trainer_list.html",
        {"trainers": trainers},
    )


# -----------------------------
# ADMIN ONLY – PROFILE DETAIL
# -----------------------------
@login_required
def admin_profile_detail(request, role, profile_id):
    if request.user.role not in ["admin", "superadmin"]:
        return HttpResponseForbidden("Access Denied")

    if role == "student":
        profile = get_object_or_404(StudentProfile, id=profile_id)

    elif role == "trainer":
        profile = get_object_or_404(TrainerProfile, id=profile_id)

    else:
        return HttpResponseForbidden("Invalid Role")

    return render(
        request,
        "profiles/admin_profile_detail.html",
        {
            "profile": profile,
            "role": role,
        },
    )
