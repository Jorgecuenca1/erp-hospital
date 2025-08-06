from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser, Patient
from accounting.models import AsientoContable, CuentaContable
import uuid
import json


class ConsentFormTemplate(models.Model):
    """Template for consent forms"""
    FORM_TYPE_CHOICES = [
        ('general', 'General Medical Consent'),
        ('surgery', 'Surgical Consent'),
        ('anesthesia', 'Anesthesia Consent'),
        ('blood_transfusion', 'Blood Transfusion Consent'),
        ('dental', 'Dental Procedure Consent'),
        ('pediatric', 'Pediatric Consent'),
        ('radiology', 'Radiology Consent'),
        ('telemedicine', 'Telemedicine Consent'),
        ('research', 'Research Participation Consent'),
        ('privacy', 'Privacy and Data Consent'),
        ('custom', 'Custom Consent Form'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
    ]
    
    title = models.CharField(max_length=200)
    form_type = models.CharField(max_length=20, choices=FORM_TYPE_CHOICES)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    
    # Content
    description = models.TextField()
    content = models.TextField(help_text="HTML content of the consent form")
    
    # Form fields configuration (JSON)
    form_fields = models.JSONField(
        default=dict,
        help_text="JSON configuration of form fields"
    )
    
    # Settings
    is_active = models.BooleanField(default=True)
    requires_witness = models.BooleanField(default=False)
    requires_guardian = models.BooleanField(default=False)
    
    # Expiration
    expires_after_days = models.IntegerField(
        null=True, 
        blank=True,
        help_text="Days after which consent expires (null = no expiration)"
    )
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consent_templates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['form_type', 'title']
        verbose_name = 'Consent Form Template'
        verbose_name_plural = 'Consent Form Templates'
    
    def __str__(self):
        return f"{self.title} ({self.get_form_type_display()})"


class ConsentForm(models.Model):
    """Individual consent form instance"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Signature'),
        ('signed', 'Signed'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Reference
    consent_id = models.CharField(max_length=100, unique=True, editable=False)
    template = models.ForeignKey(ConsentFormTemplate, on_delete=models.CASCADE, related_name='forms')
    
    # Patient information
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consent_forms')
    guardian = models.ForeignKey(
        Patient, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='guardian_consent_forms',
        help_text="Guardian for minor patients"
    )
    
    # Medical context
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='consent_forms', limit_choices_to={'user_type': 'DOCTOR'})
    procedure_name = models.CharField(max_length=200, blank=True)
    procedure_date = models.DateField(null=True, blank=True)
    
    # Form data
    form_data = models.JSONField(
        default=dict,
        help_text="Patient responses to form fields"
    )
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Signatures
    patient_signature = models.TextField(blank=True, help_text="Digital signature data")
    patient_signed_at = models.DateTimeField(null=True, blank=True)
    patient_ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    guardian_signature = models.TextField(blank=True, help_text="Guardian digital signature")
    guardian_signed_at = models.DateTimeField(null=True, blank=True)
    guardian_ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Witness
    witness_name = models.CharField(max_length=200, blank=True)
    witness_signature = models.TextField(blank=True)
    witness_signed_at = models.DateTimeField(null=True, blank=True)
    witness_relationship = models.CharField(max_length=100, blank=True)
    
    # Doctor signature
    doctor_signature = models.TextField(blank=True)
    doctor_signed_at = models.DateTimeField(null=True, blank=True)
    
    # Expiration
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Revocation
    revoked_at = models.DateTimeField(null=True, blank=True)
    revocation_reason = models.TextField(blank=True)
    revoked_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='revoked_consents'
    )
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consent_forms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Consent Form'
        verbose_name_plural = 'Consent Forms'
    
    def __str__(self):
        return f"{self.consent_id} - {self.patient.nombre} - {self.template.title}"
    
    def save(self, *args, **kwargs):
        if not self.consent_id:
            self.consent_id = f"CONSENT{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        
        # Set expiration date if template has expiration
        if self.template.expires_after_days and not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=self.template.expires_after_days)
        
        super().save(*args, **kwargs)
    
    @property
    def is_valid(self):
        """Check if consent is valid"""
        if self.status != 'signed':
            return False
        
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        
        return True
    
    @property
    def is_expired(self):
        """Check if consent is expired"""
        if self.expires_at and timezone.now() > self.expires_at:
            return True
        return False
    
    def sign_patient(self, signature_data, ip_address=None):
        """Sign consent form as patient"""
        self.patient_signature = signature_data
        self.patient_signed_at = timezone.now()
        self.patient_ip_address = ip_address
        
        # Check if all required signatures are present
        self._check_complete_signatures()
        self.save()
    
    def sign_guardian(self, signature_data, ip_address=None):
        """Sign consent form as guardian"""
        self.guardian_signature = signature_data
        self.guardian_signed_at = timezone.now()
        self.guardian_ip_address = ip_address
        
        self._check_complete_signatures()
        self.save()
    
    def sign_witness(self, signature_data, witness_name, relationship):
        """Sign consent form as witness"""
        self.witness_signature = signature_data
        self.witness_signed_at = timezone.now()
        self.witness_name = witness_name
        self.witness_relationship = relationship
        
        self._check_complete_signatures()
        self.save()
    
    def sign_doctor(self, signature_data):
        """Sign consent form as doctor"""
        self.doctor_signature = signature_data
        self.doctor_signed_at = timezone.now()
        
        self._check_complete_signatures()
        self.save()
    
    def _check_complete_signatures(self):
        """Check if all required signatures are present"""
        has_patient_signature = bool(self.patient_signature)
        has_guardian_signature = bool(self.guardian_signature) if self.template.requires_guardian else True
        has_witness_signature = bool(self.witness_signature) if self.template.requires_witness else True
        has_doctor_signature = bool(self.doctor_signature)
        
        if has_patient_signature and has_guardian_signature and has_witness_signature and has_doctor_signature:
            self.status = 'signed'
    
    def revoke(self, reason, revoked_by):
        """Revoke consent form"""
        self.status = 'revoked'
        self.revoked_at = timezone.now()
        self.revocation_reason = reason
        self.revoked_by = revoked_by
        self.save()


class ConsentFormAudit(models.Model):
    """Audit trail for consent forms"""
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('viewed', 'Viewed'),
        ('signed', 'Signed'),
        ('revoked', 'Revoked'),
        ('expired', 'Expired'),
        ('printed', 'Printed'),
        ('emailed', 'Emailed'),
    ]
    
    consent_form = models.ForeignKey(ConsentForm, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    
    # User information
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Additional data
    details = models.JSONField(default=dict, blank=True)
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Consent Form Audit'
        verbose_name_plural = 'Consent Form Audits'
    
    def __str__(self):
        return f"{self.consent_form.consent_id} - {self.action} - {self.timestamp}"


class ConsentFormNotification(models.Model):
    """Notifications for consent forms"""
    NOTIFICATION_TYPE_CHOICES = [
        ('signature_required', 'Signature Required'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
        ('completed', 'Completed'),
    ]
    
    consent_form = models.ForeignKey(ConsentForm, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    
    # Recipients
    recipient_email = models.EmailField()
    recipient_name = models.CharField(max_length=200)
    
    # Message
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Status
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Retry logic
    retry_count = models.IntegerField(default=0)
    next_retry_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Consent Form Notification'
        verbose_name_plural = 'Consent Form Notifications'
    
    def __str__(self):
        return f"{self.consent_form.consent_id} - {self.notification_type} - {self.recipient_email}"


class ConsentFormDocument(models.Model):
    """Generated PDF documents for consent forms"""
    consent_form = models.ForeignKey(ConsentForm, on_delete=models.CASCADE, related_name='documents')
    
    # Document info
    document_type = models.CharField(
        max_length=20,
        choices=[
            ('original', 'Original Form'),
            ('signed', 'Signed Form'),
            ('summary', 'Summary'),
        ],
        default='original'
    )
    
    # File
    file = models.FileField(upload_to='consent_forms/')
    file_size = models.IntegerField(null=True, blank=True)
    
    # Generation info
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-generated_at']
        verbose_name = 'Consent Form Document'
        verbose_name_plural = 'Consent Form Documents'
    
    def __str__(self):
        return f"{self.consent_form.consent_id} - {self.document_type}"


class ConsentFormConfiguration(models.Model):
    """System configuration for consent forms"""
    # Digital signature settings
    signature_required = models.BooleanField(default=True)
    allow_electronic_signature = models.BooleanField(default=True)
    require_timestamp = models.BooleanField(default=True)
    
    # Email settings
    auto_send_notifications = models.BooleanField(default=True)
    reminder_days_before_expiry = models.IntegerField(default=7)
    
    # Security settings
    require_ip_logging = models.BooleanField(default=True)
    require_user_agent_logging = models.BooleanField(default=True)
    
    # PDF settings
    auto_generate_pdf = models.BooleanField(default=True)
    include_signatures_in_pdf = models.BooleanField(default=True)
    
    # Accounting integration
    track_consent_costs = models.BooleanField(default=False)
    consent_processing_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )
    
    # Metadata
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Consent Form Configuration'
        verbose_name_plural = 'Consent Form Configurations'
    
    def __str__(self):
        return f"Consent Form Configuration - Updated {self.updated_at}"
    
    def save(self, *args, **kwargs):
        # Ensure only one configuration instance exists
        if not self.pk and ConsentFormConfiguration.objects.exists():
            raise ValueError("Only one configuration instance is allowed")
        super().save(*args, **kwargs)


class ConsentFormStatistics(models.Model):
    """Statistics for consent forms"""
    date = models.DateField(unique=True)
    
    # Counts
    total_forms = models.IntegerField(default=0)
    signed_forms = models.IntegerField(default=0)
    pending_forms = models.IntegerField(default=0)
    expired_forms = models.IntegerField(default=0)
    revoked_forms = models.IntegerField(default=0)
    
    # Performance metrics
    avg_time_to_sign = models.DurationField(null=True, blank=True)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Revenue (if tracking costs)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Consent Form Statistics'
        verbose_name_plural = 'Consent Form Statistics'
    
    def __str__(self):
        return f"Consent Statistics - {self.date}" 