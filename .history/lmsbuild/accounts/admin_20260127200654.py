from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .models import TeacherProfile, Student, Batch, StaffProfile

User = get_user_model()


# =====================================================
# CUSTOM USER ADMIN
# =====================================================
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active")
    search_fields = ("username", "email", "mobile")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("role", "mobile", "profile_pic")}),
    )


# =====================================================
# TRAINER PROFILE ADMIN
# =====================================================
@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "emp_id", "subject", "is_active")
    list_filter = ("subject", "is_active")
    search_fields = ("user__username", "emp_id")


# =====================================================
# BATCH ADMIN
# =====================================================
@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("name", "trainer", "subject", "is_active", "created_at")
    list_filter = ("subject", "is_active")
    search_fields = ("name", "trainer__user__username")


# =====================================================
# STUDENT ADMIN
# =====================================================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "trainer", "batch", "roll_no", "phone", "is_active")
    list_filter = ("trainer", "batch", "is_active")
    search_fields = ("user__username", "roll_no", "phone")


# =====================================================
# STAFF ADMIN
# =====================================================
@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "emp_id", "department", "position")
    search_fields = ("user__username", "emp_id")
