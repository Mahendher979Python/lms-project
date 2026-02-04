from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import StudentProfile, TrainerProfile, AdminProfile
from .forms import (
    StudentProfileForm,
    TrainerProfileForm,
    AdminProfileForm,
)


@login_required
def profile_view(request):
    user = request.user

    if user.role == "student":
        profile = StudentProfile.objects.get(user=user)
        return render(request, "profiles/student_profile.html", {"profile": profile})

    elif user.role == "trainer":
        profile = TrainerProfile.objects.get(user=user)
        return render(request, "profiles/trainer_profile.html", {"profile": profile})

    elif user.role in ["admin", "superadmin"]:
        profile = AdminProfile.objects.get(user=user)
        return render(request, "profiles/admin_profile.html", {"profile": profile})

    return redirect("login")


@login_required
def profile_edit(request):
    user = request.user

    if user.role == "student":
        profile = StudentProfile.objects.get(user=user)
        form = StudentProfileForm(request.POST or None, instance=profile)

    elif user.role == "trainer":
        profile = TrainerProfile.objects.get(user=user)
        form = TrainerProfileForm(request.POST or None, instance=profile)

    elif user.role in ["admin", "superadmin"]:
        profile = AdminProfile.objects.get(user=user)
        form = AdminProfileForm(request.POST or None, instance=profile)

    else:
        return redirect("login")

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("profile_view")

    return render(request, "profiles/profile_edit.html", {"form": form})
