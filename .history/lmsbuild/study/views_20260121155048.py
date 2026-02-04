from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudyItem
from accounts.models import User   # adjust if custom user path differs
from django.shortcuts import get_object_or_404

#=====================================================
#TODO  ADMIN VIEWS
#=====================================================
@login_required
def admin_todo_list(request):
    if not (request.user.is_superuser or request.user.role == "admin"):
        return redirect("login")

    todos = StudyItem.objects.filter(item_type="todo")
    return render(request, "study/admin/todo/todo_list.html", {"todos": todos})

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

    return render(request, "study/admin/todo/todo_add.html", {"students": students})

#=====================================================
#TODO  TRAINER VIEWS
#=====================================================
@login_required
def trainer_todo_list(request):
    if not (request.user.role == "trainer"):
        return redirect("login")

    todos = StudyItem.objects.filter(
        item_type="todo",
        created_by=request.user
    )

    return render(
        request,
        "study/trainer/todo/todo_list.html",
        {"todos": todos}
    )

@login_required
def trainer_todo_add(request):
    if not (request.user.role == "trainer"):
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
        return redirect("trainer_todo_list")

    return render(
        request,
        "study/trainer/todo/todo_add.html",
        {"students": students}
    )

#=====================================================
#TODO  STUDENT VIEWS
#=====================================================
@login_required
def student_todo_list(request):
    if request.user.role != "student":
        return redirect("login")

    todos = StudyItem.objects.filter(
        item_type="todo",
        assigned_to=request.user
    ).order_by("-created_at")

    return render(
        request,
        "study/student/todo/todo_list.html",
        {"todos": todos}
    )

#=====================================================
#NOTES  ADMIN VIEWS
#=====================================================
@login_required
def admin_notes_list(request):
    if not (request.user.is_superuser or request.user.role == "admin"):
        return redirect("login")

    notes = StudyItem.objects.filter(item_type="notes").order_by("-created_at")
    return render(request, "study/admin/notes_list.html", {"notes": notes})


@login_required
def admin_notes_add(request):
    if not (request.user.is_superuser or request.user.role == "admin"):
        return redirect("login")

    students = User.objects.filter(role="student")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        file = request.FILES.get("file")
        assigned_students = request.POST.getlist("students")

        note = StudyItem.objects.create(
            title=title,
            description=description,
            item_type="notes",
            file=file,
            created_by=request.user
        )
        note.assigned_to.set(assigned_students)
        return redirect("admin_notes_list")

    return render(request, "study/admin/notes_add.html", {"students": students})


@login_required
def admin_notes_edit(request, pk):
    if not (request.user.is_superuser or request.user.role == "admin"):
        return redirect("login")

    note = get_object_or_404(StudyItem, pk=pk, item_type="notes")
    students = User.objects.filter(role="student")

    if request.method == "POST":
        note.title = request.POST.get("title")
        note.description = request.POST.get("description")
        if request.FILES.get("file"):
            note.file = request.FILES.get("file")
        note.assigned_to.set(request.POST.getlist("students"))
        note.save()
        return redirect("admin_notes_list")

    return render(
        request,
        "study/admin/notes_edit.html",
        {"note": note, "students": students}
    )


@login_required
def admin_notes_delete(request, pk):
    if not (request.user.is_superuser or request.user.role == "admin"):
        return redirect("login")

    note = get_object_or_404(StudyItem, pk=pk, item_type="notes")
    note.delete()
    return redirect("admin_notes_list")
