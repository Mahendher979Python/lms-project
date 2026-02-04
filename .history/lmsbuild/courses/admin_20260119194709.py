from django.contrib import admin
from .models import (
    Course,
    Lesson,
    LessonProgress,
    SessionVideo,
    Advertisement
)

# ===============================
# 📘 Course Admin
# ===============================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "trainer", "is_published", "created_at")
    list_filter = ("level", "is_published")
    search_fields = ("title", "description")
    ordering = ("-created_at",)


# ===============================
# 📚 Lesson Admin
# ===============================
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "duration")
    list_filter = ("course",)
    ordering = ("course", "order")


# ===============================
# ✅ Lesson Progress Admin
# ===============================
@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "watched")
    list_filter = ("watched",)
    search_fields = ("student__username", "lesson__title")


# ===============================
# 🎥 Session Video Admin
# ===============================
@admin.register(SessionVideo)
class SessionVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)


# ===============================
# 📢 Advertisement Admin
# ===============================
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "is_active", "created_at")
    list_filter = ("is_active",)
