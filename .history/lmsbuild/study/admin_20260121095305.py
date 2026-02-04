from django.contrib import admin
from .models import StudyItem

@admin.register(StudyItem)
class StudyItemAdmin(admin.ModelAdmin):
    list_display = ("title", "item_type", "created_by", "created_at")
    list_filter = ("item_type",)
    search_fields = ("title",)
