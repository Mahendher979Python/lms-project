from django.db import models
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta

User = settings.AUTH_USER_MODEL

class Attendance(models.Model):
    STATUS_CHOICES = (
        ("present", "Present"),
        ("absent", "Absent"),
        ("half_day", "Half Day"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)

    date = models.DateField(default=now)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    total_work_hours = models.DurationField(null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    marked_by = models.CharField(max_length=20, default="system")

    def calculate_work_hours(self):
        if self.login_time and self.logout_time:
            self.total_work_hours = self.logout_time - self.login_time

    def save(self, *args, **kwargs):
        self.calculate_work_hours()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.date}"
