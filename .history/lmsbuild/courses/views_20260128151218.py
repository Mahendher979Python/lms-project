# =========================
# IMPORTS
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from enrollments.models import Enrollment
from enrollments.utils import is_enrolled
from django.contrib.auth import get_user_model
from accounts.decorators import admin_required
from .models import Course, Lesson, SessionVideo, Advertisement
from .forms import CourseForm, LessonForm, Lesson
from core_settings.models import TrainerSettings
from core_settings.services import has_required_attendance
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import TeacherProfile
from .models import Course

User = get_user_model()



@login_required
def create_course(request):

    # 🔒 Only trainers allowed
    if request.user.role != "trainer":
        return render(request, "403.html")

    # ⚙ Get global trainer settings
    trainer_settings = TrainerSettings.get()

    # ❌ Admin disabled course creation
    if not trainer_settings.can_create_courses:
        messages.error(request, "Course creation disabled by admin")
        return redirect("trainer_dashboard")

    # ❌ Max course limit reached
    course_count = Course.objects.filter(trainer=request.user).count()
    if course_count >= trainer_settings.max_courses:
        messages.error(
            request,
            f"You can create only {trainer_settings.max_courses} courses"
        )
        return redirect("trainer_dashboard")

    # =========================
    # COURSE CREATE LOGIC
    # =========================
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        course = Course.objects.create(
            title=title,
            description=description,
            trainer=request.user,
            is_published=not trainer_settings.course_approval_required
        )

        # 🔔 If approval required
        if trainer_settings.course_approval_required:
            messages.success(
                request,
                "Course submitted for admin approval"
            )
        else:
            messages.success(
                request,
                "Course created successfully"
            )

        return redirect("trainer_courses")

    return render(request, "courses/trainer/create_course.html")



@login_required
def complete_course(request, course_id):
    if request.user.role != "student":
        return render(request, "403.html")

    if not has_required_attendance(request.user):
        messages.error(
            request,
            "Minimum attendance requirement not met"
        )
        return redirect("student_course_detail", course_id=course_id)

    # mark course completed



# =========================================================================================
# ================= ADMIN COURSE LIST =================
@login_required
@admin_required
def admin_course_list(request):
    courses = Course.objects.all()
    return render(request, "admin/courses/list.html", {"courses": courses})


# ================= ADMIN COURSE CREATE =================
@login_required
@admin_required
def admin_course_add(request):
    teachers = TeacherProfile.objects.filter(is_active=True)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        trainer_id = request.POST.get("trainer")

        trainer = TeacherProfile.objects.get(id=trainer_id)

        Course.objects.create(
            title=title,
            description=description,
            trainer=trainer
        )

        return redirect("admin_course_list")

    return render(request, "admin/courses/create.html", {"teachers": teachers})


# ================= ADMIN COURSE EDIT =================
@login_required
@admin_required
def admin_course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    teachers = TeacherProfile.objects.filter(is_active=True)

    if request.method == "POST":
        course.title = request.POST.get("title")
        course.description = request.POST.get("description")
        trainer_id = request.POST.get("trainer")
        course.trainer = TeacherProfile.objects.get(id=trainer_id)
        course.save()

        return redirect("admin_course_list")

    return render(request, "admin/courses/edit.html", {
        "course": course,
        "teachers": teachers
    })


# ================= ADMIN COURSE DELETE =================
@login_required
@admin_required
def admin_course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect("admin_course_list")



# =======================================================================
# TRAINER – COURSE LIST
# ============================================================================
@login_required
def trainer_course_list(request):
    if request.user.role != "trainer":
        return redirect("login")

    courses = Course.objects.filter(trainer=request.user)
    return render(request, "courses/trainer/course_list.html", {"courses": courses})


# =========================
# TRAINER – CREATE COURSE
# =========================
@login_required
def trainer_course_create(request):
    if request.user.role != "trainer":
        return redirect("login")

    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.trainer = request.user
            course.save()
            return redirect("trainer_course_list")
    else:
        form = CourseForm()

    return render(request, "courses/trainer/course_form.html", {"form": form})

# =========================
# TRAINER – EDIT COURSE
# ======================================================================================
@login_required
def trainer_course_edit(request, course_id):
    if request.user.role != "trainer":
        return redirect("login")

    course = get_object_or_404(Course, id=course_id, trainer=request.user)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("trainer_course_list")
    else:
        form = CourseForm(instance=course)

    return render(request, "courses/trainer/course_form.html", {"form": form})

# =========================
# TRAINER – LESSON LIST
# ==============================================================================================
@login_required
def trainer_lesson_list(request, course_id):
    if request.user.role != "trainer":
        return redirect("login")

    course = get_object_or_404(Course, id=course_id, trainer=request.user)
    lessons = course.lessons.all().order_by("order")

    return render(request, "courses/trainer/lesson_list.html", {
        "course": course,
        "lessons": lessons
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


# =========================
# TRAINER – VIDEOS CRUD
# =========================

@login_required
def trainer_video_list(request):
    if request.user.role != "trainer":
        return redirect("login")

    videos = SessionVideo.objects.filter(created_by=request.user)

    return render(request, "courses/media/video_list.html", {
        "videos": videos
    })


@login_required
def trainer_video_add(request):
    if request.user.role != "trainer":
        return redirect("login")

    if request.method == "POST":
        file = request.FILES.get("video")

        if not file.content_type.startswith("video/"):
            messages.error(request, "Only video files are allowed")
            return redirect("trainer_video_add")

        if file.size > 500 * 1024 * 1024:
            messages.error(request, "Video must be under 500MB")
            return redirect("trainer_video_add")

        SessionVideo.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            video=file,
            created_by=request.user
        )
        return redirect("trainer_video_list")

    return render(request, "courses/media/video_form.html", {
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

    return render(request, "courses/media/video_form.html", {
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


# =====================================================================================
# STUDENT
# =====================================================================================

@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return redirect("login")

    enrollments = Enrollment.objects.filter(student=request.user).select_related("course")
    courses = [e.course for e in enrollments]

    return render(request, "accounts/student/dashboard.html", {
        "courses": courses
    })


@login_required
def student_course_list(request):
    if request.user.role != "student":
        return redirect("login")

    courses = Course.objects.filter(is_published=True)
    return render(
        request,
        "courses/student/course_list.html",
        {"courses": courses}
    )


@login_required
def student_course_detail(request, course_id):
    if request.user.role != "student":
        return redirect("login")

    course = get_object_or_404(Course, id=course_id, is_published=True)

    if not is_enrolled(request.user, course):
        return redirect("student_dashboard")

    lessons = course.lessons.all().order_by("order")

    return render(request, "courses/student/lesson_list.html", {
        "course": course,
        "lessons": lessons
    })


# =========================
# STUDENT – MY COURSES
# =========================
@login_required
def student_my_courses(request):
    courses = Course.objects.filter(enrollments__student=request.user)

    return render(
        request,
        "courses/student/my_courses.html",
        {"courses": courses}
    )


# =========================
# STUDENT – COURSE TOPICS (AJAX)
# =========================
@login_required
def student_course_topics(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    lessons = Lesson.objects.filter(course=course)

    data = {
        "topics": [
            {
                "id": lesson.id,
                "title": lesson.title,
                "video": lesson.video.url if lesson.video else ""
            }
            for lesson in lessons
        ]
    }
    return JsonResponse(data)


# =========================
# STUDENT – DOWNLOAD COURSE MATERIAL
# =========================
@login_required
def download_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if not course.materials:
        raise Http404("No materials found")

    return FileResponse(
        course.materials.open(),
        as_attachment=True,
        filename=course.materials.name
    )



# ================================
# LESSON LIST
# ================================
@login_required
def student_lesson_list(request, course_id):
    if request.user.role != "student":
        return redirect("login")

    course = get_object_or_404(
        Course,
        id=course_id,
        is_published=True
    )

    if not is_enrolled(request.user, course):
        return redirect("student_dashboard")

    lessons = course.lessons.all().order_by("order")

    watched_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__course=course,
        watched=True
    ).values_list("lesson_id", flat=True)

    return render(
        request,
        "courses/student/lesson_list.html",
        {
            "course": course,
            "lessons": lessons,
            "watched_lessons": watched_lessons
        }
    )



# =====================================================================================
# ADMIN – MEDIA
# =====================================================================================

@login_required
@admin_required
def admin_media_list(request):
    search = request.GET.get("search", "")
    status = request.GET.get("status", "")

    videos = SessionVideo.objects.all()
    ads = Advertisement.objects.all()

    if search:
        videos = videos.filter(title__icontains=search)
        ads = ads.filter(title__icontains=search)

    if status == "active":
        videos = videos.filter(is_active=True)
        ads = ads.filter(is_active=True)
    elif status == "inactive":
        videos = videos.filter(is_active=False)
        ads = ads.filter(is_active=False)

    return render(request, "courses/admin/media_list.html", {
        "videos": videos.order_by("-created_at"),
        "ads": ads.order_by("-created_at"),
        "search": search,
        "status": status
    })


# =====================================================================================
# PUBLIC MEDIA
# =====================================================================================

def public_media_view(request):
    videos = SessionVideo.objects.filter(is_active=True)
    ads = Advertisement.objects.filter(is_active=True)

    return render(request, "courses/media/public_media.html", {
        "videos": videos,
        "ads": ads
    })