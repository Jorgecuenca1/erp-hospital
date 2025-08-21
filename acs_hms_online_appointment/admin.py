from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from .models import (
    OnlineAppointmentProfile, DoctorAvailability, OnlineAppointmentSlot,
    OnlineAppointment, AppointmentReminder, OnlineAppointmentSettings,
    AppointmentFeedback, WaitingList, AgendaElectronicaDisponibilidad,
    DisponibilidadDetalle
)


@admin.register(OnlineAppointmentProfile)
class OnlineAppointmentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'email', 'date_of_birth', 'gender', 'city', 'is_verified']
    list_filter = ['is_verified', 'gender', 'city', 'state', 'country', 'preferred_language']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone_number', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'patient', 'phone_number', 'email', 'date_of_birth', 'gender')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Medical Information', {
            'fields': ('medical_history', 'allergies', 'current_medications')
        }),
        ('Profile Settings', {
            'fields': ('profile_image', 'preferred_language', 'is_verified', 'verification_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day_of_week', 'start_time', 'end_time', 'slot_type', 'consultation_fee', 'is_available', 'is_telemedicine']
    list_filter = ['day_of_week', 'slot_type', 'is_available', 'is_telemedicine']
    search_fields = ['doctor__user__username', 'doctor__user__first_name', 'doctor__user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Doctor Information', {
            'fields': ('doctor', 'day_of_week')
        }),
        ('Time Slots', {
            'fields': ('start_time', 'end_time', 'slot_duration', 'slot_type')
        }),
        ('Booking Configuration', {
            'fields': ('max_appointments', 'consultation_fee', 'is_available', 'is_telemedicine')
        }),
        ('Special Instructions', {
            'fields': ('special_instructions',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(OnlineAppointmentSlot)
class OnlineAppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'slot_date', 'slot_time', 'colored_status', 'consultation_fee', 'booked_by']
    list_filter = ['status', 'slot_date', 'doctor']
    search_fields = ['doctor__user__username', 'booked_by__user__username']
    readonly_fields = ['booking_time', 'cancelled_at', 'created_at', 'updated_at']
    date_hierarchy = 'slot_date'
    
    fieldsets = (
        ('Slot Information', {
            'fields': ('availability', 'doctor', 'slot_date', 'slot_time', 'status')
        }),
        ('Booking Details', {
            'fields': ('consultation_fee', 'booked_by', 'booking_time')
        }),
        ('Cancellation Details', {
            'fields': ('cancelled_by', 'cancelled_at', 'cancellation_reason'),
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
            'available': 'green',
            'booked': 'blue',
            'blocked': 'orange',
            'cancelled': 'red'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'


class AppointmentReminderInline(admin.TabularInline):
    model = AppointmentReminder
    extra = 0
    readonly_fields = ['sent_at']


@admin.register(OnlineAppointment)
class OnlineAppointmentAdmin(admin.ModelAdmin):
    list_display = ['appointment_id', 'patient_profile', 'doctor', 'appointment_date', 'appointment_time', 'colored_status', 'payment_status', 'is_telemedicine']
    list_filter = ['status', 'payment_status', 'appointment_type', 'is_telemedicine', 'appointment_date']
    search_fields = ['appointment_id', 'patient_profile__user__username', 'doctor__user__username', 'chief_complaint']
    readonly_fields = ['appointment_id', 'cancelled_at', 'created_at', 'updated_at']
    date_hierarchy = 'appointment_date'
    inlines = [AppointmentReminderInline]
    
    fieldsets = (
        ('Appointment Information', {
            'fields': ('appointment_id', 'slot', 'patient_profile', 'doctor', 'appointment_type')
        }),
        ('Schedule', {
            'fields': ('appointment_date', 'appointment_time', 'estimated_duration', 'status')
        }),
        ('Patient Details', {
            'fields': ('chief_complaint', 'symptoms', 'medical_history', 'current_medications')
        }),
        ('Payment', {
            'fields': ('consultation_fee', 'payment_status', 'payment_method', 'transaction_id')
        }),
        ('Telemedicine', {
            'fields': ('is_telemedicine', 'meeting_link', 'meeting_id')
        }),
        ('Follow-up', {
            'fields': ('follow_up_required', 'follow_up_date', 'follow_up_notes')
        }),
        ('Cancellation', {
            'fields': ('cancelled_by', 'cancelled_at', 'cancellation_reason', 'refund_amount'),
            'classes': ('collapse',)
        }),
        ('Feedback', {
            'fields': ('patient_rating', 'patient_feedback', 'doctor_notes')
        }),
        ('Notifications', {
            'fields': ('sms_sent', 'email_sent', 'reminder_sent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def colored_status(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'green',
            'in_progress': 'blue',
            'completed': 'purple',
            'cancelled': 'red',
            'no_show': 'gray',
            'rescheduled': 'orange'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'


@admin.register(AppointmentReminder)
class AppointmentReminderAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'reminder_type', 'scheduled_time', 'is_sent', 'delivery_status', 'sent_at']
    list_filter = ['reminder_type', 'is_sent', 'delivery_status', 'scheduled_time']
    search_fields = ['appointment__appointment_id', 'message']
    readonly_fields = ['sent_at', 'created_at']
    date_hierarchy = 'scheduled_time'
    
    fieldsets = (
        ('Reminder Information', {
            'fields': ('appointment', 'reminder_type', 'scheduled_time', 'message')
        }),
        ('Status', {
            'fields': ('is_sent', 'delivery_status', 'sent_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )


@admin.register(OnlineAppointmentSettings)
class OnlineAppointmentSettingsAdmin(admin.ModelAdmin):
    list_display = ['advance_booking_days', 'cancellation_hours', 'payment_required', 'reminder_enabled', 'telemedicine_enabled', 'is_active']
    list_filter = ['payment_required', 'reminder_enabled', 'telemedicine_enabled', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Booking Settings', {
            'fields': ('advance_booking_days', 'cancellation_hours')
        }),
        ('Payment Settings', {
            'fields': ('payment_required', 'partial_payment_allowed', 'partial_payment_percentage')
        }),
        ('Reminder Settings', {
            'fields': ('reminder_enabled', 'reminder_1_hours', 'reminder_2_hours')
        }),
        ('Telemedicine Settings', {
            'fields': ('telemedicine_enabled', 'meeting_platform')
        }),
        ('Follow-up Settings', {
            'fields': ('auto_follow_up', 'follow_up_days')
        }),
        ('Feedback Settings', {
            'fields': ('feedback_enabled', 'feedback_required')
        }),
        ('Business Hours', {
            'fields': ('business_start_time', 'business_end_time')
        }),
        ('Emergency Settings', {
            'fields': ('emergency_booking_enabled', 'emergency_fee_multiplier')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(AppointmentFeedback)
class AppointmentFeedbackAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'patient_profile', 'doctor', 'overall_rating', 'doctor_rating', 'would_recommend', 'follow_up_needed']
    list_filter = ['overall_rating', 'doctor_rating', 'would_recommend', 'follow_up_needed']
    search_fields = ['appointment__appointment_id', 'patient_profile__user__username', 'comments']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Feedback Information', {
            'fields': ('appointment', 'patient_profile', 'doctor')
        }),
        ('Ratings', {
            'fields': ('overall_rating', 'doctor_rating', 'facility_rating', 'booking_experience_rating')
        }),
        ('Comments', {
            'fields': ('comments', 'suggestions')
        }),
        ('Recommendation', {
            'fields': ('would_recommend',)
        }),
        ('Follow-up', {
            'fields': ('follow_up_needed', 'follow_up_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )


@admin.register(WaitingList)
class WaitingListAdmin(admin.ModelAdmin):
    list_display = ['patient_profile', 'doctor', 'preferred_date', 'preferred_time', 'colored_status', 'notification_sent', 'expires_at']
    list_filter = ['status', 'notification_sent', 'flexible_date', 'flexible_time', 'preferred_date']
    search_fields = ['patient_profile__user__username', 'doctor__user__username', 'notes']
    readonly_fields = ['notification_sent_at', 'created_at', 'updated_at']
    date_hierarchy = 'preferred_date'
    
    fieldsets = (
        ('Waiting List Information', {
            'fields': ('patient_profile', 'doctor', 'preferred_date', 'preferred_time')
        }),
        ('Preferences', {
            'fields': ('flexible_date', 'flexible_time')
        }),
        ('Status', {
            'fields': ('status', 'notification_sent', 'notification_sent_at', 'expires_at')
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
            'active': 'green',
            'notified': 'blue',
            'booked': 'purple',
            'cancelled': 'red',
            'expired': 'gray'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'


@admin.register(AgendaElectronicaDisponibilidad)
class AgendaElectronicaDisponibilidadAdmin(admin.ModelAdmin):
    list_display = ['profesional', 'get_periodo', 'get_horarios', 'get_dias_semana', 'sede', 'status', 'slots_generados', 'created_at']
    list_filter = ['status', 'sede', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo', 'habilitar_agenda_tus_citas', 'habilitar_doctoralia']
    search_fields = ['profesional__user__first_name', 'profesional__user__last_name', 'profesional__user__username']
    readonly_fields = ['slots_generados', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información del Profesional', {
            'fields': ('profesional', 'created_by')
        }),
        ('Rango de Fechas', {
            'fields': ('fecha_desde', 'fecha_hasta')
        }),
        ('Horarios de Mañana', {
            'fields': ('hora_inicio_am', 'hora_fin_am'),
            'classes': ('collapse',)
        }),
        ('Horarios de Tarde', {
            'fields': ('hora_inicio_pm', 'hora_fin_pm'),
            'classes': ('collapse',)
        }),
        ('Configuración', {
            'fields': ('dividir_en', 'sede')
        }),
        ('Días de la Semana', {
            'fields': ('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo')
        }),
        ('Integraciones Externas', {
            'fields': ('habilitar_agenda_tus_citas', 'habilitar_doctoralia')
        }),
        ('Estado y Seguimiento', {
            'fields': ('status', 'slots_generados')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_periodo(self, obj):
        return f"{obj.fecha_desde.strftime('%d/%m/%Y')} - {obj.fecha_hasta.strftime('%d/%m/%Y')}"
    get_periodo.short_description = 'Período'
    
    def get_horarios(self, obj):
        horarios = []
        if obj.tiene_horario_manana():
            horarios.append(f"AM: {obj.hora_inicio_am}-{obj.hora_fin_am}")
        if obj.tiene_horario_tarde():
            horarios.append(f"PM: {obj.hora_inicio_pm}-{obj.hora_fin_pm}")
        return " | ".join(horarios)
    get_horarios.short_description = 'Horarios'
    
    def get_dias_semana(self, obj):
        dias = obj.get_dias_seleccionados()
        return ", ".join(dias[:3]) + (f" +{len(dias)-3}" if len(dias) > 3 else "")
    get_dias_semana.short_description = 'Días'
    
    actions = ['generar_slots', 'activar_disponibilidad', 'desactivar_disponibilidad']
    
    def generar_slots(self, request, queryset):
        for agenda in queryset:
            slots_creados = agenda.generar_slots_disponibilidad()
            self.message_user(request, f"Se generaron {slots_creados} slots para {agenda.profesional.user.get_full_name()}")
    generar_slots.short_description = "Regenerar slots de disponibilidad"
    
    def activar_disponibilidad(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f"{updated} disponibilidades activadas.")
    activar_disponibilidad.short_description = "Activar disponibilidades seleccionadas"
    
    def desactivar_disponibilidad(self, request, queryset):
        updated = queryset.update(status='inactive')
        self.message_user(request, f"{updated} disponibilidades desactivadas.")
    desactivar_disponibilidad.short_description = "Desactivar disponibilidades seleccionadas"


@admin.register(DisponibilidadDetalle)
class DisponibilidadDetalleAdmin(admin.ModelAdmin):
    list_display = ['agenda_disponibilidad', 'fecha_disponibilidad', 'hora_inicio', 'hora_terminacion', 'agenda_tus_citas', 'doctoralia', 'is_available']
    list_filter = ['agenda_tus_citas', 'doctoralia', 'is_available', 'is_booked', 'fecha_disponibilidad']
    search_fields = ['agenda_disponibilidad__profesional__user__first_name', 'agenda_disponibilidad__profesional__user__last_name']
    readonly_fields = ['created_at']
    date_hierarchy = 'fecha_disponibilidad'
    
    fieldsets = (
        ('Información de la Disponibilidad', {
            'fields': ('agenda_disponibilidad', 'fecha_disponibilidad')
        }),
        ('Horario', {
            'fields': ('hora_inicio', 'hora_terminacion')
        }),
        ('Integraciones', {
            'fields': ('agenda_tus_citas', 'doctoralia')
        }),
        ('Estado', {
            'fields': ('is_available', 'is_booked')
        }),
        ('Auditoría', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )


# Dashboard customization
admin.site.site_header = "HMS Online Appointment Management"
admin.site.site_title = "HMS Online Appointment Admin"
admin.site.index_title = "Online Appointment Management Administration" 