from datetime import datetime, timedelta
from django.db import models

class Attendance(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    date = models.DateField()
    login_time = models.TimeField(null=True, blank=True)
    logout_time = models.TimeField(null=True, blank=True)
    total_work_hours = models.DurationField(null=True, blank=True)
    status = models.CharField(max_length=20)
    marked_by = models.CharField(max_length=20, default="system")

    def calculate_work_hours(self):
        if self.login_time and self.logout_time:
            login_dt = datetime.combine(self.date, self.login_time)
            logout_dt = datetime.combine(self.date, self.logout_time)

            if logout_dt < login_dt:
                logout_dt += timedelta(days=1)

            self.total_work_hours = logout_dt - login_dt

    def save(self, *args, **kwargs):
        self.calculate_work_hours()
        super().save(*args, **kwargs)
