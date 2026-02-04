from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required

User = get_user_model()

@login_required
@admin_required
def admin_users(request):
    role = request.GET.get('role')  # admin / trainer / student

    users = User.objects.exclude(role='admin')
    if role:
        users = users.filter(role=role)

    return render(request, 'accounts/admin/users/users_list.html', {
        'users': users
    })

@login_required
@admin_required
def admin_create_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        role = request.POST['role']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username exists")
            return redirect('admin_create_user')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email exists")
            return redirect('admin_create_user')

        password = get_random_string(8)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            is_active=True,
            is_staff=(role != 'student')
        )

        request.session['created_user'] = {
            'username': username,
            'password': password,
            'role': role
        }

        return redirect('admin_user_created')

    return render(request, 'admin/users/user_create.html')

@login_required
@admin_required
def admin_user_created(request):
    data = request.session.pop('created_user', None)
    if not data:
        return redirect('admin_users')

    return render(request, 'admin/users/user_created.html', data)

@login_required
@admin_required
def admin_edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.is_active = request.POST.get('status') == 'active'

        new_password = request.POST.get('password')
        if new_password:
            user.set_password(new_password)

        user.save()
        messages.success(request, "User updated")
        return redirect('admin_users')

    return render(request, 'admin/users/user_edit.html', {
        'user': user
    })

@login_required
@admin_required
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted")
    return redirect('admin_users')
