from django.contrib import admin
from django.utils.html import format_html
from .models import (
    EyeExamination, OphthalmologyProcedure, EyeDisease, OpticalPrescription,
    VisualFieldTest, OphthalmologyEquipment
)


@admin.register(EyeExamination)
class EyeExaminationAdmin(admin.ModelAdmin):
    list_display = ['examination_number', 'patient', 'ophthalmologist', 'examination_date', 'diagnosis']
    list_filter = ['examination_date', 'ophthalmologist']
    search_fields = ['examination_number', 'patient__first_name', 'patient__last_name', 'diagnosis']
    readonly_fields = ['examination_number', 'examination_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('examination_number', 'patient', 'appointment', 'ophthalmologist', 'examination_date')
        }),
        ('Chief Complaint', {
            'fields': ('chief_complaint', 'history_present_illness')
        }),
        ('Visual Acuity', {
            'fields': ('va_right_uncorrected', 'va_left_uncorrected', 'va_right_corrected', 'va_left_corrected')
        }),
        ('Refraction', {
            'fields': ('sphere_right', 'cylinder_right', 'axis_right', 'sphere_left', 'cylinder_left', 'axis_left')
        }),
        ('Intraocular Pressure', {
            'fields': ('iop_right', 'iop_left', 'iop_method')
        }),
        ('Pupil Examination', {
            'fields': ('pupil_right_size', 'pupil_left_size', 'pupil_right_reaction', 'pupil_left_reaction', 'rapd')
        }),
        ('Anterior Segment', {
            'fields': ('conjunctiva_right', 'conjunctiva_left', 'cornea_right', 'cornea_left', 
                      'anterior_chamber_right', 'anterior_chamber_left', 'iris_right', 'iris_left', 
                      'lens_right', 'lens_left')
        }),
        ('Posterior Segment', {
            'fields': ('vitreous_right', 'vitreous_left', 'optic_disc_right', 'optic_disc_left',
                      'macula_right', 'macula_left', 'retinal_vessels_right', 'retinal_vessels_left',
                      'peripheral_retina_right', 'peripheral_retina_left')
        }),
        ('Diagnosis and Plan', {
            'fields': ('diagnosis', 'treatment_plan', 'medications', 'follow_up_date')
        }),
        ('Additional Notes', {
            'fields': ('additional_notes',)
        }),
    )


@admin.register(OphthalmologyProcedure)
class OphthalmologyProcedureAdmin(admin.ModelAdmin):
    list_display = ['procedure_number', 'patient', 'procedure_name', 'eye_operated', 'scheduled_date', 'status', 'primary_surgeon']
    list_filter = ['procedure_type', 'status', 'eye_operated', 'scheduled_date']
    search_fields = ['procedure_number', 'patient__first_name', 'patient__last_name', 'procedure_name']
    readonly_fields = ['procedure_number']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('procedure_number', 'patient', 'eye_examination')
        }),
        ('Procedure Details', {
            'fields': ('procedure_type', 'procedure_name', 'description', 'eye_operated')
        }),
        ('Scheduling', {
            'fields': ('scheduled_date', 'actual_date', 'duration_minutes')
        }),
        ('Medical Team', {
            'fields': ('primary_surgeon', 'assistant_surgeon', 'anesthesiologist')
        }),
        ('Pre-operative', {
            'fields': ('preop_diagnosis', 'preop_medications', 'preop_instructions')
        }),
        ('Operative Details', {
            'fields': ('anesthesia_type', 'surgical_technique', 'complications')
        }),
        ('Post-operative', {
            'fields': ('postop_diagnosis', 'postop_medications', 'postop_instructions')
        }),
        ('Status & Follow-up', {
            'fields': ('status', 'follow_up_date')
        }),
    )


@admin.register(EyeDisease)
class EyeDiseaseAdmin(admin.ModelAdmin):
    list_display = ['patient', 'disease_name', 'disease_category', 'affected_eye', 'severity', 'diagnosis_date', 'is_active']
    list_filter = ['disease_category', 'severity', 'affected_eye', 'is_active', 'diagnosis_date']
    search_fields = ['patient__first_name', 'patient__last_name', 'disease_name', 'icd_code']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('patient', 'disease_name', 'disease_category', 'icd_code')
        }),
        ('Disease Details', {
            'fields': ('affected_eye', 'severity', 'onset_date', 'diagnosis_date', 'diagnosed_by')
        }),
        ('Clinical Details', {
            'fields': ('symptoms', 'clinical_findings', 'stage')
        }),
        ('Treatment', {
            'fields': ('current_treatment', 'treatment_response')
        }),
        ('Status', {
            'fields': ('is_active', 'resolved_date')
        }),
        ('Follow-up', {
            'fields': ('last_follow_up', 'next_follow_up')
        }),
    )


@admin.register(OpticalPrescription)
class OpticalPrescriptionAdmin(admin.ModelAdmin):
    list_display = ['prescription_number', 'patient', 'prescription_date', 'lens_type', 'prescribed_by', 'dispensed', 'valid_until']
    list_filter = ['lens_type', 'dispensed', 'prescription_date', 'prescribed_by']
    search_fields = ['prescription_number', 'patient__first_name', 'patient__last_name']
    readonly_fields = ['prescription_number', 'prescription_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('prescription_number', 'patient', 'eye_examination', 'prescribed_by', 'prescription_date')
        }),
        ('Right Eye', {
            'fields': ('sphere_right', 'cylinder_right', 'axis_right', 'add_right')
        }),
        ('Left Eye', {
            'fields': ('sphere_left', 'cylinder_left', 'axis_left', 'add_left')
        }),
        ('Lens Specifications', {
            'fields': ('lens_type', 'pupillary_distance')
        }),
        ('Frame & Instructions', {
            'fields': ('frame_specifications', 'special_instructions')
        }),
        ('Validity', {
            'fields': ('valid_until',)
        }),
        ('Dispensing', {
            'fields': ('dispensed', 'dispensed_date', 'dispensed_by')
        }),
    )


@admin.register(VisualFieldTest)
class VisualFieldTestAdmin(admin.ModelAdmin):
    list_display = ['test_number', 'patient', 'test_type', 'eye_tested', 'test_date', 'performed_by', 'test_reliability']
    list_filter = ['test_type', 'eye_tested', 'test_date', 'performed_by']
    search_fields = ['test_number', 'patient__first_name', 'patient__last_name']
    readonly_fields = ['test_number', 'test_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('test_number', 'patient', 'eye_examination', 'test_date', 'performed_by')
        }),
        ('Test Details', {
            'fields': ('test_type', 'eye_tested')
        }),
        ('Test Parameters', {
            'fields': ('test_strategy', 'stimulus_size', 'background_luminance')
        }),
        ('Results', {
            'fields': ('mean_deviation', 'pattern_standard_deviation', 'visual_field_index')
        }),
        ('Test Quality', {
            'fields': ('fixation_losses', 'false_positives', 'false_negatives', 'test_reliability')
        }),
        ('Interpretation', {
            'fields': ('interpretation', 'defect_pattern')
        }),
        ('Additional Data', {
            'fields': ('test_duration',)
        }),
    )


@admin.register(OphthalmologyEquipment)
class OphthalmologyEquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'model', 'serial_number', 'location', 'status', 'status_color']
    list_filter = ['equipment_type', 'status', 'manufacturer', 'location']
    search_fields = ['equipment_name', 'model', 'serial_number', 'manufacturer']
    
    def status_color(self, obj):
        colors = {
            'ACTIVE': 'green',
            'MAINTENANCE': 'orange',
            'REPAIR': 'red',
            'RETIRED': 'gray'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_color.short_description = 'Status'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('equipment_name', 'equipment_type', 'model', 'manufacturer', 'serial_number')
        }),
        ('Location & Assignment', {
            'fields': ('location', 'assigned_to')
        }),
        ('Dates', {
            'fields': ('purchase_date', 'installation_date', 'warranty_expiry')
        }),
        ('Maintenance', {
            'fields': ('last_maintenance', 'next_maintenance', 'maintenance_interval_days')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Additional Information', {
            'fields': ('specifications', 'notes')
        }),
    ) 