from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    NursingUnit, NursingShift, NursingAssessment, NursingCare,
    MedicationAdministration, NursingHandoff, PatientHandoff,
    NursingIncident, NursingSettings
)

@admin.register(NursingUnit)
class NursingUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_type', 'bed_capacity', 'current_occupancy', 'occupancy_rate', 'nurse_manager', 'is_active')
    list_filter = ('unit_type', 'is_active', 'floor')
    search_fields = ('name', 'unit_id', 'floor', 'wing')
    ordering = ('name',)
    readonly_fields = ('unit_id', 'occupancy_rate', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Unit Information', {
            'fields': ('unit_id', 'name', 'unit_type')
        }),
        ('Location', {
            'fields': ('floor', 'wing')
        }),
        ('Capacity', {
            'fields': ('bed_capacity', 'current_occupancy', 'occupancy_rate')
        }),
        ('Staff', {
            'fields': ('nurse_manager', 'charge_nurse')
        }),
        ('Contact', {
            'fields': ('phone', 'extension')
        }),
        ('Specialization', {
            'fields': ('specialty_services', 'equipment_available')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(NursingShift)
class NursingShiftAdmin(admin.ModelAdmin):
    list_display = ('get_nurse_name', 'unit', 'shift_type', 'shift_date', 'start_time', 'end_time', 'status')
    list_filter = ('shift_type', 'status', 'shift_date', 'unit')
    search_fields = ('nurse__user__first_name', 'nurse__user__last_name', 'shift_id')
    ordering = ('-shift_date', '-start_time')
    readonly_fields = ('shift_id', 'duration', 'created_at', 'updated_at')
    filter_horizontal = ('assigned_patients',)
    
    def get_nurse_name(self, obj):
        return obj.nurse.user.get_full_name()
    get_nurse_name.short_description = 'Nurse'
    
    fieldsets = (
        ('Shift Information', {
            'fields': ('shift_id', 'nurse', 'unit', 'shift_type')
        }),
        ('Schedule', {
            'fields': ('shift_date', 'start_time', 'end_time')
        }),
        ('Actual Times', {
            'fields': ('actual_start', 'actual_end', 'duration')
        }),
        ('Patient Assignment', {
            'fields': ('assigned_patients', 'max_patients')
        }),
        ('Breaks', {
            'fields': ('break_start', 'break_end', 'lunch_start', 'lunch_end')
        }),
        ('Overtime', {
            'fields': ('overtime_hours', 'overtime_reason')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Notes', {
            'fields': ('shift_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(NursingAssessment)
class NursingAssessmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'nurse', 'assessment_type', 'assessment_date', 'pain_score', 'fall_risk_level')
    list_filter = ('assessment_type', 'assessment_date', 'fall_risk_level', 'consciousness_level')
    search_fields = ('patient__first_name', 'patient__last_name', 'nurse__user__first_name', 'assessment_id')
    ordering = ('-assessment_date',)
    readonly_fields = ('assessment_id', 'created_at', 'updated_at')
    
    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"
    get_patient_name.short_description = 'Patient'
    
    fieldsets = (
        ('Assessment Information', {
            'fields': ('assessment_id', 'patient', 'nurse', 'assessment_type', 'assessment_date')
        }),
        ('Vital Signs', {
            'fields': ('temperature', 'pulse', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'respiratory_rate', 'oxygen_saturation')
        }),
        ('Pain Assessment', {
            'fields': ('pain_score', 'pain_location', 'pain_description')
        }),
        ('Neurological', {
            'fields': ('consciousness_level',)
        }),
        ('Mobility', {
            'fields': ('mobility_status',)
        }),
        ('Skin', {
            'fields': ('skin_condition',)
        }),
        ('Fall Risk', {
            'fields': ('fall_risk_score', 'fall_risk_level')
        }),
        ('Nutrition', {
            'fields': ('appetite',)
        }),
        ('Elimination', {
            'fields': ('bowel_sounds',)
        }),
        ('Assessment & Planning', {
            'fields': ('assessment_notes', 'nursing_diagnosis', 'care_plan', 'interventions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(NursingCare)
class NursingCareAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'nurse', 'care_type', 'scheduled_time', 'status', 'priority')
    list_filter = ('care_type', 'status', 'priority', 'scheduled_time')
    search_fields = ('patient__first_name', 'patient__last_name', 'nurse__user__first_name', 'care_id')
    ordering = ('-scheduled_time',)
    readonly_fields = ('care_id', 'duration', 'created_at', 'updated_at')
    
    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"
    get_patient_name.short_description = 'Patient'
    
    fieldsets = (
        ('Care Information', {
            'fields': ('care_id', 'patient', 'nurse', 'care_type', 'care_description')
        }),
        ('Scheduling', {
            'fields': ('scheduled_time', 'estimated_duration', 'priority')
        }),
        ('Execution', {
            'fields': ('status', 'start_time', 'end_time', 'duration')
        }),
        ('Outcomes', {
            'fields': ('outcome', 'patient_response')
        }),
        ('Frequency', {
            'fields': ('frequency', 'is_recurring')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(MedicationAdministration)
class MedicationAdministrationAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'nurse', 'medication_name', 'dose', 'route', 'scheduled_time', 'status')
    list_filter = ('route', 'status', 'scheduled_time')
    search_fields = ('patient__first_name', 'patient__last_name', 'medication_name', 'mar_id')
    ordering = ('-scheduled_time',)
    readonly_fields = ('mar_id', 'created_at', 'updated_at')
    
    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"
    get_patient_name.short_description = 'Patient'
    
    fieldsets = (
        ('Medication Record', {
            'fields': ('mar_id', 'patient', 'nurse')
        }),
        ('Medication Details', {
            'fields': ('medication_name', 'dose', 'route', 'frequency')
        }),
        ('Scheduling', {
            'fields': ('scheduled_time', 'administration_time', 'status')
        }),
        ('Administration Details', {
            'fields': ('site', 'lot_number', 'expiration_date')
        }),
        ('Patient Response', {
            'fields': ('patient_response', 'adverse_reactions')
        }),
        ('Not Given', {
            'fields': ('reason_not_given',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(NursingHandoff)
class NursingHandoffAdmin(admin.ModelAdmin):
    list_display = ('get_outgoing_nurse', 'get_incoming_nurse', 'unit', 'handoff_date', 'unit_census', 'is_completed')
    list_filter = ('handoff_date', 'unit', 'is_completed')
    search_fields = ('outgoing_nurse__user__first_name', 'incoming_nurse__user__first_name', 'handoff_id')
    ordering = ('-handoff_date',)
    readonly_fields = ('handoff_id', 'created_at', 'updated_at')
    filter_horizontal = ('patients',)
    
    def get_outgoing_nurse(self, obj):
        return obj.outgoing_nurse.user.get_full_name()
    get_outgoing_nurse.short_description = 'Outgoing Nurse'
    
    def get_incoming_nurse(self, obj):
        return obj.incoming_nurse.user.get_full_name()
    get_incoming_nurse.short_description = 'Incoming Nurse'
    
    fieldsets = (
        ('Handoff Information', {
            'fields': ('handoff_id', 'outgoing_nurse', 'incoming_nurse', 'unit', 'handoff_date')
        }),
        ('Unit Status', {
            'fields': ('unit_census', 'admissions', 'discharges', 'transfers')
        }),
        ('Notes', {
            'fields': ('unit_notes', 'safety_concerns')
        }),
        ('Completion', {
            'fields': ('is_completed', 'completed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(PatientHandoff)
class PatientHandoffAdmin(admin.ModelAdmin):
    list_display = ('handoff', 'get_patient_name', 'get_handoff_date')
    list_filter = ('handoff__handoff_date', 'handoff__unit')
    search_fields = ('patient__first_name', 'patient__last_name', 'handoff__handoff_id')
    ordering = ('-handoff__handoff_date',)
    readonly_fields = ('created_at',)
    
    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"
    get_patient_name.short_description = 'Patient'
    
    def get_handoff_date(self, obj):
        return obj.handoff.handoff_date
    get_handoff_date.short_description = 'Handoff Date'
    
    fieldsets = (
        ('Handoff Information', {
            'fields': ('handoff', 'patient')
        }),
        ('Patient Status', {
            'fields': ('current_condition', 'recent_changes')
        }),
        ('Care Plans', {
            'fields': ('active_orders', 'pending_procedures')
        }),
        ('Concerns', {
            'fields': ('priority_concerns', 'safety_issues')
        }),
        ('Family/Social', {
            'fields': ('family_updates', 'psychosocial_concerns')
        }),
        ('Education', {
            'fields': ('patient_education_needs',)
        }),
        ('Discharge Planning', {
            'fields': ('discharge_planning',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(NursingIncident)
class NursingIncidentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'incident_type', 'severity', 'occurred_at', 'unit', 'reported_by', 'is_resolved')
    list_filter = ('incident_type', 'severity', 'occurred_at', 'unit', 'is_resolved')
    search_fields = ('patient__first_name', 'patient__last_name', 'incident_id', 'description')
    ordering = ('-occurred_at',)
    readonly_fields = ('incident_id', 'created_at', 'updated_at')
    
    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return "N/A"
    get_patient_name.short_description = 'Patient'
    
    fieldsets = (
        ('Incident Information', {
            'fields': ('incident_id', 'patient', 'unit', 'incident_type', 'severity')
        }),
        ('Occurrence', {
            'fields': ('occurred_at', 'discovered_at')
        }),
        ('Description', {
            'fields': ('description', 'contributing_factors')
        }),
        ('Personnel', {
            'fields': ('reported_by', 'witness')
        }),
        ('Actions Taken', {
            'fields': ('immediate_actions', 'physician_notified', 'family_notified')
        }),
        ('Investigation', {
            'fields': ('investigation_required', 'investigation_notes')
        }),
        ('Follow-up', {
            'fields': ('follow_up_required', 'follow_up_actions')
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'resolved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(NursingSettings)
class NursingSettingsAdmin(admin.ModelAdmin):
    list_display = ('day_shift_start', 'day_shift_end', 'max_patients_per_nurse', 'max_patients_icu', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Shift Settings', {
            'fields': ('day_shift_start', 'day_shift_end', 'night_shift_start', 'night_shift_end')
        }),
        ('Patient Assignment', {
            'fields': ('max_patients_per_nurse', 'max_patients_icu')
        }),
        ('Documentation', {
            'fields': ('mandatory_assessment_frequency', 'vital_signs_frequency')
        }),
        ('Medication Administration', {
            'fields': ('medication_scan_required', 'double_check_high_risk')
        }),
        ('Safety', {
            'fields': ('fall_risk_reassessment', 'incident_reporting_required')
        }),
        ('Quality Measures', {
            'fields': ('pressure_ulcer_assessment', 'infection_control_measures')
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
        return not NursingSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of settings
        return False 