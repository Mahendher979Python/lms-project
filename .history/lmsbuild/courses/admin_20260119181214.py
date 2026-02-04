from django.contrib import admin
from .models import (
    Course,
    Lesson,
    LessonProgress,
    SessionVideo,
    Advertisement
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "trainer", "level", "is_published", "created_at")
    list_filter = ("level", "is_published")
    search_fields = ("title", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "duration")
    list_filter = ("course",)
    ordering = ("course", "order")


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "watched")
    list_filter = ("watched",)


@admin.register(SessionVideo)
class SessionVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "description")


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "description")


from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "level",
        "trainer",
        "is_published",
        "created_at",
    )
    list_filter = ("level", "is_published")
    search_fields = ("title",)
