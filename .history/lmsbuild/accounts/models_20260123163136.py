from django.contrib.auth.models import AbstractUser
from django.db import models


# =====================================================
# CUSTOM USER MODEL
# =====================================================
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

    profile_pic = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username


# =====================================================
# TRAINER PROFILE
# =====================================================
class TeacherProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )

    emp_id = models.CharField(max_length=20, unique=True)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} (Trainer)"


# =====================================================
# STUDENT PROFILE
# =====================================================
# =====================================================
# STUDENT PROFILE
# =====================================================
class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    trainer = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )

    roll_no = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.trainer:
            return f"{self.user.username} → {self.trainer.user.username}"
        return self.user.username

# =====================================================
# STAFF PROFILE
# =====================================================
class StaffProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )

    emp_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} (Staff)"
