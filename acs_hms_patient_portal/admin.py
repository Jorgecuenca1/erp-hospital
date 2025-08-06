from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    PatientPortalUser, PatientAppointment, PatientDocument, 
    PatientMessage, PatientBilling, PatientFeedback, PatientNotification
)


@admin.register(PatientPortalUser)
class PatientPortalUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'patient', 'is_active', 'is_verified', 'two_factor_enabled', 'created_at']
    list_filter = ['is_active', 'is_verified', 'two_factor_enabled', 'preferred_language', 'created_at']
    search_fields = ['user__username', 'patient__nombre', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'last_login_ip', 'failed_login_attempts']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'patient')
        }),
        ('Access Settings', {
            'fields': ('is_active', 'is_verified', 'two_factor_enabled')
        }),
        ('Preferences', {
            'fields': ('preferred_language', 'preferred_timezone', 'email_notifications', 'sms_notifications')
        }),
        ('Security', {
            'fields': ('last_login_ip', 'failed_login_attempts', 'locked_until'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PatientAppointment)
class PatientAppointmentAdmin(admin.ModelAdmin):
    list_display = ['portal_user', 'doctor', 'appointment_date', 'appointment_time', 'status', 'is_paid', 'consultation_fee']
    list_filter = ['status', 'is_paid', 'is_telehealth', 'appointment_date', 'created_at']
    search_fields = ['portal_user__patient__nombre', 'doctor__nombre', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'appointment_date'
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('portal_user', 'doctor', 'appointment_date', 'appointment_time', 'duration_minutes')
        }),
        ('Medical Information', {
            'fields': ('reason', 'special_instructions', 'status')
        }),
        ('Telehealth', {
            'fields': ('is_telehealth', 'telehealth_link'),
            'classes': ('collapse',)
        }),
        ('Billing', {
            'fields': ('consultation_fee', 'is_paid', 'payment_method')
        }),
        ('Accounting', {
            'fields': ('asiento_contable',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('portal_user', 'doctor', 'asiento_contable')


@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    list_display = ['portal_user', 'title', 'document_type', 'is_visible_to_patient', 'is_verified', 'uploaded_at']
    list_filter = ['document_type', 'is_visible_to_patient', 'is_verified', 'uploaded_at']
    search_fields = ['portal_user__patient__nombre', 'title', 'description']
    readonly_fields = ['uploaded_at', 'file_size', 'file_type']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('portal_user', 'title', 'document_type', 'description')
        }),
        ('File', {
            'fields': ('file', 'file_size', 'file_type')
        }),
        ('Access Control', {
            'fields': ('is_visible_to_patient', 'requires_verification', 'is_verified')
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'uploaded_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PatientMessage)
class PatientMessageAdmin(admin.ModelAdmin):
    list_display = ['portal_user', 'subject', 'message_type', 'is_read', 'is_replied', 'is_urgent', 'created_at']
    list_filter = ['message_type', 'is_read', 'is_replied', 'is_urgent', 'created_at']
    search_fields = ['portal_user__patient__nombre', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Message Information', {
            'fields': ('portal_user', 'doctor', 'subject', 'message_type', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_replied', 'is_urgent')
        }),
        ('Response', {
            'fields': ('response', 'responded_by', 'responded_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PatientBilling)
class PatientBillingAdmin(admin.ModelAdmin):
    list_display = ['bill_number', 'portal_user', 'total_amount', 'paid_amount', 'balance', 'status', 'due_date']
    list_filter = ['status', 'payment_method', 'due_date', 'paid_date', 'created_at']
    search_fields = ['bill_number', 'portal_user__patient__nombre', 'description']
    readonly_fields = ['bill_number', 'balance', 'created_at', 'updated_at']
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Bill Information', {
            'fields': ('portal_user', 'bill_number', 'description')
        }),
        ('Amounts', {
            'fields': ('total_amount', 'paid_amount', 'balance')
        }),
        ('Status', {
            'fields': ('status', 'payment_method')
        }),
        ('Dates', {
            'fields': ('due_date', 'paid_date')
        }),
        ('Accounting', {
            'fields': ('asiento_contable',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PatientFeedback)
class PatientFeedbackAdmin(admin.ModelAdmin):
    list_display = ['portal_user', 'rating', 'title', 'doctor', 'is_approved', 'is_published', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_published', 'created_at']
    search_fields = ['portal_user__patient__nombre', 'title', 'feedback']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Feedback Information', {
            'fields': ('portal_user', 'doctor', 'rating', 'title', 'feedback')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'is_published', 'moderator_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PatientNotification)
class PatientNotificationAdmin(admin.ModelAdmin):
    list_display = ['portal_user', 'notification_type', 'title', 'is_read', 'is_sent', 'send_at']
    list_filter = ['notification_type', 'is_read', 'is_sent', 'send_email', 'send_sms', 'send_push', 'created_at']
    search_fields = ['portal_user__patient__nombre', 'title', 'message']
    readonly_fields = ['created_at', 'updated_at', 'sent_at']
    date_hierarchy = 'send_at'
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('portal_user', 'notification_type', 'title', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_sent')
        }),
        ('Delivery Options', {
            'fields': ('send_email', 'send_sms', 'send_push')
        }),
        ('Scheduling', {
            'fields': ('send_at', 'sent_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    ) 