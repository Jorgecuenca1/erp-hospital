from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
from .models import (
    TheaterBooking, TheaterSchedule, TheaterEquipmentChecklist,
    TheaterPreparation, TheaterUtilization, TheaterStaff,
    TheaterIncident, TheaterInventory
)


@admin.register(TheaterBooking)
class TheaterBookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'operation_theater', 'surgery', 'scheduled_start', 'scheduled_end', 'colored_status', 'priority']
    list_filter = ['status', 'priority', 'operation_theater', 'scheduled_start']
    search_fields = ['booking_id', 'surgery__surgery_id', 'surgery__patient__name']
    readonly_fields = ['booking_id', 'duration', 'booking_date', 'created_at', 'updated_at']
    date_hierarchy = 'scheduled_start'
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_id', 'operation_theater', 'surgery', 'booked_by', 'booking_date')
        }),
        ('Scheduling', {
            'fields': ('scheduled_start', 'scheduled_end', 'actual_start', 'actual_end', 'duration')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('Preparation', {
            'fields': ('setup_time', 'cleanup_time', 'special_requirements', 'equipment_needed')
        }),
        ('Cancellation', {
            'fields': ('cancellation_reason', 'cancelled_by', 'cancelled_date'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def colored_status(self, obj):
        colors = {
            'confirmed': 'green',
            'tentative': 'orange',
            'cancelled': 'red',
            'completed': 'blue',
            'in_progress': 'purple',
            'delayed': 'red',
            'emergency': 'red'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'


@admin.register(TheaterSchedule)
class TheaterScheduleAdmin(admin.ModelAdmin):
    list_display = ['operation_theater', 'date', 'start_time', 'end_time', 'schedule_type', 'is_available', 'max_bookings']
    list_filter = ['schedule_type', 'is_available', 'date', 'operation_theater']
    search_fields = ['operation_theater__name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Schedule Information', {
            'fields': ('operation_theater', 'date', 'schedule_type')
        }),
        ('Time Slots', {
            'fields': ('start_time', 'end_time', 'is_available', 'max_bookings')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Administration', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(TheaterEquipmentChecklist)
class TheaterEquipmentChecklistAdmin(admin.ModelAdmin):
    list_display = ['checklist_id', 'booking', 'overall_status', 'checked_by', 'checked_at']
    list_filter = ['overall_status', 'checked_at', 'booking__operation_theater']
    search_fields = ['checklist_id', 'booking__booking_id', 'issues_found']
    readonly_fields = ['checklist_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('checklist_id', 'booking', 'overall_status', 'checked_by', 'checked_at')
        }),
        ('Equipment Status', {
            'fields': ('anesthesia_machine', 'ventilator', 'monitoring_equipment', 'electrocautery', 'suction_unit', 'defibrillator')
        }),
        ('Environmental Checks', {
            'fields': ('temperature_ok', 'humidity_ok', 'air_filtration_ok', 'lighting_ok', 'emergency_power_ok')
        }),
        ('Safety Checks', {
            'fields': ('fire_extinguisher_ok', 'emergency_exits_clear', 'communication_system_ok')
        }),
        ('Surgical Instruments', {
            'fields': ('instruments_sterile', 'instruments_complete', 'implants_available')
        }),
        ('Issues & Actions', {
            'fields': ('issues_found', 'corrective_actions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(TheaterPreparation)
class TheaterPreparationAdmin(admin.ModelAdmin):
    list_display = ['booking', 'preparation_type', 'assigned_to', 'scheduled_start', 'scheduled_end', 'colored_status']
    list_filter = ['preparation_type', 'status', 'scheduled_start', 'booking__operation_theater']
    search_fields = ['booking__booking_id', 'description', 'assigned_to__user__username']
    readonly_fields = ['duration', 'created_at', 'updated_at']
    date_hierarchy = 'scheduled_start'
    
    fieldsets = (
        ('Preparation Details', {
            'fields': ('booking', 'preparation_type', 'description', 'estimated_duration', 'duration')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'status')
        }),
        ('Schedule', {
            'fields': ('scheduled_start', 'scheduled_end', 'actual_start', 'actual_end')
        }),
        ('Notes & Issues', {
            'fields': ('notes', 'issues_encountered')
        }),
        ('Administration', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def colored_status(self, obj):
        colors = {
            'pending': 'orange',
            'in_progress': 'blue',
            'completed': 'green',
            'failed': 'red',
            'cancelled': 'gray'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'


@admin.register(TheaterUtilization)
class TheaterUtilizationAdmin(admin.ModelAdmin):
    list_display = ['operation_theater', 'date', 'total_surgeries', 'completed_surgeries', 'utilization_rate', 'turnover_time']
    list_filter = ['date', 'operation_theater']
    search_fields = ['operation_theater__name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('operation_theater', 'date')
        }),
        ('Hours Tracking', {
            'fields': ('total_scheduled_hours', 'total_actual_hours', 'utilization_rate', 'turnover_time')
        }),
        ('Surgery Statistics', {
            'fields': ('total_surgeries', 'completed_surgeries', 'cancelled_surgeries', 'emergency_surgeries')
        }),
        ('Downtime Tracking', {
            'fields': ('maintenance_hours', 'cleaning_hours', 'idle_hours')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(TheaterStaff)
class TheaterStaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'operation_theater', 'date', 'shift', 'is_primary', 'is_available']
    list_filter = ['role', 'shift', 'is_primary', 'is_available', 'date', 'operation_theater']
    search_fields = ['user__user__username', 'user__user__first_name', 'user__user__last_name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Staff Information', {
            'fields': ('user', 'role', 'operation_theater')
        }),
        ('Schedule', {
            'fields': ('date', 'shift', 'start_time', 'end_time')
        }),
        ('Status', {
            'fields': ('is_primary', 'is_available')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Administration', {
            'fields': ('assigned_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(TheaterIncident)
class TheaterIncidentAdmin(admin.ModelAdmin):
    list_display = ['incident_id', 'operation_theater', 'incident_type', 'severity', 'occurred_at', 'is_resolved', 'reported_by']
    list_filter = ['incident_type', 'severity', 'is_resolved', 'occurred_at', 'operation_theater']
    search_fields = ['incident_id', 'description', 'reported_by__user__username']
    readonly_fields = ['incident_id', 'created_at', 'updated_at']
    date_hierarchy = 'occurred_at'
    
    fieldsets = (
        ('Incident Information', {
            'fields': ('incident_id', 'operation_theater', 'booking', 'incident_type', 'severity')
        }),
        ('Description', {
            'fields': ('description', 'occurred_at')
        }),
        ('Actions Taken', {
            'fields': ('immediate_action_taken', 'corrective_actions', 'preventive_measures')
        }),
        ('Investigation', {
            'fields': ('reported_by', 'investigated_by', 'is_resolved', 'resolved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(TheaterInventory)
class TheaterInventoryAdmin(admin.ModelAdmin):
    list_display = ['operation_theater', 'item_name', 'item_type', 'current_stock', 'minimum_stock', 'is_low_stock', 'is_expired', 'is_critical']
    list_filter = ['item_type', 'is_critical', 'is_active', 'operation_theater']
    search_fields = ['item_name', 'batch_number', 'supplier']
    readonly_fields = ['is_low_stock', 'is_overstocked', 'is_expired', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Item Information', {
            'fields': ('operation_theater', 'item_name', 'item_type', 'unit_cost')
        }),
        ('Stock Management', {
            'fields': ('current_stock', 'minimum_stock', 'maximum_stock', 'is_low_stock', 'is_overstocked')
        }),
        ('Product Details', {
            'fields': ('expiry_date', 'batch_number', 'supplier', 'last_restocked', 'is_expired')
        }),
        ('Status', {
            'fields': ('is_critical', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


# Dashboard customization
admin.site.site_header = "HMS Operation Theater Management"
admin.site.site_title = "HMS Operation Theater Admin"
admin.site.index_title = "Operation Theater Management Administration" 