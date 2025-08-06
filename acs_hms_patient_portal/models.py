from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser, Patient
from accounting.models import AsientoContable, CuentaContable
import uuid


class PatientPortalUser(models.Model):
    """Patient portal user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='portal_users')
    
    # Access settings
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    
    # Preferences
    preferred_language = models.CharField(max_length=10, default='en')
    preferred_timezone = models.CharField(max_length=50, default='UTC')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    
    # Security
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Patient Portal User'
        verbose_name_plural = 'Patient Portal Users'
    
    def __str__(self):
        return f"{self.user.username} - {self.patient.nombre}"


class PatientAppointment(models.Model):
    """Patient portal appointment management"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
    ]
    
    portal_user = models.ForeignKey(PatientPortalUser, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'DOCTOR'})
    
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    duration_minutes = models.IntegerField(default=30)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField()
    special_instructions = models.TextField(blank=True)
    
    # Telehealth
    is_telehealth = models.BooleanField(default=False)
    telehealth_link = models.URLField(blank=True)
    
    # Billing
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, blank=True)
    
    # Accounting integration
    asiento_contable = models.ForeignKey(AsientoContable, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
        verbose_name = 'Patient Portal Appointment'
        verbose_name_plural = 'Patient Portal Appointments'
    
    def __str__(self):
        return f"{self.portal_user.patient.full_name} - {self.doctor.full_name} - {self.appointment_date}"
    
    def save(self, *args, **kwargs):
        # Create accounting entry when appointment is paid
        if self.is_paid and not self.asiento_contable:
            self.create_accounting_entry()
        super().save(*args, **kwargs)
    
    def create_accounting_entry(self):
        """Create accounting entry for paid consultation"""
        try:
            # Get or create consultation revenue account
            revenue_account, created = CuentaContable.objects.get_or_create(
                codigo='4100',
                defaults={
                    'nombre': 'Consultation Revenue',
                    'tipo': 'ingreso',
                    'descripcion': 'Revenue from patient consultations'
                }
            )
            
            # Create accounting entry
            asiento = AsientoContable.objects.create(
                fecha=timezone.now().date(),
                concepto=f'Consultation fee - {self.portal_user.patient.nombre}',
                referencia=f'PORTAL-{self.id}',
                monto=self.consultation_fee
            )
            
            self.asiento_contable = asiento
            
        except Exception as e:
            print(f"Error creating accounting entry: {e}")


class PatientDocument(models.Model):
    """Patient document management"""
    DOCUMENT_TYPE_CHOICES = [
        ('medical_record', 'Medical Record'),
        ('prescription', 'Prescription'),
        ('lab_result', 'Lab Result'),
        ('imaging', 'Imaging'),
        ('insurance', 'Insurance'),
        ('consent', 'Consent Form'),
        ('discharge', 'Discharge Summary'),
        ('other', 'Other'),
    ]
    
    portal_user = models.ForeignKey(PatientPortalUser, on_delete=models.CASCADE, related_name='documents')
    
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    # File
    file = models.FileField(upload_to='patient_documents/')
    file_size = models.IntegerField(null=True, blank=True)
    file_type = models.CharField(max_length=50, blank=True)
    
    # Access control
    is_visible_to_patient = models.BooleanField(default=True)
    requires_verification = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    # Metadata
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Patient Document'
        verbose_name_plural = 'Patient Documents'
    
    def __str__(self):
        return f"{self.portal_user.patient.nombre} - {self.title}"


class PatientMessage(models.Model):
    """Patient-doctor messaging"""
    MESSAGE_TYPE_CHOICES = [
        ('general', 'General Inquiry'),
        ('appointment', 'Appointment Related'),
        ('prescription', 'Prescription Request'),
        ('emergency', 'Emergency'),
        ('billing', 'Billing Question'),
    ]
    
    portal_user = models.ForeignKey(PatientPortalUser, on_delete=models.CASCADE, related_name='messages')
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'user_type': 'DOCTOR'})
    
    subject = models.CharField(max_length=200)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES)
    message = models.TextField()
    
    # Status
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    
    # Response
    response = models.TextField(blank=True)
    responded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='message_responses')
    responded_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Patient Message'
        verbose_name_plural = 'Patient Messages'
    
    def __str__(self):
        return f"{self.portal_user.patient.full_name} - {self.subject}"


class PatientBilling(models.Model):
    """Patient billing and payment management"""
    BILLING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('insurance', 'Insurance'),
        ('online', 'Online Payment'),
    ]
    
    portal_user = models.ForeignKey(PatientPortalUser, on_delete=models.CASCADE, related_name='billing')
    
    # Bill details
    bill_number = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Status
    status = models.CharField(max_length=20, choices=BILLING_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    
    # Dates
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    
    # Accounting integration
    asiento_contable = models.ForeignKey(AsientoContable, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Patient Billing'
        verbose_name_plural = 'Patient Billing'
    
    def __str__(self):
        return f"{self.bill_number} - {self.portal_user.patient.nombre}"
    
    def save(self, *args, **kwargs):
        # Auto-generate bill number if not provided
        if not self.bill_number:
            self.bill_number = f"PB{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        
        # Calculate balance
        self.balance = self.total_amount - self.paid_amount
        
        # Update status based on payment
        if self.paid_amount >= self.total_amount:
            self.status = 'paid'
            if not self.paid_date:
                self.paid_date = timezone.now().date()
        elif self.paid_amount > 0:
            self.status = 'partially_paid'
        elif timezone.now().date() > self.due_date:
            self.status = 'overdue'
        
        # Create accounting entry for payments
        if self.status == 'paid' and not self.asiento_contable:
            self.create_accounting_entry()
        
        super().save(*args, **kwargs)
    
    def create_accounting_entry(self):
        """Create accounting entry for patient payment"""
        try:
            # Get or create patient revenue account
            revenue_account, created = CuentaContable.objects.get_or_create(
                codigo='4200',
                defaults={
                    'nombre': 'Patient Services Revenue',
                    'tipo': 'ingreso',
                    'descripcion': 'Revenue from patient services'
                }
            )
            
            # Create accounting entry
            asiento = AsientoContable.objects.create(
                fecha=self.paid_date or timezone.now().date(),
                concepto=f'Patient payment - {self.portal_user.patient.nombre}',
                referencia=self.bill_number,
                monto=self.paid_amount
            )
            
            self.asiento_contable = asiento
            
        except Exception as e:
            print(f"Error creating accounting entry: {e}")


class PatientFeedback(models.Model):
    """Patient feedback and ratings"""
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    portal_user = models.ForeignKey(PatientPortalUser, on_delete=models.CASCADE, related_name='feedback')
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'user_type': 'DOCTOR'})
    
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    feedback = models.TextField()
    
    # Moderation
    is_approved = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    moderator_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Patient Feedback'
        verbose_name_plural = 'Patient Feedback'
    
    def __str__(self):
        return f"{self.portal_user.patient.full_name} - {self.rating} stars"


class PatientNotification(models.Model):
    """Patient portal notifications"""
    NOTIFICATION_TYPE_CHOICES = [
        ('appointment', 'Appointment Reminder'),
        ('message', 'New Message'),
        ('billing', 'Billing Notice'),
        ('result', 'Test Result Available'),
        ('system', 'System Notification'),
    ]
    
    portal_user = models.ForeignKey(PatientPortalUser, on_delete=models.CASCADE, related_name='notifications')
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Status
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    
    # Delivery
    send_email = models.BooleanField(default=True)
    send_sms = models.BooleanField(default=False)
    send_push = models.BooleanField(default=True)
    
    # Scheduling
    send_at = models.DateTimeField(default=timezone.now)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Patient Notification'
        verbose_name_plural = 'Patient Notifications'
    
    def __str__(self):
        return f"{self.portal_user.patient.nombre} - {self.title}" 