from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Attendance(models.Model):
    STATUS_CHOICES = (
        ("present", "Present"),
        ("absent", "Absent"),
        ("half_day", "Half Day"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    role = models.CharField(
        max_length=20,
        choices=(
            ("admin", "Admin"),
            ("trainer", "Trainer"),
            ("student", "Student"),
        )
    )

    date = models.DateField()

    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    # 🔥 LOCATION FIELDS (ADD HERE)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    location_address = models.TextField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="present"
    )

    marked_by = models.CharField(
        max_length=20,
        default="system"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user} - {self.date}"
