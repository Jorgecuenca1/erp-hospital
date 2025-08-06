from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    CommissionStructure, CommissionAgent, CommissionRecord,
    CommissionPayment, CommissionReport, CommissionConfiguration
)

@admin.register(CommissionStructure)
class CommissionStructureAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'calculation_type', 'percentage_rate', 'flat_fee_amount', 'is_active', 'effective_date')
    list_filter = ('service_type', 'calculation_type', 'is_active', 'effective_date')
    search_fields = ('name', 'service_type')
    ordering = ('service_type', 'name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'service_type', 'calculation_type')
        }),
        ('Commission Rates', {
            'fields': ('percentage_rate', 'flat_fee_amount', 'tier_structure', 'custom_formula')
        }),
        ('Conditions', {
            'fields': ('minimum_service_amount', 'maximum_commission')
        }),
        ('Settings', {
            'fields': ('is_active', 'effective_date', 'expiry_date')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(CommissionAgent)
class CommissionAgentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'agent_code', 'agent_type', 'get_total_commission_earned', 'get_pending_commission', 'is_active')
    list_filter = ('agent_type', 'is_active', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'agent_code', 'email')
    ordering = ('user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at', 'get_total_commission_earned', 'get_total_commission_paid', 'get_pending_commission')
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    fieldsets = (
        ('Agent Information', {
            'fields': ('user', 'agent_type', 'agent_code')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Banking Details', {
            'fields': ('bank_name', 'account_number', 'routing_number')
        }),
        ('Commission Settings', {
            'fields': ('default_commission_structure', 'commission_threshold')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Commission Summary', {
            'fields': ('get_total_commission_earned', 'get_total_commission_paid', 'get_pending_commission'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(CommissionRecord)
class CommissionRecordAdmin(admin.ModelAdmin):
    list_display = ('commission_id', 'get_agent_name', 'get_patient_name', 'service_amount', 'commission_amount', 'status', 'service_date')
    list_filter = ('status', 'service_date', 'structure', 'approved_at', 'paid_at')
    search_fields = ('commission_id', 'agent__user__first_name', 'agent__user__last_name', 'patient__first_name', 'patient__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('commission_id', 'commission_amount', 'calculation_details', 'created_at', 'updated_at')
    
    def get_agent_name(self, obj):
        return obj.agent.user.get_full_name()
    get_agent_name.short_description = 'Agent'
    
    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"
    get_patient_name.short_description = 'Patient'
    
    fieldsets = (
        ('Commission Information', {
            'fields': ('commission_id', 'agent', 'structure')
        }),
        ('Service Details', {
            'fields': ('patient', 'service_description', 'service_amount', 'service_date')
        }),
        ('Commission Calculation', {
            'fields': ('commission_amount', 'calculation_details')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Approval', {
            'fields': ('approved_by', 'approved_at', 'approval_notes')
        }),
        ('Payment', {
            'fields': ('paid_by', 'paid_at', 'payment_method', 'payment_reference')
        }),
        ('Accounting', {
            'fields': ('asiento_contable',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['approve_commissions', 'mark_as_paid']
    
    def approve_commissions(self, request, queryset):
        updated = 0
        for commission in queryset.filter(status='pending'):
            commission.approve(request.user)
            updated += 1
        self.message_user(request, f'{updated} commissions approved successfully.')
    approve_commissions.short_description = 'Approve selected commissions'
    
    def mark_as_paid(self, request, queryset):
        updated = 0
        for commission in queryset.filter(status='approved'):
            commission.pay(request.user, 'manual')
            updated += 1
        self.message_user(request, f'{updated} commissions marked as paid.')
    mark_as_paid.short_description = 'Mark selected commissions as paid'

@admin.register(CommissionPayment)
class CommissionPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'get_agent_name', 'total_amount', 'payment_method', 'payment_date', 'status')
    list_filter = ('status', 'payment_method', 'payment_date', 'processed_at')
    search_fields = ('payment_id', 'agent__user__first_name', 'agent__user__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('payment_id', 'created_at', 'updated_at')
    filter_horizontal = ('commission_records',)
    
    def get_agent_name(self, obj):
        return obj.agent.user.get_full_name()
    get_agent_name.short_description = 'Agent'
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'agent', 'total_amount')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'payment_date', 'payment_reference')
        }),
        ('Commission Records', {
            'fields': ('commission_records',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Processing', {
            'fields': ('processed_by', 'processed_at')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Accounting', {
            'fields': ('asiento_contable',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['process_payments']
    
    def process_payments(self, request, queryset):
        updated = 0
        for payment in queryset.filter(status='pending'):
            payment.process_payment(request.user)
            updated += 1
        self.message_user(request, f'{updated} payments processed successfully.')
    process_payments.short_description = 'Process selected payments'

@admin.register(CommissionReport)
class CommissionReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'title', 'report_type', 'start_date', 'end_date', 'generated_by', 'generated_at')
    list_filter = ('report_type', 'generated_at', 'start_date', 'end_date')
    search_fields = ('report_id', 'title', 'generated_by__username')
    ordering = ('-generated_at',)
    readonly_fields = ('report_id', 'report_data', 'generated_at')
    filter_horizontal = ('agent_filter', 'structure_filter')
    
    fieldsets = (
        ('Report Information', {
            'fields': ('report_id', 'report_type', 'title')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
        ('Filters', {
            'fields': ('agent_filter', 'structure_filter')
        }),
        ('Generated Data', {
            'fields': ('report_data', 'report_file')
        }),
        ('Metadata', {
            'fields': ('generated_by', 'generated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(CommissionConfiguration)
class CommissionConfigurationAdmin(admin.ModelAdmin):
    list_display = ('auto_approve_under_amount', 'minimum_payment_amount', 'payment_frequency_days', 'updated_by', 'updated_at')
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('Auto-approval Settings', {
            'fields': ('auto_approve_under_amount',)
        }),
        ('Payment Settings', {
            'fields': ('minimum_payment_amount', 'payment_frequency_days')
        }),
        ('Notification Settings', {
            'fields': ('notify_on_commission_earned', 'notify_on_payment_processed')
        }),
        ('Accounting Integration', {
            'fields': ('default_commission_account',)
        }),
        ('Metadata', {
            'fields': ('updated_by', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        # Only allow one configuration instance
        return not CommissionConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of configuration
        return False 