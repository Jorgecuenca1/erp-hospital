from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser, Patient, Appointment
import uuid


class NursingUnit(models.Model):
    """Nursing units/departments"""
    UNIT_TYPE_CHOICES = [
        ('medical', 'Medical'),
        ('surgical', 'Surgical'),
        ('icu', 'ICU'),
        ('emergency', 'Emergency'),
        ('pediatric', 'Pediatric'),
        ('obstetric', 'Obstetric'),
        ('psychiatric', 'Psychiatric'),
        ('oncology', 'Oncology'),
        ('cardiac', 'Cardiac'),
        ('orthopedic', 'Orthopedic'),
        ('rehabilitation', 'Rehabilitation'),
        ('outpatient', 'Outpatient'),
    ]
    
    unit_id = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=200)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES, default='medical')
    
    # Location
    floor = models.CharField(max_length=20, blank=True)
    wing = models.CharField(max_length=50, blank=True)
    
    # Capacity
    bed_capacity = models.IntegerField(default=0)
    current_occupancy = models.IntegerField(default=0)
    
    # Staff
    nurse_manager = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_units')
    charge_nurse = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='charge_units')
    
    # Contact
    phone = models.CharField(max_length=20, blank=True)
    extension = models.CharField(max_length=10, blank=True)
    
    # Specialization
    specialty_services = models.TextField(blank=True)
    equipment_available = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Nursing Unit'
        verbose_name_plural = 'Nursing Units'
    
    def save(self, *args, **kwargs):
        if not self.unit_id:
            self.unit_id = f"NU{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.unit_id})"
    
    @property
    def occupancy_rate(self):
        if self.bed_capacity > 0:
            return (self.current_occupancy / self.bed_capacity) * 100
        return 0


class NursingShift(models.Model):
    """Nursing shifts and schedules"""
    SHIFT_TYPE_CHOICES = [
        ('day', 'Day Shift'),
        ('evening', 'Evening Shift'),
        ('night', 'Night Shift'),
        ('double', 'Double Shift'),
        ('on_call', 'On Call'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    shift_id = models.CharField(max_length=20, unique=True, blank=True)
    nurse = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='nursing_shifts')
    unit = models.ForeignKey(NursingUnit, on_delete=models.CASCADE, related_name='shifts')
    
    # Shift details
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPE_CHOICES, default='day')
    shift_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Actual times
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Patient assignment
    assigned_patients = models.ManyToManyField(Patient, blank=True, related_name='assigned_nurses')
    max_patients = models.IntegerField(default=6)
    
    # Break times
    break_start = models.TimeField(null=True, blank=True)
    break_end = models.TimeField(null=True, blank=True)
    lunch_start = models.TimeField(null=True, blank=True)
    lunch_end = models.TimeField(null=True, blank=True)
    
    # Overtime
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    overtime_reason = models.TextField(blank=True)
    
    # Notes
    shift_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-shift_date', '-start_time']
        verbose_name = 'Nursing Shift'
        verbose_name_plural = 'Nursing Shifts'
    
    def save(self, *args, **kwargs):
        if not self.shift_id:
            self.shift_id = f"NS{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nurse.user.get_full_name()} - {self.shift_date} {self.shift_type}"
    
    @property
    def duration(self):
        if self.actual_start and self.actual_end:
            return self.actual_end - self.actual_start
        return None


class NursingAssessment(models.Model):
    """Nursing assessments"""
    ASSESSMENT_TYPE_CHOICES = [
        ('admission', 'Admission Assessment'),
        ('daily', 'Daily Assessment'),
        ('shift', 'Shift Assessment'),
        ('discharge', 'Discharge Assessment'),
        ('focused', 'Focused Assessment'),
        ('pain', 'Pain Assessment'),
        ('fall_risk', 'Fall Risk Assessment'),
        ('skin', 'Skin Assessment'),
        ('nutrition', 'Nutrition Assessment'),
    ]
    
    assessment_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='nursing_assessments')
    nurse = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='nursing_assessments')
    
    # Assessment details
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE_CHOICES, default='shift')
    assessment_date = models.DateTimeField()
    
    # Vital signs
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pulse = models.IntegerField(null=True, blank=True)
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    respiratory_rate = models.IntegerField(null=True, blank=True)
    oxygen_saturation = models.IntegerField(null=True, blank=True)
    
    # Pain assessment
    pain_score = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    pain_location = models.CharField(max_length=200, blank=True)
    pain_description = models.TextField(blank=True)
    
    # Neurological assessment
    consciousness_level = models.CharField(max_length=20, choices=[
        ('alert', 'Alert'),
        ('drowsy', 'Drowsy'),
        ('confused', 'Confused'),
        ('unconscious', 'Unconscious'),
    ], blank=True)
    
    # Mobility assessment
    mobility_status = models.CharField(max_length=20, choices=[
        ('independent', 'Independent'),
        ('assist_1', 'Assist of 1'),
        ('assist_2', 'Assist of 2'),
        ('bedrest', 'Bedrest'),
        ('wheelchair', 'Wheelchair'),
    ], blank=True)
    
    # Skin assessment
    skin_condition = models.CharField(max_length=20, choices=[
        ('intact', 'Intact'),
        ('dry', 'Dry'),
        ('oily', 'Oily'),
        ('rash', 'Rash'),
        ('lesions', 'Lesions'),
        ('wounds', 'Wounds'),
    ], blank=True)
    
    # Fall risk
    fall_risk_score = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    fall_risk_level = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
    ], blank=True)
    
    # Nutrition
    appetite = models.CharField(max_length=20, choices=[
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ], blank=True)
    
    # Elimination
    bowel_sounds = models.CharField(max_length=20, choices=[
        ('normal', 'Normal'),
        ('hyperactive', 'Hyperactive'),
        ('hypoactive', 'Hypoactive'),
        ('absent', 'Absent'),
    ], blank=True)
    
    # Assessment notes
    assessment_notes = models.TextField(blank=True)
    nursing_diagnosis = models.TextField(blank=True)
    
    # Plans
    care_plan = models.TextField(blank=True)
    interventions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-assessment_date']
        verbose_name = 'Nursing Assessment'
        verbose_name_plural = 'Nursing Assessments'
    
    def save(self, *args, **kwargs):
        if not self.assessment_id:
            self.assessment_id = f"NA{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.assessment_id} - {self.patient.full_name} - {self.assessment_type}"


class NursingCare(models.Model):
    """Nursing care activities"""
    CARE_TYPE_CHOICES = [
        ('medication', 'Medication Administration'),
        ('vital_signs', 'Vital Signs'),
        ('wound_care', 'Wound Care'),
        ('hygiene', 'Personal Hygiene'),
        ('nutrition', 'Nutrition Support'),
        ('mobility', 'Mobility Assistance'),
        ('education', 'Patient Education'),
        ('monitoring', 'Patient Monitoring'),
        ('comfort', 'Comfort Measures'),
        ('safety', 'Safety Measures'),
        ('other', 'Other Care'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('deferred', 'Deferred'),
    ]
    
    care_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='nursing_care_activities')
    nurse = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='nursing_care_activities')
    
    # Care details
    care_type = models.CharField(max_length=20, choices=CARE_TYPE_CHOICES)
    care_description = models.TextField()
    
    # Scheduling
    scheduled_time = models.DateTimeField()
    estimated_duration = models.IntegerField(default=15, help_text="Duration in minutes")
    
    # Execution
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Outcomes
    outcome = models.TextField(blank=True)
    patient_response = models.TextField(blank=True)
    
    # Frequency
    frequency = models.CharField(max_length=50, blank=True)
    is_recurring = models.BooleanField(default=False)
    
    # Priority
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], default='medium')
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_time']
        verbose_name = 'Nursing Care'
        verbose_name_plural = 'Nursing Care'
    
    def save(self, *args, **kwargs):
        if not self.care_id:
            self.care_id = f"NC{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.care_id} - {self.patient.full_name} - {self.care_type}"
    
    @property
    def duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


class MedicationAdministration(models.Model):
    """Medication administration records"""
    ADMINISTRATION_ROUTE_CHOICES = [
        ('oral', 'Oral'),
        ('iv', 'Intravenous'),
        ('im', 'Intramuscular'),
        ('sc', 'Subcutaneous'),
        ('topical', 'Topical'),
        ('inhalation', 'Inhalation'),
        ('rectal', 'Rectal'),
        ('sublingual', 'Sublingual'),
        ('nasal', 'Nasal'),
        ('ophthalmic', 'Ophthalmic'),
        ('otic', 'Otic'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('given', 'Given'),
        ('refused', 'Refused'),
        ('held', 'Held'),
        ('omitted', 'Omitted'),
    ]
    
    mar_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medication_records')
    nurse = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='medication_administrations')
    
    # Medication details
    medication_name = models.CharField(max_length=200)
    dose = models.CharField(max_length=100)
    route = models.CharField(max_length=20, choices=ADMINISTRATION_ROUTE_CHOICES)
    frequency = models.CharField(max_length=100)
    
    # Scheduling
    scheduled_time = models.DateTimeField()
    administration_time = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Administration details
    site = models.CharField(max_length=100, blank=True)
    lot_number = models.CharField(max_length=50, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    
    # Patient response
    patient_response = models.TextField(blank=True)
    adverse_reactions = models.TextField(blank=True)
    
    # Reasons for not given
    reason_not_given = models.TextField(blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_time']
        verbose_name = 'Medication Administration'
        verbose_name_plural = 'Medication Administrations'
    
    def save(self, *args, **kwargs):
        if not self.mar_id:
            self.mar_id = f"MAR{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.mar_id} - {self.patient.full_name} - {self.medication_name}"


class NursingHandoff(models.Model):
    """Nursing shift handoffs"""
    handoff_id = models.CharField(max_length=20, unique=True, blank=True)
    
    # Handoff details
    outgoing_nurse = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='outgoing_handoffs')
    incoming_nurse = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='incoming_handoffs')
    unit = models.ForeignKey(NursingUnit, on_delete=models.CASCADE, related_name='handoffs')
    
    # Timing
    handoff_date = models.DateTimeField()
    
    # Patients
    patients = models.ManyToManyField(Patient, through='PatientHandoff', related_name='handoffs')
    
    # Unit status
    unit_census = models.IntegerField(default=0)
    admissions = models.IntegerField(default=0)
    discharges = models.IntegerField(default=0)
    transfers = models.IntegerField(default=0)
    
    # General notes
    unit_notes = models.TextField(blank=True)
    safety_concerns = models.TextField(blank=True)
    
    # Completion
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-handoff_date']
        verbose_name = 'Nursing Handoff'
        verbose_name_plural = 'Nursing Handoffs'
    
    def save(self, *args, **kwargs):
        if not self.handoff_id:
            self.handoff_id = f"HO{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.handoff_id} - {self.outgoing_nurse.user.get_full_name()} to {self.incoming_nurse.user.get_full_name()}"


class PatientHandoff(models.Model):
    """Individual patient handoff information"""
    handoff = models.ForeignKey(NursingHandoff, on_delete=models.CASCADE, related_name='patient_handoffs')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='handoff_records')
    
    # Patient status
    current_condition = models.TextField()
    recent_changes = models.TextField(blank=True)
    
    # Care plans
    active_orders = models.TextField(blank=True)
    pending_procedures = models.TextField(blank=True)
    
    # Concerns
    priority_concerns = models.TextField(blank=True)
    safety_issues = models.TextField(blank=True)
    
    # Family/social
    family_updates = models.TextField(blank=True)
    psychosocial_concerns = models.TextField(blank=True)
    
    # Education
    patient_education_needs = models.TextField(blank=True)
    
    # Discharge planning
    discharge_planning = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['patient__first_name']
        verbose_name = 'Patient Handoff'
        verbose_name_plural = 'Patient Handoffs'
    
    def __str__(self):
        return f"{self.handoff.handoff_id} - {self.patient.full_name}"


class NursingIncident(models.Model):
    """Nursing incident reports"""
    INCIDENT_TYPE_CHOICES = [
        ('fall', 'Patient Fall'),
        ('medication_error', 'Medication Error'),
        ('pressure_ulcer', 'Pressure Ulcer'),
        ('infection', 'Healthcare-Associated Infection'),
        ('equipment_failure', 'Equipment Failure'),
        ('patient_safety', 'Patient Safety Event'),
        ('staff_injury', 'Staff Injury'),
        ('violence', 'Violence/Aggression'),
        ('security', 'Security Incident'),
        ('other', 'Other Incident'),
    ]
    
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('major', 'Major'),
        ('critical', 'Critical'),
    ]
    
    incident_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True, related_name='nursing_incidents')
    unit = models.ForeignKey(NursingUnit, on_delete=models.CASCADE, related_name='incidents')
    
    # Incident details
    incident_type = models.CharField(max_length=20, choices=INCIDENT_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    
    # Occurrence
    occurred_at = models.DateTimeField()
    discovered_at = models.DateTimeField(null=True, blank=True)
    
    # Description
    description = models.TextField()
    contributing_factors = models.TextField(blank=True)
    
    # Personnel involved
    reported_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='nursing_reported_incidents')
    witness = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='witnessed_nursing_incidents')
    
    # Actions taken
    immediate_actions = models.TextField(blank=True)
    physician_notified = models.BooleanField(default=False)
    family_notified = models.BooleanField(default=False)
    
    # Investigation
    investigation_required = models.BooleanField(default=False)
    investigation_notes = models.TextField(blank=True)
    
    # Follow-up
    follow_up_required = models.BooleanField(default=False)
    follow_up_actions = models.TextField(blank=True)
    
    # Resolution
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-occurred_at']
        verbose_name = 'Nursing Incident'
        verbose_name_plural = 'Nursing Incidents'
    
    def save(self, *args, **kwargs):
        if not self.incident_id:
            self.incident_id = f"NI{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.incident_id} - {self.incident_type} - {self.severity}"


class NursingSettings(models.Model):
    """System-wide nursing settings"""
    # Shift settings
    day_shift_start = models.TimeField(default='07:00')
    day_shift_end = models.TimeField(default='19:00')
    night_shift_start = models.TimeField(default='19:00')
    night_shift_end = models.TimeField(default='07:00')
    
    # Patient assignment
    max_patients_per_nurse = models.IntegerField(default=6)
    max_patients_icu = models.IntegerField(default=2)
    
    # Documentation
    mandatory_assessment_frequency = models.IntegerField(default=8, help_text="Hours between assessments")
    vital_signs_frequency = models.IntegerField(default=4, help_text="Hours between vital signs")
    
    # Medication administration
    medication_scan_required = models.BooleanField(default=True)
    double_check_high_risk = models.BooleanField(default=True)
    
    # Safety
    fall_risk_reassessment = models.IntegerField(default=24, help_text="Hours between fall risk assessments")
    incident_reporting_required = models.BooleanField(default=True)
    
    # Quality measures
    pressure_ulcer_assessment = models.BooleanField(default=True)
    infection_control_measures = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Nursing Settings'
        verbose_name_plural = 'Nursing Settings'
    
    def __str__(self):
        return f"Nursing Settings - {self.created_at.date()}" 