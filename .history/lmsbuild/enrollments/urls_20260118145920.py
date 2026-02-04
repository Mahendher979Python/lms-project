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
