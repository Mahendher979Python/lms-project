# =========================
# IMPORTS
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Course, Lesson, SessionVideo, Advertisement
from .forms import CourseForm, LessonForm, Lesson


# =========================
# ADMIN – COURSE LIST
# =========================
@login_required
def admin_course_list(request):
    if request.user.role != 'admin':
        return redirect('login')

    courses = Course.objects.all().order_by('-created_at')

    return render(request, 'courses/admin/course_list.html', {
        'courses': courses
    })


# =========================
# TRAINER – COURSE LIST
# =========================
@login_required
def trainer_course_list(request):
    if request.user.role != "trainer":
        return redirect("login")

    courses = Course.objects.filter(trainer=request.user)

    return render(
        request,
        "courses/trainer/course_list.html",
        {"courses": courses}
    )


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
            course.trainer = request.user
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
def student_course_list(request):
    if request.user.role != "student":
        return redirect("login")

    # student logic


# =========================
# TRAINER – LESSON LIST
# =========================
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


# =========================
# TRAINER – ADD LESSON
# =========================
@login_required
def trainer_lesson_add(request, course_id):
    if request.user.role != "trainer":
        return redirect("login")

    course = get_object_or_404(Course, id=course_id, trainer=request.user)

    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect("trainer_lesson_list", course_id=course.id)
    else:
        form = LessonForm()

    return render(request, "courses/trainer/lesson_form.html", {
        "course": course,
        "form": form
    })


# =========================
# TRAINER – EDIT LESSON
# =========================
@login_required
def trainer_lesson_edit(request, course_id, lesson_id):
    if request.user.role != "trainer":
        return redirect("login")

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id,
        course__id=course_id,
        course__trainer=request.user
    )

    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect("trainer_lesson_list", course_id=course_id)
    else:
        form = LessonForm(instance=lesson)

    return render(request, "courses/trainer/lesson_form.html", {
        "course": lesson.course,
        "form": form
    })


# =========================
# TRAINER – DELETE LESSON
# =========================
@login_required
def trainer_lesson_delete(request, course_id, lesson_id):
    if request.user.role != "trainer":
        return redirect("login")

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id,
        course__id=course_id,
        course__trainer=request.user
    )
    lesson.delete()

    return redirect("trainer_lesson_list", course_id=course_id)


# =========================
# PUBLIC – MEDIA VIEW
# =========================
def public_media_view(request):
    videos = SessionVideo.objects.filter(is_active=True)
    ads = Advertisement.objects.filter(is_active=True)

    return render(request, 'courses/media/public_media.html', {
        'videos': videos,
        'ads': ads
    })


# =========================
# ADMIN – MEDIA LIST
# =========================
@login_required
def admin_media_list(request):
    if request.user.role != 'admin':
        return redirect('login')

    search = request.GET.get('search', '')
    status = request.GET.get('status', '')

    videos = SessionVideo.objects.all()
    ads = Advertisement.objects.all()

    if search:
        videos = videos.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(created_by__username__icontains=search)
        )
        ads = ads.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    if status == 'active':
        videos = videos.filter(is_active=True)
        ads = ads.filter(is_active=True)
    elif status == 'inactive':
        videos = videos.filter(is_active=False)
        ads = ads.filter(is_active=False)

    return render(request, 'courses/admin/media_list.html', {
        'videos': videos.order_by('-created_at'),
        'ads': ads.order_by('-created_at'),
        'search': search,
        'status': status
    })


# =========================
# TRAINER – MEDIA DASHBOARD
# =========================
@login_required
def trainer_media_list(request):
    if request.user.role != "trainer":
        return redirect("login")

    videos = SessionVideo.objects.filter(created_by=request.user)

    return render(
        request,
        "trainer/media/media_list.html",
        {"videos": videos}
    )



# =========================
# TRAINER – VIDEOS CRUD
# =========================

@login_required
def trainer_video_list(request):
    if request.user.role != "trainer":
        return redirect("login")

    videos = SessionVideo.objects.filter(created_by=request.user)

    return render(request, "trainer/media/video_list.html", {
        "videos": videos
    })


@login_required
def trainer_video_add(request):
    if request.user.role != "trainer":
        return redirect("login")

    if request.method == "POST":
        SessionVideo.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            video=request.FILES.get("video"),
            created_by=request.user
        )
        return redirect("trainer_video_list")

    return render(request, "trainer/media/video_form.html", {
        "action": "Add"
    })


@login_required
def trainer_video_edit(request, video_id):
    if request.user.role != "trainer":
        return redirect("login")

    video = get_object_or_404(
        SessionVideo,
        id=video_id,
        created_by=request.user
    )

    if request.method == "POST":
        video.title = request.POST.get("title")
        video.description = request.POST.get("description")

        if request.FILES.get("video"):
            video.video = request.FILES.get("video")

        video.save()
        return redirect("trainer_video_list")

    return render(request, "trainer/media/video_form.html", {
        "video": video,
        "action": "Edit"
    })


@login_required
def trainer_video_delete(request, video_id):
    if request.user.role != "trainer":
        return redirect("login")

    video = get_object_or_404(
        SessionVideo,
        id=video_id,
        created_by=request.user
    )
    video.delete()

    return redirect("trainer_video_list")

#================================
# Student  Video View
#=================================

@login_required
def student_video_list(request):
    if request.user.role != "student":
        return redirect("login")

    videos = SessionVideo.objects.all().order_by("-created_at")

    return render(request, "student/video_list.html", {
        "videos": videos
    })


# =========================
# TRAINER – ADS / IMAGES CRUD
# =========================

@login_required
def trainer_ad_list(request):
    if request.user.role != "trainer":
        return redirect("login")

    ads = Advertisement.objects.filter(created_by=request.user)
    return render(request, "courses/media/ad_list.html", {
        "ads": ads
    })


@login_required
def trainer_ad_add(request):
    if request.user.role != "trainer":
        return redirect("login")

    if request.method == "POST":
        Advertisement.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            image=request.FILES.get("image"),
            created_by=request.user
        )
        return redirect("trainer_ad_list")

    return render(request, "courses/media/ad_form.html", {
        "action": "Add"
    })


@login_required
def trainer_ad_edit(request, ad_id):
    if request.user.role != "trainer":
        return redirect("login")

    ad = get_object_or_404(
        Advertisement,
        id=ad_id,
        created_by=request.user
    )

    if request.method == "POST":
        ad.title = request.POST.get("title")
        ad.description = request.POST.get("description")

        if request.FILES.get("image"):
            ad.image = request.FILES.get("image")

        ad.save()
        return redirect("trainer_ad_list")

    return render(request, "courses/media/ad_form.html", {
        "ad": ad,
        "action": "Edit"
    })


@login_required
def trainer_ad_delete(request, ad_id):
    if request.user.role != "trainer":
        return redirect("login")

    ad = get_object_or_404(
        Advertisement,
        id=ad_id,
        created_by=request.user
    )
    ad.delete()
    return redirect("trainer_ad_list")


#================================
# Student Views
#=================================

@login_required
def student_lesson_list(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)
    lessons = course.lessons.all()

    watched_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__course=course,
        watched=True
    ).values_list("lesson_id", flat=True)

    return render(request, "courses/student/lesson_list.html", {
        "course": course,
        "lessons": lessons,
        "watched_lessons": watched_lessons
    })

@login_required
def student_lesson_list(request, course_id):
    if request.user.role != "student":
        return redirect("login")

    course = get_object_or_404(
        Course,
        id=course_id,
        is_published=True
    )

    lessons = course.lessons.all().order_by("order")

    return render(
        request,
        "enrollments/student/lesson_list.html",
        {
            "course": course,
            "lessons": lessons
        }
    )
