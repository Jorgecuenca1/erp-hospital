from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    RadiologyModality, RadiologyExam, RadiologyOrder, RadiologyStudy,
    RadiologyImage, RadiologyReport, RadiologyProtocol, RadiologySettings
)

@admin.register(RadiologyModality)
class RadiologyModalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'modality_code', 'manufacturer', 'model', 'location', 'is_active')
    list_filter = ('modality_code', 'manufacturer', 'is_active', 'contrast_capable')
    search_fields = ('name', 'manufacturer', 'model', 'serial_number')
    ordering = ('modality_code', 'name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'modality_code', 'description')
        }),
        ('Technical Specifications', {
            'fields': ('manufacturer', 'model', 'serial_number', 'max_resolution', 'supported_formats')
        }),
        ('Capabilities', {
            'fields': ('contrast_capable',)
        }),
        ('Location', {
            'fields': ('location', 'room_number')
        }),
        ('Maintenance', {
            'fields': ('last_calibration', 'next_calibration', 'maintenance_notes')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(RadiologyExam)
class RadiologyExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'exam_code', 'modality', 'body_part', 'estimated_duration', 'cost', 'is_active')
    list_filter = ('modality', 'body_part', 'fasting_required', 'contrast_required', 'is_active')
    search_fields = ('exam_name', 'exam_code', 'description')
    ordering = ('modality', 'exam_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('exam_code', 'exam_name', 'description', 'modality', 'body_part')
        }),
        ('Preparation', {
            'fields': ('prep_instructions', 'fasting_required', 'contrast_required')
        }),
        ('Timing & Pricing', {
            'fields': ('estimated_duration', 'cost', 'insurance_code')
        }),
        ('Clinical Information', {
            'fields': ('common_indications', 'contraindications')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(RadiologyOrder)
class RadiologyOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'patient', 'exam', 'ordering_physician', 'status', 'priority', 'ordered_date')
    list_filter = ('status', 'priority', 'ordered_date', 'exam__modality')
    search_fields = ('order_id', 'patient__first_name', 'patient__last_name', 'ordering_physician__user__username')
    ordering = ('-ordered_date',)
    readonly_fields = ('order_id', 'ordered_date', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'patient', 'appointment', 'exam', 'ordering_physician')
        }),
        ('Clinical Information', {
            'fields': ('clinical_indication', 'clinical_history', 'provisional_diagnosis')
        }),
        ('Order Status', {
            'fields': ('status', 'priority', 'ordered_date', 'scheduled_date')
        }),
        ('Special Instructions', {
            'fields': ('special_instructions', 'contrast_allergies')
        }),
        ('Patient Safety', {
            'fields': ('pregnancy_status',)
        }),
        ('Authorization', {
            'fields': ('insurance_authorized', 'authorization_number')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(RadiologyStudy)
class RadiologyStudyAdmin(admin.ModelAdmin):
    list_display = ('study_id', 'get_patient_name', 'get_exam_name', 'technologist', 'status', 'study_date')
    list_filter = ('status', 'study_date', 'modality', 'contrast_used', 'image_quality')
    search_fields = ('study_id', 'order__patient__first_name', 'order__patient__last_name', 'technologist__user__username')
    ordering = ('-study_date',)
    readonly_fields = ('study_id', 'duration', 'created_at', 'updated_at')
    
    def get_patient_name(self, obj):
        return f"{obj.order.patient.first_name} {obj.order.patient.last_name}"
    get_patient_name.short_description = 'Patient'
    
    def get_exam_name(self, obj):
        return obj.order.exam.exam_name
    get_exam_name.short_description = 'Exam'
    
    fieldsets = (
        ('Study Information', {
            'fields': ('study_id', 'order', 'study_date', 'technologist', 'modality')
        }),
        ('Study Status', {
            'fields': ('status', 'start_time', 'end_time', 'duration')
        }),
        ('Technical Parameters', {
            'fields': ('kvp', 'mas', 'slice_thickness')
        }),
        ('Contrast Information', {
            'fields': ('contrast_used', 'contrast_type', 'contrast_volume')
        }),
        ('Quality Control', {
            'fields': ('image_quality', 'technical_notes')
        }),
        ('Image Information', {
            'fields': ('number_of_images', 'storage_location')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(RadiologyImage)
class RadiologyImageAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'study', 'image_number', 'series_number', 'image_type', 'image_quality')
    list_filter = ('image_type', 'image_quality', 'created_at')
    search_fields = ('image_id', 'study__study_id', 'study__order__patient__first_name')
    ordering = ('study', 'series_number', 'image_number')
    readonly_fields = ('image_id', 'file_size', 'created_at')
    
    fieldsets = (
        ('Image Information', {
            'fields': ('image_id', 'study', 'image_number', 'series_number', 'image_type')
        }),
        ('File Information', {
            'fields': ('file_path', 'file_size', 'file_format')
        }),
        ('Image Parameters', {
            'fields': ('matrix_size', 'pixel_spacing', 'slice_location')
        }),
        ('Annotations', {
            'fields': ('annotations', 'measurements')
        }),
        ('Quality', {
            'fields': ('image_quality',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(RadiologyReport)
class RadiologyReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'get_patient_name', 'radiologist', 'status', 'critical_findings', 'dictated_date', 'finalized_date')
    list_filter = ('status', 'critical_findings', 'dictated_date', 'finalized_date')
    search_fields = ('report_id', 'study__order__patient__first_name', 'study__order__patient__last_name', 'radiologist__user__username')
    ordering = ('-created_at',)
    readonly_fields = ('report_id', 'turnaround_time', 'created_at', 'updated_at')
    
    def get_patient_name(self, obj):
        return f"{obj.study.order.patient.first_name} {obj.study.order.patient.last_name}"
    get_patient_name.short_description = 'Patient'
    
    fieldsets = (
        ('Report Information', {
            'fields': ('report_id', 'study', 'radiologist', 'status')
        }),
        ('Report Content', {
            'fields': ('clinical_history', 'technique', 'findings', 'impression', 'recommendations')
        }),
        ('Critical Findings', {
            'fields': ('critical_findings', 'critical_communicated', 'communication_method', 'communicated_to', 'communication_time')
        }),
        ('Comparison', {
            'fields': ('comparison_studies', 'comparison_findings')
        }),
        ('Timing', {
            'fields': ('dictated_date', 'transcribed_date', 'finalized_date', 'turnaround_time')
        }),
        ('Follow-up', {
            'fields': ('follow_up_required', 'follow_up_timeframe', 'follow_up_instructions')
        }),
        ('Addendum', {
            'fields': ('addendum_text', 'addendum_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(RadiologyProtocol)
class RadiologyProtocolAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam', 'version', 'effective_date', 'is_active')
    list_filter = ('exam__modality', 'is_active', 'effective_date')
    search_fields = ('name', 'protocol_id', 'exam__exam_name')
    ordering = ('exam', 'name')
    readonly_fields = ('protocol_id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Protocol Information', {
            'fields': ('protocol_id', 'name', 'exam', 'description', 'indication')
        }),
        ('Technical Parameters', {
            'fields': ('kvp_range', 'mas_range', 'slice_thickness', 'reconstruction_algorithm')
        }),
        ('Contrast Protocol', {
            'fields': ('contrast_protocol', 'contrast_timing')
        }),
        ('Positioning', {
            'fields': ('patient_position', 'anatomical_coverage')
        }),
        ('Instructions', {
            'fields': ('patient_instructions', 'technologist_instructions')
        }),
        ('Version Control', {
            'fields': ('version', 'effective_date', 'created_by')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(RadiologySettings)
class RadiologySettingsAdmin(admin.ModelAdmin):
    list_display = ('dicom_ae_title', 'dicom_port', 'default_appointment_duration', 'max_studies_per_day', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Image Storage', {
            'fields': ('default_storage_path', 'backup_storage_path')
        }),
        ('DICOM Settings', {
            'fields': ('dicom_ae_title', 'dicom_port', 'pacs_server')
        }),
        ('Report Settings', {
            'fields': ('auto_send_reports', 'critical_result_notification')
        }),
        ('Quality Control', {
            'fields': ('image_quality_checks', 'mandatory_peer_review')
        }),
        ('Scheduling', {
            'fields': ('default_appointment_duration', 'max_studies_per_day')
        }),
        ('Patient Safety', {
            'fields': ('pregnancy_screening_required', 'contrast_allergy_screening')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        # Only allow one settings instance
        return not RadiologySettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of settings
        return False 