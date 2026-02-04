from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        "subject",
        "sender",
        "receiver",
        "batch",
        "created_at",
    )

    list_filter = (
        "created_at",
        "batch",
    )

    search_fields = (
        "subject",
        "body",
        "sender__username",
        "receiver__username",
    )

    readonly_fields = ("created_at",)

    ordering = ("-created_at",)

    fieldsets = (
        ("Message Details", {
            "fields": ("sender", "receiver", "batch", "subject", "body")
        }),
        ("System", {
            "fields": ("created_at",)
        }),
    )
