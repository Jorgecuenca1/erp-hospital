from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    ConsentFormTemplate, ConsentForm, ConsentFormAudit, 
    ConsentFormNotification, ConsentFormDocument, 
    ConsentFormConfiguration, ConsentFormStatistics
)


@admin.register(ConsentFormTemplate)
class ConsentFormTemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'form_type', 'language', 'is_active', 'requires_witness', 'requires_guardian', 'created_at']
    list_filter = ['form_type', 'language', 'is_active', 'requires_witness', 'requires_guardian', 'created_at']
    search_fields = ['title', 'description', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'form_type', 'language', 'description')
        }),
        ('Content', {
            'fields': ('content', 'form_fields')
        }),
        ('Settings', {
            'fields': ('is_active', 'requires_witness', 'requires_guardian', 'expires_after_days')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


class ConsentFormAuditInline(admin.TabularInline):
    model = ConsentFormAudit
    extra = 0
    readonly_fields = ['action', 'user', 'ip_address', 'timestamp']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ConsentForm)
class ConsentFormAdmin(admin.ModelAdmin):
    list_display = ['consent_id', 'patient', 'template', 'doctor', 'status', 'created_at', 'expires_at']
    list_filter = ['status', 'template__form_type', 'created_at', 'expires_at']
    search_fields = ['consent_id', 'patient__nombre', 'doctor__nombre', 'procedure_name']
    readonly_fields = ['consent_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('consent_id', 'template', 'status')
        }),
        ('Patient Information', {
            'fields': ('patient', 'guardian')
        }),
        ('Medical Context', {
            'fields': ('doctor', 'procedure_name', 'procedure_date')
        }),
        ('Form Data', {
            'fields': ('form_data',),
            'classes': ('collapse',)
        }),
        ('Patient Signature', {
            'fields': ('patient_signature', 'patient_signed_at', 'patient_ip_address'),
            'classes': ('collapse',)
        }),
        ('Guardian Signature', {
            'fields': ('guardian_signature', 'guardian_signed_at', 'guardian_ip_address'),
            'classes': ('collapse',)
        }),
        ('Witness', {
            'fields': ('witness_name', 'witness_relationship', 'witness_signature', 'witness_signed_at'),
            'classes': ('collapse',)
        }),
        ('Doctor Signature', {
            'fields': ('doctor_signature', 'doctor_signed_at'),
            'classes': ('collapse',)
        }),
        ('Expiration', {
            'fields': ('expires_at',)
        }),
        ('Revocation', {
            'fields': ('revoked_at', 'revocation_reason', 'revoked_by'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ConsentFormAuditInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('template', 'patient', 'doctor')


@admin.register(ConsentFormAudit)
class ConsentFormAuditAdmin(admin.ModelAdmin):
    list_display = ['consent_form', 'action', 'user', 'ip_address', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['consent_form__consent_id', 'user__username']
    readonly_fields = ['consent_form', 'action', 'user', 'ip_address', 'user_agent', 'details', 'timestamp']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ConsentFormNotification)
class ConsentFormNotificationAdmin(admin.ModelAdmin):
    list_display = ['consent_form', 'notification_type', 'recipient_email', 'is_sent', 'sent_at', 'retry_count']
    list_filter = ['notification_type', 'is_sent', 'created_at']
    search_fields = ['consent_form__consent_id', 'recipient_email', 'subject']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('consent_form', 'notification_type')
        }),
        ('Recipient', {
            'fields': ('recipient_email', 'recipient_name')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_sent', 'sent_at')
        }),
        ('Retry Logic', {
            'fields': ('retry_count', 'next_retry_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )


@admin.register(ConsentFormDocument)
class ConsentFormDocumentAdmin(admin.ModelAdmin):
    list_display = ['consent_form', 'document_type', 'file_size', 'generated_at', 'generated_by']
    list_filter = ['document_type', 'generated_at']
    search_fields = ['consent_form__consent_id']
    readonly_fields = ['file_size', 'generated_at']
    date_hierarchy = 'generated_at'
    
    fieldsets = (
        ('Document Information', {
            'fields': ('consent_form', 'document_type')
        }),
        ('File', {
            'fields': ('file', 'file_size')
        }),
        ('Generation Info', {
            'fields': ('generated_by', 'generated_at')
        })
    )


@admin.register(ConsentFormConfiguration)
class ConsentFormConfigurationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'signature_required', 'allow_electronic_signature', 'auto_send_notifications', 'updated_at']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Digital Signature Settings', {
            'fields': ('signature_required', 'allow_electronic_signature', 'require_timestamp')
        }),
        ('Email Settings', {
            'fields': ('auto_send_notifications', 'reminder_days_before_expiry')
        }),
        ('Security Settings', {
            'fields': ('require_ip_logging', 'require_user_agent_logging')
        }),
        ('PDF Settings', {
            'fields': ('auto_generate_pdf', 'include_signatures_in_pdf')
        }),
        ('Accounting Integration', {
            'fields': ('track_consent_costs', 'consent_processing_fee')
        }),
        ('Metadata', {
            'fields': ('updated_by', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        # Only allow one configuration instance
        return not ConsentFormConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ConsentFormStatistics)
class ConsentFormStatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_forms', 'signed_forms', 'pending_forms', 'completion_rate', 'total_revenue']
    list_filter = ['date', 'created_at']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Date', {
            'fields': ('date',)
        }),
        ('Counts', {
            'fields': ('total_forms', 'signed_forms', 'pending_forms', 'expired_forms', 'revoked_forms')
        }),
        ('Performance Metrics', {
            'fields': ('avg_time_to_sign', 'completion_rate')
        }),
        ('Revenue', {
            'fields': ('total_revenue',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False 