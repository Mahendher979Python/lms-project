# =========================
# IMPORTS
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Course, SessionVideo, Advertisement
from .forms import CourseForm, LessonForm   # ✅ LessonForm add cheyyali


# =========================
# TRAINER – COURSE LIST
# =========================
@login_required
def admin_course_list(request):
    # Only admin access
    if request.user.role != 'admin':
        return redirect('login')

    # All courses (latest first)
    courses = Course.objects.all().order_by('-created_at')

    return render(request, 'courses/admin/course_list.html', {
        'courses': courses
    })

# =========================
# TRAINER – CREATE COURSE
# =========================
@login_required
def trainer_course_create(request):
    if request.user.role != 'trainer':
        return redirect('login')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.trainer = request.user   # ✅ Auto assign trainer
            course.save()
            return redirect('trainer_course_list')
    else:
        form = CourseForm()

    return render(request, 'courses/trainer/course_form.html', {
        'form': form,
        'action': 'Add'
    })

# =========================
# TRAINER – EDIT COURSE
# =========================
@login_required
def trainer_course_edit(request, course_id):
    if request.user.role != 'trainer':
        return redirect('login')

    # Trainer own course only edit cheyagaladu
    course = get_object_or_404(Course, id=course_id, trainer=request.user)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('trainer_course_list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/trainer/course_form.html', {
        'form': form,
        'action': 'Edit'
    })
