from django.db import models
from django.conf import settings
from courses.models import Course
from accounts.models import User

User = settings.AUTH_USER_MODEL


def study_item_upload_path(instance, filename):
    return f"{instance.item_type}/{filename}"


class StudyItem(models.Model):
    ITEM_TYPES = (
        ("todo", "Todo"),
        ("notes", "Notes"),
        ("books", "Books"),
        ("materials", "Materials"),
    )

    VISIBILITY_CHOICES = (
        ("public", "Public"),
        ("private", "Private"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="notes/", blank=True, null=True)

    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_items"
    )

    assigned_to = models.ManyToManyField(
        User, related_name="assigned_items", blank=True
    )

    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, blank=True
    )

    visibility = models.CharField(
        max_length=20, choices=VISIBILITY_CHOICES, default="private"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def uploader_role(self):
        return self.created_by.role

    def __str__(self):
        return self.title
