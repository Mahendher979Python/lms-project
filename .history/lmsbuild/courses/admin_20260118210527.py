from django.contrib import admin
from .models import (
    Course,
    Lesson,
    LessonProgress,
    SessionVideo,
    Advertisement
)


# ==================================================
# 📘 COURSE ADMIN
# ==================================================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    autocomplete_fields = ["trainer"]


# ==================================================
# 📚 LESSON ADMIN
# ==================================================
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "order",
        "duration",
    )
    list_filter = ("course",)
    search_fields = ("title",)
    ordering = ("course", "order")


# ==================================================
# ✅ LESSON PROGRESS ADMIN
# ==================================================
@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "lesson",
        "watched",
    )
    list_filter = ("watched",)
    search_fields = ("student__username", "lesson__title")


# ==================================================
# 🎥 SESSION VIDEO ADMIN
# ==================================================
@admin.register(SessionVideo)
class SessionVideoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_by",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)


# ==================================================
# 📢 ADVERTISEMENT ADMIN
# ==================================================
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("title",)
    ordering = ("-created_at",)
