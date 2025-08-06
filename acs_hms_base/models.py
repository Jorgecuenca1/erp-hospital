from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator


class Hospital(models.Model):
    """Hospital Information"""
    name = models.CharField(max_length=200, verbose_name="Hospital Name")
    code = models.CharField(max_length=20, unique=True, verbose_name="Hospital Code")
    address = models.TextField(verbose_name="Address")
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=100, verbose_name="State/Province")
    country = models.CharField(max_length=100, verbose_name="Country")
    zip_code = models.CharField(max_length=20, verbose_name="ZIP Code")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    email = models.EmailField(verbose_name="Email")
    website = models.URLField(blank=True, null=True, verbose_name="Website")
    license_number = models.CharField(max_length=50, verbose_name="License Number")
    established_date = models.DateField(verbose_name="Established Date")
    registration_number = models.CharField(max_length=50, verbose_name="Registration Number")
    active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitals"
    
    def __str__(self):
        return self.name


class Department(models.Model):
    """Hospital Departments"""
    name = models.CharField(max_length=100, verbose_name="Department Name")
    code = models.CharField(max_length=20, unique=True, verbose_name="Department Code")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='departments')
    head_of_department = models.ForeignKey('HMSUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Location")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        unique_together = ['hospital', 'code']
    
    def __str__(self):
        return f"{self.name} - {self.hospital.name}"


class Room(models.Model):
    """Hospital Rooms"""
    ROOM_TYPE_CHOICES = [
        ('GENERAL', 'General Ward'),
        ('PRIVATE', 'Private Room'),
        ('ICU', 'Intensive Care Unit'),
        ('EMERGENCY', 'Emergency Room'),
        ('SURGERY', 'Surgery Room'),
        ('CONSULTATION', 'Consultation Room'),
        ('LABORATORY', 'Laboratory'),
        ('RADIOLOGY', 'Radiology'),
        ('PHARMACY', 'Pharmacy'),
        ('ADMINISTRATION', 'Administration'),
    ]
    
    ROOM_STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('OCCUPIED', 'Occupied'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('RESERVED', 'Reserved'),
        ('CLEANING', 'Cleaning'),
    ]
    
    number = models.CharField(max_length=20, verbose_name="Room Number")
    name = models.CharField(max_length=100, verbose_name="Room Name")
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, verbose_name="Room Type")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='rooms')
    floor = models.CharField(max_length=10, verbose_name="Floor")
    capacity = models.PositiveIntegerField(default=1, verbose_name="Capacity")
    status = models.CharField(max_length=20, choices=ROOM_STATUS_CHOICES, default='AVAILABLE', verbose_name="Status")
    amenities = models.TextField(blank=True, null=True, verbose_name="Amenities")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        unique_together = ['department', 'number']
    
    def __str__(self):
        return f"{self.number} - {self.name} ({self.department.name})"


class HMSUser(models.Model):
    """Extended User Model for HMS"""
    USER_TYPE_CHOICES = [
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('TECHNICIAN', 'Technician'),
        ('PHARMACIST', 'Pharmacist'),
        ('RADIOLOGIST', 'Radiologist'),
        ('LABORATORY_TECHNICIAN', 'Laboratory Technician'),
        ('RECEPTIONIST', 'Receptionist'),
        ('ADMINISTRATOR', 'Administrator'),
        ('PATIENT', 'Patient'),
        ('INSURANCE_AGENT', 'Insurance Agent'),
        ('MARKETING', 'Marketing'),
        ('FINANCE', 'Finance'),
        ('IT_SUPPORT', 'IT Support'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hms_profile')
    employee_id = models.CharField(max_length=20, unique=True, verbose_name="Employee ID")
    user_type = models.CharField(max_length=25, choices=USER_TYPE_CHOICES, verbose_name="User Type")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='users')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    # Personal Information
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, verbose_name="Phone")
    mobile = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, verbose_name="Mobile")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="City")
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name="State")
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name="Country")
    zip_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="ZIP Code")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="Gender")
    
    # Professional Information
    license_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="License Number")
    qualification = models.CharField(max_length=200, blank=True, null=True, verbose_name="Qualification")
    experience_years = models.PositiveIntegerField(blank=True, null=True, verbose_name="Years of Experience")
    specialization = models.CharField(max_length=100, blank=True, null=True, verbose_name="Specialization")
    
    # Employment Information
    joining_date = models.DateField(default=timezone.now, verbose_name="Joining Date")
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Salary")
    shift = models.CharField(max_length=20, blank=True, null=True, verbose_name="Shift")
    
    # Profile Information
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True, verbose_name="Photo")
    signature = models.ImageField(upload_to='user_signatures/', blank=True, null=True, verbose_name="Signature")
    
    # Status
    active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "HMS User"
        verbose_name_plural = "HMS Users"
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"
    
    @property
    def full_name(self):
        return self.user.get_full_name()


class Patient(models.Model):
    """Enhanced Patient Model"""
    PATIENT_TYPE_CHOICES = [
        ('OUTPATIENT', 'Outpatient'),
        ('INPATIENT', 'Inpatient'),
        ('EMERGENCY', 'Emergency'),
        ('CONSULTATION', 'Consultation'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
    ]
    
    # Basic Information
    patient_id = models.CharField(max_length=20, unique=True, verbose_name="Patient ID")
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Middle Name")
    
    # Demographics
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, choices=HMSUser.GENDER_CHOICES, verbose_name="Gender")
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True, verbose_name="Blood Group")
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, blank=True, null=True, verbose_name="Marital Status")
    
    # Contact Information
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, verbose_name="Phone")
    mobile = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, verbose_name="Mobile")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.TextField(verbose_name="Address")
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=100, verbose_name="State")
    country = models.CharField(max_length=100, verbose_name="Country")
    zip_code = models.CharField(max_length=20, verbose_name="ZIP Code")
    
    # Medical Information
    medical_record_number = models.CharField(max_length=20, unique=True, verbose_name="Medical Record Number")
    patient_type = models.CharField(max_length=15, choices=PATIENT_TYPE_CHOICES, default='OUTPATIENT', verbose_name="Patient Type")
    primary_doctor = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='primary_patients', limit_choices_to={'user_type': 'DOCTOR'})
    
    # Insurance Information
    insurance_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Insurance Number")
    insurance_provider = models.CharField(max_length=100, blank=True, null=True, verbose_name="Insurance Provider")
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Emergency Contact Name")
    emergency_contact_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, verbose_name="Emergency Contact Phone")
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True, verbose_name="Emergency Contact Relationship")
    
    # Medical History
    allergies = models.TextField(blank=True, null=True, verbose_name="Allergies")
    medical_history = models.TextField(blank=True, null=True, verbose_name="Medical History")
    current_medications = models.TextField(blank=True, null=True, verbose_name="Current Medications")
    
    # Profile
    photo = models.ImageField(upload_to='patient_photos/', blank=True, null=True, verbose_name="Photo")
    
    # Registration Information
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Registration Date")
    registered_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='registered_patients')
    
    # Status
    active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_id})"
    
    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


class Appointment(models.Model):
    """Enhanced Appointment Model"""
    APPOINTMENT_TYPE_CHOICES = [
        ('CONSULTATION', 'Consultation'),
        ('FOLLOW_UP', 'Follow-up'),
        ('EMERGENCY', 'Emergency'),
        ('SURGERY', 'Surgery'),
        ('LABORATORY', 'Laboratory'),
        ('RADIOLOGY', 'Radiology'),
        ('PHYSIOTHERAPY', 'Physiotherapy'),
        ('DENTAL', 'Dental'),
        ('GYNECOLOGY', 'Gynecology'),
        ('OPHTHALMOLOGY', 'Ophthalmology'),
        ('PEDIATRICS', 'Pediatrics'),
        ('AESTHETIC', 'Aesthetic'),
    ]
    
    APPOINTMENT_STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('CONFIRMED', 'Confirmed'),
        ('CHECKED_IN', 'Checked In'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
        ('RESCHEDULED', 'Rescheduled'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('NORMAL', 'Normal'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]
    
    # Basic Information
    appointment_id = models.CharField(max_length=20, unique=True, verbose_name="Appointment ID")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='doctor_appointments', limit_choices_to={'user_type': 'DOCTOR'})
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='appointments')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    
    # Scheduling Information
    appointment_date = models.DateField(verbose_name="Appointment Date")
    appointment_time = models.TimeField(verbose_name="Appointment Time")
    estimated_duration = models.DurationField(verbose_name="Estimated Duration")
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, verbose_name="Appointment Type")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='NORMAL', verbose_name="Priority")
    
    # Status and Details
    status = models.CharField(max_length=15, choices=APPOINTMENT_STATUS_CHOICES, default='SCHEDULED', verbose_name="Status")
    chief_complaint = models.TextField(blank=True, null=True, verbose_name="Chief Complaint")
    symptoms = models.TextField(blank=True, null=True, verbose_name="Symptoms")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    
    # Booking Information
    booked_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='booked_appointments')
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name="Booking Date")
    
    # Follow-up Information
    follow_up_required = models.BooleanField(default=False, verbose_name="Follow-up Required")
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Follow-up Date")
    follow_up_notes = models.TextField(blank=True, null=True, verbose_name="Follow-up Notes")
    
    # Financial Information
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Consultation Fee")
    insurance_covered = models.BooleanField(default=False, verbose_name="Insurance Covered")
    
    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ['appointment_date', 'appointment_time']
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.doctor.full_name} ({self.appointment_date})"


class MedicalRecord(models.Model):
    """Enhanced Medical Record Model"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='medical_records', limit_choices_to={'user_type': 'DOCTOR'})
    
    # Examination Details
    chief_complaint = models.TextField(verbose_name="Chief Complaint")
    history_of_present_illness = models.TextField(blank=True, null=True, verbose_name="History of Present Illness")
    physical_examination = models.TextField(blank=True, null=True, verbose_name="Physical Examination")
    
    # Vital Signs
    temperature = models.FloatField(blank=True, null=True, verbose_name="Temperature (°C)")
    blood_pressure_systolic = models.IntegerField(blank=True, null=True, verbose_name="Blood Pressure (Systolic)")
    blood_pressure_diastolic = models.IntegerField(blank=True, null=True, verbose_name="Blood Pressure (Diastolic)")
    pulse_rate = models.IntegerField(blank=True, null=True, verbose_name="Pulse Rate")
    respiratory_rate = models.IntegerField(blank=True, null=True, verbose_name="Respiratory Rate")
    oxygen_saturation = models.FloatField(blank=True, null=True, verbose_name="Oxygen Saturation (%)")
    weight = models.FloatField(blank=True, null=True, verbose_name="Weight (kg)")
    height = models.FloatField(blank=True, null=True, verbose_name="Height (cm)")
    
    # Diagnosis and Treatment
    provisional_diagnosis = models.TextField(blank=True, null=True, verbose_name="Provisional Diagnosis")
    final_diagnosis = models.TextField(blank=True, null=True, verbose_name="Final Diagnosis")
    treatment_plan = models.TextField(blank=True, null=True, verbose_name="Treatment Plan")
    prescriptions = models.TextField(blank=True, null=True, verbose_name="Prescriptions")
    
    # Additional Information
    lab_tests_ordered = models.TextField(blank=True, null=True, verbose_name="Lab Tests Ordered")
    radiology_tests_ordered = models.TextField(blank=True, null=True, verbose_name="Radiology Tests Ordered")
    referrals = models.TextField(blank=True, null=True, verbose_name="Referrals")
    
    # Record Information
    record_date = models.DateTimeField(auto_now_add=True, verbose_name="Record Date")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    
    class Meta:
        verbose_name = "Medical Record"
        verbose_name_plural = "Medical Records"
        ordering = ['-record_date']
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.record_date.strftime('%Y-%m-%d')}"


class HospitalConfiguration(models.Model):
    """Hospital Configuration Settings"""
    hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE, related_name='configuration')
    
    # General Settings
    allow_online_booking = models.BooleanField(default=True, verbose_name="Allow Online Booking")
    booking_advance_days = models.PositiveIntegerField(default=30, verbose_name="Booking Advance Days")
    appointment_duration = models.DurationField(default=timezone.timedelta(minutes=30), verbose_name="Default Appointment Duration")
    
    # Financial Settings
    default_consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Default Consultation Fee")
    currency = models.CharField(max_length=10, default='USD', verbose_name="Currency")
    
    # Notification Settings
    send_appointment_reminders = models.BooleanField(default=True, verbose_name="Send Appointment Reminders")
    reminder_hours_before = models.PositiveIntegerField(default=24, verbose_name="Reminder Hours Before")
    
    # Patient Portal Settings
    patient_portal_enabled = models.BooleanField(default=True, verbose_name="Patient Portal Enabled")
    allow_patient_registration = models.BooleanField(default=True, verbose_name="Allow Patient Registration")
    
    class Meta:
        verbose_name = "Hospital Configuration"
        verbose_name_plural = "Hospital Configurations"
    
    def __str__(self):
        return f"Configuration for {self.hospital.name}" 