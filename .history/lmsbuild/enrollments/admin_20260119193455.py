from django.contrib import admin
from .models import Enrollment, LessonProgress


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "joined_at")
    list_filter = ("course",)
    search_fields = ("student__username", "course__title")
    ordering = ("-joined_at",)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("get_student", "lesson", "watched")
    list_filter = ("watched", "lesson")
    search_fields = ("lesson__title", "enrollment__student__username")

    def get_student(self, obj):
        return obj.enrollment.student
    get_student.short_description = "Student"
