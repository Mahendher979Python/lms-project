from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")

    fieldsets = UserAdmin.fieldsets + (
        ("Role Info", {"fields": ("role",)}),
    )

from django.contrib import admin
from .models import TrainerProfile, StudentProfile, StaffProfile
from django.contrib.auth import get_user_model

User = get_user_model()


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
