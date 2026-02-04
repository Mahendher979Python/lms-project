from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

from courses.models import Course

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('trainer', 'Trainer'),
        ('student', 'Student'),
        ('staff', 'Staff'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    mobile = models.CharField(max_length=15, blank=True, null=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    roll_no = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username




class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    emp_id = models.CharField(max_length=20, unique=True)
    qualification = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    experience = models.IntegerField()

    # ✅ NEW FIELD
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username






class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=20, unique=True)
    subject = models.CharField(max_length=100)



class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
