from django.contrib import admin
from .models import Course, Lesson, LessonProgress, SessionVideo


# ================= COURSE ADMIN =================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "trainer", "level", "is_published", "created_at")
    list_filter = ("level", "is_published", "trainer")
    search_fields = ("title",)
    ordering = ("-created_at",)


# ================= LESSON ADMIN =================

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "created_at")
    list_filter = ("course",)
    search_fields = ("title",)
    ordering = ("course", "order")


# ================= LESSON PROGRESS ADMIN =================

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "watched")
    list_filter = ("watched",)
    search_fields = ("student__user__username", "lesson__title")


# ================= SESSION VIDEO ADMIN =================

@admin.register(SessionVideo)
class SessionVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "trainer", "created_at")
    list_filter = ("trainer",)
    search_fields = ("title",)
