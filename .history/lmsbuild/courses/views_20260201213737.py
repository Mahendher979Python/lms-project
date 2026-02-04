from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, CourseMaterial
from accounts.models import TeacherProfile, Batch, Student
from enrollments.models import Enrollment


# ================= ADMIN COURSES =================

@login_required
def admin_course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/admin_courses/course_list.html", {"courses": courses})


@login_required
def admin_course_create(request):

    trainers = TeacherProfile.objects.all()

    if request.method == "POST":
        Course.objectscreate(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            level=request.POST.get("level"),
            duration=request.POST.get("duration"),
            trainer=TeacherProfile.objects.get(id=request.POST.get("trainer"))
        )
        return redirect("admin_course_list")

    return render(request, "courses/admin_courses/course_add.html", {"trainers": trainers})


@login_required
def admin_course_edit(request, pk):

    course = get_object_or_404(Course, pk=pk)
    trainers = TeacherProfile.objects.all()

    if request.method == "POST":

        course.title = request.POST.get("title")
        course.description = request.POST.get("description")
        course.level = request.POST.get("level")
        course.duration = request.POST.get("duration")
        course.trainer = TeacherProfile.objects.get(id=request.POST.get("trainer"))
        course.save()

        return redirect("admin_course_list")

    return render(request, "courses/admin_courses/course_edit.html", {
        "course": course,
        "trainers": trainers
    })


@login_required
def admin_course_delete(request, pk):
    get_object_or_404(Course, pk=pk).delete()
    return redirect("admin_course_list")

# ================= ADMIN MEDIA (VIDEOS) =================

@login_required
def admin_media_list(request):

    materials = CourseMaterial.objects.filter(material_type="video").order_by("-id")

    return render(request, "courses/media/list.html", {
        "materials": materials
    })


@login_required
def admin_media_upload(request):

    if request.method == "POST":

        file = request.FILES.get("file")

        if not file or not file.content_type.startswith("video"):
            messages.error(request, "Only video files allowed")
            return redirect("admin_media_upload")

        CourseMaterial.objects.create(
            title=request.POST.get("title"),
            course=Course.objects.get(id=request.POST.get("course")),
            file=file,
            uploaded_by=request.user,
            material_type="video"
        )

        return redirect("admin_media_list")

    return render(request, "courses/media/upload.html", {
        "courses": Course.objects.all()
    })


@login_required
def admin_media_edit(request, pk):

    media = get_object_or_404(CourseMaterial, id=pk, material_type="video")

    if request.method == "POST":

        media.title = request.POST.get("title")

        if request.FILES.get("file"):

            file = request.FILES.get("file")

            if not file.content_type.startswith("video"):
                messages.error(request, "Only video files allowed")
                return redirect("admin_media_edit", pk=pk)

            media.file = file

        media.save()
        return redirect("admin_media_list")

    return render(request, "courses/media/edit.html", {
        "media": media
    })


@login_required
def admin_media_delete(request, pk):
    get_object_or_404(CourseMaterial, id=pk).delete()
    return redirect("admin_media_list")


# ================= ADMIN MATERIALS (PDF + IMAGES) =================

@login_required
def admin_material_all_list(request):

    materials = CourseMaterial.objects.filter(
        material_type__in=["pdf", "image"]
    ).order_by("-id")

    return render(request, "courses/material/admin/all_list.html", {
        "materials": materials
    })


@login_required
def admin_material_upload(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":

        file = request.FILES.get("file")

        if not file:
            messages.error(request, "File required")
            return redirect("admin_material_upload", course_id=course.id)

        ext = file.name.split('.')[-1].lower()

        if ext == "pdf":
            material_type = "pdf"
        elif file.content_type.startswith("image"):
            material_type = "image"
        else:
            messages.error(request, "Only PDF or Image allowed")
            return redirect("admin_material_upload", course_id=course.id)

        CourseMaterial.objects.create(
            course=course,
            title=request.POST.get("title"),
            file=file,
            uploaded_by=request.user,
            material_type=material_type
        )

        return redirect("admin_material_all_list")

    return render(request, "courses/material/admin/upload.html", {
        "course": course
    })


@login_required
def admin_material_edit(request, pk):

    material = get_object_or_404(
        CourseMaterial,
        id=pk,
        material_type__in=["pdf", "image"]
    )

    if request.method == "POST":

        material.title = request.POST.get("title")

        if request.FILES.get("file"):

            file = request.FILES.get("file")
            ext = file.name.split('.')[-1].lower()

            if ext != "pdf" and not file.content_type.startswith("image"):
                messages.error(request, "Only PDF or Image allowed")
                return redirect("admin_material_edit", pk=pk)

            material.file = file

        material.save()
        return redirect("admin_material_all_list")

    return render(request, "courses/material/admin/edit.html", {
        "material": material
    })


@login_required
def admin_material_delete(request, pk):
    get_object_or_404(CourseMaterial, id=pk).delete()
    return redirect("admin_material_all_list")

# ================= TRAINER COURSES =================

@login_required
def trainer_course_list(request):

    teacher = request.user.teacher_profile
    courses = Course.objects.filter(trainer=teacher)

    return render(request, "courses/trainer_courses/course_list.html", {
        "courses": courses
    })


@login_required
def trainer_course_preview(request, course_id):

    teacher = request.user.teacher_profile
    course = get_object_or_404(Course, id=course_id, trainer=teacher)

    return render(request, "courses/trainer_courses/course_preview.html", {
        "course": course
    })


# ================= TRAINER MATERIALS =================

@login_required
def trainer_material_list(request, course_id):

    teacher = request.user.teacher_profile
    course = get_object_or_404(Course, id=course_id, trainer=teacher)
    materials = CourseMaterial.objects.filter(course=course)

    return render(request, "courses/material/trainer/list.html", {
        "course": course,
        "materials": materials
    })


@login_required
def trainer_material_redirect(request):

    teacher = request.user.teacher_profile
    course = Course.objects.filter(trainer=teacher).first()

    if not course:
        messages.error(request, "No course assigned")
        return redirect("trainer_course_list")

    return redirect("trainer_materials", course_id=course.id)


@login_required
def trainer_material_upload(request, course_id):

    teacher = request.user.teacher_profile
    course = get_object_or_404(Course, id=course_id, trainer=teacher)

    if request.method == "POST":

        file = request.FILES.get("file")
        ext = file.name.split('.')[-1].lower()

        if ext == "pdf":
            material_type = "pdf"
        elif ext in ["mp4", "mov"]:
            material_type = "video"
        else:
            material_type = "image"

        CourseMaterial.objects.create(
            course=course,
            title=request.POST.get("title"),
            file=file,
            uploaded_by=request.user,
            material_type=material_type
        )

        return redirect("trainer_materials", course_id=course.id)

    return render(request, "courses/material/trainer/upload.html", {
        "course": course
    })


@login_required
def trainer_material_delete(request, pk):

    teacher = request.user.teacher_profile
    material = get_object_or_404(CourseMaterial, id=pk, course__trainer=teacher)
    material.delete()

    return redirect("trainer_materials", course_id=material.course.id)


@login_required
def trainer_material_edit(request, pk):

    teacher = request.user.teacher_profile
    material = get_object_or_404(CourseMaterial, id=pk, course__trainer=teacher)

    if request.method == "POST":

        material.title = request.POST.get("title")

        if request.FILES.get("file"):
            material.file = request.FILES.get("file")

        material.save()

        return redirect("trainer_materials", course_id=material.course.id)

    return render(request, "courses/material/trainer/edit.html", {
        "material": material
    })


# ================= TRAINER STUDENTS =================

@login_required
def trainer_material_students(request, course_id):

    teacher = request.user.teacher_profile
    course = get_object_or_404(Course, id=course_id, trainer=teacher)

    batches = Batch.objects.filter(trainer=teacher)
    students = Student.objects.filter(batch__in=batches)

    return render(request, "courses/trainer_courses/student.html", {
        "course": course,
        "students": students
    })


@login_required
def trainer_students_redirect(request):

    teacher = request.user.teacher_profile
    course = Course.objects.filter(trainer=teacher).first()

    if not course:
        messages.error(request, "No course assigned")
        return redirect("trainer_course_list")

    return redirect("trainer_material_students", course_id=course.id)


# ================= STUDENT COURSES (NEW) =================

@login_required
def student_course_list(request):

    student = request.user.student

    enrollments = Enrollment.objects.filter(student=student)
    courses = Course.objects.filter(batch__enrollment__student=student).distinct()

    return render(request, "courses/student_courses/course_list.html", {
        "courses": courses
    })


# ================= STUDENT MATERIALS =================
@login_required
def student_material_redirect(request):

    enrollment = Enrollment.objects.filter(student=request.user).first()

    if not enrollment:
        messages.error(request, "No course enrolled")
        return redirect("student_dashboard")

    return redirect("student_material_list", course_id=enrollment.batch.course.id)


@login_required
def student_material_list(request, course_id):

    student = request.user.student

    enrolled = Enrollment.objects.filter(
        student=student,
        batch__course_id=course_id
    ).exists()

    if not enrolled:
        messages.error(request, "You are not enrolled in this course")
        return redirect("student_dashboard")

    course = get_object_or_404(Course, id=course_id)
    materials = CourseMaterial.objects.filter(course=course)

    return render(request, "courses/material/student/list.html", {
        "course": course,
        "materials": materials
    })
