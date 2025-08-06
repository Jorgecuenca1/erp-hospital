from django.contrib import admin
from .models import MedicalDevice, ProductionOrder, QualityCheck, BillOfMaterials


@admin.register(MedicalDevice)
class MedicalDeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_type', 'model_number', 'manufacturer', 'serial_number', 'status')
    list_filter = ('status', 'device_type', 'manufacturer')
    search_fields = ('name', 'serial_number', 'model_number')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'device', 'quantity', 'priority', 'status', 'assigned_to')
    list_filter = ('status', 'priority', 'assigned_to')
    search_fields = ('order_number', 'device__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(QualityCheck)
class QualityCheckAdmin(admin.ModelAdmin):
    list_display = ('production_order', 'check_type', 'result', 'inspector', 'checked_at')
    list_filter = ('result', 'inspector')
    search_fields = ('production_order__order_number', 'check_type')


@admin.register(BillOfMaterials)
class BillOfMaterialsAdmin(admin.ModelAdmin):
    list_display = ('device', 'component_name', 'quantity_required', 'unit_cost', 'supplier', 'is_critical')
    list_filter = ('is_critical', 'supplier')
    search_fields = ('device__name', 'component_name') 