from django.db import models
from accounts.models import User
from courses.models import Course

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)  # ✅ ADD THIS

    class Meta:
        unique_together = ("student", "course")
