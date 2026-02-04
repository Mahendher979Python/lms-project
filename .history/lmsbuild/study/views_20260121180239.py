from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from courses.models import Course   # ✅ THIS WAS MISSING
from .models import StudyItem

from courses.models import Course   # adjust if custom user path differs
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


# =====================================================
# NOTES – ADMIN VIEWS (CRUD)
# =====================================================

@login_required
def admin_notes_list(request):
    if not (request.user.is_superuser or request.user.role == "admin"):
        return redirect("login")

    notes = StudyItem.objects.filter(item_type="notes")
    return render(request, "study/admin/notes/notes_list.html", {"notes": notes})


@login_required
def admin_notes_add(request):
    if not (request.user.is_superuser or request.user.role == "admin"):
        return redirect("login")

    students = User.objects.filter(role="student")
    trainers = User.objects.filter(role="trainer")
    courses = Course.objects.all()

    if request.method == "POST":
        note = StudyItem.objects.create(
            title=request.POST["title"],
            description=request.POST.get("description"),
            file=request.FILES.get("file"),
            item_type="notes",
            created_by=request.user,
            course_id=request.POST.get("course") or None,
            visibility=request.POST.get("visibility"),
            is_active=True,
        )

        assigned_users = request.POST.getlist("assigned_to")
        note.assigned_to.set(assigned_users)

        return redirect("admin_notes_list")

    return render(
        request,
        "study/admin/notes/notes_add.html",
        {
            "students": students,
            "trainers": trainers,
            "courses": courses,
        },
    )


@login_required
def admin_notes_edit(request, pk):
    if not (request.user.is_superuser or request.user.role == "admin"):
        return redirect("login")

    note = get_object_or_404(StudyItem, pk=pk, item_type="notes")
    students = User.objects.filter(role="student")
    trainers = User.objects.filter(role="trainer")
    courses = Course.objects.all()

    if request.method == "POST":
        note.title = request.POST.get("title")
        note.description = request.POST.get("description")
        note.course_id = request.POST.get("course") or None
        note.visibility = request.POST.get("visibility")
        note.is_active = True if request.POST.get("is_active") else False

        if request.FILES.get("file"):
            note.file = request.FILES.get("file")

        note.assigned_to.set(request.POST.getlist("assigned_to"))
        note.save()
        return redirect("admin_notes_list")

    return render(
        request,
        "study/admin/notes/notes_edit.html",
        {
            "note": note,
            "students": students,
            "trainers": trainers,
            "courses": courses,
        },
    )


@login_required
def admin_notes_delete(request, pk):
    if not (request.user.is_superuser or request.user.role == "admin"):
        return redirect("login")

    note = get_object_or_404(StudyItem, pk=pk, item_type="notes")
    note.delete()
    return redirect("admin_notes_list")


# =====================================================
# NOTES – TRAINER VIEWS (ADD + EDIT)
# =====================================================

@login_required
def trainer_notes_list(request):
    if request.user.role != "trainer":
        return redirect("login")

    notes = StudyItem.objects.filter(
        item_type="notes",
        created_by=request.user
    )
    return render(request, "study/trainer/notes/notes_list.html", {"notes": notes})

@login_required
def admin_notes_add(request):
    if not (request.user.is_superuser or request.user.role == "admin"):
        return redirect("login")

    students = User.objects.filter(role="student")
    trainers = User.objects.filter(role="trainer")
    courses = Course.objects.all()

    if request.method == "POST":
        note = StudyItem.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            file=request.FILES.get("file"),
            item_type="notes",
            created_by=request.user,
            course_id=request.POST.get("course") or None,
            visibility=request.POST.get("visibility", "private"),  # ✅ FIX
            is_active=True,
        )

        note.assigned_to.set(request.POST.getlist("assigned_to"))
        return redirect("admin_notes_list")

    return render(
        request,
        "study/admin/notes/notes_add.html",
        {
            "students": students,
            "trainers": trainers,
            "courses": courses,
        },
    )


@login_required
def trainer_notes_edit(request, pk):
    if request.user.role != "trainer":
        return redirect("login")

    note = get_object_or_404(
        StudyItem,
        pk=pk,
        item_type="notes",
        created_by=request.user
    )
    students = User.objects.filter(role="student")

    if request.method == "POST":
        note.title = request.POST.get("title")
        note.description = request.POST.get("description")

        if request.FILES.get("file"):
            note.file = request.FILES.get("file")

        note.assigned_to.set(request.POST.getlist("assigned_to"))
        note.save()
        return redirect("trainer_notes_list")

    return render(
        request,
        "study/trainer/notes/notes_edit.html",
        {"note": note, "students": students},
    )


# =====================================================
# NOTES – STUDENT VIEW (READ ONLY)
# =====================================================

@login_required
def student_notes_list(request):
    if request.user.role != "student":
        return redirect("login")

    notes = StudyItem.objects.filter(
        item_type="notes",
        assigned_to=request.user,
        is_active=True
    ).select_related("created_by").order_by("-created_at")

    return render(
        request,
        "study/student/notes/notes_list.html",
        {"notes": notes}
    )




