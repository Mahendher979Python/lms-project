from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required

User = get_user_model()

# ===============================
# USER LIST
# ===============================
@login_required
@admin_required
def admin_users(request):
    role = request.GET.get('role')  # student / trainer

    users = User.objects.exclude(role='admin')
    if role:
        users = users.filter(role=role)

    return render(
        request,
        "accounts/admin/users/users_list.html",
        {"users": users}
    )

# ===============================
# CREATE USER
# ===============================
from django.db import IntegrityError

@login_required
@admin_required
def admin_create_user(request):
    if request.method == "POST":
        role = request.POST.get("role")
        email = request.POST.get("email")

        if not email or not role:
            messages.error(request, "All fields are required")
            return redirect("admin_create_user")

        # 🔐 AUTO UNIQUE USERNAME
        base_username = email.split("@")[0]
        username = base_username
        count = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{count}"
            count += 1

        password = get_random_string(8)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                is_active=True,
                is_staff=(role != "student")
            )
        except IntegrityError:
            messages.error(request, "User already exists")
            return redirect("admin_create_user")

        request.session["created_user"] = {
            "username": username,
            "password": password,
            "role": role
        }

        return redirect("admin_user_created")

    return render(request, "accounts/admin/users/create_user.html")

# ===============================
# SHOW PASSWORD (ONCE)
# ===============================
@login_required
@admin_required
def admin_user_created(request):
    data = request.session.pop("created_user", None)
    if not data:
        return redirect("admin_users")

    return render(
        request,
        "accounts/admin/users/user_created.html",
        data
    )

# ===============================
# EDIT USER
# ===============================
@login_required
@admin_required
def admin_edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.is_active = request.POST.get("status") == "active"

        new_password = request.POST.get("password")
        if new_password:
            user.set_password(new_password)

        user.save()
        messages.success(request, "User updated successfully")
        return redirect("admin_users")

    return render(
        request,
        "accounts/admin/users/user_edit.html",
        {"user": user}
    )

# ===============================
# DELETE USER
# ===============================
@login_required
@admin_required
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect("admin_users")
