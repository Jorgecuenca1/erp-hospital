from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import Patient, HMSUser, Department, MedicalRecord, Appointment
from acs_hms_hospitalization.models import Admission


class LabTestCategory(models.Model):
    """Laboratory Test Categories"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    code = models.CharField(max_length=20, unique=True, verbose_name="Category Code")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Lab Test Category"
        verbose_name_plural = "Lab Test Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class LabTest(models.Model):
    """Laboratory Tests"""
    TEST_TYPE_CHOICES = [
        ('BLOOD', 'Blood Test'),
        ('URINE', 'Urine Test'),
        ('STOOL', 'Stool Test'),
        ('CULTURE', 'Culture'),
        ('BIOCHEMISTRY', 'Biochemistry'),
        ('HEMATOLOGY', 'Hematology'),
        ('IMMUNOLOGY', 'Immunology'),
        ('MICROBIOLOGY', 'Microbiology'),
        ('PATHOLOGY', 'Pathology'),
        ('RADIOLOGY', 'Radiology'),
        ('MOLECULAR', 'Molecular'),
        ('GENETIC', 'Genetic'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Test Name")
    code = models.CharField(max_length=20, unique=True, verbose_name="Test Code")
    category = models.ForeignKey(LabTestCategory, on_delete=models.CASCADE, related_name='tests')
    test_type = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES, verbose_name="Test Type")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    
    # Test Requirements
    sample_type = models.CharField(max_length=100, verbose_name="Sample Type")
    sample_volume = models.CharField(max_length=50, blank=True, null=True, verbose_name="Sample Volume")
    container_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Container Type")
    special_instructions = models.TextField(blank=True, null=True, verbose_name="Special Instructions")
    
    # Test Properties
    reference_range = models.CharField(max_length=200, blank=True, null=True, verbose_name="Reference Range")
    units = models.CharField(max_length=50, blank=True, null=True, verbose_name="Units")
    normal_range_min = models.FloatField(blank=True, null=True, verbose_name="Normal Range Min")
    normal_range_max = models.FloatField(blank=True, null=True, verbose_name="Normal Range Max")
    
    # Processing
    processing_time = models.DurationField(verbose_name="Processing Time")
    requires_fasting = models.BooleanField(default=False, verbose_name="Requires Fasting")
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_outsourced = models.BooleanField(default=False, verbose_name="Outsourced")
    
    class Meta:
        verbose_name = "Lab Test"
        verbose_name_plural = "Lab Tests"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class LabEquipment(models.Model):
    """Laboratory Equipment"""
    name = models.CharField(max_length=200, verbose_name="Equipment Name")
    model = models.CharField(max_length=100, verbose_name="Model")
    manufacturer = models.CharField(max_length=100, verbose_name="Manufacturer")
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Serial Number")
    
    # Location
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='lab_equipment')
    location = models.CharField(max_length=200, verbose_name="Location")
    
    # Specifications
    specifications = models.TextField(blank=True, null=True, verbose_name="Specifications")
    
    # Maintenance
    installation_date = models.DateField(verbose_name="Installation Date")
    last_maintenance_date = models.DateField(blank=True, null=True, verbose_name="Last Maintenance Date")
    next_maintenance_date = models.DateField(blank=True, null=True, verbose_name="Next Maintenance Date")
    warranty_expiry = models.DateField(blank=True, null=True, verbose_name="Warranty Expiry")
    
    # Status
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('REPAIR', 'Under Repair'),
        ('RETIRED', 'Retired'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name="Status")
    
    class Meta:
        verbose_name = "Lab Equipment"
        verbose_name_plural = "Lab Equipment"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.serial_number})"


class LabTestOrder(models.Model):
    """Laboratory Test Orders"""
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SAMPLE_COLLECTED', 'Sample Collected'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('REJECTED', 'Rejected'),
    ]
    
    PRIORITY_CHOICES = [
        ('ROUTINE', 'Routine'),
        ('URGENT', 'Urgent'),
        ('STAT', 'STAT'),
        ('ASAP', 'ASAP'),
    ]
    
    # Order Information
    order_number = models.CharField(max_length=20, unique=True, verbose_name="Order Number")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_orders')
    ordered_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='ordered_lab_tests', limit_choices_to={'user_type': 'DOCTOR'})
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Order Date")
    
    # Clinical Information
    clinical_notes = models.TextField(blank=True, null=True, verbose_name="Clinical Notes")
    diagnosis = models.TextField(blank=True, null=True, verbose_name="Diagnosis")
    
    # Relationships
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_orders')
    admission = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_orders')
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_orders')
    
    # Status
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING', verbose_name="Status")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='ROUTINE', verbose_name="Priority")
    
    # Processing
    sample_collected_date = models.DateTimeField(blank=True, null=True, verbose_name="Sample Collected Date")
    collected_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='collected_samples')
    
    # Financial
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total Amount")
    insurance_covered = models.BooleanField(default=False, verbose_name="Insurance Covered")
    
    class Meta:
        verbose_name = "Lab Test Order"
        verbose_name_plural = "Lab Test Orders"
        ordering = ['-order_date']
    
    def __str__(self):
        return f"Order {self.order_number} - {self.patient.full_name}"


class LabTestOrderItem(models.Model):
    """Individual tests in a lab order"""
    order = models.ForeignKey(LabTestOrder, on_delete=models.CASCADE, related_name='test_items')
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")
    
    # Test Status
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SAMPLE_COLLECTED', 'Sample Collected'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('REJECTED', 'Rejected'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")
    
    class Meta:
        verbose_name = "Lab Test Order Item"
        verbose_name_plural = "Lab Test Order Items"
        unique_together = ['order', 'test']
    
    def __str__(self):
        return f"{self.test.name} - {self.order.order_number}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class LabSample(models.Model):
    """Laboratory Sample Management"""
    SAMPLE_STATUS_CHOICES = [
        ('COLLECTED', 'Collected'),
        ('RECEIVED', 'Received'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
        ('LOST', 'Lost'),
    ]
    
    # Sample Information
    sample_number = models.CharField(max_length=20, unique=True, verbose_name="Sample Number")
    order = models.ForeignKey(LabTestOrder, on_delete=models.CASCADE, related_name='samples')
    sample_type = models.CharField(max_length=100, verbose_name="Sample Type")
    
    # Collection Information
    collection_date = models.DateTimeField(verbose_name="Collection Date")
    collected_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='collected_lab_samples')
    collection_notes = models.TextField(blank=True, null=True, verbose_name="Collection Notes")
    
    # Sample Properties
    volume = models.CharField(max_length=50, blank=True, null=True, verbose_name="Volume")
    container_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Container Type")
    
    # Handling
    received_date = models.DateTimeField(blank=True, null=True, verbose_name="Received Date")
    received_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_lab_samples')
    
    # Quality Control
    quality_acceptable = models.BooleanField(default=True, verbose_name="Quality Acceptable")
    quality_notes = models.TextField(blank=True, null=True, verbose_name="Quality Notes")
    
    # Status
    status = models.CharField(max_length=20, choices=SAMPLE_STATUS_CHOICES, default='COLLECTED', verbose_name="Status")
    
    class Meta:
        verbose_name = "Lab Sample"
        verbose_name_plural = "Lab Samples"
        ordering = ['-collection_date']
    
    def __str__(self):
        return f"Sample {self.sample_number} - {self.order.patient.full_name}"


class LabResult(models.Model):
    """Laboratory Test Results"""
    RESULT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PRELIMINARY', 'Preliminary'),
        ('FINAL', 'Final'),
        ('AMENDED', 'Amended'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    # Result Information
    order_item = models.OneToOneField(LabTestOrderItem, on_delete=models.CASCADE, related_name='result')
    sample = models.ForeignKey(LabSample, on_delete=models.CASCADE, related_name='results')
    
    # Result Data
    result_value = models.TextField(blank=True, null=True, verbose_name="Result Value")
    numeric_value = models.FloatField(blank=True, null=True, verbose_name="Numeric Value")
    result_text = models.TextField(blank=True, null=True, verbose_name="Result Text")
    
    # Reference and Analysis
    reference_range = models.CharField(max_length=200, blank=True, null=True, verbose_name="Reference Range")
    units = models.CharField(max_length=50, blank=True, null=True, verbose_name="Units")
    abnormal_flag = models.BooleanField(default=False, verbose_name="Abnormal Flag")
    critical_flag = models.BooleanField(default=False, verbose_name="Critical Flag")
    
    # Processing Information
    tested_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='tested_results')
    equipment_used = models.ForeignKey(LabEquipment, on_delete=models.SET_NULL, null=True, blank=True, related_name='test_results')
    test_date = models.DateTimeField(verbose_name="Test Date")
    
    # Validation
    validated_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='validated_results', limit_choices_to={'user_type__in': ['DOCTOR', 'LABORATORY_TECHNICIAN']})
    validated_date = models.DateTimeField(blank=True, null=True, verbose_name="Validated Date")
    
    # Status
    status = models.CharField(max_length=20, choices=RESULT_STATUS_CHOICES, default='PENDING', verbose_name="Status")
    
    # Comments
    technician_comments = models.TextField(blank=True, null=True, verbose_name="Technician Comments")
    pathologist_comments = models.TextField(blank=True, null=True, verbose_name="Pathologist Comments")
    
    class Meta:
        verbose_name = "Lab Result"
        verbose_name_plural = "Lab Results"
        ordering = ['-test_date']
    
    def __str__(self):
        return f"Result - {self.order_item.test.name} for {self.sample.order.patient.full_name}"


class LabReport(models.Model):
    """Laboratory Report Generation"""
    REPORT_STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('FINAL', 'Final'),
        ('DELIVERED', 'Delivered'),
    ]
    
    # Report Information
    report_number = models.CharField(max_length=20, unique=True, verbose_name="Report Number")
    order = models.OneToOneField(LabTestOrder, on_delete=models.CASCADE, related_name='report')
    
    # Report Generation
    generated_date = models.DateTimeField(auto_now_add=True, verbose_name="Generated Date")
    generated_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='generated_reports')
    
    # Report Content
    report_summary = models.TextField(blank=True, null=True, verbose_name="Report Summary")
    interpretation = models.TextField(blank=True, null=True, verbose_name="Interpretation")
    recommendations = models.TextField(blank=True, null=True, verbose_name="Recommendations")
    
    # Validation
    reviewed_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_reports', limit_choices_to={'user_type': 'DOCTOR'})
    reviewed_date = models.DateTimeField(blank=True, null=True, verbose_name="Reviewed Date")
    
    # Status
    status = models.CharField(max_length=20, choices=REPORT_STATUS_CHOICES, default='DRAFT', verbose_name="Status")
    
    # Delivery
    delivered_to = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='delivered_reports')
    delivery_date = models.DateTimeField(blank=True, null=True, verbose_name="Delivery Date")
    delivery_method = models.CharField(max_length=50, blank=True, null=True, verbose_name="Delivery Method")
    
    class Meta:
        verbose_name = "Lab Report"
        verbose_name_plural = "Lab Reports"
        ordering = ['-generated_date']
    
    def __str__(self):
        return f"Report {self.report_number} - {self.order.patient.full_name}"


class LabQualityControl(models.Model):
    """Laboratory Quality Control"""
    QC_TYPE_CHOICES = [
        ('DAILY', 'Daily QC'),
        ('WEEKLY', 'Weekly QC'),
        ('MONTHLY', 'Monthly QC'),
        ('CALIBRATION', 'Calibration'),
        ('MAINTENANCE', 'Maintenance'),
    ]
    
    # QC Information
    qc_date = models.DateField(verbose_name="QC Date")
    qc_type = models.CharField(max_length=20, choices=QC_TYPE_CHOICES, verbose_name="QC Type")
    equipment = models.ForeignKey(LabEquipment, on_delete=models.CASCADE, related_name='quality_controls')
    performed_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='performed_qcs')
    
    # QC Results
    control_lot = models.CharField(max_length=50, blank=True, null=True, verbose_name="Control Lot")
    expected_value = models.CharField(max_length=100, blank=True, null=True, verbose_name="Expected Value")
    actual_value = models.CharField(max_length=100, blank=True, null=True, verbose_name="Actual Value")
    
    # Status
    passed = models.BooleanField(default=True, verbose_name="Passed")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    
    # Corrective Actions
    corrective_action_required = models.BooleanField(default=False, verbose_name="Corrective Action Required")
    corrective_action_taken = models.TextField(blank=True, null=True, verbose_name="Corrective Action Taken")
    
    class Meta:
        verbose_name = "Lab Quality Control"
        verbose_name_plural = "Lab Quality Controls"
        ordering = ['-qc_date']
    
    def __str__(self):
        return f"QC {self.qc_type} - {self.equipment.name} ({self.qc_date})"


class LabWorkshift(models.Model):
    """Laboratory Work Shifts"""
    SHIFT_CHOICES = [
        ('MORNING', 'Morning'),
        ('AFTERNOON', 'Afternoon'),
        ('EVENING', 'Evening'),
        ('NIGHT', 'Night'),
    ]
    
    # Shift Information
    shift_date = models.DateField(verbose_name="Shift Date")
    shift_type = models.CharField(max_length=20, choices=SHIFT_CHOICES, verbose_name="Shift Type")
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")
    
    # Staff
    supervisor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='supervised_shifts')
    technicians = models.ManyToManyField(HMSUser, related_name='lab_shifts', limit_choices_to={'user_type': 'LABORATORY_TECHNICIAN'})
    
    # Statistics
    samples_processed = models.PositiveIntegerField(default=0, verbose_name="Samples Processed")
    tests_completed = models.PositiveIntegerField(default=0, verbose_name="Tests Completed")
    
    # Notes
    shift_notes = models.TextField(blank=True, null=True, verbose_name="Shift Notes")
    
    class Meta:
        verbose_name = "Lab Work Shift"
        verbose_name_plural = "Lab Work Shifts"
        ordering = ['-shift_date', '-start_time']
    
    def __str__(self):
        return f"{self.shift_type} Shift - {self.shift_date}" 