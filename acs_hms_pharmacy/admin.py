from django.contrib import admin
from django.utils.html import format_html
from .models import DrugCategory, Manufacturer, Drug, DrugInventory, Prescription, PrescriptionItem, PharmacyDispensing, DispensingItem, PharmacyBilling, PharmacySettings, DrugInteraction, PharmacyStockAdjustment

@admin.register(DrugCategory)
class DrugCategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(DrugInventory)
class DrugInventoryAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(PharmacyDispensing)
class PharmacyDispensingAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(DispensingItem)
class DispensingItemAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(PharmacyBilling)
class PharmacyBillingAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(PharmacySettings)
class PharmacySettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(DrugInteraction)
class DrugInteractionAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(PharmacyStockAdjustment)
class PharmacyStockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

