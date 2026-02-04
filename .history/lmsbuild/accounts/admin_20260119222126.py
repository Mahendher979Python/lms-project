from django.contrib import admin
from .models import (
    User,
    StudentProfile,
    TrainerProfile,
    TeacherProfile,
    StaffProfile
)

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    extra = 0

class TrainerProfileInline(admin.StackedInline):
    model = TrainerProfile
    extra = 0

class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    extra = 0

class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'mobile', 'is_active', 'date_of_joining')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'mobile')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []

        if obj.role == 'student':
            return [StudentProfileInline(self.model, self.admin_site)]
        elif obj.role == 'trainer':
            return [TrainerProfileInline(self.model, self.admin_site)]
        elif obj.role == 'teacher':
            return [TeacherProfileInline(self.model, self.admin_site)]
        elif obj.role == 'staff':
            return [StaffProfileInline(self.model, self.admin_site)]
        return []


admin.site.register(StudentProfile)
admin.site.register(TrainerProfile)
admin.site.register(TeacherProfile)
admin.site.register(StaffProfile)
