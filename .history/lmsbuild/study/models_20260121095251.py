from django.db import models
from django.conf import settings
from courses.models import Course

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

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPES
    )

    file = models.FileField(
        upload_to=study_item_upload_path,
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to=study_item_upload_path,
        blank=True,
        null=True
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="study_items"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_study_items"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.item_type})"
