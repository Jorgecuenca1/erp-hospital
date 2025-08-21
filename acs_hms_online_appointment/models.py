from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser, Patient, Appointment
import uuid


class OnlineAppointmentProfile(models.Model):
    """Patient profile for online appointment booking"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='online_profile')
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, null=True, blank=True)
    
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_phone = models.CharField(max_length=20)
    
    medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    
    profile_image = models.ImageField(upload_to='patient_profiles/', null=True, blank=True)
    
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True)
    
    preferred_language = models.CharField(max_length=20, choices=[
        ('english', 'English'),
        ('hindi', 'Hindi'),
        ('spanish', 'Spanish'),
        ('french', 'French'),
        ('other', 'Other')
    ], default='english')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Online Appointment Profile'
        verbose_name_plural = 'Online Appointment Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone_number}"


class DoctorAvailability(models.Model):
    """Doctor availability slots for online booking"""
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    SLOT_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('emergency', 'Emergency'),
        ('telemedicine', 'Telemedicine'),
    ]
    
    SEDE_CHOICES = [
        ('PRINCIPAL', 'PRINCIPAL'),
        ('SUCURSAL_1', 'SUCURSAL 1'),
        ('SUCURSAL_2', 'SUCURSAL 2'),
        ('CONSULTORIO_EXTERNO', 'CONSULTORIO EXTERNO'),
    ]
    
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='online_availability')
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    slot_duration = models.IntegerField(default=30, help_text="Duration in minutes")
    slot_type = models.CharField(max_length=20, choices=SLOT_TYPE_CHOICES, default='consultation')
    
    max_appointments = models.IntegerField(default=1)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Información de sede
    sede = models.CharField(max_length=50, choices=SEDE_CHOICES, default='PRINCIPAL')
    
    is_available = models.BooleanField(default=True)
    is_telemedicine = models.BooleanField(default=False)
    
    # Integraciones externas
    habilitar_agenda_tus_citas = models.BooleanField(default=False, help_text="Habilitar en plataforma Agenda tus citas")
    habilitar_doctoralia = models.BooleanField(default=False, help_text="Habilitar en plataforma Doctoralia")
    
    special_instructions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
        verbose_name = 'Doctor Availability'
        verbose_name_plural = 'Doctor Availability'
    
    def __str__(self):
        return f"{self.doctor.user.get_full_name()} - {self.get_day_of_week_display()} ({self.start_time}-{self.end_time})"


class OnlineAppointmentSlot(models.Model):
    """Individual appointment slots generated from doctor availability"""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('blocked', 'Blocked'),
        ('cancelled', 'Cancelled'),
    ]
    
    availability = models.ForeignKey(DoctorAvailability, on_delete=models.CASCADE, related_name='slots')
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='appointment_slots')
    
    slot_date = models.DateField()
    slot_time = models.TimeField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Booking details
    booked_by = models.ForeignKey(OnlineAppointmentProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='booked_slots')
    booking_time = models.DateTimeField(null=True, blank=True)
    
    # Cancellation details
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cancelled_slots')
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['slot_date', 'slot_time']
        unique_together = ['doctor', 'slot_date', 'slot_time']
        verbose_name = 'Online Appointment Slot'
        verbose_name_plural = 'Online Appointment Slots'
    
    def __str__(self):
        return f"{self.doctor.user.get_full_name()} - {self.slot_date} {self.slot_time}"
    
    @property
    def is_past(self):
        return timezone.now().date() > self.slot_date or (
            timezone.now().date() == self.slot_date and 
            timezone.now().time() > self.slot_time
        )


class OnlineAppointment(models.Model):
    """Online appointment bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]
    
    APPOINTMENT_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('emergency', 'Emergency'),
        ('telemedicine', 'Telemedicine'),
        ('second_opinion', 'Second Opinion'),
    ]
    
    appointment_id = models.CharField(max_length=20, unique=True, blank=True)
    slot = models.OneToOneField(OnlineAppointmentSlot, on_delete=models.CASCADE, related_name='appointment')
    patient_profile = models.ForeignKey(OnlineAppointmentProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='online_appointments')
    
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='consultation')
    
    # Scheduling details
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    estimated_duration = models.IntegerField(default=30, help_text="Duration in minutes")
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Patient details
    chief_complaint = models.TextField()
    symptoms = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    
    # Payment details
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    
    # Appointment details
    is_telemedicine = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True)
    meeting_id = models.CharField(max_length=100, blank=True)
    
    # Follow-up details
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    follow_up_notes = models.TextField(blank=True)
    
    # Cancellation details
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cancelled_appointments')
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    refund_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Feedback
    patient_rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    patient_feedback = models.TextField(blank=True)
    doctor_notes = models.TextField(blank=True)
    
    # Notifications
    sms_sent = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    reminder_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
        verbose_name = 'Online Appointment'
        verbose_name_plural = 'Online Appointments'
    
    def save(self, *args, **kwargs):
        if not self.appointment_id:
            self.appointment_id = f"OA{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.appointment_id} - {self.patient_profile.user.get_full_name()} - {self.doctor.user.get_full_name()}"
    
    @property
    def is_upcoming(self):
        return timezone.now().date() < self.appointment_date or (
            timezone.now().date() == self.appointment_date and 
            timezone.now().time() < self.appointment_time
        )


class AppointmentReminder(models.Model):
    """Appointment reminders configuration"""
    REMINDER_TYPE_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('push_notification', 'Push Notification'),
    ]
    
    appointment = models.ForeignKey(OnlineAppointment, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE_CHOICES)
    
    scheduled_time = models.DateTimeField()
    sent_at = models.DateTimeField(null=True, blank=True)
    
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    
    delivery_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ], default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['scheduled_time']
        verbose_name = 'Appointment Reminder'
        verbose_name_plural = 'Appointment Reminders'
    
    def __str__(self):
        return f"{self.appointment.appointment_id} - {self.get_reminder_type_display()}"


class OnlineAppointmentSettings(models.Model):
    """System settings for online appointments"""
    # Booking settings
    advance_booking_days = models.IntegerField(default=30, help_text="How many days in advance can patients book")
    cancellation_hours = models.IntegerField(default=24, help_text="Minimum hours before appointment for cancellation")
    
    # Payment settings
    payment_required = models.BooleanField(default=True)
    partial_payment_allowed = models.BooleanField(default=True)
    partial_payment_percentage = models.IntegerField(default=50, validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    # Reminder settings
    reminder_enabled = models.BooleanField(default=True)
    reminder_1_hours = models.IntegerField(default=24, help_text="First reminder hours before appointment")
    reminder_2_hours = models.IntegerField(default=2, help_text="Second reminder hours before appointment")
    
    # Telemedicine settings
    telemedicine_enabled = models.BooleanField(default=True)
    meeting_platform = models.CharField(max_length=50, default='zoom')
    
    # Follow-up settings
    auto_follow_up = models.BooleanField(default=True)
    follow_up_days = models.IntegerField(default=7, help_text="Days after appointment for follow-up")
    
    # Feedback settings
    feedback_enabled = models.BooleanField(default=True)
    feedback_required = models.BooleanField(default=False)
    
    # Business hours
    business_start_time = models.TimeField(default='09:00')
    business_end_time = models.TimeField(default='18:00')
    
    # Emergency settings
    emergency_booking_enabled = models.BooleanField(default=True)
    emergency_fee_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.5)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Online Appointment Settings'
        verbose_name_plural = 'Online Appointment Settings'
    
    def __str__(self):
        return f"Online Appointment Settings - {self.created_at.date()}"


class AppointmentFeedback(models.Model):
    """Patient feedback for appointments"""
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    ]
    
    appointment = models.OneToOneField(OnlineAppointment, on_delete=models.CASCADE, related_name='feedback')
    patient_profile = models.ForeignKey(OnlineAppointmentProfile, on_delete=models.CASCADE, related_name='feedbacks')
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='appointment_feedbacks')
    
    # Ratings
    overall_rating = models.IntegerField(choices=RATING_CHOICES)
    doctor_rating = models.IntegerField(choices=RATING_CHOICES)
    facility_rating = models.IntegerField(choices=RATING_CHOICES)
    booking_experience_rating = models.IntegerField(choices=RATING_CHOICES)
    
    # Comments
    comments = models.TextField(blank=True)
    suggestions = models.TextField(blank=True)
    
    # Recommendation
    would_recommend = models.BooleanField(default=True)
    
    # Follow-up
    follow_up_needed = models.BooleanField(default=False)
    follow_up_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Appointment Feedback'
        verbose_name_plural = 'Appointment Feedbacks'
    
    def __str__(self):
        return f"{self.appointment.appointment_id} - {self.overall_rating} stars"


class WaitingList(models.Model):
    """Waiting list for fully booked slots"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('notified', 'Notified'),
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    patient_profile = models.ForeignKey(OnlineAppointmentProfile, on_delete=models.CASCADE, related_name='waiting_lists')
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='waiting_lists')
    
    preferred_date = models.DateField()
    preferred_time = models.TimeField(null=True, blank=True)
    
    flexible_date = models.BooleanField(default=True)
    flexible_time = models.BooleanField(default=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    notification_sent = models.BooleanField(default=False)
    notification_sent_at = models.DateTimeField(null=True, blank=True)
    
    expires_at = models.DateTimeField()
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Waiting List'
        verbose_name_plural = 'Waiting Lists'
    
    def __str__(self):
        return f"{self.patient_profile.user.get_full_name()} - {self.doctor.user.get_full_name()}"


class AgendaElectronicaDisponibilidad(models.Model):
    """Modelo para gestionar la disponibilidad creada desde agenda electrónica"""
    
    STATUS_CHOICES = [
        ('active', 'Activa'),
        ('inactive', 'Inactiva'),
        ('expired', 'Expirada'),
    ]
    
    # Información del profesional
    profesional = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='agenda_disponibilidades')
    
    # Rango de fechas
    fecha_desde = models.DateField(help_text="Fecha de inicio de la disponibilidad")
    fecha_hasta = models.DateField(help_text="Fecha de fin de la disponibilidad")
    
    # Horarios de mañana
    hora_inicio_am = models.TimeField(null=True, blank=True, help_text="Hora de inicio turno mañana")
    hora_fin_am = models.TimeField(null=True, blank=True, help_text="Hora de fin turno mañana")
    
    # Horarios de tarde
    hora_inicio_pm = models.TimeField(null=True, blank=True, help_text="Hora de inicio turno tarde")
    hora_fin_pm = models.TimeField(null=True, blank=True, help_text="Hora de fin turno tarde")
    
    # Configuración de citas
    dividir_en = models.IntegerField(default=30, help_text="Duración de cada cita en minutos")
    
    # Sede
    sede = models.CharField(
        max_length=50, 
        choices=DoctorAvailability.SEDE_CHOICES, 
        default='PRINCIPAL',
        help_text="Sede donde se creará la disponibilidad"
    )
    
    # Días de la semana
    lunes = models.BooleanField(default=False)
    martes = models.BooleanField(default=False)
    miercoles = models.BooleanField(default=False)
    jueves = models.BooleanField(default=False)
    viernes = models.BooleanField(default=False)
    sabado = models.BooleanField(default=False)
    domingo = models.BooleanField(default=False)
    
    # Integraciones externas
    habilitar_agenda_tus_citas = models.BooleanField(default=False)
    habilitar_doctoralia = models.BooleanField(default=False)
    
    # Estado y seguimiento
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    slots_generados = models.IntegerField(default=0, help_text="Cantidad de slots generados")
    
    # Auditoría
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='agenda_creadas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Agenda Electrónica Disponibilidad'
        verbose_name_plural = 'Agenda Electrónica Disponibilidades'
    
    def __str__(self):
        return f"{self.profesional.user.get_full_name()} - {self.fecha_desde} a {self.fecha_hasta} ({self.sede})"
    
    def get_dias_seleccionados(self):
        """Retorna los días de la semana seleccionados como lista"""
        dias = []
        if self.lunes: dias.append('Lunes')
        if self.martes: dias.append('Martes')
        if self.miercoles: dias.append('Miércoles')
        if self.jueves: dias.append('Jueves')
        if self.viernes: dias.append('Viernes')
        if self.sabado: dias.append('Sábado')
        if self.domingo: dias.append('Domingo')
        return dias
    
    def get_dias_seleccionados_en(self):
        """Retorna los días de la semana seleccionados en inglés para DoctorAvailability"""
        day_mapping = {
            'lunes': 'monday',
            'martes': 'tuesday',
            'miercoles': 'wednesday',
            'jueves': 'thursday',
            'viernes': 'friday',
            'sabado': 'saturday',
            'domingo': 'sunday',
        }
        
        dias_en = []
        if self.lunes: dias_en.append('monday')
        if self.martes: dias_en.append('tuesday')
        if self.miercoles: dias_en.append('wednesday')
        if self.jueves: dias_en.append('thursday')
        if self.viernes: dias_en.append('friday')
        if self.sabado: dias_en.append('saturday')
        if self.domingo: dias_en.append('sunday')
        
        return dias_en
    
    def tiene_horario_manana(self):
        """Verifica si tiene horario de mañana configurado"""
        return self.hora_inicio_am and self.hora_fin_am
    
    def tiene_horario_tarde(self):
        """Verifica si tiene horario de tarde configurado"""
        return self.hora_inicio_pm and self.hora_fin_pm
    
    def generar_slots_disponibilidad(self):
        """Genera los slots de disponibilidad basados en la configuración"""
        from datetime import datetime, timedelta
        
        slots_creados = 0
        current_date = self.fecha_desde
        
        # Mapeo de días de la semana (0=lunes, 6=domingo)
        weekday_mapping = {
            0: self.lunes,    # Monday
            1: self.martes,   # Tuesday
            2: self.miercoles, # Wednesday
            3: self.jueves,   # Thursday
            4: self.viernes,  # Friday
            5: self.sabado,   # Saturday
            6: self.domingo,  # Sunday
        }
        
        day_choices_mapping = {
            0: 'monday',
            1: 'tuesday',
            2: 'wednesday',
            3: 'thursday',
            4: 'friday',
            5: 'saturday',
            6: 'sunday',
        }
        
        while current_date <= self.fecha_hasta:
            weekday = current_date.weekday()
            
            # Verificar si este día de la semana está seleccionado
            if weekday_mapping.get(weekday, False):
                day_choice = day_choices_mapping[weekday]
                
                # Crear disponibilidad para horario de mañana
                if self.tiene_horario_manana():
                    availability_am, created = DoctorAvailability.objects.get_or_create(
                        doctor=self.profesional,
                        day_of_week=day_choice,
                        start_time=self.hora_inicio_am,
                        end_time=self.hora_fin_am,
                        defaults={
                            'slot_duration': self.dividir_en,
                            'sede': self.sede,
                            'habilitar_agenda_tus_citas': self.habilitar_agenda_tus_citas,
                            'habilitar_doctoralia': self.habilitar_doctoralia,
                            'slot_type': 'consultation',
                        }
                    )
                    if created:
                        slots_creados += 1
                
                # Crear disponibilidad para horario de tarde
                if self.tiene_horario_tarde():
                    availability_pm, created = DoctorAvailability.objects.get_or_create(
                        doctor=self.profesional,
                        day_of_week=day_choice,
                        start_time=self.hora_inicio_pm,
                        end_time=self.hora_fin_pm,
                        defaults={
                            'slot_duration': self.dividir_en,
                            'sede': self.sede,
                            'habilitar_agenda_tus_citas': self.habilitar_agenda_tus_citas,
                            'habilitar_doctoralia': self.habilitar_doctoralia,
                            'slot_type': 'consultation',
                        }
                    )
                    if created:
                        slots_creados += 1
            
            current_date += timedelta(days=1)
        
        # Actualizar contador de slots generados
        self.slots_generados = slots_creados
        self.save()
        
        return slots_creados


class DisponibilidadDetalle(models.Model):
    """Detalle de la disponibilidad generada para mostrar en tabla"""
    
    agenda_disponibilidad = models.ForeignKey(
        AgendaElectronicaDisponibilidad, 
        on_delete=models.CASCADE, 
        related_name='detalles'
    )
    
    fecha_disponibilidad = models.DateField()
    hora_inicio = models.TimeField()
    hora_terminacion = models.TimeField()
    
    # Integraciones
    agenda_tus_citas = models.BooleanField(default=False)
    doctoralia = models.BooleanField(default=False)
    
    # Estado del slot
    is_available = models.BooleanField(default=True)
    is_booked = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['fecha_disponibilidad', 'hora_inicio']
        verbose_name = 'Detalle de Disponibilidad'
        verbose_name_plural = 'Detalles de Disponibilidad'
    
    def __str__(self):
        return f"{self.fecha_disponibilidad} - {self.hora_inicio} a {self.hora_terminacion}" 