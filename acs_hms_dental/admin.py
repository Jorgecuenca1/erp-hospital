from django.contrib import admin
from django.utils.html import format_html
from .models import (
    DentalExamination, ToothChart, DentalTreatment, 
    DentalProcedure, DentalEquipment, DentalMaterial
)

@admin.register(DentalExamination)
class DentalExaminationAdmin(admin.ModelAdmin):
    list_display = ['examination_number', 'patient', 'dentist', 'examination_date', 'urgency', 'follow_up_date']
    list_filter = ['examination_date', 'urgency', 'dental_anxiety', 'oral_hygiene_status']
    search_fields = ['examination_number', 'patient__first_name', 'patient__last_name']
    date_hierarchy = 'examination_date'

@admin.register(ToothChart)
class ToothChartAdmin(admin.ModelAdmin):
    list_display = ['patient', 'examination', 'tooth_number', 'tooth_status', 'mobility']
    list_filter = ['tooth_status', 'mobility', 'examination__examination_date']
    search_fields = ['patient__first_name', 'patient__last_name', 'tooth_number']
    ordering = ['tooth_number']

@admin.register(DentalTreatment)
class DentalTreatmentAdmin(admin.ModelAdmin):
    list_display = ['treatment_name', 'treatment_code', 'category', 'duration_minutes', 'base_price', 'is_active']
    list_filter = ['category', 'is_active', 'requires_anesthesia', 'requires_assistant']
    search_fields = ['treatment_name', 'treatment_code', 'description']
    ordering = ['treatment_name']

@admin.register(DentalProcedure)
class DentalProcedureAdmin(admin.ModelAdmin):
    list_display = ['procedure_number', 'patient', 'treatment', 'scheduled_date', 'status', 'primary_dentist', 'procedure_cost']
    list_filter = ['status', 'scheduled_date', 'treatment__category', 'anesthesia_used', 'insurance_covered']
    search_fields = ['procedure_number', 'patient__first_name', 'patient__last_name', 'treatment__treatment_name']
    date_hierarchy = 'scheduled_date'

@admin.register(DentalEquipment)
class DentalEquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'brand', 'model', 'status', 'location', 'assigned_to']
    list_filter = ['equipment_type', 'status', 'brand']
    search_fields = ['equipment_name', 'brand', 'model', 'serial_number']
    ordering = ['equipment_name']

@admin.register(DentalMaterial)
class DentalMaterialAdmin(admin.ModelAdmin):
    list_display = ['material_name', 'material_code', 'material_type', 'brand', 'current_stock', 'cost_per_unit', 'is_active']
    list_filter = ['material_type', 'is_active', 'brand']
    search_fields = ['material_name', 'material_code', 'brand']
    ordering = ['material_name']
