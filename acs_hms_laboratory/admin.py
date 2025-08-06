from django.contrib import admin
from django.utils.html import format_html
from .models import (
    LabTestCategory, LabTest, LabEquipment, LabTestOrder, 
    LabTestOrderItem, LabSample, LabResult, LabReport, 
    LabQualityControl, LabWorkshift
)

@admin.register(LabTestCategory)
class LabTestCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category', 'test_type', 'price', 'is_active']
    list_filter = ['category', 'test_type', 'is_active', 'is_outsourced', 'requires_fasting']
    search_fields = ['name', 'code', 'description']
    ordering = ['name']

@admin.register(LabEquipment)
class LabEquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'manufacturer', 'serial_number', 'status', 'location']
    list_filter = ['status', 'manufacturer', 'department']
    search_fields = ['name', 'model', 'manufacturer', 'serial_number']
    ordering = ['name']

@admin.register(LabTestOrder)
class LabTestOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'patient', 'ordered_by', 'order_date', 'status', 'priority', 'total_amount']
    list_filter = ['status', 'priority', 'order_date', 'insurance_covered']
    search_fields = ['order_number', 'patient__first_name', 'patient__last_name']
    date_hierarchy = 'order_date'

@admin.register(LabTestOrderItem)
class LabTestOrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'test', 'quantity', 'unit_price', 'total_price', 'status']
    list_filter = ['status', 'test__category']
    search_fields = ['order__order_number', 'test__name']

@admin.register(LabSample)
class LabSampleAdmin(admin.ModelAdmin):
    list_display = ['sample_number', 'order', 'sample_type', 'collection_date', 'status', 'quality_acceptable']
    list_filter = ['status', 'sample_type', 'collection_date', 'quality_acceptable']
    search_fields = ['sample_number', 'order__order_number']
    date_hierarchy = 'collection_date'

@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ['order_item', 'sample', 'tested_by', 'test_date', 'status', 'abnormal_flag', 'critical_flag']
    list_filter = ['status', 'test_date', 'abnormal_flag', 'critical_flag']
    search_fields = ['order_item__order__order_number', 'order_item__test__name']
    date_hierarchy = 'test_date'

@admin.register(LabReport)
class LabReportAdmin(admin.ModelAdmin):
    list_display = ['report_number', 'order', 'generated_by', 'generated_date', 'status', 'reviewed_by']
    list_filter = ['status', 'generated_date', 'delivery_method']
    search_fields = ['report_number', 'order__order_number']
    date_hierarchy = 'generated_date'

@admin.register(LabQualityControl)
class LabQualityControlAdmin(admin.ModelAdmin):
    list_display = ['qc_date', 'qc_type', 'equipment', 'performed_by', 'passed', 'corrective_action_required']
    list_filter = ['qc_type', 'qc_date', 'passed', 'corrective_action_required']
    search_fields = ['equipment__name', 'control_lot']
    date_hierarchy = 'qc_date'

@admin.register(LabWorkshift)
class LabWorkshiftAdmin(admin.ModelAdmin):
    list_display = ['shift_date', 'shift_type', 'supervisor', 'start_time', 'end_time', 'samples_processed', 'tests_completed']
    list_filter = ['shift_type', 'shift_date', 'supervisor']
    search_fields = ['supervisor__first_name', 'supervisor__last_name']
    date_hierarchy = 'shift_date'
    filter_horizontal = ['technicians']
