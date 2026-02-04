from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Course, SessionVideo, Advertisement
from .forms import CourseForm


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



@login_required
def trainer_course_create(request):
    if request.user.role != 'trainer':
        return redirect('login')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.trainer = request.user   # 🔥 auto assign
            course.save()
            return redirect('trainer_course_list')
    else:
        form = CourseForm()

    return render(request, 'courses/trainer/course_form.html', {
        'form': form,
        'action': 'Add'
    })

@login_required
def trainer_course_edit(request, course_id):
    if request.user.role != 'trainer':
        return redirect('login')

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

@login_required
def trainer_lesson_list(request, course_id):
    if request.user.role != 'trainer':
        return redirect('login')

    course = get_object_or_404(Course, id=course_id, trainer=request.user)
    lessons = course.lessons.all().order_by('order')

    return render(request, 'courses/trainer/lesson_list.html', {
        'course': course,
        'lessons': lessons
    })


@login_required
def trainer_lesson_add(request, course_id):
    if request.user.role != 'trainer':
        return redirect('login')

    course = get_object_or_404(Course, id=course_id, trainer=request.user)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('trainer_lesson_list', course_id=course.id)
    else:
        form = LessonForm()

    return render(request, 'courses/trainer/lesson_form.html', {
        'course': course,
        'form': form
    })



def public_media_view(request):
    videos = SessionVideo.objects.filter(is_active=True)
    ads = Advertisement.objects.filter(is_active=True)

    return render(request, 'courses/media/public_media.html', {
        'videos': videos,
        'ads': ads
    })

from .models import SessionVideo, Advertisement
from django.contrib.auth.decorators import login_required

@login_required
def admin_media_list(request):
    if request.user.role != 'admin':
        return redirect('login')

    videos = SessionVideo.objects.all()
    ads = Advertisement.objects.all()

    return render(request, 'courses/admin/media_list.html', {
        'videos': videos,
        'ads': ads
    })
