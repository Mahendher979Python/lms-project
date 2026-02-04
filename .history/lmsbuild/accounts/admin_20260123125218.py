from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Student, TeacherProfile, StaffProfile

User = get_user_model()


# =====================================================
# INLINE PROFILES
# =====================================================
class StudentInline(admin.StackedInline):
    model = Student
    extra = 0
    can_delete = False


class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    extra = 0
    can_delete = False


class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    extra = 0
    can_delete = False


# =====================================================
# CUSTOM USER ADMIN
# =====================================================
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "role", "mobile", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "mobile")

    def get_inline_instances(self, request, obj=None):
        """
        Show profile inline based on user role
        """
        if not obj:
            return []

        if obj.role == "student":
            return [StudentInline(self.model, self.admin_site)]
        elif obj.role == "trainer":
            return [TeacherProfileInline(self.model, self.admin_site)]
        elif obj.role == "staff":
            return [StaffProfileInline(self.model, self.admin_site)]

        return []


# =====================================================
# STUDENT ADMIN (IMPORTANT)
# =====================================================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "roll_no",
        "phone",
        "trainer"
    )

    list_filter = (
        "trainer",
    )

    search_fields = (
        "user__username",
        "roll_no",
        "trainer__user__username"
    )

    raw_id_fields = ("user", "trainer")


# =====================================================
# TRAINER ADMIN
# =====================================================
@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "emp_id",
        "subject",
    )

    search_fields = (
        "user__username",
        "emp_id",
        "subject",
    )


# =====================================================
# STAFF ADMIN
# =====================================================
@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "emp_id",
        "department",
        "position",
    )

    search_fields = (
        "user__username",
        "emp_id",
        "department",
        "position",
    )
