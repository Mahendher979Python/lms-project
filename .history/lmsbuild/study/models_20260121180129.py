from django.db import models
from django.conf import settings
from courses.models import Course
from accounts.models import User
from django.contrib.auth import get_user_model


User = get_user_model()

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

    # ======================
    # BASIC INFO
    # ======================
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    file = models.FileField(
        upload_to="notes/",
        null=True,
        blank=True
    )

    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPES
    )

    # ======================
    # RELATIONS
    # ======================
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_items"
    )

    assigned_to = models.ManyToManyField(
        User,
        related_name="assigned_items",
        blank=True
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # ======================
    # VISIBILITY / STATUS
    # ======================
    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="private"   # ✅ NO IntegrityError
    )

    is_active = models.BooleanField(default=True)

    # ======================
    # TIMESTAMPS
    # ======================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ======================
    # HELPERS
    # ======================
    def uploader_role(self):
        return self.created_by.role

    def __str__(self):
        return f"{self.title} ({self.item_type})"
