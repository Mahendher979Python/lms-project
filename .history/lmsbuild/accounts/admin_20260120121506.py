from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    Student,
    TrainerProfile,
    TeacherProfile,
    StaffProfile
)

User = get_user_model()

# ================= INLINE CLASSES =================

class StudentInline(admin.StackedInline):
    model = Student
    extra = 0
    can_delete = False


class TrainerProfileInline(admin.StackedInline):
    model = TrainerProfile
    extra = 0


class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    extra = 0


class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    extra = 0


# ================= STUDENT PROFILE ADMIN =================

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "roll_no", "phone", "is_active")
    list_filter = ("user__is_active",)
    search_fields = ("user__username", "user__email", "roll_no", "phone")

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    def is_active(self, obj):
        return obj.user.is_active

    is_active.boolean = True
    is_active.short_description = "Active"


# ================= CUSTOM USER ADMIN =================

class UserAdmin(BaseUserAdmin):
    list_display = ("username", "role", "mobile", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("username", "mobile")

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []

        if obj.role == "student":
            return [StudentInline(self.model, self.admin_site)]

        elif obj.role == "trainer":
            return [TrainerProfileInline(self.model, self.admin_site)]

        elif obj.role == "teacher":
            return [TeacherProfileInline(self.model, self.admin_site)]

        elif obj.role == "staff":
            return [StaffProfileInline(self.model, self.admin_site)]

        return []


# ================= REGISTER USER ADMIN =================

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# ================= REGISTER OTHER PROFILES =================

admin.site.register(TrainerProfile)
admin.site.register(TeacherProfile)
admin.site.register(StaffProfile)
