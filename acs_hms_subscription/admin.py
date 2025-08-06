from django.contrib import admin
from django.utils.html import format_html
from .models import SubscriptionPlan, HospitalSubscription, SubscriptionInvoice, SubscriptionUsage, SubscriptionModuleAccess, SubscriptionDiscount, SubscriptionPayment

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(HospitalSubscription)
class HospitalSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(SubscriptionInvoice)
class SubscriptionInvoiceAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(SubscriptionUsage)
class SubscriptionUsageAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(SubscriptionModuleAccess)
class SubscriptionModuleAccessAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(SubscriptionDiscount)
class SubscriptionDiscountAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_filter = []
    search_fields = []
    ordering = ['id']

