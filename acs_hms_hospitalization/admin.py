from django.contrib import admin
from django.utils.html import format_html
from .models import Admission, RoomAssignment, DailyRounds, NursingCare, DischargeRecord, MedicationAdministration, InpatientBilling

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(RoomAssignment)
class RoomAssignmentAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(DailyRounds)
class DailyRoundsAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(NursingCare)
class NursingCareAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(DischargeRecord)
class DischargeRecordAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(MedicationAdministration)
class MedicationAdministrationAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(InpatientBilling)
class InpatientBillingAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

