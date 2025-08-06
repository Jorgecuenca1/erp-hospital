from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import Patient, HMSUser, Appointment


class DentalExamination(models.Model):
    """Dental Examination Records"""
    examination_number = models.CharField(max_length=20, unique=True, verbose_name="Examination Number")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='dental_examinations')
    dentist = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='dental_examinations')
    examination_date = models.DateTimeField(default=timezone.now, verbose_name="Examination Date")
    
    # Chief Complaint
    chief_complaint = models.TextField(verbose_name="Chief Complaint")
    history_present_illness = models.TextField(blank=True, null=True, verbose_name="History of Present Illness")
    
    # Dental History
    previous_dental_treatment = models.TextField(blank=True, null=True, verbose_name="Previous Dental Treatment")
    last_dental_visit = models.DateField(blank=True, null=True, verbose_name="Last Dental Visit")
    dental_anxiety = models.BooleanField(default=False, verbose_name="Dental Anxiety")
    
    # Oral Hygiene
    brushing_frequency = models.CharField(max_length=50, blank=True, null=True, verbose_name="Brushing Frequency")
    flossing_frequency = models.CharField(max_length=50, blank=True, null=True, verbose_name="Flossing Frequency")
    mouthwash_use = models.BooleanField(default=False, verbose_name="Uses Mouthwash")
    
    # Habits
    smoking = models.BooleanField(default=False, verbose_name="Smoking")
    alcohol_consumption = models.CharField(max_length=50, blank=True, null=True, verbose_name="Alcohol Consumption")
    teeth_grinding = models.BooleanField(default=False, verbose_name="Teeth Grinding (Bruxism)")
    nail_biting = models.BooleanField(default=False, verbose_name="Nail Biting")
    
    # Clinical Examination
    oral_hygiene_status = models.CharField(max_length=20, choices=[
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
        ('POOR', 'Poor'),
    ], blank=True, null=True, verbose_name="Oral Hygiene Status")
    
    # Soft Tissue Examination
    gums_condition = models.TextField(blank=True, null=True, verbose_name="Gums Condition")
    tongue_condition = models.TextField(blank=True, null=True, verbose_name="Tongue Condition")
    lips_condition = models.TextField(blank=True, null=True, verbose_name="Lips Condition")
    cheeks_condition = models.TextField(blank=True, null=True, verbose_name="Cheeks Condition")
    palate_condition = models.TextField(blank=True, null=True, verbose_name="Palate Condition")
    
    # Occlusion
    occlusion_class = models.CharField(max_length=20, choices=[
        ('CLASS_I', 'Class I'),
        ('CLASS_II', 'Class II'),
        ('CLASS_III', 'Class III'),
    ], blank=True, null=True, verbose_name="Occlusion Class")
    
    overjet = models.FloatField(blank=True, null=True, verbose_name="Overjet (mm)")
    overbite = models.FloatField(blank=True, null=True, verbose_name="Overbite (mm)")
    
    # Periodontal Assessment
    bleeding_on_probing = models.BooleanField(default=False, verbose_name="Bleeding on Probing")
    pocket_depth_max = models.FloatField(blank=True, null=True, verbose_name="Maximum Pocket Depth (mm)")
    recession_present = models.BooleanField(default=False, verbose_name="Recession Present")
    
    # TMJ Assessment
    tmj_clicking = models.BooleanField(default=False, verbose_name="TMJ Clicking")
    tmj_pain = models.BooleanField(default=False, verbose_name="TMJ Pain")
    mouth_opening_limitation = models.BooleanField(default=False, verbose_name="Mouth Opening Limitation")
    
    # Diagnosis and Plan
    diagnosis = models.TextField(verbose_name="Diagnosis")
    treatment_plan = models.TextField(blank=True, null=True, verbose_name="Treatment Plan")
    urgency = models.CharField(max_length=20, choices=[
        ('EMERGENCY', 'Emergency'),
        ('URGENT', 'Urgent'),
        ('ROUTINE', 'Routine'),
        ('ELECTIVE', 'Elective'),
    ], default='ROUTINE', verbose_name="Treatment Urgency")
    
    # Follow-up
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    notes = models.TextField(blank=True, null=True, verbose_name="Additional Notes")
    
    class Meta:
        verbose_name = "Dental Examination"
        verbose_name_plural = "Dental Examinations"
        ordering = ['-examination_date']
    
    def __str__(self):
        return f"Dental Exam {self.examination_number} - {self.patient.full_name}"


class ToothChart(models.Model):
    """Dental Chart for tracking individual teeth"""
    TOOTH_STATUS_CHOICES = [
        ('HEALTHY', 'Healthy'),
        ('DECAY', 'Decay'),
        ('FILLED', 'Filled'),
        ('CROWN', 'Crown'),
        ('BRIDGE', 'Bridge'),
        ('IMPLANT', 'Implant'),
        ('MISSING', 'Missing'),
        ('EXTRACTED', 'Extracted'),
        ('ROOT_CANAL', 'Root Canal'),
        ('FRACTURED', 'Fractured'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='tooth_charts')
    examination = models.ForeignKey(DentalExamination, on_delete=models.CASCADE, related_name='tooth_charts')
    
    # Tooth Identification (Universal Numbering System)
    tooth_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(32)],
        verbose_name="Tooth Number (1-32)"
    )
    
    # Tooth Condition
    tooth_status = models.CharField(max_length=20, choices=TOOTH_STATUS_CHOICES, verbose_name="Tooth Status")
    condition_notes = models.TextField(blank=True, null=True, verbose_name="Condition Notes")
    
    # Surface Conditions (for posterior teeth)
    mesial_surface = models.CharField(max_length=20, blank=True, null=True, verbose_name="Mesial Surface")
    distal_surface = models.CharField(max_length=20, blank=True, null=True, verbose_name="Distal Surface")
    buccal_surface = models.CharField(max_length=20, blank=True, null=True, verbose_name="Buccal Surface")
    lingual_surface = models.CharField(max_length=20, blank=True, null=True, verbose_name="Lingual Surface")
    occlusal_surface = models.CharField(max_length=20, blank=True, null=True, verbose_name="Occlusal Surface")
    
    # Periodontal Measurements
    probing_depth_mb = models.FloatField(blank=True, null=True, verbose_name="Probing Depth MB (mm)")
    probing_depth_b = models.FloatField(blank=True, null=True, verbose_name="Probing Depth B (mm)")
    probing_depth_db = models.FloatField(blank=True, null=True, verbose_name="Probing Depth DB (mm)")
    probing_depth_ml = models.FloatField(blank=True, null=True, verbose_name="Probing Depth ML (mm)")
    probing_depth_l = models.FloatField(blank=True, null=True, verbose_name="Probing Depth L (mm)")
    probing_depth_dl = models.FloatField(blank=True, null=True, verbose_name="Probing Depth DL (mm)")
    
    # Mobility
    mobility = models.CharField(max_length=20, choices=[
        ('0', 'Class 0 (Normal)'),
        ('1', 'Class 1 (Slight)'),
        ('2', 'Class 2 (Moderate)'),
        ('3', 'Class 3 (Severe)'),
    ], blank=True, null=True, verbose_name="Tooth Mobility")
    
    class Meta:
        verbose_name = "Tooth Chart"
        verbose_name_plural = "Tooth Charts"
        unique_together = ['examination', 'tooth_number']
        ordering = ['tooth_number']
    
    def __str__(self):
        return f"Tooth #{self.tooth_number} - {self.patient.full_name}"


class DentalTreatment(models.Model):
    """Dental Treatment Procedures"""
    TREATMENT_CATEGORY_CHOICES = [
        ('PREVENTIVE', 'Preventive'),
        ('RESTORATIVE', 'Restorative'),
        ('ENDODONTIC', 'Endodontic'),
        ('PERIODONTAL', 'Periodontal'),
        ('ORAL_SURGERY', 'Oral Surgery'),
        ('ORTHODONTIC', 'Orthodontic'),
        ('PROSTHODONTIC', 'Prosthodontic'),
        ('COSMETIC', 'Cosmetic'),
        ('EMERGENCY', 'Emergency'),
    ]
    
    treatment_name = models.CharField(max_length=200, verbose_name="Treatment Name")
    treatment_code = models.CharField(max_length=20, unique=True, verbose_name="Treatment Code")
    category = models.CharField(max_length=20, choices=TREATMENT_CATEGORY_CHOICES, verbose_name="Category")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    
    # Duration and Pricing
    duration_minutes = models.PositiveIntegerField(verbose_name="Duration (Minutes)")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Base Price")
    
    # Requirements
    requires_anesthesia = models.BooleanField(default=False, verbose_name="Requires Anesthesia")
    requires_assistant = models.BooleanField(default=False, verbose_name="Requires Assistant")
    
    # Instructions
    pre_treatment_instructions = models.TextField(blank=True, null=True, verbose_name="Pre-treatment Instructions")
    post_treatment_instructions = models.TextField(blank=True, null=True, verbose_name="Post-treatment Instructions")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Dental Treatment"
        verbose_name_plural = "Dental Treatments"
        ordering = ['treatment_name']
    
    def __str__(self):
        return f"{self.treatment_name} ({self.treatment_code})"


class DentalProcedure(models.Model):
    """Dental Procedure Records"""
    PROCEDURE_STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('POSTPONED', 'Postponed'),
    ]
    
    procedure_number = models.CharField(max_length=20, unique=True, verbose_name="Procedure Number")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='dental_procedures')
    examination = models.ForeignKey(DentalExamination, on_delete=models.SET_NULL, null=True, blank=True, related_name='procedures')
    treatment = models.ForeignKey(DentalTreatment, on_delete=models.CASCADE, related_name='procedures')
    
    # Scheduling
    scheduled_date = models.DateTimeField(verbose_name="Scheduled Date")
    actual_start_time = models.DateTimeField(blank=True, null=True, verbose_name="Actual Start Time")
    actual_end_time = models.DateTimeField(blank=True, null=True, verbose_name="Actual End Time")
    
    # Staff
    primary_dentist = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='primary_dental_procedures')
    assistant = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assisted_dental_procedures')
    
    # Affected Teeth
    affected_teeth = models.CharField(max_length=200, verbose_name="Affected Teeth Numbers")
    
    # Anesthesia
    anesthesia_used = models.BooleanField(default=False, verbose_name="Anesthesia Used")
    anesthesia_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Anesthesia Type")
    anesthesia_amount = models.CharField(max_length=50, blank=True, null=True, verbose_name="Anesthesia Amount")
    
    # Procedure Details
    procedure_notes = models.TextField(blank=True, null=True, verbose_name="Procedure Notes")
    materials_used = models.TextField(blank=True, null=True, verbose_name="Materials Used")
    technique_used = models.TextField(blank=True, null=True, verbose_name="Technique Used")
    
    # Results and Complications
    procedure_outcome = models.TextField(blank=True, null=True, verbose_name="Procedure Outcome")
    complications = models.TextField(blank=True, null=True, verbose_name="Complications")
    
    # Post-procedure
    post_procedure_instructions = models.TextField(blank=True, null=True, verbose_name="Post-procedure Instructions")
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    
    # Financial
    procedure_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Procedure Cost")
    insurance_covered = models.BooleanField(default=False, verbose_name="Insurance Covered")
    patient_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Patient Payment")
    
    # Status
    status = models.CharField(max_length=20, choices=PROCEDURE_STATUS_CHOICES, default='SCHEDULED', verbose_name="Status")
    
    class Meta:
        verbose_name = "Dental Procedure"
        verbose_name_plural = "Dental Procedures"
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.treatment.treatment_name} - {self.patient.full_name}"


class DentalEquipment(models.Model):
    """Dental Equipment Management"""
    EQUIPMENT_TYPE_CHOICES = [
        ('DENTAL_CHAIR', 'Dental Chair'),
        ('XRAY_UNIT', 'X-Ray Unit'),
        ('AUTOCLAVE', 'Autoclave'),
        ('ULTRASONIC_CLEANER', 'Ultrasonic Cleaner'),
        ('COMPRESSOR', 'Air Compressor'),
        ('SUCTION_UNIT', 'Suction Unit'),
        ('LASER', 'Dental Laser'),
        ('INTRAORAL_CAMERA', 'Intraoral Camera'),
        ('CURING_LIGHT', 'Curing Light'),
        ('SCALER', 'Ultrasonic Scaler'),
        ('HANDPIECE', 'Dental Handpiece'),
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
    
    # Location
    location = models.CharField(max_length=200, verbose_name="Location")
    assigned_to = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_dental_equipment')
    
    # Maintenance
    last_maintenance = models.DateField(blank=True, null=True, verbose_name="Last Maintenance")
    next_maintenance = models.DateField(blank=True, null=True, verbose_name="Next Maintenance")
    maintenance_interval_days = models.PositiveIntegerField(default=90, verbose_name="Maintenance Interval (Days)")
    
    # Status
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('REPAIR', 'Under Repair'),
        ('RETIRED', 'Retired'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name="Status")
    
    # Additional Information
    specifications = models.TextField(blank=True, null=True, verbose_name="Specifications")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Dental Equipment"
        verbose_name_plural = "Dental Equipment"
        ordering = ['equipment_name']
    
    def __str__(self):
        return f"{self.equipment_name} ({self.serial_number})"


class DentalMaterial(models.Model):
    """Dental Materials and Supplies"""
    MATERIAL_TYPE_CHOICES = [
        ('FILLING', 'Filling Material'),
        ('IMPRESSION', 'Impression Material'),
        ('CEMENT', 'Dental Cement'),
        ('ANESTHETIC', 'Anesthetic'),
        ('CLEANING', 'Cleaning Supplies'),
        ('PROTECTIVE', 'Protective Equipment'),
        ('INSTRUMENT', 'Dental Instruments'),
        ('MEDICATION', 'Dental Medication'),
        ('PROSTHETIC', 'Prosthetic Material'),
        ('ORTHODONTIC', 'Orthodontic Material'),
    ]
    
    material_name = models.CharField(max_length=200, verbose_name="Material Name")
    material_code = models.CharField(max_length=20, unique=True, verbose_name="Material Code")
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES, verbose_name="Material Type")
    brand = models.CharField(max_length=100, verbose_name="Brand")
    
    # Details
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    composition = models.TextField(blank=True, null=True, verbose_name="Composition")
    
    # Usage
    indications = models.TextField(blank=True, null=True, verbose_name="Indications")
    contraindications = models.TextField(blank=True, null=True, verbose_name="Contraindications")
    usage_instructions = models.TextField(blank=True, null=True, verbose_name="Usage Instructions")
    
    # Inventory
    unit_type = models.CharField(max_length=50, verbose_name="Unit Type")
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cost per Unit")
    current_stock = models.PositiveIntegerField(default=0, verbose_name="Current Stock")
    minimum_stock = models.PositiveIntegerField(default=10, verbose_name="Minimum Stock Level")
    
    # Storage
    storage_requirements = models.TextField(blank=True, null=True, verbose_name="Storage Requirements")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Expiry Date")
    
    # Supplier
    supplier = models.CharField(max_length=200, verbose_name="Supplier")
    supplier_contact = models.CharField(max_length=200, blank=True, null=True, verbose_name="Supplier Contact")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Dental Material"
        verbose_name_plural = "Dental Materials"
        ordering = ['material_name']
    
    def __str__(self):
        return f"{self.material_name} ({self.brand})" 