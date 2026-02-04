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

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} ({self.subject})"


# =====================================================
# BATCH MODEL
# =====================================================
class Batch(models.Model):
    name = models.CharField(max_length=100)

    trainer = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name="batches"
    )

    # Auto copy trainer subject (optional but safe)
    subject = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically set subject from trainer
        if self.trainer:
            self.subject = self.trainer.subject
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.subject}"


# =====================================================
# STUDENT PROFILE
# =====================================================
class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    trainer = models.ForeignKey(TeacherProfile,on_delete=models.SET_NULL,null=True,blank=True)
    batch = models.ForeignKey(Batch,on_delete=models.SET_NULL,null=True,blank=True)
    roll_no = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)

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
