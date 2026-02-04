from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject","sender","receiver","batch","created_at")
    list_filter = ("created_at","batch")
    search_fields = ("subject","body")
