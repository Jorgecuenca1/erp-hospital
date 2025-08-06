from django.contrib import admin
from .models import MedicalEquipment, MaintenanceSchedule, MaintenanceRecord, MaintenanceAlert


@admin.register(MedicalEquipment)
class MedicalEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'equipment_type', 'serial_number', 'location', 'department', 'status')
    list_filter = ('status', 'equipment_type', 'department', 'manufacturer')
    search_fields = ('name', 'serial_number', 'model_number')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'maintenance_type', 'frequency', 'next_maintenance', 'priority', 'status')
    list_filter = ('maintenance_type', 'frequency', 'priority', 'status')
    search_fields = ('equipment__name', 'equipment__serial_number')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'maintenance_date', 'technician', 'maintenance_type', 'cost', 'downtime_hours')
    list_filter = ('maintenance_type', 'maintenance_date', 'technician')
    search_fields = ('equipment__name', 'equipment__serial_number', 'description')
    readonly_fields = ('created_at',)


@admin.register(MaintenanceAlert)
class MaintenanceAlertAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'alert_type', 'priority', 'is_read', 'created_at')
    list_filter = ('alert_type', 'priority', 'is_read')
    search_fields = ('equipment__name', 'message')
    readonly_fields = ('created_at',) 