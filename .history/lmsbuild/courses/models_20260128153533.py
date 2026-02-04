from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import TeacherProfile, Student


# ==================================================
# 🎥 VIDEO VALIDATOR
# ==================================================

def validate_video_size(file):
    if file.size > 500 * 1024 * 1024:  # 500MB
        raise ValidationError("Video must be under 500MB")


# ==================================================
# 📘 COURSE
# ==================================================

class Course(models.Model):

    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    duration = models.CharField(max_length=50)

    # Trainer owns course
    trainer = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    thumbnail = models.ImageField(upload_to="courses/thumbnails/", null=True, blank=True)
    intro_video = models.FileField(upload_to="courses/intro_videos/", null=True, blank=True)
    syllabus_pdf = models.FileField(upload_to="courses/syllabus/", null=True, blank=True)

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ==================================================
# 📚 LESSON (Each course has many lessons)
# ==================================================

class Lesson(models.Model):

    course = models.ForeignKey(
        Course,
        related_name="lessons",
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    video = models.FileField(
        upload_to="lesson_videos/",
        null=True,
        blank=True,
        validators=[validate_video_size]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


# ==================================================
# ✅ STUDENT LESSON PROGRESS
# ==================================================

class LessonProgress(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="lesson_progress"
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )

    watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ("student", "lesson")

    def __str__(self):
        return f"{self.student.user.username} - {self.lesson.title}"


# ==================================================
# 🎥 TRAINER SESSION VIDEOS (Optional)
# ==================================================

class SessionVideo(models.Model):

    trainer = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name="session_videos"
    )

    title = models.CharField(max_length=200)
    video = models.FileField(upload_to="session_videos/", validators=[validate_video_size])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
