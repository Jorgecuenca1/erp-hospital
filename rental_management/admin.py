from django.contrib import admin
from .models import RentalEquipment, RentalAgreement, RentalPayment, RentalInspection


@admin.register(RentalEquipment)
class RentalEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'manufacturer', 'serial_number', 'availability_status', 'daily_rate')
    list_filter = ('category', 'availability_status', 'manufacturer')
    search_fields = ('name', 'serial_number', 'model')


@admin.register(RentalAgreement)
class RentalAgreementAdmin(admin.ModelAdmin):
    list_display = ('agreement_number', 'equipment', 'renter_name', 'start_date', 'end_date', 'status', 'total_amount')
    list_filter = ('status', 'rental_period', 'start_date')
    search_fields = ('agreement_number', 'renter_name', 'equipment__name')


@admin.register(RentalPayment)
class RentalPaymentAdmin(admin.ModelAdmin):
    list_display = ('agreement', 'payment_date', 'amount', 'payment_method', 'payment_type')
    list_filter = ('payment_method', 'payment_type', 'payment_date')
    search_fields = ('agreement__agreement_number', 'transaction_id')


@admin.register(RentalInspection)
class RentalInspectionAdmin(admin.ModelAdmin):
    list_display = ('agreement', 'inspection_type', 'inspection_date', 'inspector', 'condition', 'damage_cost')
    list_filter = ('inspection_type', 'condition', 'inspection_date')
    search_fields = ('agreement__agreement_number', 'inspector__username') 