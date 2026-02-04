from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import StudyItem
from accounts.models import User   # adjust if custom user path differs


@login_required
def admin_todo_list(request):
    if not (request.user.is_superuser or request.user.role == "admin"):
        return redirect("login")

    todos = StudyItem.objects.filter(item_type="todo")
    return render(request, "study/admin/todo_list.html", {"todos": todos})


@login_required
def admin_todo_add(request):
    if not (request.user.is_superuser or request.user.role == "admin"):
        return redirect("login")

    students = User.objects.filter(role="student")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        file = request.FILES.get("file")
        assigned_students = request.POST.getlist("students")

        todo = StudyItem.objects.create(
            title=title,
            description=description,
            item_type="todo",
            file=file,
            created_by=request.user
        )

        todo.assigned_to.set(assigned_students)
        return redirect("admin_todo_list")

    return render(request, "study/admin/todo_add.html", {"students": students})
