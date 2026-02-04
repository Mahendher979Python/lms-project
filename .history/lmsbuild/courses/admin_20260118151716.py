from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'trainer', 'is_published', 'created_at')
    list_filter = ('level', 'is_published')
    search_fields = ('title',)
    list_editable = ('is_published',)

from django.contrib import admin
from .models import Course, Lesson, SessionVideo, Advertisement

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(SessionVideo)
admin.site.register(Advertisement)
