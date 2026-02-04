from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import Enrollment


@login_required
def student_course_detail(request, course_id):
    if request.user.role != 'student':
        return redirect('login')

    course = get_object_or_404(Course, id=course_id, is_published=True)

    # Check enrollment
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        return redirect('student_course_list')

    lessons = course.lessons.all().order_by('order')

    return render(request, 'enrollments/student/course_detail.html', {
        'course': course,
        'lessons': lessons
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
