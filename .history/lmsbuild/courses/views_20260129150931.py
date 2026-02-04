from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from accounts.models import TeacherProfile
from .models import Course, CourseMaterial
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import CourseMaterial




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

# ================= ADMIN MEDIA LIST =================
@login_required
def admin_media_list(request):
    materials = CourseMaterial.objects.all().order_by("-created_at")
    return render(request, "courses/media/list.html", {
        "materials": materials
    })

@login_required
def admin_media_upload(request):

    if request.method == "POST":

        title = request.POST.get("title")
        course_id = request.POST.get("course")
        file = request.FILES.get("file")

        # ---------------- VIDEO VALIDATION ----------------
        if not file.content_type.startswith("video"):
            messages.error(request, "Only video files allowed!")
            return redirect("admin_media_upload")
        # -------------------------------------------------

        course = Course.objects.get(id=course_id)

        CourseMaterial.objects.create(
            title=title,
            course=course,
            file=file,
            uploaded_by=request.user
        )

        return redirect("admin_media_list")

    courses = Course.objects.all()
    return render(request,"courses/media/upload.html",{"courses":courses})

# ================= ADMIN MATERIAL LIST =================
@login_required
def admin_material_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    materials = CourseMaterial.objects.filter(course=course)

    return render(request, "courses/material/admin/list.html", {
        "course": course,
        "materials": materials
    })

# ================= ADMIN MATERIAL UPLOAD =================
@login_required
def admin_material_upload(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        CourseMaterial.objects.create(
            course=course,
            title=request.POST.get("title"),
            file=request.FILES.get("file")
        )

        return redirect("admin_material_list", course_id=course.id)

    return render(request, "courses/material/admin/upload.html", {
        "course": course
    })


# ================= TRAINER MATERIAL LIST ========================================================================================
@login_required
def trainer_material_list(request, course_id):
    course = get_object_or_404(Course, id=course_id, trainer=request.user)
    materials = CourseMaterial.objects.filter(course=course)

    return render(request, "courses/material/trainer/list.html", {
        "course": course,
        "materials": materials
    })

@login_required
def trainer_material_upload(request, course_id):
    course = get_object_or_404(Course, id=course_id, trainer=request.user)

    if request.method == "POST":
        CourseMaterial.objects.create(
            course=course,
            title=request.POST.get("title"),
            file=request.FILES.get("file")
        )

        return redirect("trainer_material_list", course_id=course.id)

    return render(request, "courses/material/trainer/upload.html", {
        "course": course
    })

# Trainer Courses List===========================
@login_required
def trainer_course_list(request):
    courses = Course.objects.filter(trainer=request.user)
    return render(request, "courses/trainer/course_list.html", {
        "courses": courses
    })


