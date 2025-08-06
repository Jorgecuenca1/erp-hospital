from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser
from accounting.models import AsientoContable, CuentaContable
import uuid


class CertificationBody(models.Model):
    """Certification issuing bodies"""
    name = models.CharField(max_length=200)
    acronym = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100)
    
    # Contact information
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Accreditation
    is_accredited = models.BooleanField(default=True)
    accreditation_number = models.CharField(max_length=100, blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Certification Body'
        verbose_name_plural = 'Certification Bodies'
    
    def __str__(self):
        return f"{self.name} ({self.acronym})" if self.acronym else self.name


class CertificationType(models.Model):
    """Types of certifications"""
    CATEGORY_CHOICES = [
        ('medical', 'Medical License'),
        ('specialty', 'Specialty Certification'),
        ('continuing_education', 'Continuing Education'),
        ('safety', 'Safety Certification'),
        ('quality', 'Quality Certification'),
        ('technology', 'Technology Certification'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    
    # Certification body
    certification_body = models.ForeignKey(
        CertificationBody, 
        on_delete=models.CASCADE, 
        related_name='certification_types'
    )
    
    # Validity and renewal
    validity_period_months = models.IntegerField(
        default=12,
        help_text="Validity period in months"
    )
    renewal_required = models.BooleanField(default=True)
    
    # Requirements
    continuing_education_hours = models.IntegerField(
        default=0,
        help_text="Required CE hours for renewal"
    )
    
    # Settings
    is_active = models.BooleanField(default=True)
    is_mandatory = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Certification Type'
        verbose_name_plural = 'Certification Types'
    
    def __str__(self):
        return f"{self.name} - {self.certification_body.name}"


class DoctorCertification(models.Model):
    """Doctor certifications"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
        ('revoked', 'Revoked'),
        ('pending_renewal', 'Pending Renewal'),
    ]
    
    # Doctor and certification type
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='certifications', limit_choices_to={'user_type': 'DOCTOR'})
    certification_type = models.ForeignKey(
        CertificationType, 
        on_delete=models.CASCADE, 
        related_name='doctor_certifications'
    )
    
    # Certification details
    certificate_number = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Files
    certificate_file = models.FileField(upload_to='certifications/', null=True, blank=True)
    
    # Renewal information
    last_renewal_date = models.DateField(null=True, blank=True)
    next_renewal_date = models.DateField(null=True, blank=True)
    
    # Continuing education
    ce_hours_completed = models.IntegerField(default=0)
    ce_hours_required = models.IntegerField(default=0)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='verified_certifications'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-issue_date']
        unique_together = ['doctor', 'certification_type', 'certificate_number']
        verbose_name = 'Doctor Certification'
        verbose_name_plural = 'Doctor Certifications'
    
    def __str__(self):
        return f"{self.doctor.nombre} - {self.certification_type.name}"
    
    @property
    def is_expired(self):
        """Check if certification is expired"""
        return timezone.now().date() > self.expiry_date
    
    @property
    def days_until_expiry(self):
        """Days until expiry"""
        delta = self.expiry_date - timezone.now().date()
        return delta.days
    
    @property
    def is_expiring_soon(self):
        """Check if certification is expiring soon (within 30 days)"""
        return self.days_until_expiry <= 30
    
    def renew(self, new_expiry_date, renewal_fee=0):
        """Renew certification"""
        self.last_renewal_date = timezone.now().date()
        self.expiry_date = new_expiry_date
        self.next_renewal_date = new_expiry_date
        self.status = 'active'
        self.save()
        
        # Create renewal record
        CertificationRenewal.objects.create(
            doctor_certification=self,
            renewal_date=timezone.now().date(),
            new_expiry_date=new_expiry_date,
            renewal_fee=renewal_fee
        )


class CertificationRenewal(models.Model):
    """Certification renewal records"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    # Reference
    renewal_id = models.CharField(max_length=100, unique=True, editable=False)
    
    # Certification
    doctor_certification = models.ForeignKey(
        DoctorCertification, 
        on_delete=models.CASCADE, 
        related_name='renewals'
    )
    
    # Renewal details
    renewal_date = models.DateField()
    new_expiry_date = models.DateField()
    renewal_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Approval
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_renewals'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Payment
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Files
    renewal_application = models.FileField(upload_to='renewals/', null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certification_renewals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Certification Renewal'
        verbose_name_plural = 'Certification Renewals'
    
    def __str__(self):
        return f"{self.renewal_id} - {self.doctor_certification}"
    
    def save(self, *args, **kwargs):
        if not self.renewal_id:
            self.renewal_id = f"REN{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        
        super().save(*args, **kwargs)


class ContinuingEducation(models.Model):
    """Continuing education records"""
    EDUCATION_TYPE_CHOICES = [
        ('course', 'Course'),
        ('workshop', 'Workshop'),
        ('conference', 'Conference'),
        ('seminar', 'Seminar'),
        ('webinar', 'Webinar'),
        ('other', 'Other'),
    ]
    
    # Doctor
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='continuing_education', limit_choices_to={'user_type': 'DOCTOR'})
    
    # Education details
    title = models.CharField(max_length=200)
    education_type = models.CharField(max_length=20, choices=EDUCATION_TYPE_CHOICES)
    provider = models.CharField(max_length=200)
    
    # Credits
    credit_hours = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    
    # Status
    is_completed = models.BooleanField(default=False)
    
    # Certification
    certificate_file = models.FileField(upload_to='continuing_education/', null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Continuing Education'
        verbose_name_plural = 'Continuing Education'
    
    def __str__(self):
        return f"{self.doctor.nombre} - {self.title}"


class CertificationAudit(models.Model):
    """Certification audit log"""
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('verified', 'Verified'),
        ('renewed', 'Renewed'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
        ('revoked', 'Revoked'),
    ]
    
    # Certification
    doctor_certification = models.ForeignKey(
        DoctorCertification, 
        on_delete=models.CASCADE, 
        related_name='audit_logs'
    )
    
    # Action
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    
    # User
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Metadata
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Certification Audit'
        verbose_name_plural = 'Certification Audits'
    
    def __str__(self):
        return f"{self.doctor_certification} - {self.action}"


class CertificationNotification(models.Model):
    """Certification notifications"""
    NOTIFICATION_TYPE_CHOICES = [
        ('expiry_warning', 'Expiry Warning'),
        ('expired', 'Expired'),
        ('renewal_required', 'Renewal Required'),
        ('verification_required', 'Verification Required'),
    ]
    
    # Doctor and certification
    doctor_certification = models.ForeignKey(
        DoctorCertification, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    
    # Notification details
    notification_type = models.CharField(max_length=25, choices=NOTIFICATION_TYPE_CHOICES)
    message = models.TextField()
    
    # Status
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Certification Notification'
        verbose_name_plural = 'Certification Notifications'
    
    def __str__(self):
        return f"{self.doctor_certification} - {self.notification_type}"


class CertificationStatistics(models.Model):
    """Certification statistics"""
    date = models.DateField(unique=True)
    
    # Counts
    total_certifications = models.IntegerField(default=0)
    active_certifications = models.IntegerField(default=0)
    expired_certifications = models.IntegerField(default=0)
    expiring_soon = models.IntegerField(default=0)
    
    # By category
    medical_licenses = models.IntegerField(default=0)
    specialty_certifications = models.IntegerField(default=0)
    continuing_education = models.IntegerField(default=0)
    
    # Renewals
    renewals_processed = models.IntegerField(default=0)
    renewals_pending = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Certification Statistics'
        verbose_name_plural = 'Certification Statistics'
    
    def __str__(self):
        return f"Certification Statistics - {self.date}" 