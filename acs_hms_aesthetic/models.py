from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import Patient, HMSUser, Appointment


class AestheticTreatment(models.Model):
    """Aesthetic Treatments and Procedures"""
    TREATMENT_CATEGORY_CHOICES = [
        ('FACIAL', 'Facial Treatments'),
        ('BODY_CONTOURING', 'Body Contouring'),
        ('SKIN_REJUVENATION', 'Skin Rejuvenation'),
        ('ANTI_AGING', 'Anti-Aging'),
        ('HAIR_REMOVAL', 'Hair Removal'),
        ('SCAR_TREATMENT', 'Scar Treatment'),
        ('PIGMENTATION', 'Pigmentation Treatment'),
        ('BOTOX', 'Botox Injections'),
        ('FILLERS', 'Dermal Fillers'),
        ('CHEMICAL_PEEL', 'Chemical Peels'),
    ]
    
    treatment_name = models.CharField(max_length=200, verbose_name="Treatment Name")
    treatment_code = models.CharField(max_length=20, unique=True, verbose_name="Treatment Code")
    category = models.CharField(max_length=20, choices=TREATMENT_CATEGORY_CHOICES, verbose_name="Category")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    
    # Duration and Pricing
    duration_minutes = models.PositiveIntegerField(verbose_name="Duration (Minutes)")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Base Price")
    
    # Treatment Details
    preparation_instructions = models.TextField(blank=True, null=True, verbose_name="Preparation Instructions")
    aftercare_instructions = models.TextField(blank=True, null=True, verbose_name="Aftercare Instructions")
    contraindications = models.TextField(blank=True, null=True, verbose_name="Contraindications")
    
    # Session Requirements
    recommended_sessions = models.PositiveIntegerField(default=1, verbose_name="Recommended Sessions")
    interval_between_sessions = models.PositiveIntegerField(blank=True, null=True, verbose_name="Interval Between Sessions (Days)")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Aesthetic Treatment"
        verbose_name_plural = "Aesthetic Treatments"
        ordering = ['treatment_name']
    
    def __str__(self):
        return f"{self.treatment_name} ({self.treatment_code})"


class AestheticConsultation(models.Model):
    """Aesthetic Consultation Records"""
    consultation_number = models.CharField(max_length=20, unique=True, verbose_name="Consultation Number")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='aesthetic_consultations')
    consultant = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='aesthetic_consultations')
    consultation_date = models.DateTimeField(default=timezone.now, verbose_name="Consultation Date")
    
    # Patient Concerns
    chief_complaint = models.TextField(verbose_name="Chief Complaint")
    aesthetic_goals = models.TextField(verbose_name="Aesthetic Goals")
    
    # Medical History
    previous_treatments = models.TextField(blank=True, null=True, verbose_name="Previous Aesthetic Treatments")
    allergies = models.TextField(blank=True, null=True, verbose_name="Allergies")
    current_medications = models.TextField(blank=True, null=True, verbose_name="Current Medications")
    medical_conditions = models.TextField(blank=True, null=True, verbose_name="Medical Conditions")
    
    # Skin Assessment
    skin_type = models.CharField(max_length=20, choices=[
        ('TYPE1', 'Type I (Very Fair)'),
        ('TYPE2', 'Type II (Fair)'),
        ('TYPE3', 'Type III (Medium)'),
        ('TYPE4', 'Type IV (Olive)'),
        ('TYPE5', 'Type V (Brown)'),
        ('TYPE6', 'Type VI (Black)'),
    ], blank=True, null=True, verbose_name="Skin Type")
    
    skin_condition = models.TextField(blank=True, null=True, verbose_name="Skin Condition Assessment")
    problem_areas = models.TextField(blank=True, null=True, verbose_name="Problem Areas")
    
    # Treatment Plan
    recommended_treatments = models.ManyToManyField(AestheticTreatment, blank=True, related_name='consultations')
    treatment_plan = models.TextField(blank=True, null=True, verbose_name="Treatment Plan")
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Estimated Cost")
    
    # Photography
    before_photos = models.BooleanField(default=False, verbose_name="Before Photos Taken")
    photo_consent = models.BooleanField(default=False, verbose_name="Photo Consent Given")
    
    # Follow-up
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    notes = models.TextField(blank=True, null=True, verbose_name="Additional Notes")
    
    class Meta:
        verbose_name = "Aesthetic Consultation"
        verbose_name_plural = "Aesthetic Consultations"
        ordering = ['-consultation_date']
    
    def __str__(self):
        return f"Consultation {self.consultation_number} - {self.patient.full_name}"


class AestheticProcedure(models.Model):
    """Aesthetic Procedure Records"""
    PROCEDURE_STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('POSTPONED', 'Postponed'),
    ]
    
    procedure_number = models.CharField(max_length=20, unique=True, verbose_name="Procedure Number")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='aesthetic_procedures')
    consultation = models.ForeignKey(AestheticConsultation, on_delete=models.SET_NULL, null=True, blank=True, related_name='procedures')
    treatment = models.ForeignKey(AestheticTreatment, on_delete=models.CASCADE, related_name='procedures')
    
    # Scheduling
    scheduled_date = models.DateTimeField(verbose_name="Scheduled Date")
    actual_start_time = models.DateTimeField(blank=True, null=True, verbose_name="Actual Start Time")
    actual_end_time = models.DateTimeField(blank=True, null=True, verbose_name="Actual End Time")
    
    # Staff
    primary_practitioner = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='primary_aesthetic_procedures')
    assistant = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assisted_aesthetic_procedures')
    
    # Pre-procedure
    pre_procedure_assessment = models.TextField(blank=True, null=True, verbose_name="Pre-procedure Assessment")
    consent_obtained = models.BooleanField(default=False, verbose_name="Consent Obtained")
    
    # Procedure Details
    procedure_notes = models.TextField(blank=True, null=True, verbose_name="Procedure Notes")
    products_used = models.TextField(blank=True, null=True, verbose_name="Products Used")
    technique_used = models.TextField(blank=True, null=True, verbose_name="Technique Used")
    
    # Session Information
    session_number = models.PositiveIntegerField(default=1, verbose_name="Session Number")
    total_planned_sessions = models.PositiveIntegerField(default=1, verbose_name="Total Planned Sessions")
    
    # Results and Complications
    immediate_results = models.TextField(blank=True, null=True, verbose_name="Immediate Results")
    complications = models.TextField(blank=True, null=True, verbose_name="Complications")
    patient_satisfaction = models.IntegerField(
        blank=True, null=True, 
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Patient Satisfaction (1-10)"
    )
    
    # Post-procedure Care
    post_procedure_instructions = models.TextField(blank=True, null=True, verbose_name="Post-procedure Instructions")
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    
    # Financial
    procedure_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Procedure Cost")
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Discount Applied")
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Final Cost")
    
    # Status
    status = models.CharField(max_length=20, choices=PROCEDURE_STATUS_CHOICES, default='SCHEDULED', verbose_name="Status")
    
    class Meta:
        verbose_name = "Aesthetic Procedure"
        verbose_name_plural = "Aesthetic Procedures"
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.treatment.treatment_name} - {self.patient.full_name} (Session {self.session_number})"
    
    def save(self, *args, **kwargs):
        self.final_cost = self.procedure_cost - self.discount_applied
        super().save(*args, **kwargs)


class AestheticProduct(models.Model):
    """Aesthetic Products and Supplies"""
    PRODUCT_TYPE_CHOICES = [
        ('INJECTABLE', 'Injectable'),
        ('TOPICAL', 'Topical'),
        ('DEVICE_CONSUMABLE', 'Device Consumable'),
        ('SKINCARE', 'Skincare Product'),
        ('SUPPLEMENT', 'Supplement'),
        ('EQUIPMENT', 'Equipment'),
    ]
    
    product_name = models.CharField(max_length=200, verbose_name="Product Name")
    product_code = models.CharField(max_length=20, unique=True, verbose_name="Product Code")
    brand = models.CharField(max_length=100, verbose_name="Brand")
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, verbose_name="Product Type")
    
    # Product Details
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    ingredients = models.TextField(blank=True, null=True, verbose_name="Ingredients")
    concentration = models.CharField(max_length=100, blank=True, null=True, verbose_name="Concentration")
    
    # Usage
    indications = models.TextField(blank=True, null=True, verbose_name="Indications")
    contraindications = models.TextField(blank=True, null=True, verbose_name="Contraindications")
    usage_instructions = models.TextField(blank=True, null=True, verbose_name="Usage Instructions")
    
    # Inventory
    unit_size = models.CharField(max_length=50, verbose_name="Unit Size")
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cost per Unit")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Selling Price")
    current_stock = models.PositiveIntegerField(default=0, verbose_name="Current Stock")
    minimum_stock = models.PositiveIntegerField(default=10, verbose_name="Minimum Stock Level")
    
    # Storage and Expiry
    storage_requirements = models.TextField(blank=True, null=True, verbose_name="Storage Requirements")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Expiry Date")
    
    # Supplier
    supplier = models.CharField(max_length=200, blank=True, null=True, verbose_name="Supplier")
    supplier_contact = models.CharField(max_length=200, blank=True, null=True, verbose_name="Supplier Contact")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Aesthetic Product"
        verbose_name_plural = "Aesthetic Products"
        ordering = ['product_name']
    
    def __str__(self):
        return f"{self.product_name} ({self.brand})"


class AestheticEquipment(models.Model):
    """Aesthetic Equipment Management"""
    EQUIPMENT_TYPE_CHOICES = [
        ('LASER', 'Laser Equipment'),
        ('IPL', 'IPL Equipment'),
        ('RADIOFREQUENCY', 'Radio Frequency'),
        ('ULTRASOUND', 'Ultrasound'),
        ('CRYOTHERAPY', 'Cryotherapy'),
        ('MICRODERMABRASION', 'Microdermabrasion'),
        ('LED_THERAPY', 'LED Therapy'),
        ('MICRONEEDLING', 'Microneedling Device'),
        ('VACUUM_THERAPY', 'Vacuum Therapy'),
        ('GENERAL', 'General Equipment'),
    ]
    
    equipment_name = models.CharField(max_length=200, verbose_name="Equipment Name")
    equipment_type = models.CharField(max_length=20, choices=EQUIPMENT_TYPE_CHOICES, verbose_name="Equipment Type")
    brand = models.CharField(max_length=100, verbose_name="Brand")
    model = models.CharField(max_length=100, verbose_name="Model")
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Serial Number")
    
    # Purchase Information
    purchase_date = models.DateField(verbose_name="Purchase Date")
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Purchase Cost")
    supplier = models.CharField(max_length=200, verbose_name="Supplier")
    warranty_expiry = models.DateField(blank=True, null=True, verbose_name="Warranty Expiry")
    
    # Location and Assignment
    location = models.CharField(max_length=200, verbose_name="Location")
    assigned_to = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_aesthetic_equipment')
    
    # Maintenance
    last_maintenance = models.DateField(blank=True, null=True, verbose_name="Last Maintenance")
    next_maintenance = models.DateField(blank=True, null=True, verbose_name="Next Maintenance")
    maintenance_interval_days = models.PositiveIntegerField(default=90, verbose_name="Maintenance Interval (Days)")
    
    # Calibration
    last_calibration = models.DateField(blank=True, null=True, verbose_name="Last Calibration")
    next_calibration = models.DateField(blank=True, null=True, verbose_name="Next Calibration")
    calibration_interval_days = models.PositiveIntegerField(default=365, verbose_name="Calibration Interval (Days)")
    
    # Usage Statistics
    total_usage_hours = models.PositiveIntegerField(default=0, verbose_name="Total Usage Hours")
    shots_fired = models.PositiveIntegerField(default=0, verbose_name="Shots Fired (for laser equipment)")
    
    # Status
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('REPAIR', 'Under Repair'),
        ('CALIBRATION', 'Under Calibration'),
        ('RETIRED', 'Retired'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name="Status")
    
    # Additional Information
    specifications = models.TextField(blank=True, null=True, verbose_name="Specifications")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Aesthetic Equipment"
        verbose_name_plural = "Aesthetic Equipment"
        ordering = ['equipment_name']
    
    def __str__(self):
        return f"{self.equipment_name} ({self.serial_number})"


class PatientPhotoRecord(models.Model):
    """Patient Photo Documentation"""
    PHOTO_TYPE_CHOICES = [
        ('BEFORE', 'Before Treatment'),
        ('DURING', 'During Treatment'),
        ('AFTER', 'After Treatment'),
        ('FOLLOW_UP', 'Follow-up'),
        ('COMPLICATION', 'Complication Documentation'),
    ]
    
    ANATOMICAL_AREA_CHOICES = [
        ('FACE_FULL', 'Full Face'),
        ('FACE_PROFILE', 'Face Profile'),
        ('FOREHEAD', 'Forehead'),
        ('EYES', 'Eyes'),
        ('NOSE', 'Nose'),
        ('CHEEKS', 'Cheeks'),
        ('LIPS', 'Lips'),
        ('NECK', 'Neck'),
        ('CHEST', 'Chest'),
        ('ARMS', 'Arms'),
        ('LEGS', 'Legs'),
        ('BACK', 'Back'),
        ('OTHER', 'Other'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='photo_records')
    procedure = models.ForeignKey(AestheticProcedure, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')
    
    # Photo Details
    photo_type = models.CharField(max_length=20, choices=PHOTO_TYPE_CHOICES, verbose_name="Photo Type")
    anatomical_area = models.CharField(max_length=20, choices=ANATOMICAL_AREA_CHOICES, verbose_name="Anatomical Area")
    photo_date = models.DateTimeField(default=timezone.now, verbose_name="Photo Date")
    taken_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='taken_photos')
    
    # File Information
    photo_file = models.ImageField(upload_to='aesthetic_photos/', verbose_name="Photo File")
    photo_description = models.TextField(blank=True, null=True, verbose_name="Photo Description")
    
    # Consent and Privacy
    consent_obtained = models.BooleanField(default=False, verbose_name="Consent Obtained")
    use_for_marketing = models.BooleanField(default=False, verbose_name="Use for Marketing")
    use_for_education = models.BooleanField(default=False, verbose_name="Use for Education")
    
    class Meta:
        verbose_name = "Patient Photo Record"
        verbose_name_plural = "Patient Photo Records"
        ordering = ['-photo_date']
    
    def __str__(self):
        return f"{self.get_photo_type_display()} - {self.patient.full_name} ({self.photo_date.date()})" 