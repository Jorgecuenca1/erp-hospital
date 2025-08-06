from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import Patient, HMSUser, Appointment, MedicalRecord


class EyeExamination(models.Model):
    """Comprehensive Eye Examination Records"""
    VISUAL_ACUITY_CHOICES = [
        ('20/20', '20/20'),
        ('20/25', '20/25'),
        ('20/30', '20/30'),
        ('20/40', '20/40'),
        ('20/50', '20/50'),
        ('20/60', '20/60'),
        ('20/70', '20/70'),
        ('20/80', '20/80'),
        ('20/100', '20/100'),
        ('20/200', '20/200'),
        ('CF', 'Count Fingers'),
        ('HM', 'Hand Motion'),
        ('LP', 'Light Perception'),
        ('NLP', 'No Light Perception'),
    ]
    
    # Basic Information
    examination_number = models.CharField(max_length=20, unique=True, verbose_name="Examination Number")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='eye_examinations')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='eye_examinations')
    ophthalmologist = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='eye_examinations', limit_choices_to={'user_type': 'DOCTOR'})
    examination_date = models.DateTimeField(default=timezone.now, verbose_name="Examination Date")
    
    # Chief Complaint
    chief_complaint = models.TextField(verbose_name="Chief Complaint")
    history_present_illness = models.TextField(blank=True, null=True, verbose_name="History of Present Illness")
    
    # Visual Acuity
    va_right_uncorrected = models.CharField(max_length=10, choices=VISUAL_ACUITY_CHOICES, blank=True, null=True, verbose_name="VA Right (Uncorrected)")
    va_left_uncorrected = models.CharField(max_length=10, choices=VISUAL_ACUITY_CHOICES, blank=True, null=True, verbose_name="VA Left (Uncorrected)")
    va_right_corrected = models.CharField(max_length=10, choices=VISUAL_ACUITY_CHOICES, blank=True, null=True, verbose_name="VA Right (Corrected)")
    va_left_corrected = models.CharField(max_length=10, choices=VISUAL_ACUITY_CHOICES, blank=True, null=True, verbose_name="VA Left (Corrected)")
    
    # Refraction
    sphere_right = models.FloatField(blank=True, null=True, verbose_name="Sphere Right")
    cylinder_right = models.FloatField(blank=True, null=True, verbose_name="Cylinder Right")
    axis_right = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(180)], verbose_name="Axis Right")
    sphere_left = models.FloatField(blank=True, null=True, verbose_name="Sphere Left")
    cylinder_left = models.FloatField(blank=True, null=True, verbose_name="Cylinder Left")
    axis_left = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(180)], verbose_name="Axis Left")
    
    # Intraocular Pressure
    iop_right = models.IntegerField(blank=True, null=True, verbose_name="IOP Right (mmHg)")
    iop_left = models.IntegerField(blank=True, null=True, verbose_name="IOP Left (mmHg)")
    iop_method = models.CharField(max_length=50, blank=True, null=True, verbose_name="IOP Measurement Method")
    
    # Pupil Examination
    pupil_right_size = models.FloatField(blank=True, null=True, verbose_name="Pupil Right Size (mm)")
    pupil_left_size = models.FloatField(blank=True, null=True, verbose_name="Pupil Left Size (mm)")
    pupil_right_reaction = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pupil Right Reaction")
    pupil_left_reaction = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pupil Left Reaction")
    rapd = models.BooleanField(default=False, verbose_name="Relative Afferent Pupillary Defect")
    
    # Anterior Segment
    conjunctiva_right = models.TextField(blank=True, null=True, verbose_name="Conjunctiva Right")
    conjunctiva_left = models.TextField(blank=True, null=True, verbose_name="Conjunctiva Left")
    cornea_right = models.TextField(blank=True, null=True, verbose_name="Cornea Right")
    cornea_left = models.TextField(blank=True, null=True, verbose_name="Cornea Left")
    anterior_chamber_right = models.TextField(blank=True, null=True, verbose_name="Anterior Chamber Right")
    anterior_chamber_left = models.TextField(blank=True, null=True, verbose_name="Anterior Chamber Left")
    iris_right = models.TextField(blank=True, null=True, verbose_name="Iris Right")
    iris_left = models.TextField(blank=True, null=True, verbose_name="Iris Left")
    lens_right = models.TextField(blank=True, null=True, verbose_name="Lens Right")
    lens_left = models.TextField(blank=True, null=True, verbose_name="Lens Left")
    
    # Posterior Segment
    vitreous_right = models.TextField(blank=True, null=True, verbose_name="Vitreous Right")
    vitreous_left = models.TextField(blank=True, null=True, verbose_name="Vitreous Left")
    optic_disc_right = models.TextField(blank=True, null=True, verbose_name="Optic Disc Right")
    optic_disc_left = models.TextField(blank=True, null=True, verbose_name="Optic Disc Left")
    macula_right = models.TextField(blank=True, null=True, verbose_name="Macula Right")
    macula_left = models.TextField(blank=True, null=True, verbose_name="Macula Left")
    retinal_vessels_right = models.TextField(blank=True, null=True, verbose_name="Retinal Vessels Right")
    retinal_vessels_left = models.TextField(blank=True, null=True, verbose_name="Retinal Vessels Left")
    peripheral_retina_right = models.TextField(blank=True, null=True, verbose_name="Peripheral Retina Right")
    peripheral_retina_left = models.TextField(blank=True, null=True, verbose_name="Peripheral Retina Left")
    
    # Diagnosis and Plan
    diagnosis = models.TextField(verbose_name="Diagnosis")
    treatment_plan = models.TextField(blank=True, null=True, verbose_name="Treatment Plan")
    medications = models.TextField(blank=True, null=True, verbose_name="Medications")
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    
    # Additional Notes
    additional_notes = models.TextField(blank=True, null=True, verbose_name="Additional Notes")
    
    class Meta:
        verbose_name = "Eye Examination"
        verbose_name_plural = "Eye Examinations"
        ordering = ['-examination_date']
    
    def __str__(self):
        return f"Eye Exam {self.examination_number} - {self.patient.full_name}"


class OphthalmologyProcedure(models.Model):
    """Ophthalmology Procedures"""
    PROCEDURE_TYPE_CHOICES = [
        ('CATARACT_SURGERY', 'Cataract Surgery'),
        ('GLAUCOMA_SURGERY', 'Glaucoma Surgery'),
        ('RETINAL_SURGERY', 'Retinal Surgery'),
        ('CORNEAL_SURGERY', 'Corneal Surgery'),
        ('REFRACTIVE_SURGERY', 'Refractive Surgery'),
        ('OCULOPLASTIC_SURGERY', 'Oculoplastic Surgery'),
        ('LASER_THERAPY', 'Laser Therapy'),
        ('INJECTION', 'Injection'),
        ('BIOPSY', 'Biopsy'),
        ('FOREIGN_BODY_REMOVAL', 'Foreign Body Removal'),
    ]
    
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('POSTPONED', 'Postponed'),
    ]
    
    # Basic Information
    procedure_number = models.CharField(max_length=20, unique=True, verbose_name="Procedure Number")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='ophthalmology_procedures')
    eye_examination = models.ForeignKey(EyeExamination, on_delete=models.SET_NULL, null=True, blank=True, related_name='procedures')
    
    # Procedure Details
    procedure_type = models.CharField(max_length=30, choices=PROCEDURE_TYPE_CHOICES, verbose_name="Procedure Type")
    procedure_name = models.CharField(max_length=200, verbose_name="Procedure Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    
    # Eye Selection
    eye_operated = models.CharField(max_length=10, choices=[('RIGHT', 'Right'), ('LEFT', 'Left'), ('BOTH', 'Both')], verbose_name="Eye Operated")
    
    # Scheduling
    scheduled_date = models.DateTimeField(verbose_name="Scheduled Date")
    actual_date = models.DateTimeField(blank=True, null=True, verbose_name="Actual Date")
    duration_minutes = models.PositiveIntegerField(blank=True, null=True, verbose_name="Duration (Minutes)")
    
    # Medical Team
    primary_surgeon = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='primary_eye_surgeries', limit_choices_to={'user_type': 'DOCTOR'})
    assistant_surgeon = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assistant_eye_surgeries', limit_choices_to={'user_type': 'DOCTOR'})
    anesthesiologist = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='eye_anesthesia')
    
    # Pre-operative
    preop_diagnosis = models.TextField(verbose_name="Pre-operative Diagnosis")
    preop_medications = models.TextField(blank=True, null=True, verbose_name="Pre-operative Medications")
    preop_instructions = models.TextField(blank=True, null=True, verbose_name="Pre-operative Instructions")
    
    # Operative Details
    anesthesia_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Anesthesia Type")
    surgical_technique = models.TextField(blank=True, null=True, verbose_name="Surgical Technique")
    complications = models.TextField(blank=True, null=True, verbose_name="Complications")
    
    # Post-operative
    postop_diagnosis = models.TextField(blank=True, null=True, verbose_name="Post-operative Diagnosis")
    postop_medications = models.TextField(blank=True, null=True, verbose_name="Post-operative Medications")
    postop_instructions = models.TextField(blank=True, null=True, verbose_name="Post-operative Instructions")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED', verbose_name="Status")
    
    # Follow-up
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    
    class Meta:
        verbose_name = "Ophthalmology Procedure"
        verbose_name_plural = "Ophthalmology Procedures"
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.procedure_name} - {self.patient.full_name}"


class EyeDisease(models.Model):
    """Eye Disease Management"""
    DISEASE_CATEGORY_CHOICES = [
        ('GLAUCOMA', 'Glaucoma'),
        ('CATARACT', 'Cataract'),
        ('RETINAL', 'Retinal Disease'),
        ('CORNEAL', 'Corneal Disease'),
        ('REFRACTIVE', 'Refractive Error'),
        ('INFLAMMATORY', 'Inflammatory Disease'),
        ('INFECTIOUS', 'Infectious Disease'),
        ('NEOPLASTIC', 'Neoplastic Disease'),
        ('TRAUMA', 'Trauma'),
        ('CONGENITAL', 'Congenital Anomaly'),
    ]
    
    SEVERITY_CHOICES = [
        ('MILD', 'Mild'),
        ('MODERATE', 'Moderate'),
        ('SEVERE', 'Severe'),
        ('CRITICAL', 'Critical'),
    ]
    
    # Basic Information
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='eye_diseases')
    disease_name = models.CharField(max_length=200, verbose_name="Disease Name")
    disease_category = models.CharField(max_length=20, choices=DISEASE_CATEGORY_CHOICES, verbose_name="Disease Category")
    icd_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="ICD Code")
    
    # Disease Details
    affected_eye = models.CharField(max_length=10, choices=[('RIGHT', 'Right'), ('LEFT', 'Left'), ('BOTH', 'Both')], verbose_name="Affected Eye")
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, verbose_name="Severity")
    onset_date = models.DateField(verbose_name="Onset Date")
    diagnosis_date = models.DateField(verbose_name="Diagnosis Date")
    diagnosed_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='diagnosed_eye_diseases')
    
    # Clinical Details
    symptoms = models.TextField(verbose_name="Symptoms")
    clinical_findings = models.TextField(blank=True, null=True, verbose_name="Clinical Findings")
    stage = models.CharField(max_length=100, blank=True, null=True, verbose_name="Disease Stage")
    
    # Treatment
    current_treatment = models.TextField(blank=True, null=True, verbose_name="Current Treatment")
    treatment_response = models.TextField(blank=True, null=True, verbose_name="Treatment Response")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    resolved_date = models.DateField(blank=True, null=True, verbose_name="Resolved Date")
    
    # Follow-up
    last_follow_up = models.DateField(blank=True, null=True, verbose_name="Last Follow-up")
    next_follow_up = models.DateField(blank=True, null=True, verbose_name="Next Follow-up")
    
    class Meta:
        verbose_name = "Eye Disease"
        verbose_name_plural = "Eye Diseases"
        ordering = ['-diagnosis_date']
    
    def __str__(self):
        return f"{self.disease_name} - {self.patient.full_name}"


class OpticalPrescription(models.Model):
    """Optical Prescription Management"""
    LENS_TYPE_CHOICES = [
        ('SINGLE_VISION', 'Single Vision'),
        ('BIFOCAL', 'Bifocal'),
        ('TRIFOCAL', 'Trifocal'),
        ('PROGRESSIVE', 'Progressive'),
        ('READING', 'Reading Only'),
    ]
    
    # Basic Information
    prescription_number = models.CharField(max_length=20, unique=True, verbose_name="Prescription Number")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='optical_prescriptions')
    eye_examination = models.ForeignKey(EyeExamination, on_delete=models.CASCADE, related_name='prescriptions')
    prescribed_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='optical_prescriptions')
    prescription_date = models.DateField(default=timezone.now, verbose_name="Prescription Date")
    
    # Right Eye
    sphere_right = models.FloatField(verbose_name="Sphere Right")
    cylinder_right = models.FloatField(default=0, verbose_name="Cylinder Right")
    axis_right = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(180)], verbose_name="Axis Right")
    add_right = models.FloatField(default=0, verbose_name="Add Right")
    
    # Left Eye
    sphere_left = models.FloatField(verbose_name="Sphere Left")
    cylinder_left = models.FloatField(default=0, verbose_name="Cylinder Left")
    axis_left = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(180)], verbose_name="Axis Left")
    add_left = models.FloatField(default=0, verbose_name="Add Left")
    
    # Lens Specifications
    lens_type = models.CharField(max_length=20, choices=LENS_TYPE_CHOICES, verbose_name="Lens Type")
    pupillary_distance = models.FloatField(verbose_name="Pupillary Distance (mm)")
    
    # Frame Specifications
    frame_specifications = models.TextField(blank=True, null=True, verbose_name="Frame Specifications")
    
    # Special Instructions
    special_instructions = models.TextField(blank=True, null=True, verbose_name="Special Instructions")
    
    # Validity
    valid_until = models.DateField(verbose_name="Valid Until")
    
    # Dispensing
    dispensed = models.BooleanField(default=False, verbose_name="Dispensed")
    dispensed_date = models.DateField(blank=True, null=True, verbose_name="Dispensed Date")
    dispensed_by = models.CharField(max_length=100, blank=True, null=True, verbose_name="Dispensed By")
    
    class Meta:
        verbose_name = "Optical Prescription"
        verbose_name_plural = "Optical Prescriptions"
        ordering = ['-prescription_date']
    
    def __str__(self):
        return f"Prescription {self.prescription_number} - {self.patient.full_name}"


class VisualFieldTest(models.Model):
    """Visual Field Test Results"""
    TEST_TYPE_CHOICES = [
        ('HUMPHREY', 'Humphrey Visual Field'),
        ('GOLDMAN', 'Goldman Perimetry'),
        ('OCTOPUS', 'Octopus Perimetry'),
        ('CONFRONTATION', 'Confrontation Test'),
    ]
    
    # Basic Information
    test_number = models.CharField(max_length=20, unique=True, verbose_name="Test Number")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visual_field_tests')
    eye_examination = models.ForeignKey(EyeExamination, on_delete=models.SET_NULL, null=True, blank=True, related_name='visual_field_tests')
    test_date = models.DateTimeField(default=timezone.now, verbose_name="Test Date")
    performed_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='visual_field_tests')
    
    # Test Details
    test_type = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES, verbose_name="Test Type")
    eye_tested = models.CharField(max_length=10, choices=[('RIGHT', 'Right'), ('LEFT', 'Left')], verbose_name="Eye Tested")
    
    # Test Parameters
    test_strategy = models.CharField(max_length=100, blank=True, null=True, verbose_name="Test Strategy")
    stimulus_size = models.CharField(max_length=50, blank=True, null=True, verbose_name="Stimulus Size")
    background_luminance = models.CharField(max_length=50, blank=True, null=True, verbose_name="Background Luminance")
    
    # Results
    mean_deviation = models.FloatField(blank=True, null=True, verbose_name="Mean Deviation (dB)")
    pattern_standard_deviation = models.FloatField(blank=True, null=True, verbose_name="Pattern Standard Deviation (dB)")
    visual_field_index = models.FloatField(blank=True, null=True, verbose_name="Visual Field Index (%)")
    
    # Test Quality
    fixation_losses = models.CharField(max_length=20, blank=True, null=True, verbose_name="Fixation Losses")
    false_positives = models.CharField(max_length=20, blank=True, null=True, verbose_name="False Positives")
    false_negatives = models.CharField(max_length=20, blank=True, null=True, verbose_name="False Negatives")
    
    # Interpretation
    interpretation = models.TextField(blank=True, null=True, verbose_name="Interpretation")
    defect_pattern = models.TextField(blank=True, null=True, verbose_name="Defect Pattern")
    
    # Additional Data
    test_duration = models.PositiveIntegerField(blank=True, null=True, verbose_name="Test Duration (minutes)")
    test_reliability = models.CharField(max_length=20, blank=True, null=True, verbose_name="Test Reliability")
    
    class Meta:
        verbose_name = "Visual Field Test"
        verbose_name_plural = "Visual Field Tests"
        ordering = ['-test_date']
    
    def __str__(self):
        return f"VF Test {self.test_number} - {self.patient.full_name} ({self.eye_tested})"


class OphthalmologyEquipment(models.Model):
    """Ophthalmology Equipment Management"""
    EQUIPMENT_TYPE_CHOICES = [
        ('SLIT_LAMP', 'Slit Lamp'),
        ('TONOMETER', 'Tonometer'),
        ('OPHTHALMOSCOPE', 'Ophthalmoscope'),
        ('AUTOREFRACTOR', 'Auto Refractor'),
        ('KERATOMETER', 'Keratometer'),
        ('OCT', 'Optical Coherence Tomography'),
        ('FUNDUS_CAMERA', 'Fundus Camera'),
        ('PERIMETER', 'Visual Field Analyzer'),
        ('ULTRASOUND', 'Ophthalmic Ultrasound'),
        ('LASER', 'Ophthalmic Laser'),
        ('MICROSCOPE', 'Operating Microscope'),
        ('PHACOEMULSIFIER', 'Phacoemulsifier'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('REPAIR', 'Under Repair'),
        ('RETIRED', 'Retired'),
    ]
    
    # Basic Information
    equipment_name = models.CharField(max_length=100, verbose_name="Equipment Name")
    equipment_type = models.CharField(max_length=20, choices=EQUIPMENT_TYPE_CHOICES, verbose_name="Equipment Type")
    model = models.CharField(max_length=100, verbose_name="Model")
    manufacturer = models.CharField(max_length=100, verbose_name="Manufacturer")
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Serial Number")
    
    # Location and Assignment
    location = models.CharField(max_length=200, verbose_name="Location")
    assigned_to = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_eye_equipment')
    
    # Dates
    purchase_date = models.DateField(verbose_name="Purchase Date")
    installation_date = models.DateField(verbose_name="Installation Date")
    warranty_expiry = models.DateField(blank=True, null=True, verbose_name="Warranty Expiry")
    
    # Maintenance
    last_maintenance = models.DateField(blank=True, null=True, verbose_name="Last Maintenance")
    next_maintenance = models.DateField(blank=True, null=True, verbose_name="Next Maintenance")
    maintenance_interval_days = models.PositiveIntegerField(default=90, verbose_name="Maintenance Interval (Days)")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name="Status")
    
    # Additional Information
    specifications = models.TextField(blank=True, null=True, verbose_name="Specifications")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Ophthalmology Equipment"
        verbose_name_plural = "Ophthalmology Equipment"
        ordering = ['equipment_name']
    
    def __str__(self):
        return f"{self.equipment_name} ({self.serial_number})" 