from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    WaitingScreen, WaitingQueue, ScreenAnnouncement, 
    HealthTip, ScreenConfiguration
)

@admin.register(WaitingScreen)
class WaitingScreenAdmin(admin.ModelAdmin):
    list_display = ('name', 'screen_type', 'location', 'is_active', 'updated_at')
    list_filter = ('screen_type', 'is_active', 'created_at')
    search_fields = ('name', 'location')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'screen_type', 'location')
        }),
        ('Display Settings', {
            'fields': ('display_queue', 'display_announcements', 'display_health_tips', 'display_weather')
        }),
        ('Auto-refresh Settings', {
            'fields': ('refresh_interval',)
        }),
        ('Theme Settings', {
            'fields': ('theme_color', 'logo_file')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(WaitingQueue)
class WaitingQueueAdmin(admin.ModelAdmin):
    list_display = ('queue_number', 'get_patient_name', 'get_doctor_name', 'screen', 'status', 'arrival_time', 'wait_time_minutes')
    list_filter = ('status', 'arrival_time', 'screen', 'doctor')
    search_fields = ('queue_number', 'patient__first_name', 'patient__last_name', 'doctor__user__first_name', 'doctor__user__last_name')
    ordering = ('arrival_time',)
    readonly_fields = ('wait_time_minutes', 'created_at', 'updated_at')
    
    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"
    get_patient_name.short_description = 'Patient'
    
    def get_doctor_name(self, obj):
        return obj.doctor.user.get_full_name()
    get_doctor_name.short_description = 'Doctor'
    
    fieldsets = (
        ('Queue Information', {
            'fields': ('queue_number', 'patient', 'doctor', 'screen')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timing', {
            'fields': ('arrival_time', 'called_time', 'start_time', 'end_time')
        }),
        ('Wait Time', {
            'fields': ('estimated_wait_minutes', 'wait_time_minutes')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['call_patients', 'mark_in_progress', 'mark_completed']
    
    def call_patients(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for queue in queryset.filter(status='waiting'):
            queue.status = 'called'
            queue.called_time = timezone.now()
            queue.save()
            updated += 1
        self.message_user(request, f'{updated} patients called successfully.')
    call_patients.short_description = 'Call selected patients'
    
    def mark_in_progress(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for queue in queryset.filter(status='called'):
            queue.status = 'in_progress'
            queue.start_time = timezone.now()
            queue.save()
            updated += 1
        self.message_user(request, f'{updated} patients marked as in progress.')
    mark_in_progress.short_description = 'Mark as in progress'
    
    def mark_completed(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for queue in queryset.filter(status='in_progress'):
            queue.status = 'completed'
            queue.end_time = timezone.now()
            queue.save()
            updated += 1
        self.message_user(request, f'{updated} patients marked as completed.')
    mark_completed.short_description = 'Mark as completed'

@admin.register(ScreenAnnouncement)
class ScreenAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'announcement_type', 'priority', 'is_active', 'start_date', 'end_date', 'created_by')
    list_filter = ('announcement_type', 'is_active', 'priority', 'start_date', 'created_at')
    search_fields = ('title', 'content', 'created_by__username')
    ordering = ('-priority', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('screens',)
    
    fieldsets = (
        ('Announcement Information', {
            'fields': ('title', 'content', 'announcement_type', 'priority')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'start_date', 'end_date')
        }),
        ('Target Screens', {
            'fields': ('screens',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(HealthTip)
class HealthTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'created_by', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'content', 'created_by__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Health Tip Information', {
            'fields': ('title', 'content', 'category')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ScreenConfiguration)
class ScreenConfigurationAdmin(admin.ModelAdmin):
    list_display = ('default_refresh_interval', 'default_theme_color', 'show_queue_numbers', 'show_wait_times', 'updated_by', 'updated_at')
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('Default Settings', {
            'fields': ('default_refresh_interval', 'default_theme_color')
        }),
        ('Display Settings', {
            'fields': ('show_queue_numbers', 'show_wait_times', 'show_doctor_names')
        }),
        ('Audio Settings', {
            'fields': ('enable_audio_announcements', 'audio_language')
        }),
        ('Health Tips Settings', {
            'fields': ('health_tips_interval',)
        }),
        ('Metadata', {
            'fields': ('updated_by', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        # Only allow one configuration instance
        return not ScreenConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of configuration
        return False 