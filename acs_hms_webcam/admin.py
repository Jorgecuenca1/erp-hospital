from django.contrib import admin
from django.utils.html import format_html
from .models import WebcamDevice, WebcamSession, WebcamRecording, WebcamAlert, WebcamSettings

@admin.register(WebcamDevice)
class WebcamDeviceAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(WebcamSession)
class WebcamSessionAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(WebcamRecording)
class WebcamRecordingAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(WebcamAlert)
class WebcamAlertAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(WebcamSettings)
class WebcamSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

