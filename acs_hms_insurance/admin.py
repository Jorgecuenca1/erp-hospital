from django.contrib import admin
from django.utils.html import format_html
from .models import InsuranceProvider, InsurancePlan, PatientInsurance, InsuranceClaim, InsurancePreauthorization, InsuranceVerification, InsuranceSettings

@admin.register(InsuranceProvider)
class InsuranceProviderAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(InsurancePlan)
class InsurancePlanAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(PatientInsurance)
class PatientInsuranceAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(InsurancePreauthorization)
class InsurancePreauthorizationAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(InsuranceVerification)
class InsuranceVerificationAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(InsuranceSettings)
class InsuranceSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

