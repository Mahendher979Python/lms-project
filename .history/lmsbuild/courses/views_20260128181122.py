from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from accounts.models import TeacherProfile
from .models import Course, CourseMaterial
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required



# ================= ADMIN COURSE LIST =================
@login_required
def admin_course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/admin_courses/course_list.html", {
        "courses": courses
    })

# ================= ADMIN COURSE CREATE =================
@login_required
def admin_course_create(request):
    trainers = TeacherProfile.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        level = request.POST.get("level")
        duration = request.POST.get("duration")
        trainer_id = request.POST.get("trainer")

        trainer = TeacherProfile.objects.get(id=trainer_id)

        Course.objects.create(
            title=title,
            description=description,
            level=level,
            duration=duration,
            trainer=trainer
        )

        return redirect("admin_course_list")

    return render(request, "courses/admin_courses/course_add.html", {
        "trainers": trainers
    })

# ================= ADMIN COURSE EDIT =================
@login_required
def admin_course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    trainers = TeacherProfile.objects.all()

    if request.method == "POST":
        course.title = request.POST.get("title")
        course.description = request.POST.get("description")
        course.level = request.POST.get("level")
        course.duration = request.POST.get("duration")
        trainer_id = request.POST.get("trainer")
        course.trainer = TeacherProfile.objects.get(id=trainer_id)
        course.save()

        return redirect("admin_course_list")

    return render(request, "courses/admin_courses/course_edit.html", {
        "course": course,
        "trainers": trainers
    })

# ================= ADMIN COURSE DELETE =================
@login_required
def admin_course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect("admin_course_list")


# ================= TRAINER MATERIAL LIST =================
@login_required
def trainer_material_list(request, course_id):
    course = get_object_or_404(Course, id=course_id, trainer=request.user)
    materials = CourseMaterial.objects.filter(course=course)

    return render(request, "courses/trainer/material/list.html", {
        "course": course,
        "materials": materials
    })


@login_required
def trainer_material_upload(request, course_id):

    course = get_object_or_404(Course, id=course_id, trainer=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        file = request.FILES.get("file")

        CourseMaterial.objects.create(
            course=course,
            title=title,
            file=file,
            uploaded_by=request.user
        )

        return redirect("trainer_material_list", course_id=course.id)

    return render(request, "courses/trainer/material/upload.html", {"course": course})

def admin_media_list(request):
    return render(request, "courses/media/list.html")
