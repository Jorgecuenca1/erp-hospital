from django.contrib import admin
from django.utils.html import format_html
from .models import (
    AestheticTreatment, AestheticConsultation, AestheticProcedure,
    AestheticProduct, AestheticEquipment, PatientPhotoRecord
)

@admin.register(AestheticTreatment)
class AestheticTreatmentAdmin(admin.ModelAdmin):
    list_display = ['treatment_name', 'treatment_code', 'category', 'duration_minutes', 'base_price', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['treatment_name', 'treatment_code', 'description']
    ordering = ['treatment_name']

@admin.register(AestheticConsultation)
class AestheticConsultationAdmin(admin.ModelAdmin):
    list_display = ['consultation_number', 'patient', 'consultant', 'consultation_date', 'skin_type', 'follow_up_date']
    list_filter = ['consultation_date', 'skin_type', 'consultant']
    search_fields = ['consultation_number', 'patient__first_name', 'patient__last_name']
    date_hierarchy = 'consultation_date'
    filter_horizontal = ['recommended_treatments']

@admin.register(AestheticProcedure)
class AestheticProcedureAdmin(admin.ModelAdmin):
    list_display = ['procedure_number', 'patient', 'treatment', 'scheduled_date', 'status', 'session_number', 'final_cost']
    list_filter = ['status', 'scheduled_date', 'treatment__category', 'primary_practitioner']
    search_fields = ['procedure_number', 'patient__first_name', 'patient__last_name', 'treatment__treatment_name']
    date_hierarchy = 'scheduled_date'

@admin.register(AestheticProduct)
class AestheticProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_code', 'brand', 'product_type', 'current_stock', 'selling_price', 'is_active']
    list_filter = ['product_type', 'is_active', 'brand']
    search_fields = ['product_name', 'product_code', 'brand']
    ordering = ['product_name']

@admin.register(AestheticEquipment)
class AestheticEquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'brand', 'model', 'status', 'location', 'assigned_to']
    list_filter = ['equipment_type', 'status', 'brand']
    search_fields = ['equipment_name', 'brand', 'model', 'serial_number']
    ordering = ['equipment_name']

@admin.register(PatientPhotoRecord)
class PatientPhotoRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'photo_type', 'anatomical_area', 'photo_date', 'taken_by', 'consent_obtained']
    list_filter = ['photo_type', 'anatomical_area', 'photo_date', 'consent_obtained']
    search_fields = ['patient__first_name', 'patient__last_name', 'photo_description']
    date_hierarchy = 'photo_date'
