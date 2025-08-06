from django.contrib import admin
from django.utils.html import format_html
from .models import (
    BloodGroup, BloodDonor, BloodDonation, BloodUnit, 
    BloodRequest, BloodIssuance, BloodTransfusion, BloodBankSettings
)

@admin.register(BloodGroup)
class BloodGroupAdmin(admin.ModelAdmin):
    list_display = ['abo_type', 'rh_factor', '__str__']
    list_filter = ['abo_type', 'rh_factor']
    ordering = ['abo_type', 'rh_factor']

@admin.register(BloodDonor)
class BloodDonorAdmin(admin.ModelAdmin):
    list_display = ['donor_id', 'first_name', 'last_name', 'blood_group', 'donor_type', 'status', 'age', 'is_eligible']
    list_filter = ['donor_type', 'status', 'blood_group', 'gender']
    search_fields = ['donor_id', 'first_name', 'last_name', 'phone', 'email']
    readonly_fields = ['donor_id', 'age', 'is_eligible']
    ordering = ['last_name', 'first_name']

@admin.register(BloodDonation)
class BloodDonationAdmin(admin.ModelAdmin):
    list_display = ['donation_id', 'donor', 'donation_type', 'donation_date', 'volume_collected', 'status', 'phlebotomist']
    list_filter = ['donation_type', 'status', 'donation_date', 'pre_screening_passed']
    search_fields = ['donation_id', 'donor__first_name', 'donor__last_name', 'donor__donor_id']
    date_hierarchy = 'donation_date'

@admin.register(BloodUnit)
class BloodUnitAdmin(admin.ModelAdmin):
    list_display = ['unit_id', 'blood_group', 'component', 'volume', 'collection_date', 'expiry_date', 'status', 'is_expired']
    list_filter = ['component', 'status', 'blood_group', 'collection_date']
    search_fields = ['unit_id', 'donation__donor__first_name', 'donation__donor__last_name']
    readonly_fields = ['unit_id', 'is_expired', 'is_available', 'days_until_expiry']
    date_hierarchy = 'collection_date'

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['request_id', 'patient', 'blood_group', 'component_required', 'units_required', 'urgency', 'status', 'required_by']
    list_filter = ['urgency', 'status', 'blood_group', 'component_required']
    search_fields = ['request_id', 'patient__first_name', 'patient__last_name']
    date_hierarchy = 'created_at'

@admin.register(BloodIssuance)
class BloodIssuanceAdmin(admin.ModelAdmin):
    list_display = ['issuance_id', 'request', 'blood_unit', 'issued_date', 'issued_by', 'received_by', 'cross_match_result']
    list_filter = ['issued_date', 'cross_match_result', 'cross_match_performed']
    search_fields = ['issuance_id', 'request__request_id', 'blood_unit__unit_id']
    date_hierarchy = 'issued_date'

@admin.register(BloodTransfusion)
class BloodTransfusionAdmin(admin.ModelAdmin):
    list_display = ['transfusion_id', 'patient', 'transfusion_type', 'volume_transfused', 'start_time', 'status', 'administered_by']
    list_filter = ['transfusion_type', 'status', 'start_time', 'reaction_type']
    search_fields = ['transfusion_id', 'patient__first_name', 'patient__last_name']
    date_hierarchy = 'start_time'

@admin.register(BloodBankSettings)
class BloodBankSettingsAdmin(admin.ModelAdmin):
    list_display = ['is_active', 'whole_blood_storage_temp', 'plasma_storage_temp', 'platelet_storage_temp']
    list_filter = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
