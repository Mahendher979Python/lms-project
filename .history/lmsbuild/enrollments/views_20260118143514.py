from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import Enrollment

@login_required
def student_course_list(request):
    if request.user.role != 'student':
        return redirect('login')

    courses = Course.objects.filter(is_published=True)
    enrolled_ids = Enrollment.objects.filter(
        student=request.user
    ).values_list('course_id', flat=True)

    return render(request, 'enrollments/student/course_list.html', {
        'courses': courses,
        'enrolled_ids': enrolled_ids
    })


@login_required
def enroll_course(request, course_id):
    if request.user.role != 'student':
        return redirect('login')

    course = get_object_or_404(Course, id=course_id, is_published=True)
    Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )
    return redirect('student_course_list')
