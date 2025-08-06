from django.db import models
from django.utils import timezone
from datetime import timedelta
from acs_hms_base.models import Patient, HMSUser, Room, Department, MedicalRecord


class Admission(models.Model):
    """Patient Admission Management"""
    ADMISSION_TYPE_CHOICES = [
        ('EMERGENCY', 'Emergency'),
        ('ELECTIVE', 'Elective'),
        ('TRANSFER', 'Transfer'),
        ('OBSERVATION', 'Observation'),
        ('DAY_CARE', 'Day Care'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('DISCHARGED', 'Discharged'),
        ('TRANSFERRED', 'Transferred'),
        ('DECEASED', 'Deceased'),
        ('ABSCOND', 'Abscond'),
    ]
    
    # Basic Information
    admission_number = models.CharField(max_length=20, unique=True, verbose_name="Admission Number")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='admissions')
    admission_date = models.DateTimeField(verbose_name="Admission Date")
    admission_type = models.CharField(max_length=20, choices=ADMISSION_TYPE_CHOICES, verbose_name="Admission Type")
    
    # Medical Information
    chief_complaint = models.TextField(verbose_name="Chief Complaint")
    provisional_diagnosis = models.TextField(blank=True, null=True, verbose_name="Provisional Diagnosis")
    final_diagnosis = models.TextField(blank=True, null=True, verbose_name="Final Diagnosis")
    
    # Department and Staff
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='admissions')
    attending_doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='admitted_patients', limit_choices_to={'user_type': 'DOCTOR'})
    referred_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_admissions')
    
    # Room Assignment
    current_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_admissions')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name="Status")
    
    # Discharge Information
    discharge_date = models.DateTimeField(blank=True, null=True, verbose_name="Discharge Date")
    discharge_summary = models.TextField(blank=True, null=True, verbose_name="Discharge Summary")
    discharge_instructions = models.TextField(blank=True, null=True, verbose_name="Discharge Instructions")
    
    # Insurance Information
    insurance_approval = models.BooleanField(default=False, verbose_name="Insurance Approval")
    insurance_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Insurance Number")
    
    # Financial Information
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Estimated Cost")
    total_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Total Charges")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Amount Paid")
    
    # Record Information
    admitted_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='processed_admissions')
    
    class Meta:
        verbose_name = "Admission"
        verbose_name_plural = "Admissions"
        ordering = ['-admission_date']
    
    def __str__(self):
        return f"Admission {self.admission_number} - {self.patient.full_name}"
    
    @property
    def length_of_stay(self):
        """Calculate length of stay in days"""
        if self.discharge_date:
            return (self.discharge_date - self.admission_date).days
        return (timezone.now() - self.admission_date).days
    
    @property
    def balance_amount(self):
        """Calculate balance amount"""
        if self.total_charges:
            return self.total_charges - self.amount_paid
        return 0


class RoomAssignment(models.Model):
    """Room Assignment History"""
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='room_assignments')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='assignments')
    assigned_date = models.DateTimeField(verbose_name="Assigned Date")
    transferred_date = models.DateTimeField(blank=True, null=True, verbose_name="Transferred Date")
    
    ASSIGNMENT_STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('TRANSFERRED', 'Transferred'),
        ('DISCHARGED', 'Discharged'),
    ]
    
    status = models.CharField(max_length=20, choices=ASSIGNMENT_STATUS_CHOICES, default='ACTIVE', verbose_name="Status")
    assigned_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='room_assignments')
    
    # Bed Information
    bed_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="Bed Number")
    
    # Transfer Reason
    transfer_reason = models.TextField(blank=True, null=True, verbose_name="Transfer Reason")
    
    class Meta:
        verbose_name = "Room Assignment"
        verbose_name_plural = "Room Assignments"
        ordering = ['-assigned_date']
    
    def __str__(self):
        return f"{self.room.number} - {self.admission.patient.full_name} ({self.assigned_date})"


class DailyRounds(models.Model):
    """Daily Medical Rounds"""
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='daily_rounds')
    round_date = models.DateField(verbose_name="Round Date")
    round_time = models.TimeField(verbose_name="Round Time")
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='daily_rounds', limit_choices_to={'user_type': 'DOCTOR'})
    
    # Vital Signs
    temperature = models.FloatField(blank=True, null=True, verbose_name="Temperature (°C)")
    blood_pressure_systolic = models.IntegerField(blank=True, null=True, verbose_name="Blood Pressure (Systolic)")
    blood_pressure_diastolic = models.IntegerField(blank=True, null=True, verbose_name="Blood Pressure (Diastolic)")
    pulse_rate = models.IntegerField(blank=True, null=True, verbose_name="Pulse Rate")
    respiratory_rate = models.IntegerField(blank=True, null=True, verbose_name="Respiratory Rate")
    oxygen_saturation = models.FloatField(blank=True, null=True, verbose_name="Oxygen Saturation (%)")
    
    # Assessment
    general_condition = models.TextField(blank=True, null=True, verbose_name="General Condition")
    symptom_assessment = models.TextField(blank=True, null=True, verbose_name="Symptom Assessment")
    physical_examination = models.TextField(blank=True, null=True, verbose_name="Physical Examination")
    
    # Treatment
    treatment_plan = models.TextField(blank=True, null=True, verbose_name="Treatment Plan")
    medications = models.TextField(blank=True, null=True, verbose_name="Medications")
    investigations_ordered = models.TextField(blank=True, null=True, verbose_name="Investigations Ordered")
    
    # Progress
    progress_notes = models.TextField(blank=True, null=True, verbose_name="Progress Notes")
    
    # Discharge Planning
    discharge_planning = models.TextField(blank=True, null=True, verbose_name="Discharge Planning")
    
    class Meta:
        verbose_name = "Daily Round"
        verbose_name_plural = "Daily Rounds"
        ordering = ['-round_date', '-round_time']
    
    def __str__(self):
        return f"Round - {self.admission.patient.full_name} ({self.round_date})"


class NursingCare(models.Model):
    """Nursing Care Records"""
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='nursing_care')
    care_date = models.DateField(verbose_name="Care Date")
    care_time = models.TimeField(verbose_name="Care Time")
    nurse = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='nursing_care', limit_choices_to={'user_type': 'NURSE'})
    
    # Vital Signs
    temperature = models.FloatField(blank=True, null=True, verbose_name="Temperature (°C)")
    blood_pressure_systolic = models.IntegerField(blank=True, null=True, verbose_name="Blood Pressure (Systolic)")
    blood_pressure_diastolic = models.IntegerField(blank=True, null=True, verbose_name="Blood Pressure (Diastolic)")
    pulse_rate = models.IntegerField(blank=True, null=True, verbose_name="Pulse Rate")
    respiratory_rate = models.IntegerField(blank=True, null=True, verbose_name="Respiratory Rate")
    oxygen_saturation = models.FloatField(blank=True, null=True, verbose_name="Oxygen Saturation (%)")
    
    # Intake and Output
    fluid_intake = models.FloatField(blank=True, null=True, verbose_name="Fluid Intake (ml)")
    urine_output = models.FloatField(blank=True, null=True, verbose_name="Urine Output (ml)")
    
    # Patient Care
    hygiene_care = models.TextField(blank=True, null=True, verbose_name="Hygiene Care")
    mobility_assistance = models.TextField(blank=True, null=True, verbose_name="Mobility Assistance")
    nutrition_assistance = models.TextField(blank=True, null=True, verbose_name="Nutrition Assistance")
    
    # Medication Administration
    medications_given = models.TextField(blank=True, null=True, verbose_name="Medications Given")
    
    # Patient Response
    patient_response = models.TextField(blank=True, null=True, verbose_name="Patient Response")
    
    # Nursing Notes
    nursing_notes = models.TextField(blank=True, null=True, verbose_name="Nursing Notes")
    
    class Meta:
        verbose_name = "Nursing Care"
        verbose_name_plural = "Nursing Care"
        ordering = ['-care_date', '-care_time']
    
    def __str__(self):
        return f"Nursing Care - {self.admission.patient.full_name} ({self.care_date})"


class DischargeRecord(models.Model):
    """Discharge Records"""
    admission = models.OneToOneField(Admission, on_delete=models.CASCADE, related_name='discharge_record')
    discharge_date = models.DateTimeField(verbose_name="Discharge Date")
    discharge_type = models.CharField(max_length=40, choices=[
        ('ROUTINE', 'Routine'),
        ('DISCHARGE_AGAINST_MEDICAL_ADVICE', 'Discharge Against Medical Advice'),
        ('TRANSFER', 'Transfer'),
        ('DEATH', 'Death'),
        ('ABSCOND', 'Abscond'),
    ], verbose_name="Discharge Type")
    
    # Medical Information
    final_diagnosis = models.TextField(verbose_name="Final Diagnosis")
    secondary_diagnosis = models.TextField(blank=True, null=True, verbose_name="Secondary Diagnosis")
    procedures_performed = models.TextField(blank=True, null=True, verbose_name="Procedures Performed")
    
    # Condition at Discharge
    condition_at_discharge = models.CharField(max_length=20, choices=[
        ('IMPROVED', 'Improved'),
        ('STABLE', 'Stable'),
        ('DETERIORATED', 'Deteriorated'),
        ('UNCHANGED', 'Unchanged'),
    ], verbose_name="Condition at Discharge")
    
    # Discharge Instructions
    discharge_instructions = models.TextField(verbose_name="Discharge Instructions")
    medications_prescribed = models.TextField(blank=True, null=True, verbose_name="Medications Prescribed")
    follow_up_instructions = models.TextField(blank=True, null=True, verbose_name="Follow-up Instructions")
    
    # Follow-up Appointments
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    follow_up_doctor = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='follow_up_patients')
    
    # Discharge Summary
    hospital_course = models.TextField(blank=True, null=True, verbose_name="Hospital Course")
    complications = models.TextField(blank=True, null=True, verbose_name="Complications")
    
    # Responsible Staff
    discharged_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='discharged_patients')
    
    class Meta:
        verbose_name = "Discharge Record"
        verbose_name_plural = "Discharge Records"
        ordering = ['-discharge_date']
    
    def __str__(self):
        return f"Discharge - {self.admission.patient.full_name} ({self.discharge_date})"


class MedicationAdministration(models.Model):
    """Medication Administration Records"""
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='medication_administrations')
    medication_name = models.CharField(max_length=100, verbose_name="Medication Name")
    dosage = models.CharField(max_length=50, verbose_name="Dosage")
    route = models.CharField(max_length=20, choices=[
        ('ORAL', 'Oral'),
        ('IV', 'Intravenous'),
        ('IM', 'Intramuscular'),
        ('SC', 'Subcutaneous'),
        ('TOPICAL', 'Topical'),
        ('INHALATION', 'Inhalation'),
    ], verbose_name="Route")
    
    # Administration Details
    administration_date = models.DateField(verbose_name="Administration Date")
    administration_time = models.TimeField(verbose_name="Administration Time")
    administered_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='administered_medications')
    
    # Prescription Details
    prescribed_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='prescribed_medications', limit_choices_to={'user_type': 'DOCTOR'})
    prescription_date = models.DateField(verbose_name="Prescription Date")
    
    # Administration Status
    STATUS_CHOICES = [
        ('GIVEN', 'Given'),
        ('REFUSED', 'Refused'),
        ('WITHHELD', 'Withheld'),
        ('MISSED', 'Missed'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='GIVEN', verbose_name="Status")
    
    # Notes
    administration_notes = models.TextField(blank=True, null=True, verbose_name="Administration Notes")
    patient_response = models.TextField(blank=True, null=True, verbose_name="Patient Response")
    
    class Meta:
        verbose_name = "Medication Administration"
        verbose_name_plural = "Medication Administrations"
        ordering = ['-administration_date', '-administration_time']
    
    def __str__(self):
        return f"{self.medication_name} - {self.admission.patient.full_name} ({self.administration_date})"


class InpatientBilling(models.Model):
    """Inpatient Billing Management"""
    admission = models.OneToOneField(Admission, on_delete=models.CASCADE, related_name='billing')
    
    # Room Charges
    room_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Room Charges")
    nursing_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Nursing Charges")
    
    # Medical Charges
    consultation_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Consultation Charges")
    procedure_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Procedure Charges")
    
    # Investigation Charges
    laboratory_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Laboratory Charges")
    radiology_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Radiology Charges")
    
    # Medication Charges
    medication_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Medication Charges")
    
    # Other Charges
    miscellaneous_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Miscellaneous Charges")
    
    # Total and Payment
    total_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total Charges")
    insurance_coverage = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Insurance Coverage")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Discount")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Amount Paid")
    
    # Payment Status
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PARTIAL', 'Partial'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
    ]
    
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING', verbose_name="Payment Status")
    
    class Meta:
        verbose_name = "Inpatient Billing"
        verbose_name_plural = "Inpatient Billing"
    
    def __str__(self):
        return f"Billing - {self.admission.patient.full_name}"
    
    @property
    def balance_amount(self):
        """Calculate balance amount"""
        return self.total_charges - self.insurance_coverage - self.discount - self.amount_paid 