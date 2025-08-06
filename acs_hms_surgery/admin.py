from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import (
    SurgeryType, OperationTheater, SurgeryTeam, Surgery, 
    SurgeryEquipment, SurgerySupplies, SurgerySupplyUsage,
    PostOperativeCare, SurgeryComplications
)


@admin.register(SurgeryType)
class SurgeryTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'specialty', 'risk_level', 'estimated_duration', 'requires_anesthesia', 'standard_cost', 'is_active']
    list_filter = ['specialty', 'risk_level', 'requires_anesthesia', 'requires_icu', 'is_active']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'specialty', 'description')
        }),
        ('Surgery Details', {
            'fields': ('estimated_duration', 'risk_level', 'requires_anesthesia', 'requires_icu', 'requires_blood_bank')
        }),
        ('Financial', {
            'fields': ('standard_cost',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(OperationTheater)
class OperationTheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'theater_number', 'theater_type', 'floor', 'status', 'capacity', 'is_active']
    list_filter = ['theater_type', 'status', 'floor', 'is_active']
    search_fields = ['name', 'theater_number']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'theater_number', 'theater_type', 'floor', 'capacity')
        }),
        ('Status & Equipment', {
            'fields': ('status', 'equipment_list', 'temperature_control', 'air_filtration', 'emergency_backup')
        }),
        ('Maintenance', {
            'fields': ('last_maintenance', 'next_maintenance', 'notes')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(SurgeryTeam)
class SurgeryTeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'role', 'specialization', 'experience_years', 'is_available', 'is_active']
    list_filter = ['role', 'is_available', 'is_active']
    search_fields = ['name', 'user__username', 'specialization']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'user', 'role', 'specialization')
        }),
        ('Experience', {
            'fields': ('experience_years', 'certification')
        }),
        ('Status', {
            'fields': ('is_available', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


class SurgerySupplyUsageInline(admin.TabularInline):
    model = SurgerySupplyUsage
    extra = 1
    readonly_fields = ['total_cost', 'used_at']


class PostOperativeCareInline(admin.TabularInline):
    model = PostOperativeCare
    extra = 1
    readonly_fields = ['created_at', 'updated_at']


class SurgeryComplicationsInline(admin.TabularInline):
    model = SurgeryComplications
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Surgery)
class SurgeryAdmin(admin.ModelAdmin):
    list_display = ['surgery_id', 'patient', 'surgery_type', 'primary_surgeon', 'scheduled_date', 'status', 'priority', 'colored_status']
    list_filter = ['status', 'priority', 'surgery_type__specialty', 'scheduled_date', 'anesthesia_type']
    search_fields = ['surgery_id', 'patient__name', 'surgery_type__name', 'primary_surgeon__user__username']
    readonly_fields = ['surgery_id', 'duration', 'created_at', 'updated_at']
    date_hierarchy = 'scheduled_date'
    inlines = [SurgerySupplyUsageInline, PostOperativeCareInline, SurgeryComplicationsInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('surgery_id', 'patient', 'surgery_type', 'operation_theater', 'primary_surgeon', 'team_members')
        }),
        ('Scheduling', {
            'fields': ('scheduled_date', 'actual_start_time', 'actual_end_time', 'duration')
        }),
        ('Surgery Details', {
            'fields': ('status', 'priority', 'anesthesia_type')
        }),
        ('Pre-Operative', {
            'fields': ('pre_op_diagnosis', 'pre_op_notes', 'pre_op_vitals', 'pre_op_checklist'),
            'classes': ('collapse',)
        }),
        ('Intra-Operative', {
            'fields': ('operative_procedure', 'operative_notes', 'complications', 'blood_loss', 'fluids_given'),
            'classes': ('collapse',)
        }),
        ('Post-Operative', {
            'fields': ('post_op_diagnosis', 'post_op_notes', 'post_op_instructions', 'recovery_notes'),
            'classes': ('collapse',)
        }),
        ('Financial', {
            'fields': ('estimated_cost', 'actual_cost')
        }),
        ('Administrative', {
            'fields': ('consent_obtained', 'consent_date', 'insurance_approved')
        }),
        ('Cancellation', {
            'fields': ('cancelled_reason', 'cancelled_by', 'cancelled_date'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def colored_status(self, obj):
        colors = {
            'scheduled': 'blue',
            'pre_op': 'orange',
            'in_progress': 'green',
            'completed': 'purple',
            'cancelled': 'red',
            'postponed': 'gray',
            'emergency': 'red'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'
    
    filter_horizontal = ('team_members',)


@admin.register(SurgeryEquipment)
class SurgeryEquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'equipment_type', 'serial_number', 'operation_theater', 'is_operational', 'is_active']
    list_filter = ['equipment_type', 'is_operational', 'is_active', 'operation_theater']
    search_fields = ['name', 'serial_number', 'model', 'manufacturer']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'equipment_type', 'model', 'manufacturer', 'serial_number')
        }),
        ('Location', {
            'fields': ('operation_theater',)
        }),
        ('Purchase & Warranty', {
            'fields': ('purchase_date', 'warranty_expires')
        }),
        ('Maintenance', {
            'fields': ('last_maintenance', 'next_maintenance', 'maintenance_notes')
        }),
        ('Status', {
            'fields': ('is_operational', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(SurgerySupplies)
class SurgerySuppliesAdmin(admin.ModelAdmin):
    list_display = ['name', 'supply_type', 'stock_quantity', 'minimum_stock', 'unit_cost', 'is_low_stock', 'is_expired', 'is_active']
    list_filter = ['supply_type', 'is_sterile', 'is_disposable', 'is_active']
    search_fields = ['name', 'brand', 'batch_number']
    readonly_fields = ['is_low_stock', 'is_expired', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'supply_type', 'brand', 'unit_of_measure', 'unit_cost')
        }),
        ('Stock Management', {
            'fields': ('stock_quantity', 'minimum_stock', 'is_low_stock')
        }),
        ('Product Details', {
            'fields': ('expiry_date', 'batch_number', 'is_sterile', 'is_disposable', 'is_expired')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(SurgerySupplyUsage)
class SurgerySupplyUsageAdmin(admin.ModelAdmin):
    list_display = ['surgery', 'supply', 'quantity_used', 'unit_cost', 'total_cost', 'used_by', 'used_at']
    list_filter = ['used_at', 'supply__supply_type']
    search_fields = ['surgery__surgery_id', 'supply__name', 'used_by__user__username']
    readonly_fields = ['total_cost', 'used_at']
    fieldsets = (
        ('Usage Information', {
            'fields': ('surgery', 'supply', 'quantity_used', 'unit_cost', 'total_cost')
        }),
        ('Additional Info', {
            'fields': ('notes', 'used_by', 'used_at')
        })
    )


@admin.register(PostOperativeCare)
class PostOperativeCareAdmin(admin.ModelAdmin):
    list_display = ['surgery', 'care_type', 'assigned_to', 'status', 'start_date', 'end_date']
    list_filter = ['care_type', 'status', 'start_date']
    search_fields = ['surgery__surgery_id', 'instructions', 'assigned_to__user__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Care Information', {
            'fields': ('surgery', 'care_type', 'instructions', 'frequency', 'duration')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'status')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(SurgeryComplications)
class SurgeryComplicationsAdmin(admin.ModelAdmin):
    list_display = ['surgery', 'complication_type', 'severity', 'occurred_at', 'is_resolved', 'reported_by']
    list_filter = ['complication_type', 'severity', 'is_resolved', 'occurred_at']
    search_fields = ['surgery__surgery_id', 'description', 'reported_by__user__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Complication Details', {
            'fields': ('surgery', 'complication_type', 'severity', 'description')
        }),
        ('Timeline', {
            'fields': ('occurred_at', 'resolved_at', 'is_resolved')
        }),
        ('Treatment', {
            'fields': ('treatment_given', 'outcome')
        }),
        ('Reporting', {
            'fields': ('reported_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


# Custom admin site configuration
admin.site.site_header = "HMS Surgery Management"
admin.site.site_title = "HMS Surgery Admin"
admin.site.index_title = "Surgery Management Administration" 