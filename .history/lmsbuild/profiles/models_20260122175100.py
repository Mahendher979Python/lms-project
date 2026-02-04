
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# -------------------------
# STUDENT PROFILE
# -------------------------
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    education = models.CharField(max_length=255, blank=True)
    college = models.CharField(max_length=255, blank=True)
    semester = models.CharField(max_length=50, blank=True)

    skills = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/students/", blank=True, null=True)

    enrolled_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Student: {self.user}"

# -------------------------
# TRAINER PROFILE
# -------------------------
class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    qualification = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField(default=0)

    expertise = models.TextField(help_text="Ex: Python, Django, React")
    certifications = models.TextField(blank=True)

    resume = models.FileField(upload_to="resumes/trainers/", blank=True, null=True)

    rating = models.FloatField(default=0.0)
    is_approved = models.BooleanField(default=False)

    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Trainer: {self.user}"

# -------------------------
# ADMIN PROFILE
# -------------------------
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, default="Admin")

    can_manage_users = models.BooleanField(default=True)
    can_manage_courses = models.BooleanField(default=True)
    can_view_reports = models.BooleanField(default=True)

    def __str__(self):
        return f"Admin: {self.user}"
