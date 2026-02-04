from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# ======================================================
# CUSTOM USER MODEL
# ======================================================
class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("trainer", "Trainer"),
        ("student", "Student"),
        ("staff", "Staff"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import TrainerProfile, StudentProfile, StaffProfile
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")

    fieldsets = UserAdmin.fieldsets + (
        ("Role Info", {"fields": ("role",)}),
    )




# -----------------------------
# USER ADMIN (BASIC VIEW)
# -----------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active")
    search_fields = ("username", "email")


# -----------------------------
# TRAINER ADMIN
# -----------------------------
@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "first_name",
        "surname",
        "qualification",
        "designation",
        "phone",
        "joining_date",
    )
    search_fields = ("employee_id", "first_name", "surname", "phone")
    list_filter = ("designation", "joining_date")


# -----------------------------
# STUDENT ADMIN
# -----------------------------
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "first_name",
        "surname",
        "phone",
        "qualification",
    )
    search_fields = ("student_id", "first_name", "surname", "phone")
    filter_horizontal = ("courses",)


# -----------------------------
# STAFF ADMIN
# -----------------------------
@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "first_name",
        "surname",
        "designation",
        "phone",
    )
    search_fields = ("employee_id", "first_name", "surname", "phone")

# ======================================================
# TRAINER / TEACHER PROFILE
# ======================================================
class TrainerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trainer_profile"
    )

    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    joining_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.surname} (Trainer)"


# ======================================================
# STUDENT PROFILE
# ======================================================
class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=200)
    address = models.TextField()

    courses = models.ManyToManyField(
        "courses.Course",
        blank=True,
        related_name="students"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.surname} (Student)"


# ======================================================
# STAFF PROFILE
# ======================================================
class StaffProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )

    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.surname} (Staff)"
