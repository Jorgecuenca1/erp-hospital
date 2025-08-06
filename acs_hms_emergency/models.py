from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import Patient, HMSUser, Hospital, Department
from acs_hms_hospitalization.models import Admission


class Ambulance(models.Model):
    """Ambulance Fleet Management"""
    AMBULANCE_TYPE_CHOICES = [
        ('BASIC', 'Basic Life Support (BLS)'),
        ('ADVANCED', 'Advanced Life Support (ALS)'),
        ('CRITICAL', 'Critical Care Transport'),
        ('NEONATAL', 'Neonatal Transport'),
        ('PSYCHIATRIC', 'Psychiatric Transport'),
    ]
    
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('DISPATCHED', 'Dispatched'),
        ('ON_SCENE', 'On Scene'),
        ('TRANSPORTING', 'Transporting'),
        ('AT_HOSPITAL', 'At Hospital'),
        ('OUT_OF_SERVICE', 'Out of Service'),
        ('MAINTENANCE', 'Under Maintenance'),
    ]
    
    # Basic Information
    ambulance_number = models.CharField(max_length=20, unique=True, verbose_name="Ambulance Number")
    vehicle_registration = models.CharField(max_length=20, unique=True, verbose_name="Vehicle Registration")
    ambulance_type = models.CharField(max_length=20, choices=AMBULANCE_TYPE_CHOICES, verbose_name="Type")
    
    # Vehicle Details
    make = models.CharField(max_length=50, verbose_name="Make")
    model = models.CharField(max_length=50, verbose_name="Model")
    year = models.PositiveIntegerField(verbose_name="Year")
    
    # Equipment
    equipment_list = models.TextField(blank=True, null=True, verbose_name="Equipment List")
    medical_equipment = models.TextField(blank=True, null=True, verbose_name="Medical Equipment")
    
    # Operational
    base_location = models.CharField(max_length=200, verbose_name="Base Location")
    current_location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Current Location")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE', verbose_name="Status")
    
    # Crew
    primary_driver = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='primary_ambulance_driver')
    primary_paramedic = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='primary_ambulance_paramedic')
    
    # Maintenance
    last_maintenance_date = models.DateField(blank=True, null=True, verbose_name="Last Maintenance Date")
    next_maintenance_date = models.DateField(blank=True, null=True, verbose_name="Next Maintenance Date")
    maintenance_notes = models.TextField(blank=True, null=True, verbose_name="Maintenance Notes")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Ambulance"
        verbose_name_plural = "Ambulances"
        ordering = ['ambulance_number']
    
    def __str__(self):
        return f"{self.ambulance_number} - {self.get_ambulance_type_display()}"


class EmergencyCall(models.Model):
    """Emergency Call Management"""
    PRIORITY_CHOICES = [
        ('ALPHA', 'Alpha - Non-Emergency'),
        ('BRAVO', 'Bravo - Minor Emergency'),
        ('CHARLIE', 'Charlie - Moderate Emergency'),
        ('DELTA', 'Delta - Major Emergency'),
        ('ECHO', 'Echo - Life Threatening'),
    ]
    
    CALL_TYPE_CHOICES = [
        ('MEDICAL', 'Medical Emergency'),
        ('TRAUMA', 'Trauma/Accident'),
        ('CARDIAC', 'Cardiac Arrest'),
        ('RESPIRATORY', 'Respiratory Emergency'),
        ('OBSTETRIC', 'Obstetric Emergency'),
        ('PEDIATRIC', 'Pediatric Emergency'),
        ('PSYCHIATRIC', 'Psychiatric Emergency'),
        ('POISON', 'Poisoning'),
        ('BURN', 'Burn Injury'),
        ('TRANSFER', 'Inter-facility Transfer'),
    ]
    
    STATUS_CHOICES = [
        ('RECEIVED', 'Call Received'),
        ('DISPATCHED', 'Ambulance Dispatched'),
        ('ON_SCENE', 'On Scene'),
        ('TRANSPORTING', 'Transporting'),
        ('AT_HOSPITAL', 'At Hospital'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    # Call Information
    call_number = models.CharField(max_length=20, unique=True, verbose_name="Call Number")
    call_date = models.DateTimeField(auto_now_add=True, verbose_name="Call Date")
    caller_name = models.CharField(max_length=100, verbose_name="Caller Name")
    caller_phone = models.CharField(max_length=20, verbose_name="Caller Phone")
    
    # Emergency Details
    call_type = models.CharField(max_length=20, choices=CALL_TYPE_CHOICES, verbose_name="Call Type")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, verbose_name="Priority")
    chief_complaint = models.TextField(verbose_name="Chief Complaint")
    
    # Location
    incident_address = models.TextField(verbose_name="Incident Address")
    incident_latitude = models.FloatField(blank=True, null=True, verbose_name="Latitude")
    incident_longitude = models.FloatField(blank=True, null=True, verbose_name="Longitude")
    
    # Patient Information
    patient_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Patient Name")
    patient_age = models.PositiveIntegerField(blank=True, null=True, verbose_name="Patient Age")
    patient_gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], blank=True, null=True, verbose_name="Patient Gender")
    
    # Dispatch Information
    dispatched_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='dispatched_calls')
    dispatch_time = models.DateTimeField(blank=True, null=True, verbose_name="Dispatch Time")
    ambulance = models.ForeignKey(Ambulance, on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_calls')
    
    # Response Times
    response_time_minutes = models.PositiveIntegerField(blank=True, null=True, verbose_name="Response Time (Minutes)")
    on_scene_time = models.DateTimeField(blank=True, null=True, verbose_name="On Scene Time")
    transport_time = models.DateTimeField(blank=True, null=True, verbose_name="Transport Time")
    hospital_arrival_time = models.DateTimeField(blank=True, null=True, verbose_name="Hospital Arrival Time")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RECEIVED', verbose_name="Status")
    
    # Destination
    destination_hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_calls')
    
    # Notes
    dispatch_notes = models.TextField(blank=True, null=True, verbose_name="Dispatch Notes")
    completion_notes = models.TextField(blank=True, null=True, verbose_name="Completion Notes")
    
    class Meta:
        verbose_name = "Emergency Call"
        verbose_name_plural = "Emergency Calls"
        ordering = ['-call_date']
    
    def __str__(self):
        return f"Call {self.call_number} - {self.get_call_type_display()}"


class EmergencyCase(models.Model):
    """Emergency Department Cases"""
    TRIAGE_LEVEL_CHOICES = [
        ('1', 'Level 1 - Immediate (Red)'),
        ('2', 'Level 2 - Urgent (Orange)'),
        ('3', 'Level 3 - Less Urgent (Yellow)'),
        ('4', 'Level 4 - Non-urgent (Green)'),
        ('5', 'Level 5 - Routine (Blue)'),
    ]
    
    ARRIVAL_MODE_CHOICES = [
        ('AMBULANCE', 'Ambulance'),
        ('WALK_IN', 'Walk-in'),
        ('HELICOPTER', 'Helicopter'),
        ('TRANSFER', 'Transfer'),
        ('POLICE', 'Police'),
        ('PRIVATE_VEHICLE', 'Private Vehicle'),
    ]
    
    CASE_STATUS_CHOICES = [
        ('TRIAGED', 'Triaged'),
        ('WAITING', 'Waiting'),
        ('IN_TREATMENT', 'In Treatment'),
        ('OBSERVATION', 'Under Observation'),
        ('ADMITTED', 'Admitted'),
        ('DISCHARGED', 'Discharged'),
        ('TRANSFERRED', 'Transferred'),
        ('DECEASED', 'Deceased'),
        ('LEFT_AMA', 'Left Against Medical Advice'),
    ]
    
    # Case Information
    case_number = models.CharField(max_length=20, unique=True, verbose_name="Case Number")
    arrival_date = models.DateTimeField(auto_now_add=True, verbose_name="Arrival Date")
    arrival_mode = models.CharField(max_length=20, choices=ARRIVAL_MODE_CHOICES, verbose_name="Arrival Mode")
    
    # Patient Information
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='emergency_cases')
    
    # Triage Information
    triage_level = models.CharField(max_length=1, choices=TRIAGE_LEVEL_CHOICES, verbose_name="Triage Level")
    triage_time = models.DateTimeField(verbose_name="Triage Time")
    triage_nurse = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='triaged_cases', limit_choices_to={'user_type': 'NURSE'})
    
    # Chief Complaint
    chief_complaint = models.TextField(verbose_name="Chief Complaint")
    presenting_symptoms = models.TextField(blank=True, null=True, verbose_name="Presenting Symptoms")
    
    # Vital Signs at Triage
    temperature = models.FloatField(blank=True, null=True, verbose_name="Temperature (°C)")
    blood_pressure_systolic = models.IntegerField(blank=True, null=True, verbose_name="Blood Pressure (Systolic)")
    blood_pressure_diastolic = models.IntegerField(blank=True, null=True, verbose_name="Blood Pressure (Diastolic)")
    pulse_rate = models.IntegerField(blank=True, null=True, verbose_name="Pulse Rate")
    respiratory_rate = models.IntegerField(blank=True, null=True, verbose_name="Respiratory Rate")
    oxygen_saturation = models.FloatField(blank=True, null=True, verbose_name="Oxygen Saturation (%)")
    pain_score = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Pain Score (0-10)")
    
    # Treatment Information
    assigned_doctor = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_cases', limit_choices_to={'user_type': 'DOCTOR'})
    treatment_start_time = models.DateTimeField(blank=True, null=True, verbose_name="Treatment Start Time")
    
    # Status
    status = models.CharField(max_length=20, choices=CASE_STATUS_CHOICES, default='TRIAGED', verbose_name="Status")
    
    # Outcome
    diagnosis = models.TextField(blank=True, null=True, verbose_name="Diagnosis")
    treatment_provided = models.TextField(blank=True, null=True, verbose_name="Treatment Provided")
    discharge_time = models.DateTimeField(blank=True, null=True, verbose_name="Discharge Time")
    discharge_instructions = models.TextField(blank=True, null=True, verbose_name="Discharge Instructions")
    
    # Follow-up
    follow_up_required = models.BooleanField(default=False, verbose_name="Follow-up Required")
    follow_up_instructions = models.TextField(blank=True, null=True, verbose_name="Follow-up Instructions")
    
    # Related Records
    emergency_call = models.ForeignKey(EmergencyCall, on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_cases')
    admission = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_cases')
    
    class Meta:
        verbose_name = "Emergency Case"
        verbose_name_plural = "Emergency Cases"
        ordering = ['-arrival_date']
    
    def __str__(self):
        return f"Case {self.case_number} - {self.patient.full_name}"


class EmergencyTreatment(models.Model):
    """Emergency Treatment Records"""
    emergency_case = models.ForeignKey(EmergencyCase, on_delete=models.CASCADE, related_name='treatments')
    treatment_time = models.DateTimeField(verbose_name="Treatment Time")
    performed_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='emergency_treatments')
    
    # Treatment Details
    procedure_performed = models.TextField(verbose_name="Procedure Performed")
    medications_given = models.TextField(blank=True, null=True, verbose_name="Medications Given")
    
    # Response
    patient_response = models.TextField(blank=True, null=True, verbose_name="Patient Response")
    complications = models.TextField(blank=True, null=True, verbose_name="Complications")
    
    # Notes
    treatment_notes = models.TextField(blank=True, null=True, verbose_name="Treatment Notes")
    
    class Meta:
        verbose_name = "Emergency Treatment"
        verbose_name_plural = "Emergency Treatments"
        ordering = ['-treatment_time']
    
    def __str__(self):
        return f"Treatment for {self.emergency_case.case_number} at {self.treatment_time}"


class AmbulanceTrip(models.Model):
    """Ambulance Trip Records"""
    TRIP_TYPE_CHOICES = [
        ('EMERGENCY', 'Emergency Response'),
        ('TRANSFER', 'Inter-facility Transfer'),
        ('DISCHARGE', 'Discharge Transport'),
        ('ROUTINE', 'Routine Transport'),
        ('STANDBY', 'Standby Coverage'),
    ]
    
    TRIP_STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    # Trip Information
    trip_number = models.CharField(max_length=20, unique=True, verbose_name="Trip Number")
    ambulance = models.ForeignKey(Ambulance, on_delete=models.CASCADE, related_name='trips')
    trip_type = models.CharField(max_length=20, choices=TRIP_TYPE_CHOICES, verbose_name="Trip Type")
    
    # Crew
    driver = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='ambulance_trips_driver')
    paramedic = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='ambulance_trips_paramedic')
    additional_crew = models.ManyToManyField(HMSUser, blank=True, related_name='ambulance_trips_crew')
    
    # Trip Details
    start_time = models.DateTimeField(verbose_name="Start Time")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="End Time")
    
    # Locations
    origin_address = models.TextField(verbose_name="Origin Address")
    destination_address = models.TextField(verbose_name="Destination Address")
    
    # Patient Information
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='ambulance_trips')
    
    # Medical Information
    patient_condition = models.TextField(verbose_name="Patient Condition")
    vital_signs_departure = models.TextField(blank=True, null=True, verbose_name="Vital Signs at Departure")
    vital_signs_arrival = models.TextField(blank=True, null=True, verbose_name="Vital Signs at Arrival")
    
    # Treatment During Transport
    treatment_during_transport = models.TextField(blank=True, null=True, verbose_name="Treatment During Transport")
    medications_administered = models.TextField(blank=True, null=True, verbose_name="Medications Administered")
    
    # Status
    status = models.CharField(max_length=20, choices=TRIP_STATUS_CHOICES, default='SCHEDULED', verbose_name="Status")
    
    # Mileage
    starting_mileage = models.PositiveIntegerField(verbose_name="Starting Mileage")
    ending_mileage = models.PositiveIntegerField(blank=True, null=True, verbose_name="Ending Mileage")
    
    # Related Records
    emergency_call = models.ForeignKey(EmergencyCall, on_delete=models.SET_NULL, null=True, blank=True, related_name='ambulance_trips')
    emergency_case = models.ForeignKey(EmergencyCase, on_delete=models.SET_NULL, null=True, blank=True, related_name='ambulance_trips')
    
    # Notes
    trip_notes = models.TextField(blank=True, null=True, verbose_name="Trip Notes")
    
    class Meta:
        verbose_name = "Ambulance Trip"
        verbose_name_plural = "Ambulance Trips"
        ordering = ['-start_time']
    
    def __str__(self):
        return f"Trip {self.trip_number} - {self.ambulance.ambulance_number}"


class EmergencyEquipment(models.Model):
    """Emergency Equipment Management"""
    EQUIPMENT_TYPE_CHOICES = [
        ('DEFIBRILLATOR', 'Defibrillator'),
        ('VENTILATOR', 'Ventilator'),
        ('MONITOR', 'Patient Monitor'),
        ('SUCTION', 'Suction Unit'),
        ('OXYGEN', 'Oxygen System'),
        ('STRETCHER', 'Stretcher'),
        ('WHEELCHAIR', 'Wheelchair'),
        ('TRAUMA_KIT', 'Trauma Kit'),
        ('DRUG_KIT', 'Drug Kit'),
        ('INTUBATION', 'Intubation Kit'),
    ]
    
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('IN_USE', 'In Use'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('OUT_OF_ORDER', 'Out of Order'),
        ('CLEANING', 'Cleaning'),
    ]
    
    # Equipment Information
    equipment_name = models.CharField(max_length=100, verbose_name="Equipment Name")
    equipment_type = models.CharField(max_length=20, choices=EQUIPMENT_TYPE_CHOICES, verbose_name="Equipment Type")
    serial_number = models.CharField(max_length=50, unique=True, verbose_name="Serial Number")
    
    # Location
    current_location = models.CharField(max_length=100, verbose_name="Current Location")
    assigned_ambulance = models.ForeignKey(Ambulance, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipment')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE', verbose_name="Status")
    
    # Maintenance
    last_maintenance_date = models.DateField(blank=True, null=True, verbose_name="Last Maintenance Date")
    next_maintenance_date = models.DateField(blank=True, null=True, verbose_name="Next Maintenance Date")
    
    # Notes
    equipment_notes = models.TextField(blank=True, null=True, verbose_name="Equipment Notes")
    
    class Meta:
        verbose_name = "Emergency Equipment"
        verbose_name_plural = "Emergency Equipment"
        ordering = ['equipment_name']
    
    def __str__(self):
        return f"{self.equipment_name} ({self.serial_number})"


class EmergencyProtocol(models.Model):
    """Emergency Treatment Protocols"""
    PROTOCOL_TYPE_CHOICES = [
        ('CARDIAC', 'Cardiac Emergency'),
        ('TRAUMA', 'Trauma Protocol'),
        ('STROKE', 'Stroke Protocol'),
        ('RESPIRATORY', 'Respiratory Emergency'),
        ('POISONING', 'Poisoning Protocol'),
        ('BURNS', 'Burns Protocol'),
        ('OBSTETRIC', 'Obstetric Emergency'),
        ('PEDIATRIC', 'Pediatric Emergency'),
        ('PSYCHIATRIC', 'Psychiatric Emergency'),
        ('GENERAL', 'General Protocol'),
    ]
    
    # Protocol Information
    protocol_name = models.CharField(max_length=100, verbose_name="Protocol Name")
    protocol_type = models.CharField(max_length=20, choices=PROTOCOL_TYPE_CHOICES, verbose_name="Protocol Type")
    protocol_code = models.CharField(max_length=20, unique=True, verbose_name="Protocol Code")
    
    # Content
    description = models.TextField(verbose_name="Description")
    indications = models.TextField(verbose_name="Indications")
    contraindications = models.TextField(blank=True, null=True, verbose_name="Contraindications")
    
    # Procedure Steps
    assessment_steps = models.TextField(verbose_name="Assessment Steps")
    treatment_steps = models.TextField(verbose_name="Treatment Steps")
    medication_protocol = models.TextField(blank=True, null=True, verbose_name="Medication Protocol")
    
    # Equipment Required
    required_equipment = models.TextField(blank=True, null=True, verbose_name="Required Equipment")
    
    # Version Control
    version = models.CharField(max_length=10, verbose_name="Version")
    effective_date = models.DateField(verbose_name="Effective Date")
    review_date = models.DateField(verbose_name="Review Date")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Emergency Protocol"
        verbose_name_plural = "Emergency Protocols"
        ordering = ['protocol_name']
    
    def __str__(self):
        return f"{self.protocol_name} ({self.protocol_code})" 