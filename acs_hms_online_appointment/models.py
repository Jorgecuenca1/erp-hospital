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
    
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='online_availability')
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    slot_duration = models.IntegerField(default=30, help_text="Duration in minutes")
    slot_type = models.CharField(max_length=20, choices=SLOT_TYPE_CHOICES, default='consultation')
    
    max_appointments = models.IntegerField(default=1)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    is_available = models.BooleanField(default=True)
    is_telemedicine = models.BooleanField(default=False)
    
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