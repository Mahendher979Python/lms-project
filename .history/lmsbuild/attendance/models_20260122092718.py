from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    location_address = models.TextField(null=True, blank=True) # Optional: Store address
    status = models.CharField(max_length=20, default="absent") # present, absent, half_day

    @property
    def working_hours(self):
        """Calculates total working hours if logged out"""
        if self.login_time and self.logout_time:
            diff = self.logout_time - self.login_time
            seconds = diff.total_seconds()
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        return "Active" if self.login_time else "-"

    def __str__(self):
        return f"{self.user.username} - {self.date}"