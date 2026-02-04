from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        "subject",
        "sender",
        "receiver",
        "is_read",
        "created_at",
    )

    list_filter = ("is_read", "created_at")

    search_fields = (
        "subject",
        "body",
        "sender__username",
        "receiver__username",
    )

    readonly_fields = ("created_at",)

    ordering = ("-created_at",)

    fieldsets = (
        ("Message Info", {
            "fields": ("sender", "receiver", "subject", "body")
        }),
        ("Status", {
            "fields": ("is_read", "created_at")
        }),
    )
