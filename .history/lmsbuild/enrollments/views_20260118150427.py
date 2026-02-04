from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import Enrollment


# 1️⃣ STUDENT – COURSE LIST
@login_required
def student_course_list(request):
    if request.user.role != 'student':
        return redirect('login')

    courses = Course.objects.filter(is_published=True)

    enrolled_ids = Enrollment.objects.filter(
        student=request.user
    ).values_list('course_id', flat=True)

    return render(
        request,
        'enrollments/student/course_list.html',
        {
            'courses': courses,
            'enrolled_ids': enrolled_ids
        }
    )


# 2️⃣ STUDENT – COURSE DETAIL + LESSONS
@login_required
def student_course_detail(request, course_id):
    if request.user.role != 'student':
        return redirect('login')

    course = get_object_or_404(
        Course,
        id=course_id,
        is_published=True
    )

    # allow only enrolled students
    if not Enrollment.objects.filter(
        student=request.user,
        course=course
    ).exists():
        return redirect('student_course_list')

    lessons = course.lessons.all().order_by('order')

    return render(
        request,
        'enrollments/student/course_detail.html',
        {
            'course': course,
            'lessons': lessons
        }
    )


# 3️⃣ STUDENT – ENROLL COURSE
@login_required
def enroll_course(request, course_id):
    if request.user.role != 'student':
        return redirect('login')

    course = get_object_or_404(
        Course,
        id=course_id,
        is_published=True
    )

    Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    return redirect('student_course_list')
