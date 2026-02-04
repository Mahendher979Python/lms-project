from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

User = settings.AUTH_USER_MODEL


# ==================================================
# 🎥 VIDEO VALIDATORS
# ==================================================
def validate_video_size(file):
    if file.size > 500 * 1024 * 1024:  # 500MB
        raise ValidationError("Video must be under 500MB")

def validate_video_type(file):
    if not file.content_type.startswith("video/"):
        raise ValidationError("Only video files are allowed")


# ==================================================
# 📘 COURSE MODEL
# ==================================================
class Course(models.Model):

    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    duration = models.CharField(max_length=50)

    trainer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "trainer"},
        related_name="assigned_courses"
    )

    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ==================================================
# 📚 LESSON MODEL
# ==================================================
class Lesson(models.Model):

    course = models.ForeignKey(
        Course,
        related_name="lessons",
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.CharField(max_length=20)
    order = models.PositiveIntegerField(default=1)

    video = models.FileField(
        upload_to="lesson_videos/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.course.title} - {self.title}"


# ==================================================
# ✅ LESSON PROGRESS
# ==================================================
class LessonProgress(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"}
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )

    watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ("student", "lesson")

    def __str__(self):
        return f"{self.student} - {self.lesson.title}"


# ==================================================
# 🎥 SESSION VIDEO (TRAINER / ADMIN)
# ==================================================
class SessionVideo(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    video = models.FileField(
        upload_to="session_videos/",
        validators=[validate_video_size, validate_video_type]
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role__in": ["admin", "trainer"]},
        related_name="session_videos"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ==================================================
# 📢 ADVERTISEMENT MODEL
# ==================================================
class Advertisement(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to="ads/")

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role__in": ["admin", "trainer"]},
        related_name="ads"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
