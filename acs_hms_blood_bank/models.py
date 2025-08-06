from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser, Patient, Appointment
import uuid


class BloodGroup(models.Model):
    """Blood group types"""
    ABO_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]
    
    RH_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
    ]
    
    abo_type = models.CharField(max_length=2, choices=ABO_CHOICES)
    rh_factor = models.CharField(max_length=8, choices=RH_CHOICES)
    
    class Meta:
        unique_together = ['abo_type', 'rh_factor']
        ordering = ['abo_type', 'rh_factor']
        verbose_name = 'Blood Group'
        verbose_name_plural = 'Blood Groups'
    
    def __str__(self):
        return f"{self.abo_type}{'+' if self.rh_factor == 'positive' else '-'}"


class BloodDonor(models.Model):
    """Blood donors registry"""
    DONOR_TYPE_CHOICES = [
        ('voluntary', 'Voluntary'),
        ('family', 'Family Replacement'),
        ('paid', 'Paid'),
        ('autologous', 'Autologous'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deferred', 'Deferred'),
        ('blacklisted', 'Blacklisted'),
    ]
    
    donor_id = models.CharField(max_length=20, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # Personal Information
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    
    # Contact Information
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    
    # Medical Information
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE, related_name='donors')
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    
    # Donor Details
    donor_type = models.CharField(max_length=20, choices=DONOR_TYPE_CHOICES, default='voluntary')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # First donation
    first_donation_date = models.DateField(null=True, blank=True)
    
    # Medical History
    medical_conditions = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    
    # Deferral Information
    deferral_reason = models.TextField(blank=True)
    deferral_date = models.DateField(null=True, blank=True)
    deferral_end_date = models.DateField(null=True, blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Blood Donor'
        verbose_name_plural = 'Blood Donors'
    
    def save(self, *args, **kwargs):
        if not self.donor_id:
            self.donor_id = f"BD{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.donor_id})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    @property
    def is_eligible(self):
        """Check if donor is eligible for donation"""
        if self.status != 'active':
            return False
        
        # Check age (18-65 years)
        if not (18 <= self.age <= 65):
            return False
        
        # Check weight (min 50 kg)
        if self.weight < 50:
            return False
        
        # Check deferral
        if self.deferral_end_date and self.deferral_end_date > timezone.now().date():
            return False
        
        return True


class BloodDonation(models.Model):
    """Blood donation records"""
    DONATION_TYPE_CHOICES = [
        ('whole_blood', 'Whole Blood'),
        ('plasma', 'Plasma'),
        ('platelets', 'Platelets'),
        ('red_cells', 'Red Blood Cells'),
        ('apheresis', 'Apheresis'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('deferred', 'Deferred'),
    ]
    
    donation_id = models.CharField(max_length=20, unique=True, blank=True)
    donor = models.ForeignKey(BloodDonor, on_delete=models.CASCADE, related_name='donations')
    
    # Donation Details
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPE_CHOICES, default='whole_blood')
    donation_date = models.DateTimeField()
    volume_collected = models.DecimalField(max_digits=6, decimal_places=2, help_text="Volume in ml")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Pre-donation screening
    pre_screening_passed = models.BooleanField(default=False)
    hemoglobin_level = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    pulse_rate = models.IntegerField(null=True, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    weight_at_donation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Staff involved
    phlebotomist = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='blood_donations')
    physician = models.ForeignKey(HMSUser, on_delete=models.CASCADE, null=True, blank=True, related_name='supervised_donations')
    
    # Collection details
    collection_start_time = models.DateTimeField(null=True, blank=True)
    collection_end_time = models.DateTimeField(null=True, blank=True)
    collection_bag_number = models.CharField(max_length=50, blank=True)
    
    # Adverse reactions
    adverse_reactions = models.TextField(blank=True)
    reaction_severity = models.CharField(max_length=20, choices=[
        ('none', 'None'),
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ], default='none')
    
    # Post-donation care
    post_donation_instructions = models.TextField(blank=True)
    
    # Deferral information
    deferral_reason = models.TextField(blank=True)
    next_eligible_date = models.DateField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-donation_date']
        verbose_name = 'Blood Donation'
        verbose_name_plural = 'Blood Donations'
    
    def save(self, *args, **kwargs):
        if not self.donation_id:
            self.donation_id = f"DON{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.donation_id} - {self.donor.full_name} - {self.donation_date.date()}"
    
    @property
    def duration(self):
        if self.collection_start_time and self.collection_end_time:
            return self.collection_end_time - self.collection_start_time
        return None


class BloodUnit(models.Model):
    """Blood units/bags inventory"""
    COMPONENT_CHOICES = [
        ('whole_blood', 'Whole Blood'),
        ('packed_rbc', 'Packed Red Blood Cells'),
        ('platelets', 'Platelets'),
        ('plasma', 'Fresh Frozen Plasma'),
        ('cryoprecipitate', 'Cryoprecipitate'),
        ('albumin', 'Albumin'),
        ('immunoglobulin', 'Immunoglobulin'),
    ]
    
    STATUS_CHOICES = [
        ('collected', 'Collected'),
        ('processing', 'Processing'),
        ('tested', 'Tested'),
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('issued', 'Issued'),
        ('expired', 'Expired'),
        ('discarded', 'Discarded'),
    ]
    
    unit_id = models.CharField(max_length=20, unique=True, blank=True)
    donation = models.ForeignKey(BloodDonation, on_delete=models.CASCADE, related_name='blood_units')
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE, related_name='blood_units')
    
    # Unit details
    component = models.CharField(max_length=20, choices=COMPONENT_CHOICES, default='whole_blood')
    volume = models.DecimalField(max_digits=6, decimal_places=2, help_text="Volume in ml")
    
    # Collection details
    collection_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='collected')
    
    # Testing
    testing_completed = models.BooleanField(default=False)
    test_results = models.JSONField(default=dict, blank=True)
    
    # Screening tests
    hiv_test = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('negative', 'Negative'),
        ('positive', 'Positive'),
        ('indeterminate', 'Indeterminate'),
    ], default='pending')
    
    hepatitis_b_test = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('negative', 'Negative'),
        ('positive', 'Positive'),
        ('indeterminate', 'Indeterminate'),
    ], default='pending')
    
    hepatitis_c_test = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('negative', 'Negative'),
        ('positive', 'Positive'),
        ('indeterminate', 'Indeterminate'),
    ], default='pending')
    
    syphilis_test = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('negative', 'Negative'),
        ('positive', 'Positive'),
        ('indeterminate', 'Indeterminate'),
    ], default='pending')
    
    # Storage
    storage_location = models.CharField(max_length=100, blank=True)
    storage_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Cross-matching
    cross_match_patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='cross_matched_units')
    cross_match_result = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('compatible', 'Compatible'),
        ('incompatible', 'Incompatible'),
    ], blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['collection_date']
        verbose_name = 'Blood Unit'
        verbose_name_plural = 'Blood Units'
    
    def save(self, *args, **kwargs):
        if not self.unit_id:
            self.unit_id = f"BU{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.unit_id} - {self.blood_group} - {self.component}"
    
    @property
    def is_expired(self):
        return timezone.now() > self.expiry_date
    
    @property
    def is_available(self):
        return self.status == 'available' and not self.is_expired and self.testing_completed
    
    @property
    def days_until_expiry(self):
        if self.expiry_date:
            return (self.expiry_date - timezone.now()).days
        return None


class BloodRequest(models.Model):
    """Blood requisition requests"""
    URGENCY_CHOICES = [
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('partial', 'Partially Fulfilled'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    ]
    
    request_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='blood_requests')
    requesting_physician = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='blood_requests')
    
    # Request details
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE, related_name='requests')
    component_required = models.CharField(max_length=20, choices=BloodUnit.COMPONENT_CHOICES, default='packed_rbc')
    units_required = models.IntegerField(default=1)
    
    # Clinical information
    indication = models.TextField()
    hemoglobin_level = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    hematocrit = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    # Priority
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='routine')
    required_by = models.DateTimeField()
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Approval
    approved_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_blood_requests')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Fulfillment
    units_issued = models.IntegerField(default=0)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blood Request'
        verbose_name_plural = 'Blood Requests'
    
    def save(self, *args, **kwargs):
        if not self.request_id:
            self.request_id = f"BR{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.request_id} - {self.patient.name} - {self.component_required}"
    
    @property
    def is_fulfilled(self):
        return self.units_issued >= self.units_required


class BloodIssuance(models.Model):
    """Blood unit issuance records"""
    issuance_id = models.CharField(max_length=20, unique=True, blank=True)
    request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='issuances')
    blood_unit = models.OneToOneField(BloodUnit, on_delete=models.CASCADE, related_name='issuance')
    
    # Issuance details
    issued_date = models.DateTimeField()
    issued_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='blood_issuances')
    received_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='received_blood')
    
    # Cross-matching
    cross_match_performed = models.BooleanField(default=True)
    cross_match_result = models.CharField(max_length=20, choices=[
        ('compatible', 'Compatible'),
        ('incompatible', 'Incompatible'),
    ], default='compatible')
    
    # Transportation
    transport_container = models.CharField(max_length=100, blank=True)
    transport_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Return/wastage
    units_returned = models.IntegerField(default=0)
    units_wasted = models.IntegerField(default=0)
    wastage_reason = models.TextField(blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-issued_date']
        verbose_name = 'Blood Issuance'
        verbose_name_plural = 'Blood Issuances'
    
    def save(self, *args, **kwargs):
        if not self.issuance_id:
            self.issuance_id = f"BI{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.issuance_id} - {self.blood_unit.unit_id}"


class BloodTransfusion(models.Model):
    """Blood transfusion records"""
    TRANSFUSION_TYPE_CHOICES = [
        ('whole_blood', 'Whole Blood'),
        ('packed_rbc', 'Packed Red Blood Cells'),
        ('platelets', 'Platelets'),
        ('plasma', 'Fresh Frozen Plasma'),
        ('cryoprecipitate', 'Cryoprecipitate'),
        ('exchange', 'Exchange Transfusion'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('stopped', 'Stopped'),
        ('cancelled', 'Cancelled'),
    ]
    
    transfusion_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='blood_transfusions')
    issuance = models.ForeignKey(BloodIssuance, on_delete=models.CASCADE, related_name='transfusions')
    
    # Transfusion details
    transfusion_type = models.CharField(max_length=20, choices=TRANSFUSION_TYPE_CHOICES, default='packed_rbc')
    volume_transfused = models.DecimalField(max_digits=6, decimal_places=2, help_text="Volume in ml")
    
    # Timing
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Staff
    administered_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='administered_transfusions')
    monitored_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, null=True, blank=True, related_name='monitored_transfusions')
    
    # Pre-transfusion
    pre_transfusion_vitals = models.JSONField(default=dict, blank=True)
    
    # During transfusion
    transfusion_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Rate in ml/hr")
    
    # Post-transfusion
    post_transfusion_vitals = models.JSONField(default=dict, blank=True)
    
    # Adverse reactions
    adverse_reactions = models.TextField(blank=True)
    reaction_type = models.CharField(max_length=20, choices=[
        ('none', 'None'),
        ('allergic', 'Allergic'),
        ('febrile', 'Febrile'),
        ('hemolytic', 'Hemolytic'),
        ('circulatory', 'Circulatory Overload'),
        ('other', 'Other'),
    ], default='none')
    
    # Intervention
    intervention_required = models.BooleanField(default=False)
    intervention_details = models.TextField(blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_time']
        verbose_name = 'Blood Transfusion'
        verbose_name_plural = 'Blood Transfusions'
    
    def save(self, *args, **kwargs):
        if not self.transfusion_id:
            self.transfusion_id = f"BT{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.transfusion_id} - {self.patient.name}"
    
    @property
    def duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


class BloodBankSettings(models.Model):
    """Blood bank system settings"""
    # Storage settings
    whole_blood_storage_temp = models.DecimalField(max_digits=5, decimal_places=2, default=4.0)
    plasma_storage_temp = models.DecimalField(max_digits=5, decimal_places=2, default=-18.0)
    platelet_storage_temp = models.DecimalField(max_digits=5, decimal_places=2, default=22.0)
    
    # Expiry settings
    whole_blood_shelf_life = models.IntegerField(default=35, help_text="Days")
    packed_rbc_shelf_life = models.IntegerField(default=42, help_text="Days")
    plasma_shelf_life = models.IntegerField(default=365, help_text="Days")
    platelet_shelf_life = models.IntegerField(default=5, help_text="Days")
    
    # Donor settings
    min_donation_interval = models.IntegerField(default=56, help_text="Days between donations")
    min_donor_age = models.IntegerField(default=18)
    max_donor_age = models.IntegerField(default=65)
    min_donor_weight = models.DecimalField(max_digits=5, decimal_places=2, default=50.0)
    min_hemoglobin = models.DecimalField(max_digits=4, decimal_places=2, default=12.5)
    
    # Testing requirements
    mandatory_tests = models.JSONField(default=list, blank=True)
    
    # Notifications
    low_stock_alert = models.IntegerField(default=5, help_text="Alert when units below this number")
    expiry_alert_days = models.IntegerField(default=7, help_text="Alert days before expiry")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Blood Bank Settings'
        verbose_name_plural = 'Blood Bank Settings'
    
    def __str__(self):
        return f"Blood Bank Settings - {self.created_at.date()}" 