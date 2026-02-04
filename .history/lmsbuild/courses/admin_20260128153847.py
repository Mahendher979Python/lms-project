from django.contrib import admin
from .models import Course, Lesson, LessonProgress, SessionVideo


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "trainer", "level", "is_published", "created_at")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "watched")


@admin.register(SessionVideo)
class SessionVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "trainer", "created_at")
