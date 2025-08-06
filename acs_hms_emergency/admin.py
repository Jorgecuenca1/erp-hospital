from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Ambulance, EmergencyCall, EmergencyCase, EmergencyTreatment,
    AmbulanceTrip, EmergencyEquipment, EmergencyProtocol
)


@admin.register(Ambulance)
class AmbulanceAdmin(admin.ModelAdmin):
    list_display = ['ambulance_number', 'ambulance_type', 'status', 'status_color', 'base_location', 'is_active']
    list_filter = ['ambulance_type', 'status', 'is_active', 'make']
    search_fields = ['ambulance_number', 'vehicle_registration', 'make', 'model']
    readonly_fields = ['ambulance_number']
    
    def status_color(self, obj):
        colors = {
            'AVAILABLE': 'green',
            'DISPATCHED': 'orange',
            'ON_SCENE': 'blue',
            'TRANSPORTING': 'purple',
            'AT_HOSPITAL': 'teal',
            'OUT_OF_SERVICE': 'red',
            'MAINTENANCE': 'gray'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_color.short_description = 'Status'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('ambulance_number', 'vehicle_registration', 'ambulance_type')
        }),
        ('Vehicle Details', {
            'fields': ('make', 'model', 'year')
        }),
        ('Equipment', {
            'fields': ('equipment_list', 'medical_equipment')
        }),
        ('Operational', {
            'fields': ('base_location', 'current_location', 'status')
        }),
        ('Crew', {
            'fields': ('primary_driver', 'primary_paramedic')
        }),
        ('Maintenance', {
            'fields': ('last_maintenance_date', 'next_maintenance_date', 'maintenance_notes')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(EmergencyCall)
class EmergencyCallAdmin(admin.ModelAdmin):
    list_display = ['call_number', 'call_type', 'priority', 'caller_name', 'call_date', 'status', 'ambulance']
    list_filter = ['call_type', 'priority', 'status', 'call_date']
    search_fields = ['call_number', 'caller_name', 'caller_phone', 'incident_address']
    readonly_fields = ['call_number', 'call_date', 'response_time_minutes']
    
    fieldsets = (
        ('Call Information', {
            'fields': ('call_number', 'call_date', 'caller_name', 'caller_phone')
        }),
        ('Emergency Details', {
            'fields': ('call_type', 'priority', 'chief_complaint')
        }),
        ('Location', {
            'fields': ('incident_address', 'incident_latitude', 'incident_longitude')
        }),
        ('Patient Information', {
            'fields': ('patient_name', 'patient_age', 'patient_gender')
        }),
        ('Dispatch', {
            'fields': ('dispatched_by', 'dispatch_time', 'ambulance')
        }),
        ('Response Times', {
            'fields': ('response_time_minutes', 'on_scene_time', 'transport_time', 'hospital_arrival_time')
        }),
        ('Status & Destination', {
            'fields': ('status', 'destination_hospital')
        }),
        ('Notes', {
            'fields': ('dispatch_notes', 'completion_notes')
        }),
    )


class EmergencyTreatmentInline(admin.TabularInline):
    model = EmergencyTreatment
    extra = 0
    readonly_fields = ['treatment_time']


@admin.register(EmergencyCase)
class EmergencyCaseAdmin(admin.ModelAdmin):
    list_display = ['case_number', 'patient', 'triage_level', 'arrival_date', 'status', 'assigned_doctor']
    list_filter = ['triage_level', 'status', 'arrival_mode', 'arrival_date']
    search_fields = ['case_number', 'patient__first_name', 'patient__last_name', 'chief_complaint']
    readonly_fields = ['case_number', 'arrival_date']
    
    fieldsets = (
        ('Case Information', {
            'fields': ('case_number', 'arrival_date', 'arrival_mode', 'patient')
        }),
        ('Triage', {
            'fields': ('triage_level', 'triage_time', 'triage_nurse')
        }),
        ('Presentation', {
            'fields': ('chief_complaint', 'presenting_symptoms')
        }),
        ('Vital Signs', {
            'fields': ('temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic', 
                      'pulse_rate', 'respiratory_rate', 'oxygen_saturation', 'pain_score')
        }),
        ('Treatment', {
            'fields': ('assigned_doctor', 'treatment_start_time', 'status')
        }),
        ('Outcome', {
            'fields': ('diagnosis', 'treatment_provided', 'discharge_time', 'discharge_instructions')
        }),
        ('Follow-up', {
            'fields': ('follow_up_required', 'follow_up_instructions')
        }),
        ('Related Records', {
            'fields': ('emergency_call', 'admission')
        }),
    )


@admin.register(EmergencyTreatment)
class EmergencyTreatmentAdmin(admin.ModelAdmin):
    list_display = ['emergency_case', 'treatment_time', 'performed_by', 'procedure_performed']
    list_filter = ['treatment_time', 'performed_by__user_type']
    search_fields = ['emergency_case__case_number', 'procedure_performed']
    readonly_fields = ['treatment_time']


@admin.register(AmbulanceTrip)
class AmbulanceTripAdmin(admin.ModelAdmin):
    list_display = ['trip_number', 'ambulance', 'trip_type', 'patient', 'start_time', 'status']
    list_filter = ['trip_type', 'status', 'start_time']
    search_fields = ['trip_number', 'patient__first_name', 'patient__last_name', 'ambulance__ambulance_number']
    readonly_fields = ['trip_number']
    filter_horizontal = ['additional_crew']
    
    fieldsets = (
        ('Trip Information', {
            'fields': ('trip_number', 'ambulance', 'trip_type')
        }),
        ('Crew', {
            'fields': ('driver', 'paramedic', 'additional_crew')
        }),
        ('Schedule', {
            'fields': ('start_time', 'end_time')
        }),
        ('Locations', {
            'fields': ('origin_address', 'destination_address')
        }),
        ('Patient Information', {
            'fields': ('patient', 'patient_condition')
        }),
        ('Medical Information', {
            'fields': ('vital_signs_departure', 'vital_signs_arrival', 'treatment_during_transport', 'medications_administered')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Mileage', {
            'fields': ('starting_mileage', 'ending_mileage')
        }),
        ('Related Records', {
            'fields': ('emergency_call', 'emergency_case')
        }),
        ('Notes', {
            'fields': ('trip_notes',)
        }),
    )


@admin.register(EmergencyEquipment)
class EmergencyEquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'serial_number', 'current_location', 'status', 'assigned_ambulance']
    list_filter = ['equipment_type', 'status', 'assigned_ambulance']
    search_fields = ['equipment_name', 'serial_number', 'current_location']
    
    fieldsets = (
        ('Equipment Information', {
            'fields': ('equipment_name', 'equipment_type', 'serial_number')
        }),
        ('Location', {
            'fields': ('current_location', 'assigned_ambulance')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Maintenance', {
            'fields': ('last_maintenance_date', 'next_maintenance_date')
        }),
        ('Notes', {
            'fields': ('equipment_notes',)
        }),
    )


@admin.register(EmergencyProtocol)
class EmergencyProtocolAdmin(admin.ModelAdmin):
    list_display = ['protocol_name', 'protocol_type', 'protocol_code', 'version', 'effective_date', 'is_active']
    list_filter = ['protocol_type', 'is_active', 'effective_date']
    search_fields = ['protocol_name', 'protocol_code', 'description']
    
    fieldsets = (
        ('Protocol Information', {
            'fields': ('protocol_name', 'protocol_type', 'protocol_code')
        }),
        ('Content', {
            'fields': ('description', 'indications', 'contraindications')
        }),
        ('Procedure', {
            'fields': ('assessment_steps', 'treatment_steps', 'medication_protocol')
        }),
        ('Equipment', {
            'fields': ('required_equipment',)
        }),
        ('Version Control', {
            'fields': ('version', 'effective_date', 'review_date')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


 