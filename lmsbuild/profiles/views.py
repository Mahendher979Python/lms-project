from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from .models import StudentProfile, TrainerProfile, AdminProfile
from .forms import (
    StudentProfileForm,
    TrainerProfileForm,
    AdminProfileForm,
    UserProfilePicForm,
)

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
            defaults={
                "qualification": "",
                "experience_years": 0,
                "expertise": "",
                "certifications": "",
            },
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
        {"profile": profile, "role": role},
    )


# -----------------------------
# PROFILE EDIT (WITH PROFILE PIC)
# -----------------------------
@login_required
def profile_edit(request):
    user = request.user

    # PROFILE PIC FORM (COMMON)
    user_form = UserProfilePicForm(
        request.POST or None,
        request.FILES or None,
        instance=user,
    )

    # ROLE BASED PROFILE FORM
    if user.role == "trainer":
        profile, _ = TrainerProfile.objects.get_or_create(
            user=user,
            defaults={
                "qualification": "",
                "experience_years": 0,
                "expertise": "",
                "certifications": "",
            },
        )
        form = TrainerProfileForm(request.POST or None, instance=profile)

    elif user.role == "student":
        profile, _ = StudentProfile.objects.get_or_create(user=user)
        form = StudentProfileForm(request.POST or None, instance=profile)

    elif user.role in ["admin", "superadmin"]:
        profile, _ = AdminProfile.objects.get_or_create(user=user)
        form = AdminProfileForm(request.POST or None, instance=profile)

    else:
        return redirect("login")

    # SAVE BOTH FORMS
    if request.method == "POST":
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            return redirect("profile_view")

    return render(
        request,
        "profiles/profile_edit.html",
        {
            "form": form,
            "user_form": user_form,
        },
    )
