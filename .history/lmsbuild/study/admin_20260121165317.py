from django.contrib import admin
from .models import StudyItem


@admin.register(StudyItem)
class StudyItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "item_type",
        "course",
        "created_by",
        "visibility",
        "is_active",
        "created_at",
    )

    list_filter = (
        "item_type",
        "visibility",
        "is_active",
        "course",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "created_by__username",
        "created_by__email",
    )

    filter_horizontal = ("assigned_to",)

    readonly_fields = ("created_at", "updated_at")

    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "description", "item_type", "file")
        }),
        ("Relations", {
            "fields": ("course", "created_by", "assigned_to")
        }),
        ("Settings", {
            "fields": ("visibility", "is_active")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )
