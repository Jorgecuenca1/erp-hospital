from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser, Patient, Appointment
import uuid


class SurgeryType(models.Model):
    """Types of surgeries available in the hospital"""
    SPECIALTY_CHOICES = [
        ('general', 'General Surgery'),
        ('cardiac', 'Cardiac Surgery'),
        ('orthopedic', 'Orthopedic Surgery'),
        ('neurological', 'Neurological Surgery'),
        ('plastic', 'Plastic Surgery'),
        ('ophthalmology', 'Ophthalmology Surgery'),
        ('gynecology', 'Gynecological Surgery'),
        ('pediatric', 'Pediatric Surgery'),
        ('vascular', 'Vascular Surgery'),
        ('thoracic', 'Thoracic Surgery'),
        ('urological', 'Urological Surgery'),
        ('oncological', 'Oncological Surgery'),
        ('gastroenterology', 'Gastroenterological Surgery'),
        ('ent', 'ENT Surgery'),
        ('dermatology', 'Dermatological Surgery'),
    ]
    
    RISK_LEVEL_CHOICES = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    specialty = models.CharField(max_length=20, choices=SPECIALTY_CHOICES)
    description = models.TextField()
    estimated_duration = models.IntegerField(help_text="Duration in minutes", validators=[MinValueValidator(1)])
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, default='medium')
    requires_anesthesia = models.BooleanField(default=True)
    requires_icu = models.BooleanField(default=False)
    requires_blood_bank = models.BooleanField(default=False)
    standard_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['specialty', 'name']
        verbose_name = 'Surgery Type'
        verbose_name_plural = 'Surgery Types'
    
    def __str__(self):
        return f"{self.name} ({self.specialty})"


class OperationTheater(models.Model):
    """Operation theaters/rooms management"""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('cleaning', 'Cleaning'),
        ('reserved', 'Reserved'),
    ]
    
    THEATER_TYPE_CHOICES = [
        ('general', 'General Purpose'),
        ('cardiac', 'Cardiac Surgery'),
        ('orthopedic', 'Orthopedic Surgery'),
        ('neurological', 'Neurological Surgery'),
        ('emergency', 'Emergency Surgery'),
        ('day_surgery', 'Day Surgery'),
        ('hybrid', 'Hybrid Theater'),
    ]
    
    name = models.CharField(max_length=100)
    theater_number = models.CharField(max_length=20, unique=True)
    theater_type = models.CharField(max_length=20, choices=THEATER_TYPE_CHOICES)
    floor = models.CharField(max_length=20)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    equipment_list = models.TextField(blank=True)
    last_maintenance = models.DateTimeField(null=True, blank=True)
    next_maintenance = models.DateTimeField(null=True, blank=True)
    temperature_control = models.BooleanField(default=True)
    air_filtration = models.BooleanField(default=True)
    emergency_backup = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['theater_number']
        verbose_name = 'Operation Theater'
        verbose_name_plural = 'Operation Theaters'
    
    def __str__(self):
        return f"{self.name} - {self.theater_number}"


class SurgeryTeam(models.Model):
    """Surgery team members and their roles"""
    ROLE_CHOICES = [
        ('primary_surgeon', 'Primary Surgeon'),
        ('assistant_surgeon', 'Assistant Surgeon'),
        ('anesthesiologist', 'Anesthesiologist'),
        ('scrub_nurse', 'Scrub Nurse'),
        ('circulating_nurse', 'Circulating Nurse'),
        ('technician', 'Technician'),
        ('resident', 'Resident'),
        ('observer', 'Observer'),
    ]
    
    name = models.CharField(max_length=200)
    user = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='surgery_teams')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    specialization = models.CharField(max_length=200, blank=True)
    experience_years = models.IntegerField(validators=[MinValueValidator(0)])
    certification = models.CharField(max_length=200, blank=True)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['role', 'name']
        verbose_name = 'Surgery Team Member'
        verbose_name_plural = 'Surgery Team Members'
    
    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"


class Surgery(models.Model):
    """Main surgery records"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('pre_op', 'Pre-Operative'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
        ('emergency', 'Emergency'),
    ]
    
    ANESTHESIA_TYPE_CHOICES = [
        ('general', 'General Anesthesia'),
        ('regional', 'Regional Anesthesia'),
        ('local', 'Local Anesthesia'),
        ('spinal', 'Spinal Anesthesia'),
        ('epidural', 'Epidural Anesthesia'),
        ('conscious_sedation', 'Conscious Sedation'),
        ('none', 'No Anesthesia'),
    ]
    
    PRIORITY_CHOICES = [
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
        ('elective', 'Elective'),
    ]
    
    surgery_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='surgeries')
    surgery_type = models.ForeignKey(SurgeryType, on_delete=models.CASCADE)
    operation_theater = models.ForeignKey(OperationTheater, on_delete=models.CASCADE)
    primary_surgeon = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='primary_surgeries')
    team_members = models.ManyToManyField(SurgeryTeam, blank=True)
    
    scheduled_date = models.DateTimeField()
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='routine')
    anesthesia_type = models.CharField(max_length=20, choices=ANESTHESIA_TYPE_CHOICES, default='general')
    
    # Pre-operative information
    pre_op_diagnosis = models.TextField()
    pre_op_notes = models.TextField(blank=True)
    pre_op_vitals = models.JSONField(default=dict, blank=True)
    pre_op_checklist = models.JSONField(default=dict, blank=True)
    
    # Intra-operative information
    operative_procedure = models.TextField(blank=True)
    operative_notes = models.TextField(blank=True)
    intra_operative_complications = models.TextField(blank=True)
    blood_loss = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fluids_given = models.TextField(blank=True)
    
    # Post-operative information
    post_op_diagnosis = models.TextField(blank=True)
    post_op_notes = models.TextField(blank=True)
    post_op_instructions = models.TextField(blank=True)
    recovery_notes = models.TextField(blank=True)
    
    # Financial information
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Administrative
    consent_obtained = models.BooleanField(default=False)
    consent_date = models.DateTimeField(null=True, blank=True)
    insurance_approved = models.BooleanField(default=False)
    
    cancelled_reason = models.TextField(blank=True)
    cancelled_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='cancelled_surgeries')
    cancelled_date = models.DateTimeField(null=True, blank=True)
    
    created_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='created_surgeries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_date']
        verbose_name = 'Surgery'
        verbose_name_plural = 'Surgeries'
    
    def save(self, *args, **kwargs):
        if not self.surgery_id:
            self.surgery_id = f"SUR{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.surgery_id} - {self.patient.name} - {self.surgery_type.name}"
    
    @property
    def duration(self):
        """Calculate surgery duration"""
        if self.actual_start_time and self.actual_end_time:
            return self.actual_end_time - self.actual_start_time
        return None
    
    @property
    def is_completed(self):
        return self.status == 'completed'
    
    @property
    def is_in_progress(self):
        return self.status == 'in_progress'


class SurgeryEquipment(models.Model):
    """Equipment used in surgeries"""
    EQUIPMENT_TYPE_CHOICES = [
        ('surgical_instruments', 'Surgical Instruments'),
        ('monitoring_equipment', 'Monitoring Equipment'),
        ('anesthesia_machine', 'Anesthesia Machine'),
        ('ventilator', 'Ventilator'),
        ('electrocautery', 'Electrocautery'),
        ('laser', 'Laser Equipment'),
        ('microscope', 'Surgical Microscope'),
        ('c_arm', 'C-Arm'),
        ('defibrillator', 'Defibrillator'),
        ('infusion_pump', 'Infusion Pump'),
        ('suction_unit', 'Suction Unit'),
        ('other', 'Other Equipment'),
    ]
    
    name = models.CharField(max_length=200)
    equipment_type = models.CharField(max_length=30, choices=EQUIPMENT_TYPE_CHOICES)
    model = models.CharField(max_length=100, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, unique=True)
    operation_theater = models.ForeignKey(OperationTheater, on_delete=models.CASCADE, related_name='equipment')
    
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expires = models.DateField(null=True, blank=True)
    last_maintenance = models.DateTimeField(null=True, blank=True)
    next_maintenance = models.DateTimeField(null=True, blank=True)
    
    is_operational = models.BooleanField(default=True)
    maintenance_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['equipment_type', 'name']
        verbose_name = 'Surgery Equipment'
        verbose_name_plural = 'Surgery Equipment'
    
    def __str__(self):
        return f"{self.name} - {self.serial_number}"


class SurgerySupplies(models.Model):
    """Medical supplies used in surgeries"""
    SUPPLY_TYPE_CHOICES = [
        ('sutures', 'Sutures'),
        ('gauze', 'Gauze'),
        ('bandages', 'Bandages'),
        ('gloves', 'Gloves'),
        ('masks', 'Masks'),
        ('gowns', 'Surgical Gowns'),
        ('drapes', 'Surgical Drapes'),
        ('implants', 'Implants'),
        ('prosthetics', 'Prosthetics'),
        ('medications', 'Medications'),
        ('antiseptics', 'Antiseptics'),
        ('contrast_agents', 'Contrast Agents'),
        ('other', 'Other Supplies'),
    ]
    
    name = models.CharField(max_length=200)
    supply_type = models.CharField(max_length=20, choices=SUPPLY_TYPE_CHOICES)
    brand = models.CharField(max_length=100, blank=True)
    unit_of_measure = models.CharField(max_length=20, default='pieces')
    unit_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    stock_quantity = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=10)
    
    expiry_date = models.DateField(null=True, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    
    is_sterile = models.BooleanField(default=False)
    is_disposable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['supply_type', 'name']
        verbose_name = 'Surgery Supplies'
        verbose_name_plural = 'Surgery Supplies'
    
    def __str__(self):
        return f"{self.name} - {self.supply_type}"
    
    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.minimum_stock
    
    @property
    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False


class SurgerySupplyUsage(models.Model):
    """Track supplies used in each surgery"""
    surgery = models.ForeignKey(Surgery, on_delete=models.CASCADE, related_name='supply_usage')
    supply = models.ForeignKey(SurgerySupplies, on_delete=models.CASCADE)
    quantity_used = models.IntegerField(validators=[MinValueValidator(1)])
    unit_cost = models.DecimalField(max_digits=8, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    used_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-used_at']
        verbose_name = 'Surgery Supply Usage'
        verbose_name_plural = 'Surgery Supply Usage'
    
    def save(self, *args, **kwargs):
        self.total_cost = self.quantity_used * self.unit_cost
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.surgery.surgery_id} - {self.supply.name} - {self.quantity_used}"


class PostOperativeCare(models.Model):
    """Post-operative care instructions and monitoring"""
    CARE_TYPE_CHOICES = [
        ('wound_care', 'Wound Care'),
        ('medication', 'Medication'),
        ('diet', 'Diet Instructions'),
        ('activity', 'Activity Restrictions'),
        ('follow_up', 'Follow-up Appointments'),
        ('monitoring', 'Vital Signs Monitoring'),
        ('physiotherapy', 'Physiotherapy'),
        ('other', 'Other Care'),
    ]
    
    surgery = models.ForeignKey(Surgery, on_delete=models.CASCADE, related_name='post_op_care')
    care_type = models.CharField(max_length=20, choices=CARE_TYPE_CHOICES)
    instructions = models.TextField()
    frequency = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    
    assigned_to = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='assigned_post_op_care')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='created_post_op_care')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Post-Operative Care'
        verbose_name_plural = 'Post-Operative Care'
    
    def __str__(self):
        return f"{self.surgery.surgery_id} - {self.get_care_type_display()}"


class SurgeryComplications(models.Model):
    """Track complications during or after surgery"""
    COMPLICATION_TYPE_CHOICES = [
        ('bleeding', 'Bleeding'),
        ('infection', 'Infection'),
        ('anesthesia_reaction', 'Anesthesia Reaction'),
        ('organ_damage', 'Organ Damage'),
        ('blood_clot', 'Blood Clot'),
        ('pneumonia', 'Pneumonia'),
        ('wound_dehiscence', 'Wound Dehiscence'),
        ('allergic_reaction', 'Allergic Reaction'),
        ('cardiac_event', 'Cardiac Event'),
        ('respiratory_event', 'Respiratory Event'),
        ('other', 'Other Complication'),
    ]
    
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('critical', 'Critical'),
    ]
    
    surgery = models.ForeignKey(Surgery, on_delete=models.CASCADE, related_name='complications')
    complication_type = models.CharField(max_length=20, choices=COMPLICATION_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    description = models.TextField()
    
    occurred_at = models.DateTimeField()
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    treatment_given = models.TextField(blank=True)
    outcome = models.TextField(blank=True)
    
    reported_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='reported_complications')
    is_resolved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-occurred_at']
        verbose_name = 'Surgery Complication'
        verbose_name_plural = 'Surgery Complications'
    
    def __str__(self):
        return f"{self.surgery.surgery_id} - {self.get_complication_type_display()} ({self.severity})" 