from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "sender", "receiver", "is_read", "created_at")
    search_fields = ("subject", "body")
    list_filter = ("is_read", "created_at")


