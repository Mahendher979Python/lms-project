from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import Enrollment

from core_settings.decorators import student_approval_required, student_active_required


# ==================================================
# STUDENT – COURSE LIST
# ==================================================

@login_required
def student_course_list(request):

    if request.user.role != "student":
        return redirect("login")

    student = request.user.student   # Student profile

    # 1️⃣ Courses assigned to student's trainer
    trainer_courses = Course.objects.filter(trainer=student.trainer)

    # 2️⃣ Enrolled course ids
    enrolled_ids = Enrollment.objects.filter(
        student=request.user,
        is_active=True
    ).values_list("course_id", flat=True)

    # 3️⃣ FINAL: only trainer + enrolled
    courses = trainer_courses.filter(id__in=enrolled_ids)

    return render(
        request,
        "enrollments/student/course_list.html",
        {
            "courses": courses,
        }
    )



# ==================================================
# STUDENT – COURSE DETAIL + LESSONS
# ==================================================

@login_required
def student_course_detail(request, course_id):

    if request.user.role != "student":
        return redirect("login")

    course = get_object_or_404(Course, id=course_id)

    # Allow only enrolled students
    if not Enrollment.objects.filter(
        student=request.user,
        course=course,
        is_active=True
    ).exists():
        return redirect("student_course_list")

    lessons = course.lessons.all()

    return render(
        request,
        "enrollments/student/course_detail.html",
        {
            "course": course,
            "lessons": lessons
        }
    )


# ==================================================
# STUDENT – ENROLL COURSE
# ==================================================

@login_required
@student_approval_required
@student_active_required
def enroll_course(request, course_id):

    if request.user.role != "student":
        return redirect("login")

    course = get_object_or_404(Course, id=course_id)

    Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    return redirect("student_course_list")

