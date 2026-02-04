from django.conf import settings
from django.db import models
from accounts.models import TeacherProfile, Student
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



# ================= COURSE =================
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

    trainer = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ================= COURSE MATERIAL =================

class CourseMaterial(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="materials"
    )

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="materials/")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ================= LESSON =================

class Lesson(models.Model):

    course = models.ForeignKey(
        Course,
        related_name="lessons",
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)
    video = models.FileField(upload_to="lesson_videos/", null=True, blank=True)
    pdf = models.FileField(upload_to="lesson_pdfs/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


