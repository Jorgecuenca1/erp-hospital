from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser, Patient, Appointment
import uuid


class InsuranceProvider(models.Model):
    """Insurance companies and providers"""
    PROVIDER_TYPE_CHOICES = [
        ('government', 'Government'),
        ('private', 'Private'),
        ('corporate', 'Corporate'),
        ('individual', 'Individual'),
        ('group', 'Group'),
    ]
    
    provider_id = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=200)
    provider_type = models.CharField(max_length=20, choices=PROVIDER_TYPE_CHOICES, default='private')
    
    # Contact information
    contact_person = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    
    # Address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='India')
    
    # Business details
    license_number = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    
    # Network information
    network_type = models.CharField(max_length=20, choices=[
        ('in_network', 'In Network'),
        ('out_network', 'Out of Network'),
        ('both', 'Both'),
    ], default='in_network')
    
    # Payment details
    payment_terms = models.CharField(max_length=100, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    contract_start = models.DateField(null=True, blank=True)
    contract_end = models.DateField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Insurance Provider'
        verbose_name_plural = 'Insurance Providers'
    
    def save(self, *args, **kwargs):
        if not self.provider_id:
            self.provider_id = f"IP{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.provider_id})"
    
    @property
    def is_contract_active(self):
        today = timezone.now().date()
        if self.contract_start and self.contract_end:
            return self.contract_start <= today <= self.contract_end
        return True


class InsurancePlan(models.Model):
    """Insurance plans offered by providers"""
    PLAN_TYPE_CHOICES = [
        ('hmo', 'Health Maintenance Organization'),
        ('ppo', 'Preferred Provider Organization'),
        ('pos', 'Point of Service'),
        ('hdhp', 'High Deductible Health Plan'),
        ('catastrophic', 'Catastrophic'),
        ('medicaid', 'Medicaid'),
        ('medicare', 'Medicare'),
        ('other', 'Other'),
    ]
    
    COVERAGE_LEVEL_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]
    
    plan_id = models.CharField(max_length=20, unique=True, blank=True)
    provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE, related_name='plans')
    
    plan_name = models.CharField(max_length=200)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES, default='ppo')
    coverage_level = models.CharField(max_length=20, choices=COVERAGE_LEVEL_CHOICES, default='silver')
    
    # Coverage details
    annual_deductible = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    out_of_pocket_max = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Coverage percentages
    inpatient_coverage = models.DecimalField(max_digits=5, decimal_places=2, default=80.00)
    outpatient_coverage = models.DecimalField(max_digits=5, decimal_places=2, default=80.00)
    emergency_coverage = models.DecimalField(max_digits=5, decimal_places=2, default=80.00)
    prescription_coverage = models.DecimalField(max_digits=5, decimal_places=2, default=80.00)
    
    # Co-pays
    primary_care_copay = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    specialist_copay = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    emergency_copay = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Benefits
    maternity_coverage = models.BooleanField(default=True)
    mental_health_coverage = models.BooleanField(default=True)
    dental_coverage = models.BooleanField(default=False)
    vision_coverage = models.BooleanField(default=False)
    
    # Network
    network_name = models.CharField(max_length=200, blank=True)
    provider_network = models.TextField(blank=True)
    
    # Eligibility
    min_age = models.IntegerField(default=0)
    max_age = models.IntegerField(default=100)
    
    # Pre-authorization requirements
    requires_preauth = models.BooleanField(default=False)
    preauth_procedures = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    
    # Documentation
    plan_document = models.FileField(upload_to='insurance/plans/', null=True, blank=True)
    summary_of_benefits = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['provider', 'plan_name']
        verbose_name = 'Insurance Plan'
        verbose_name_plural = 'Insurance Plans'
    
    def save(self, *args, **kwargs):
        if not self.plan_id:
            self.plan_id = f"PLN{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.provider.name} - {self.plan_name}"
    
    @property
    def is_active_plan(self):
        today = timezone.now().date()
        if self.termination_date:
            return self.effective_date <= today <= self.termination_date
        return self.effective_date <= today


class PatientInsurance(models.Model):
    """Patient insurance coverage"""
    RELATIONSHIP_CHOICES = [
        ('self', 'Self'),
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    insurance_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='insurance_coverage')
    plan = models.ForeignKey(InsurancePlan, on_delete=models.CASCADE, related_name='covered_patients')
    
    # Policy details
    policy_number = models.CharField(max_length=100)
    group_number = models.CharField(max_length=100, blank=True)
    member_id = models.CharField(max_length=100, blank=True)
    
    # Coverage details
    coverage_start = models.DateField()
    coverage_end = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Insured person details
    insured_name = models.CharField(max_length=200)
    insured_dob = models.DateField()
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default='self')
    
    # Employer information
    employer_name = models.CharField(max_length=200, blank=True)
    employer_address = models.TextField(blank=True)
    
    # Benefits used
    deductible_met = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    out_of_pocket_met = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Priority
    is_primary = models.BooleanField(default=True)
    priority_order = models.IntegerField(default=1)
    
    # Verification
    last_verified = models.DateTimeField(null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=[
        ('verified', 'Verified'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
    ], default='pending')
    
    # Authorization
    authorization_number = models.CharField(max_length=100, blank=True)
    authorization_date = models.DateField(null=True, blank=True)
    
    # Documents
    insurance_card_front = models.ImageField(upload_to='insurance/cards/', null=True, blank=True)
    insurance_card_back = models.ImageField(upload_to='insurance/cards/', null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['patient', 'priority_order']
        verbose_name = 'Patient Insurance'
        verbose_name_plural = 'Patient Insurance'
    
    def save(self, *args, **kwargs):
        if not self.insurance_id:
            self.insurance_id = f"INS{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.patient.name} - {self.plan.plan_name}"
    
    @property
    def is_active(self):
        today = timezone.now().date()
        return (self.status == 'active' and 
                self.coverage_start <= today and 
                (self.coverage_end is None or self.coverage_end >= today))


class InsuranceClaim(models.Model):
    """Insurance claims and processing"""
    CLAIM_TYPE_CHOICES = [
        ('medical', 'Medical'),
        ('dental', 'Dental'),
        ('vision', 'Vision'),
        ('prescription', 'Prescription'),
        ('hospital', 'Hospital'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('partial', 'Partial Payment'),
        ('paid', 'Paid'),
        ('appealed', 'Appealed'),
        ('cancelled', 'Cancelled'),
    ]
    
    claim_id = models.CharField(max_length=20, unique=True, blank=True)
    patient_insurance = models.ForeignKey(PatientInsurance, on_delete=models.CASCADE, related_name='claims')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='insurance_claims')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True, related_name='insurance_claims')
    
    claim_type = models.CharField(max_length=20, choices=CLAIM_TYPE_CHOICES, default='medical')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Service details
    service_date = models.DateField()
    service_provider = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='insurance_claims')
    
    # Financial details
    total_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    insurance_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    patient_responsibility = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    copay_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductible_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Diagnosis and procedures
    primary_diagnosis = models.CharField(max_length=10, blank=True)
    secondary_diagnosis = models.CharField(max_length=500, blank=True)
    procedures = models.TextField(blank=True)
    
    # Claim processing
    submitted_date = models.DateTimeField(null=True, blank=True)
    processed_date = models.DateTimeField(null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Insurance response
    insurance_claim_number = models.CharField(max_length=100, blank=True)
    explanation_of_benefits = models.TextField(blank=True)
    denial_reason = models.TextField(blank=True)
    
    # Appeals
    appeal_date = models.DateTimeField(null=True, blank=True)
    appeal_reason = models.TextField(blank=True)
    appeal_outcome = models.TextField(blank=True)
    
    # Documents
    claim_form = models.FileField(upload_to='insurance/claims/', null=True, blank=True)
    supporting_documents = models.FileField(upload_to='insurance/claims/docs/', null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Processing info
    processed_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_claims')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-service_date']
        verbose_name = 'Insurance Claim'
        verbose_name_plural = 'Insurance Claims'
    
    def save(self, *args, **kwargs):
        if not self.claim_id:
            self.claim_id = f"CLM{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.claim_id} - {self.patient.name}"
    
    @property
    def is_processed(self):
        return self.status in ['approved', 'denied', 'paid']
    
    @property
    def amount_due(self):
        return self.total_charges - self.insurance_payment


class InsurancePreauthorization(models.Model):
    """Pre-authorization requests and approvals"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    URGENCY_CHOICES = [
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
    ]
    
    preauth_id = models.CharField(max_length=20, unique=True, blank=True)
    patient_insurance = models.ForeignKey(PatientInsurance, on_delete=models.CASCADE, related_name='preauthorizations')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='preauthorizations')
    
    # Service details
    service_type = models.CharField(max_length=200)
    procedure_code = models.CharField(max_length=20, blank=True)
    diagnosis_code = models.CharField(max_length=20, blank=True)
    
    # Provider information
    requesting_provider = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='preauth_requests')
    service_provider = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='preauth_services')
    
    # Request details
    request_date = models.DateTimeField(auto_now_add=True)
    service_date = models.DateField()
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='routine')
    
    # Clinical information
    clinical_notes = models.TextField()
    medical_necessity = models.TextField()
    supporting_documentation = models.FileField(upload_to='insurance/preauth/', null=True, blank=True)
    
    # Authorization details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    authorization_number = models.CharField(max_length=100, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    
    # Financial
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Response
    response_date = models.DateTimeField(null=True, blank=True)
    response_notes = models.TextField(blank=True)
    denial_reason = models.TextField(blank=True)
    
    # Follow-up
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    
    # Contact
    insurance_contact = models.CharField(max_length=200, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-request_date']
        verbose_name = 'Insurance Preauthorization'
        verbose_name_plural = 'Insurance Preauthorizations'
    
    def save(self, *args, **kwargs):
        if not self.preauth_id:
            self.preauth_id = f"PA{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.preauth_id} - {self.service_type}"
    
    @property
    def is_approved(self):
        return self.status == 'approved'
    
    @property
    def is_expired(self):
        return self.expiration_date and timezone.now() > self.expiration_date


class InsuranceVerification(models.Model):
    """Insurance verification records"""
    VERIFICATION_TYPE_CHOICES = [
        ('eligibility', 'Eligibility'),
        ('benefits', 'Benefits'),
        ('preauth', 'Pre-authorization'),
        ('claim_status', 'Claim Status'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
    ]
    
    verification_id = models.CharField(max_length=20, unique=True, blank=True)
    patient_insurance = models.ForeignKey(PatientInsurance, on_delete=models.CASCADE, related_name='verifications')
    
    verification_type = models.CharField(max_length=20, choices=VERIFICATION_TYPE_CHOICES, default='eligibility')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Verification details
    verification_date = models.DateTimeField(auto_now_add=True)
    verification_method = models.CharField(max_length=50, blank=True)
    
    # Response
    response_data = models.JSONField(default=dict, blank=True)
    response_date = models.DateTimeField(null=True, blank=True)
    
    # Results
    eligibility_confirmed = models.BooleanField(default=False)
    benefits_verified = models.BooleanField(default=False)
    
    # Coverage details
    coverage_effective_date = models.DateField(null=True, blank=True)
    coverage_termination_date = models.DateField(null=True, blank=True)
    
    # Financial information
    deductible_remaining = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    out_of_pocket_remaining = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Notes
    verification_notes = models.TextField(blank=True)
    
    # Verification staff
    verified_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='verifications')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-verification_date']
        verbose_name = 'Insurance Verification'
        verbose_name_plural = 'Insurance Verifications'
    
    def save(self, *args, **kwargs):
        if not self.verification_id:
            self.verification_id = f"VER{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.verification_id} - {self.patient_insurance.patient.name}"


class InsuranceSettings(models.Model):
    """System-wide insurance settings"""
    # Verification settings
    auto_verify_insurance = models.BooleanField(default=True)
    verification_frequency_days = models.IntegerField(default=30)
    
    # Claim settings
    auto_submit_claims = models.BooleanField(default=False)
    claim_submission_batch_size = models.IntegerField(default=50)
    
    # Pre-authorization settings
    preauth_required_amount = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    preauth_reminder_days = models.IntegerField(default=7)
    
    # Payment settings
    payment_posting_auto = models.BooleanField(default=False)
    payment_posting_tolerance = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    
    # Notification settings
    claim_status_notifications = models.BooleanField(default=True)
    verification_expiry_notifications = models.BooleanField(default=True)
    
    # Integration settings
    clearinghouse_integration = models.BooleanField(default=False)
    edi_enabled = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Insurance Settings'
        verbose_name_plural = 'Insurance Settings'
    
    def __str__(self):
        return f"Insurance Settings - {self.created_at.date()}" 