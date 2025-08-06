from django.contrib import admin
from .models import (
    GynecologyPatient, Pregnancy, AntenatalVisit, GynecologyProcedure,
    GynecologyMedicalRecord, ContraceptiveConsultation, MenopauseManagement
)


@admin.register(GynecologyPatient)
class GynecologyPatientAdmin(admin.ModelAdmin):
    list_display = ('patient', 'gravida', 'para', 'current_contraceptive', 'last_pap_smear')
    list_filter = ('current_contraceptive', 'menstrual_cycle')
    search_fields = ('patient__first_name', 'patient__last_name', 'patient__patient_id')
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient',)
        }),
        ('Gynecological History', {
            'fields': ('menarche_age', 'menopause_age')
        }),
        ('Menstrual History', {
            'fields': ('menstrual_cycle', 'cycle_length', 'flow_duration', 'last_menstrual_period')
        }),
        ('Obstetric History', {
            'fields': ('gravida', 'para', 'term_deliveries', 'preterm_deliveries', 'abortions', 'living_children')
        }),
        ('Contraceptive History', {
            'fields': ('current_contraceptive', 'contraceptive_duration')
        }),
        ('Screening History', {
            'fields': ('last_pap_smear', 'pap_smear_result', 'last_mammogram', 'mammogram_result')
        }),
        ('Additional Information', {
            'fields': ('surgical_history', 'family_history')
        }),
    )


@admin.register(Pregnancy)
class PregnancyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'pregnancy_number', 'status', 'gestational_age', 'expected_delivery_date')
    list_filter = ('status', 'high_risk', 'delivery_type')
    search_fields = ('patient__patient__first_name', 'patient__patient__last_name')
    date_hierarchy = 'expected_delivery_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('patient', 'pregnancy_number')
        }),
        ('Pregnancy Dates', {
            'fields': ('last_menstrual_period', 'expected_delivery_date', 'actual_delivery_date')
        }),
        ('Pregnancy Status', {
            'fields': ('status', 'gestational_age')
        }),
        ('Risk Assessment', {
            'fields': ('high_risk', 'risk_factors')
        }),
        ('Delivery Information', {
            'fields': ('delivery_type', 'birth_weight', 'complications')
        }),
    )


@admin.register(AntenatalVisit)
class AntenatalVisitAdmin(admin.ModelAdmin):
    list_display = ('pregnancy', 'visit_date', 'gestational_age', 'weight', 'blood_pressure_systolic', 'fetal_heart_rate')
    list_filter = ('visit_date', 'ultrasound_done')
    search_fields = ('pregnancy__patient__patient__first_name', 'pregnancy__patient__patient__last_name')
    date_hierarchy = 'visit_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('pregnancy', 'visit_date', 'gestational_age', 'doctor')
        }),
        ('Physical Examination', {
            'fields': ('weight', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'fundal_height')
        }),
        ('Fetal Assessment', {
            'fields': ('fetal_heart_rate', 'fetal_movement', 'presentation')
        }),
        ('Laboratory Results', {
            'fields': ('hemoglobin', 'urine_protein', 'urine_glucose')
        }),
        ('Ultrasound', {
            'fields': ('ultrasound_done', 'estimated_fetal_weight', 'amniotic_fluid')
        }),
        ('Advice and Follow-up', {
            'fields': ('advice', 'next_visit_date', 'notes')
        }),
    )


@admin.register(GynecologyProcedure)
class GynecologyProcedureAdmin(admin.ModelAdmin):
    list_display = ('patient', 'procedure_type', 'procedure_date', 'doctor', 'anesthesia_type')
    list_filter = ('procedure_type', 'anesthesia_type', 'specimen_sent')
    search_fields = ('patient__patient__first_name', 'patient__patient__last_name', 'indication')
    date_hierarchy = 'procedure_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('patient', 'procedure_type', 'procedure_date', 'doctor')
        }),
        ('Procedure Details', {
            'fields': ('indication', 'procedure_details', 'findings', 'complications')
        }),
        ('Anesthesia', {
            'fields': ('anesthesia_type',)
        }),
        ('Post-operative Care', {
            'fields': ('post_operative_instructions', 'follow_up_date')
        }),
        ('Specimens', {
            'fields': ('specimen_sent', 'specimen_details', 'pathology_report')
        }),
    )


@admin.register(GynecologyMedicalRecord)
class GynecologyMedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('gynecology_patient', 'medical_record')
    search_fields = ('gynecology_patient__patient__first_name', 'gynecology_patient__patient__last_name')
    fieldsets = (
        ('Basic Information', {
            'fields': ('medical_record', 'gynecology_patient')
        }),
        ('Gynecological Examination', {
            'fields': ('external_genitalia', 'vaginal_examination', 'cervical_examination', 'bimanual_examination')
        }),
        ('Breast Examination', {
            'fields': ('breast_examination',)
        }),
        ('Specific Symptoms', {
            'fields': ('vaginal_discharge', 'pelvic_pain', 'menstrual_irregularities')
        }),
        ('Investigations', {
            'fields': ('ultrasound_findings', 'laboratory_results')
        }),
        ('Diagnosis & Treatment', {
            'fields': ('gynecological_diagnosis', 'hormonal_therapy', 'surgical_plan')
        }),
    )


@admin.register(ContraceptiveConsultation)
class ContraceptiveConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'consultation_date', 'current_method', 'method_provided', 'follow_up_required')
    list_filter = ('current_method', 'method_provided', 'follow_up_required')
    search_fields = ('patient__patient__first_name', 'patient__patient__last_name')
    date_hierarchy = 'consultation_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('patient', 'consultation_date', 'doctor')
        }),
        ('Contraceptive Methods', {
            'fields': ('current_method', 'satisfaction_with_current', 'desired_method', 'method_provided')
        }),
        ('Counseling', {
            'fields': ('counseling_topics', 'side_effects_discussed')
        }),
        ('Follow-up', {
            'fields': ('follow_up_required', 'follow_up_date', 'notes')
        }),
    )


@admin.register(MenopauseManagement)
class MenopauseManagementAdmin(admin.ModelAdmin):
    list_display = ('patient', 'assessment_date', 'menopause_status', 'symptom_severity', 'treatment_type')
    list_filter = ('menopause_status', 'symptom_severity', 'treatment_type')
    search_fields = ('patient__patient__first_name', 'patient__patient__last_name')
    date_hierarchy = 'assessment_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('patient', 'assessment_date', 'doctor', 'menopause_status')
        }),
        ('Symptoms', {
            'fields': ('hot_flashes', 'night_sweats', 'mood_changes', 'sleep_disturbances', 'vaginal_dryness', 'decreased_libido')
        }),
        ('Assessment', {
            'fields': ('symptom_severity', 'quality_of_life_impact')
        }),
        ('Treatment', {
            'fields': ('treatment_type', 'treatment_details')
        }),
        ('Monitoring', {
            'fields': ('bone_density_assessment', 'cardiovascular_assessment')
        }),
        ('Follow-up', {
            'fields': ('follow_up_date', 'notes')
        }),
    ) 