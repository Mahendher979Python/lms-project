from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from accounts.models import TeacherProfile, Batch,Course
from .models import Course, CourseMaterial
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from enrollments.models import Enrollment






# ================= ADMIN COURSE LIST =========================================CRUD
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

# ================= ADMIN MEDIA LIST ===========================================================CRUD
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

@login_required
def admin_media_edit(request, material_id):

    media = get_object_or_404(CourseMaterial, id=material_id)

    if request.method == "POST":
        media.title = request.POST.get("title")

        if request.FILES.get("file"):
            file = request.FILES.get("file")

            # VIDEO VALIDATION AGAIN
            if not file.content_type.startswith("video"):
                messages.error(request, "Only video files allowed!")
                return redirect("admin_media_edit", material_id=material_id)

            media.file = file

        media.save()

        return redirect("admin_media_list")

    return render(request, "courses/media/edit.html", {
        "media": media
    })

@login_required
def admin_media_delete(request, material_id):

    media = get_object_or_404(CourseMaterial, id=material_id)

    media.delete()

    return redirect("admin_media_list")


# ================= ADMIN MATERIAL =================CRUD===================================================

@login_required
def admin_material_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    materials = CourseMaterial.objects.filter(course=course)

    return render(request, "courses/material/admin/list.html", {
        "course": course,
        "materials": materials
    })

@login_required
def admin_material_upload(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        CourseMaterial.objects.create(
            course=course,
            title=request.POST.get("title"),
            file=request.FILES.get("file"),
            uploaded_by=request.user      # 🔥 ADD THIS
        )
        return redirect("admin_material_list", course_id=course.id)

    return render(request, "courses/material/admin/upload.html", {"course": course})

@login_required
def admin_material_edit(request, material_id):

    material = get_object_or_404(CourseMaterial, id=material_id)

    if request.method == "POST":
        material.title = request.POST.get("title")

        # Replace file only if new file selected
        if request.FILES.get("file"):
            material.file = request.FILES.get("file")

        material.save()

        return redirect("admin_material_list", course_id=material.course.id)

    return render(request, "courses/material/admin/edit.html", {
        "material": material
    })

@login_required
def admin_material_delete(request, material_id):
    material = get_object_or_404(CourseMaterial, id=material_id)
    course_id = material.course.id
    material.delete()
    return redirect("admin_material_list", course_id=course_id)

#====================================================================================================================

# ============================ TRAINER COURSE LIST ============================

@login_required
def trainer_course_list(request):
    teacher = request.user.teacher_profile

    courses = Course.objects.filter(
        trainer=teacher
    ).select_related()

    return render(request, "courses/trainer_courses/course_list.html", {
        "courses": courses
    })


# ============================ TRAINER COURSE PREVIEW =========================

@login_required
def trainer_course_preview(request, course_id):
    teacher = request.user.teacher_profile

    course = get_object_or_404(
        Course,
        id=course_id,
        trainer=teacher
    )

    return render(request, "courses/trainer_courses/course_preview.html", {
        "course": course
    })


# ============================ TRAINER MATERIAL LIST ==========================

@login_required
def trainer_material_list(request, course_id):
    teacher = request.user.teacher_profile

    course = get_object_or_404(
        Course,
        id=course_id,
        trainer=teacher
    )

    materials = CourseMaterial.objects.filter(course=course)

    return render(request, "courses/material/trainer/list.html", {
        "course": course,
        "materials": materials
    })


# ============================ TRAINER STUDENTS ===============================

@login_required
def trainer_students(request, course_id):
    teacher = request.user.teacher_profile

    course = get_object_or_404(
        Course,
        id=course_id,
        trainer=teacher
    )

    batches = Batch.objects.filter(course=course)

    students = Enrollment.objects.filter(
        batch__in=batches
    ).select_related("student", "batch")

    return render(request, "courses/trainer_courses/students_courses.html", {
        "course": course,
        "students": students
    })


# ============================ TRAINER MATERIAL UPLOAD ========================

@login_required
def trainer_material_upload(request, course_id):
    teacher = request.user.teacher_profile

    course = get_object_or_404(
        Course,
        id=course_id,
        trainer=teacher
    )

    if request.method == "POST":
        title = request.POST.get("title")
        file = request.FILES.get("file")

        if not title or not file:
            messages.error(request, "Title and file are required.")
            return redirect("trainer_material_upload", course_id=course.id)

        CourseMaterial.objects.create(
            course=course,
            title=title,
            file=file,
            uploaded_by=request.user
        )

        messages.success(request, "Material uploaded successfully.")

        return redirect("trainer_materials", course_id=course.id)

    return render(request, "courses/material/trainer/upload.html", {
        "course": course
    })

# ============================ TRAINER MATERIAL EDIT ============================

@login_required
def trainer_material_edit(request, pk):

    teacher = request.user.teacher_profile

    material = get_object_or_404(
        CourseMaterial,
        id=pk,
        course__trainer=teacher
    )

    if request.method == "POST":

        material.title = request.POST.get("title")

        if request.FILES.get("file"):
            material.file = request.FILES.get("file")

        material.save()

        return redirect("trainer_materials", course_id=material.course.id)

    return render(request, "courses/material/trainer/edit.html", {
        "material": material
    })

# ============================ TRAINER MATERIAL DELETE ==========================

@login_required
def trainer_material_delete(request, pk):

    teacher = request.user.teacher_profile

    material = get_object_or_404(
        CourseMaterial,
        id=pk,
        course__trainer=teacher
    )

    course_id = material.course.id

    material.delete()

    return redirect("trainer_materials", course_id=course_id)
