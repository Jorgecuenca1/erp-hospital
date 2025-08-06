from django.contrib import admin
from .models import (
    Hospital, Department, Room, HMSUser, Patient, 
    Appointment, MedicalRecord, HospitalConfiguration
)


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city', 'phone', 'active')
    list_filter = ('active', 'city', 'country')
    search_fields = ('name', 'code', 'license_number')
    readonly_fields = ('id',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'license_number', 'registration_number')
        }),
        ('Contact Information', {
            'fields': ('address', 'city', 'state', 'country', 'zip_code', 'phone', 'email', 'website')
        }),
        ('Additional Information', {
            'fields': ('established_date', 'active')
        }),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'hospital', 'head_of_department', 'active')
    list_filter = ('active', 'hospital')
    search_fields = ('name', 'code', 'description')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'hospital', 'head_of_department')
        }),
        ('Contact Information', {
            'fields': ('location', 'phone', 'email')
        }),
        ('Additional Information', {
            'fields': ('description', 'active')
        }),
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'room_type', 'department', 'floor', 'status', 'capacity')
    list_filter = ('room_type', 'status', 'department', 'floor')
    search_fields = ('number', 'name', 'amenities')
    fieldsets = (
        ('Basic Information', {
            'fields': ('number', 'name', 'room_type', 'department', 'floor')
        }),
        ('Capacity & Status', {
            'fields': ('capacity', 'status', 'active')
        }),
        ('Additional Information', {
            'fields': ('amenities', 'notes')
        }),
    )


@admin.register(HMSUser)
class HMSUserAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'user_type', 'department', 'hospital', 'active')
    list_filter = ('user_type', 'hospital', 'department', 'active', 'gender')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'license_number')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'employee_id', 'user_type', 'hospital', 'department')
        }),
        ('Personal Information', {
            'fields': ('phone', 'mobile', 'address', 'city', 'state', 'country', 'zip_code', 'date_of_birth', 'gender')
        }),
        ('Professional Information', {
            'fields': ('license_number', 'qualification', 'experience_years', 'specialization')
        }),
        ('Employment Information', {
            'fields': ('joining_date', 'salary', 'shift')
        }),
        ('Profile', {
            'fields': ('photo', 'signature', 'active')
        }),
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'full_name', 'date_of_birth', 'gender', 'blood_group', 'patient_type', 'active')
    list_filter = ('patient_type', 'gender', 'blood_group', 'marital_status', 'active')
    search_fields = ('patient_id', 'first_name', 'last_name', 'medical_record_number', 'phone', 'email')
    readonly_fields = ('registration_date', 'age')
    fieldsets = (
        ('Basic Information', {
            'fields': ('patient_id', 'first_name', 'middle_name', 'last_name', 'medical_record_number')
        }),
        ('Demographics', {
            'fields': ('date_of_birth', 'gender', 'blood_group', 'marital_status')
        }),
        ('Contact Information', {
            'fields': ('phone', 'mobile', 'email', 'address', 'city', 'state', 'country', 'zip_code')
        }),
        ('Medical Information', {
            'fields': ('patient_type', 'primary_doctor', 'allergies', 'medical_history', 'current_medications')
        }),
        ('Insurance Information', {
            'fields': ('insurance_number', 'insurance_provider')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Registration Information', {
            'fields': ('registration_date', 'registered_by', 'photo', 'active')
        }),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'appointment_type')
    list_filter = ('status', 'appointment_type', 'priority', 'appointment_date', 'department')
    search_fields = ('appointment_id', 'patient__first_name', 'patient__last_name', 'doctor__user__first_name', 'doctor__user__last_name')
    date_hierarchy = 'appointment_date'
    readonly_fields = ('booking_date',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('appointment_id', 'patient', 'doctor', 'department', 'room')
        }),
        ('Scheduling', {
            'fields': ('appointment_date', 'appointment_time', 'estimated_duration', 'appointment_type', 'priority')
        }),
        ('Status & Details', {
            'fields': ('status', 'chief_complaint', 'symptoms', 'notes')
        }),
        ('Booking Information', {
            'fields': ('booked_by', 'booking_date')
        }),
        ('Follow-up', {
            'fields': ('follow_up_required', 'follow_up_date', 'follow_up_notes')
        }),
        ('Financial', {
            'fields': ('consultation_fee', 'insurance_covered')
        }),
    )


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'record_date', 'provisional_diagnosis', 'final_diagnosis')
    list_filter = ('record_date', 'doctor', 'patient__patient_type')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__user__first_name', 'doctor__user__last_name', 'chief_complaint')
    date_hierarchy = 'record_date'
    readonly_fields = ('record_date', 'updated_date')
    fieldsets = (
        ('Basic Information', {
            'fields': ('patient', 'appointment', 'doctor', 'record_date', 'updated_date')
        }),
        ('Examination', {
            'fields': ('chief_complaint', 'history_of_present_illness', 'physical_examination')
        }),
        ('Vital Signs', {
            'fields': ('temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'pulse_rate', 'respiratory_rate', 'oxygen_saturation', 'weight', 'height')
        }),
        ('Diagnosis & Treatment', {
            'fields': ('provisional_diagnosis', 'final_diagnosis', 'treatment_plan', 'prescriptions')
        }),
        ('Additional Information', {
            'fields': ('lab_tests_ordered', 'radiology_tests_ordered', 'referrals')
        }),
    )


@admin.register(HospitalConfiguration)
class HospitalConfigurationAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'allow_online_booking', 'default_consultation_fee', 'currency')
    fieldsets = (
        ('General Settings', {
            'fields': ('hospital', 'allow_online_booking', 'booking_advance_days', 'appointment_duration')
        }),
        ('Financial Settings', {
            'fields': ('default_consultation_fee', 'currency')
        }),
        ('Notification Settings', {
            'fields': ('send_appointment_reminders', 'reminder_hours_before')
        }),
        ('Patient Portal Settings', {
            'fields': ('patient_portal_enabled', 'allow_patient_registration')
        }),
    ) 