from django.contrib import admin
from django.utils.html import format_html
from .models import VideoCallPlatform, VideoCallRoom, VideoCall, VideoCallParticipant, VideoCallRecording, VideoCallSettings

@admin.register(VideoCallPlatform)
class VideoCallPlatformAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(VideoCallRoom)
class VideoCallRoomAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(VideoCall)
class VideoCallAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(VideoCallParticipant)
class VideoCallParticipantAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(VideoCallRecording)
class VideoCallRecordingAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(VideoCallSettings)
class VideoCallSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

