from django.contrib import admin
from .models import ChatSession, ChatMessage

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'agent', 'start_time', 'end_time', 'active')
    list_filter = ('active', 'start_time', 'agent')
    search_fields = ('uuid', 'user__username', 'agent__username', 'topic')
    raw_id_fields = ('user', 'agent')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'sender', 'timestamp', 'is_read')
    list_filter = ('session__active', 'timestamp', 'sender', 'is_read')
    search_fields = ('session__uuid', 'sender__username', 'message')
    raw_id_fields = ('session', 'sender')
    date_hierarchy = 'timestamp'
    ordering = ('timestamp',)
