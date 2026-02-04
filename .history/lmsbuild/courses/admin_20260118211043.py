from django.contrib import admin
from .models import Course, SessionVideo, LessonProgress, Advertisement


# =========================
# COURSE ADMIN
# =========================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "trainer")
    search_fields = ("title", "trainer__username")
    autocomplete_fields = ["trainer"]


# =========================
# SESSION VIDEO ADMIN
# =========================
@admin.register(SessionVideo)
class SessionVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "created_by__username")
    autocomplete_fields = ["created_by"]


# =========================
# LESSON PROGRESS ADMIN
# =========================
@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "completed")
    list_filter = ("completed",)
    autocomplete_fields = ["student", "course"]


# =========================
# ADVERTISEMENT ADMIN
# =========================
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
