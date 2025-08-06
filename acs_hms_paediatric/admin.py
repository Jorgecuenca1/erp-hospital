from django.contrib import admin
from django.utils.html import format_html
from .models import (
    PediatricPatient, GrowthChart, VaccinationRecord, 
    DevelopmentalAssessment, PediatricMedicalRecord, 
    NutritionalAssessment, PediatricProcedure
)

@admin.register(PediatricPatient)
class PediatricPatientAdmin(admin.ModelAdmin):
    list_display = ['patient', 'birth_weight', 'gestational_age', 'current_feeding_type', 'school_attending']
    list_filter = ['delivery_type', 'current_feeding_type', 'school_attending', 'learning_difficulties']
    search_fields = ['patient__first_name', 'patient__last_name']
    readonly_fields = ['age_in_months']
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient', 'age_in_months')
        }),
        ('Birth Information', {
            'fields': ('birth_weight', 'birth_height', 'birth_head_circumference', 'gestational_age', 'delivery_type', 'apgar_score_1_min', 'apgar_score_5_min')
        }),
        ('Feeding History', {
            'fields': ('current_feeding_type', 'breastfeeding_duration', 'solid_food_start_age')
        }),
        ('Developmental Milestones', {
            'fields': ('head_control_age', 'sitting_age', 'crawling_age', 'walking_age', 'first_word_age')
        }),
        ('School Information', {
            'fields': ('school_attending', 'school_grade', 'learning_difficulties')
        }),
        ('Social History', {
            'fields': ('parents_marital_status', 'siblings_count', 'family_structure')
        }),
        ('Medical History', {
            'fields': ('previous_hospitalizations', 'chronic_conditions')
        }),
    )

@admin.register(GrowthChart)
class GrowthChartAdmin(admin.ModelAdmin):
    list_display = ['patient', 'measurement_date', 'age_in_months', 'weight', 'height', 'nutritional_status']
    list_filter = ['measurement_date', 'nutritional_status']
    search_fields = ['patient__patient__first_name', 'patient__patient__last_name']
    date_hierarchy = 'measurement_date'

@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'vaccine_type', 'dose_number', 'vaccination_date', 'age_given', 'administered_by']
    list_filter = ['vaccine_type', 'vaccination_date', 'administered_by']
    search_fields = ['patient__patient__first_name', 'patient__patient__last_name', 'vaccine_type']
    date_hierarchy = 'vaccination_date'

@admin.register(DevelopmentalAssessment)
class DevelopmentalAssessmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'assessment_date', 'age_in_months', 'doctor', 'development_status', 'follow_up_required']
    list_filter = ['assessment_date', 'development_status', 'follow_up_required', 'doctor']
    search_fields = ['patient__patient__first_name', 'patient__patient__last_name']
    date_hierarchy = 'assessment_date'

@admin.register(PediatricMedicalRecord)
class PediatricMedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['medical_record', 'pediatric_patient', 'weight_for_age', 'height_for_age']
    list_filter = ['weight_for_age', 'height_for_age']
    search_fields = ['pediatric_patient__patient__first_name', 'pediatric_patient__patient__last_name']

@admin.register(NutritionalAssessment)
class NutritionalAssessmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'assessment_date', 'doctor', 'nutritional_status', 'follow_up_date']
    list_filter = ['assessment_date', 'nutritional_status', 'doctor']
    search_fields = ['patient__patient__first_name', 'patient__patient__last_name']
    date_hierarchy = 'assessment_date'

@admin.register(PediatricProcedure)
class PediatricProcedureAdmin(admin.ModelAdmin):
    list_display = ['patient', 'procedure_type', 'procedure_date', 'doctor', 'consent_obtained', 'follow_up_required']
    list_filter = ['procedure_type', 'procedure_date', 'consent_obtained', 'follow_up_required', 'doctor']
    search_fields = ['patient__patient__first_name', 'patient__patient__last_name', 'procedure_type']
    date_hierarchy = 'procedure_date'
