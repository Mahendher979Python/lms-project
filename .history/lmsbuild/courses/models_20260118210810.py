from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "trainer"}
    )

    def __str__(self):
        return self.title


class SessionVideo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video = models.FileField(upload_to="session_videos/")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "trainer"}
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LessonProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"}
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)



class SessionVideo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video = models.FileField(upload_to="session_videos/")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={"role__in": ["admin", "trainer"]})
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.title


# ==================================================
# 📢 ADVERTISEMENT MODEL
# ==================================================
class Advertisement(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to="ads/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
