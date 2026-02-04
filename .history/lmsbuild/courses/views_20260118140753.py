from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course


@login_required
def admin_course_list(request):
    if request.user.role != 'admin':
        return redirect('login')

    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses/admin/course_list.html', {
        'courses': courses
    })


@login_required
def trainer_course_list(request):
    if request.user.role != 'trainer':
        return redirect('login')

    courses = Course.objects.filter(trainer=request.user)
    return render(request, 'courses/trainer/course_list.html', {
        'courses': courses
    })
