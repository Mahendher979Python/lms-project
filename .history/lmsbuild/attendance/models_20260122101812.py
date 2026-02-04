from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime


User = settings.AUTH_USER_MODEL


class Attendance(models.Model):
    STATUS_CHOICES = (
        ("present", "Present"),
        ("absent", "Absent"),
        ("halfday", "Half Day"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    date = models.DateField()
    login_time = models.TimeField(null=True, blank=True)
    logout_time = models.TimeField(null=True, blank=True)
    total_work_hours = models.BigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    marked_by = models.CharField(max_length=20)

    def calculate_work_hours(self):
        if self.login_time and self.logout_time:
            login_dt = datetime.combine(self.date, self.login_time)
            logout_dt = datetime.combine(self.date, self.logout_time)

            diff = logout_dt - login_dt
            self.total_work_hours = int(diff.total_seconds() // 3600)

    def save(self, *args, **kwargs):
        self.calculate_work_hours()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.date}"




def calculate_work_hours(self):
    if self.login_time and self.logout_time:
        login_dt = datetime.combine(self.date, self.login_time)
        logout_dt = datetime.combine(self.date, self.logout_time)

        if logout_dt < login_dt:
            logout_dt += timedelta(days=1)

        self.total_work_hours = logout_dt - login_dt
