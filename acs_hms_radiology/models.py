from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser, Patient, Appointment
import uuid


class RadiologyModality(models.Model):
    """Radiology imaging modalities"""
    MODALITY_CHOICES = [
        ('XR', 'X-Ray'),
        ('CT', 'CT Scan'),
        ('MRI', 'MRI'),
        ('US', 'Ultrasound'),
        ('NM', 'Nuclear Medicine'),
        ('PET', 'PET Scan'),
        ('MAMMO', 'Mammography'),
        ('FLUORO', 'Fluoroscopy'),
        ('ANGIO', 'Angiography'),
        ('DEXA', 'DEXA Scan'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    modality_code = models.CharField(max_length=10, choices=MODALITY_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    # Technical specifications
    manufacturer = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    
    # Capabilities
    max_resolution = models.CharField(max_length=50, blank=True)
    supported_formats = models.CharField(max_length=200, blank=True)
    contrast_capable = models.BooleanField(default=False)
    
    # Location and status
    location = models.CharField(max_length=200, blank=True)
    room_number = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Maintenance
    last_calibration = models.DateTimeField(null=True, blank=True)
    next_calibration = models.DateTimeField(null=True, blank=True)
    maintenance_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['modality_code', 'name']
        verbose_name = 'Radiology Modality'
        verbose_name_plural = 'Radiology Modalities'
    
    def __str__(self):
        return f"{self.name} ({self.modality_code})"


class RadiologyExam(models.Model):
    """Radiology examination types"""
    BODY_PART_CHOICES = [
        ('head', 'Head'),
        ('neck', 'Neck'),
        ('chest', 'Chest'),
        ('abdomen', 'Abdomen'),
        ('pelvis', 'Pelvis'),
        ('spine', 'Spine'),
        ('extremities', 'Extremities'),
        ('cardiac', 'Cardiac'),
        ('vascular', 'Vascular'),
        ('breast', 'Breast'),
        ('other', 'Other'),
    ]
    
    exam_code = models.CharField(max_length=20, unique=True)
    exam_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Exam details
    modality = models.ForeignKey(RadiologyModality, on_delete=models.CASCADE, related_name='exams')
    body_part = models.CharField(max_length=20, choices=BODY_PART_CHOICES)
    
    # Preparation requirements
    prep_instructions = models.TextField(blank=True)
    fasting_required = models.BooleanField(default=False)
    contrast_required = models.BooleanField(default=False)
    
    # Timing
    estimated_duration = models.IntegerField(default=30, help_text="Duration in minutes")
    
    # Pricing
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    insurance_code = models.CharField(max_length=20, blank=True)
    
    # Clinical information
    common_indications = models.TextField(blank=True)
    contraindications = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['modality', 'exam_name']
        verbose_name = 'Radiology Exam'
        verbose_name_plural = 'Radiology Exams'
    
    def __str__(self):
        return f"{self.exam_name} ({self.exam_code})"


class RadiologyOrder(models.Model):
    """Radiology study orders"""
    PRIORITY_CHOICES = [
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('stat', 'STAT'),
        ('add_on', 'Add-on'),
    ]
    
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('hold', 'Hold'),
    ]
    
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='radiology_orders')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True, related_name='radiology_orders')
    
    # Order details
    exam = models.ForeignKey(RadiologyExam, on_delete=models.CASCADE, related_name='orders')
    ordering_physician = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='radiology_orders')
    
    # Clinical information
    clinical_indication = models.TextField()
    clinical_history = models.TextField(blank=True)
    provisional_diagnosis = models.TextField(blank=True)
    
    # Order status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='routine')
    
    # Scheduling
    ordered_date = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    
    # Special instructions
    special_instructions = models.TextField(blank=True)
    contrast_allergies = models.TextField(blank=True)
    
    # Pregnancy screening
    pregnancy_status = models.CharField(max_length=20, choices=[
        ('not_applicable', 'Not Applicable'),
        ('not_pregnant', 'Not Pregnant'),
        ('pregnant', 'Pregnant'),
        ('unknown', 'Unknown'),
    ], default='not_applicable')
    
    # Authorization
    insurance_authorized = models.BooleanField(default=False)
    authorization_number = models.CharField(max_length=100, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-ordered_date']
        verbose_name = 'Radiology Order'
        verbose_name_plural = 'Radiology Orders'
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"RO{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.order_id} - {self.patient.name} - {self.exam.exam_name}"


class RadiologyStudy(models.Model):
    """Radiology study execution"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    study_id = models.CharField(max_length=20, unique=True, blank=True)
    order = models.OneToOneField(RadiologyOrder, on_delete=models.CASCADE, related_name='study')
    
    # Study execution
    study_date = models.DateTimeField()
    technologist = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='radiology_studies')
    modality = models.ForeignKey(RadiologyModality, on_delete=models.CASCADE, related_name='studies')
    
    # Study details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Technical parameters
    kvp = models.IntegerField(null=True, blank=True)
    mas = models.IntegerField(null=True, blank=True)
    slice_thickness = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Contrast information
    contrast_used = models.BooleanField(default=False)
    contrast_type = models.CharField(max_length=100, blank=True)
    contrast_volume = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    # Quality control
    image_quality = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('acceptable', 'Acceptable'),
        ('poor', 'Poor'),
    ], blank=True)
    
    # Study notes
    technical_notes = models.TextField(blank=True)
    
    # Image information
    number_of_images = models.IntegerField(default=0)
    storage_location = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-study_date']
        verbose_name = 'Radiology Study'
        verbose_name_plural = 'Radiology Studies'
    
    def save(self, *args, **kwargs):
        if not self.study_id:
            self.study_id = f"RS{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.study_id} - {self.order.patient.name}"
    
    @property
    def duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


class RadiologyImage(models.Model):
    """Individual radiology images"""
    IMAGE_TYPE_CHOICES = [
        ('DICOM', 'DICOM'),
        ('JPEG', 'JPEG'),
        ('PNG', 'PNG'),
        ('TIFF', 'TIFF'),
        ('BMP', 'BMP'),
    ]
    
    image_id = models.CharField(max_length=20, unique=True, blank=True)
    study = models.ForeignKey(RadiologyStudy, on_delete=models.CASCADE, related_name='images')
    
    # Image details
    image_number = models.IntegerField()
    series_number = models.IntegerField(default=1)
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES, default='DICOM')
    
    # File information
    file_path = models.CharField(max_length=500, blank=True)
    file_size = models.BigIntegerField(default=0)
    file_format = models.CharField(max_length=20, blank=True)
    
    # Image parameters
    matrix_size = models.CharField(max_length=50, blank=True)
    pixel_spacing = models.CharField(max_length=50, blank=True)
    slice_location = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Annotations
    annotations = models.JSONField(default=dict, blank=True)
    measurements = models.JSONField(default=list, blank=True)
    
    # Quality
    image_quality = models.CharField(max_length=20, choices=[
        ('diagnostic', 'Diagnostic'),
        ('limited', 'Limited'),
        ('non_diagnostic', 'Non-diagnostic'),
    ], default='diagnostic')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['study', 'series_number', 'image_number']
        verbose_name = 'Radiology Image'
        verbose_name_plural = 'Radiology Images'
    
    def save(self, *args, **kwargs):
        if not self.image_id:
            self.image_id = f"IMG{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.image_id} - {self.study.study_id} - Image {self.image_number}"


class RadiologyReport(models.Model):
    """Radiology interpretation reports"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('revised', 'Revised'),
        ('addendum', 'Addendum'),
    ]
    
    report_id = models.CharField(max_length=20, unique=True, blank=True)
    study = models.OneToOneField(RadiologyStudy, on_delete=models.CASCADE, related_name='report')
    
    # Report details
    radiologist = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='radiology_reports')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Report content
    clinical_history = models.TextField(blank=True)
    technique = models.TextField(blank=True)
    findings = models.TextField()
    impression = models.TextField()
    recommendations = models.TextField(blank=True)
    
    # Critical findings
    critical_findings = models.BooleanField(default=False)
    critical_communicated = models.BooleanField(default=False)
    communication_method = models.CharField(max_length=50, blank=True)
    communicated_to = models.CharField(max_length=200, blank=True)
    communication_time = models.DateTimeField(null=True, blank=True)
    
    # Comparison
    comparison_studies = models.TextField(blank=True)
    comparison_findings = models.TextField(blank=True)
    
    # Report timing
    dictated_date = models.DateTimeField(null=True, blank=True)
    transcribed_date = models.DateTimeField(null=True, blank=True)
    finalized_date = models.DateTimeField(null=True, blank=True)
    
    # Follow-up
    follow_up_required = models.BooleanField(default=False)
    follow_up_timeframe = models.CharField(max_length=100, blank=True)
    follow_up_instructions = models.TextField(blank=True)
    
    # Addendum
    addendum_text = models.TextField(blank=True)
    addendum_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Radiology Report'
        verbose_name_plural = 'Radiology Reports'
    
    def save(self, *args, **kwargs):
        if not self.report_id:
            self.report_id = f"RR{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.report_id} - {self.study.order.patient.name}"
    
    @property
    def turnaround_time(self):
        if self.study.end_time and self.finalized_date:
            return self.finalized_date - self.study.end_time
        return None


class RadiologyProtocol(models.Model):
    """Imaging protocols for different exams"""
    protocol_id = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=200)
    exam = models.ForeignKey(RadiologyExam, on_delete=models.CASCADE, related_name='protocols')
    
    # Protocol details
    description = models.TextField(blank=True)
    indication = models.TextField(blank=True)
    
    # Technical parameters
    kvp_range = models.CharField(max_length=50, blank=True)
    mas_range = models.CharField(max_length=50, blank=True)
    slice_thickness = models.CharField(max_length=50, blank=True)
    reconstruction_algorithm = models.CharField(max_length=100, blank=True)
    
    # Contrast protocol
    contrast_protocol = models.TextField(blank=True)
    contrast_timing = models.CharField(max_length=100, blank=True)
    
    # Positioning
    patient_position = models.CharField(max_length=100, blank=True)
    anatomical_coverage = models.TextField(blank=True)
    
    # Instructions
    patient_instructions = models.TextField(blank=True)
    technologist_instructions = models.TextField(blank=True)
    
    # Version control
    version = models.CharField(max_length=20, default='1.0')
    effective_date = models.DateField()
    
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='created_protocols')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['exam', 'name']
        verbose_name = 'Radiology Protocol'
        verbose_name_plural = 'Radiology Protocols'
    
    def save(self, *args, **kwargs):
        if not self.protocol_id:
            self.protocol_id = f"RP{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.exam.exam_name}"


class RadiologySettings(models.Model):
    """System-wide radiology settings"""
    # Image storage
    default_storage_path = models.CharField(max_length=500, default='/media/radiology/')
    backup_storage_path = models.CharField(max_length=500, blank=True)
    
    # DICOM settings
    dicom_ae_title = models.CharField(max_length=16, default='HOSPITAL')
    dicom_port = models.IntegerField(default=104)
    pacs_server = models.CharField(max_length=200, blank=True)
    
    # Report settings
    auto_send_reports = models.BooleanField(default=True)
    critical_result_notification = models.BooleanField(default=True)
    
    # Quality control
    image_quality_checks = models.BooleanField(default=True)
    mandatory_peer_review = models.BooleanField(default=False)
    
    # Scheduling
    default_appointment_duration = models.IntegerField(default=30)
    max_studies_per_day = models.IntegerField(default=50)
    
    # Patient safety
    pregnancy_screening_required = models.BooleanField(default=True)
    contrast_allergy_screening = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Radiology Settings'
        verbose_name_plural = 'Radiology Settings'
    
    def __str__(self):
        return f"Radiology Settings - {self.created_at.date()}" 