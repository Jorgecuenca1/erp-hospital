from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser, Patient
from acs_hms_surgery.models import Surgery, OperationTheater
import uuid


class TheaterBooking(models.Model):
    """Theater booking and scheduling"""
    BOOKING_STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('tentative', 'Tentative'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('delayed', 'Delayed'),
        ('emergency', 'Emergency'),
    ]
    
    PRIORITY_CHOICES = [
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
        ('elective', 'Elective'),
    ]
    
    booking_id = models.CharField(max_length=20, unique=True, blank=True)
    operation_theater = models.ForeignKey(OperationTheater, on_delete=models.CASCADE, related_name='bookings')
    surgery = models.OneToOneField(Surgery, on_delete=models.CASCADE, related_name='theater_booking')
    
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='confirmed')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='routine')
    
    setup_time = models.IntegerField(default=30, help_text="Setup time in minutes")
    cleanup_time = models.IntegerField(default=30, help_text="Cleanup time in minutes")
    
    special_requirements = models.TextField(blank=True)
    equipment_needed = models.TextField(blank=True)
    
    booked_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='theater_bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    
    cancellation_reason = models.TextField(blank=True)
    cancelled_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='cancelled_bookings')
    cancelled_date = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_start']
        verbose_name = 'Theater Booking'
        verbose_name_plural = 'Theater Bookings'
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = f"TB{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.booking_id} - {self.operation_theater.name} - {self.surgery.surgery_id}"
    
    @property
    def duration(self):
        if self.actual_start and self.actual_end:
            return self.actual_end - self.actual_start
        return self.scheduled_end - self.scheduled_start
    
    @property
    def is_overdue(self):
        return self.scheduled_end < timezone.now() and self.status not in ['completed', 'cancelled']


class TheaterSchedule(models.Model):
    """Theater daily schedule management"""
    SCHEDULE_TYPE_CHOICES = [
        ('regular', 'Regular Hours'),
        ('emergency', 'Emergency Hours'),
        ('maintenance', 'Maintenance'),
        ('cleaning', 'Deep Cleaning'),
        ('blocked', 'Blocked'),
    ]
    
    operation_theater = models.ForeignKey(OperationTheater, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPE_CHOICES, default='regular')
    
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    is_available = models.BooleanField(default=True)
    max_bookings = models.IntegerField(default=4)
    
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='theater_schedules')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['operation_theater', 'date', 'start_time']
        verbose_name = 'Theater Schedule'
        verbose_name_plural = 'Theater Schedules'
    
    def __str__(self):
        return f"{self.operation_theater.name} - {self.date} ({self.start_time}-{self.end_time})"


class TheaterEquipmentChecklist(models.Model):
    """Pre-surgery equipment checklist"""
    CHECKLIST_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    EQUIPMENT_STATUS_CHOICES = [
        ('available', 'Available'),
        ('not_available', 'Not Available'),
        ('maintenance', 'Under Maintenance'),
        ('calibration', 'Needs Calibration'),
    ]
    
    booking = models.ForeignKey(TheaterBooking, on_delete=models.CASCADE, related_name='equipment_checklists')
    checklist_id = models.CharField(max_length=20, unique=True, blank=True)
    
    # Basic equipment checks
    anesthesia_machine = models.CharField(max_length=20, choices=EQUIPMENT_STATUS_CHOICES, default='available')
    ventilator = models.CharField(max_length=20, choices=EQUIPMENT_STATUS_CHOICES, default='available')
    monitoring_equipment = models.CharField(max_length=20, choices=EQUIPMENT_STATUS_CHOICES, default='available')
    electrocautery = models.CharField(max_length=20, choices=EQUIPMENT_STATUS_CHOICES, default='available')
    suction_unit = models.CharField(max_length=20, choices=EQUIPMENT_STATUS_CHOICES, default='available')
    defibrillator = models.CharField(max_length=20, choices=EQUIPMENT_STATUS_CHOICES, default='available')
    
    # Environmental checks
    temperature_ok = models.BooleanField(default=True)
    humidity_ok = models.BooleanField(default=True)
    air_filtration_ok = models.BooleanField(default=True)
    lighting_ok = models.BooleanField(default=True)
    emergency_power_ok = models.BooleanField(default=True)
    
    # Safety checks
    fire_extinguisher_ok = models.BooleanField(default=True)
    emergency_exits_clear = models.BooleanField(default=True)
    communication_system_ok = models.BooleanField(default=True)
    
    # Surgical instruments
    instruments_sterile = models.BooleanField(default=True)
    instruments_complete = models.BooleanField(default=True)
    implants_available = models.BooleanField(default=True)
    
    overall_status = models.CharField(max_length=20, choices=CHECKLIST_STATUS_CHOICES, default='pending')
    
    checked_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='equipment_checklists')
    checked_at = models.DateTimeField(null=True, blank=True)
    
    issues_found = models.TextField(blank=True)
    corrective_actions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Equipment Checklist'
        verbose_name_plural = 'Equipment Checklists'
    
    def save(self, *args, **kwargs):
        if not self.checklist_id:
            self.checklist_id = f"EC{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.checklist_id} - {self.booking.booking_id}"


class TheaterPreparation(models.Model):
    """Theater preparation activities"""
    PREPARATION_TYPE_CHOICES = [
        ('setup', 'Setup'),
        ('sterilization', 'Sterilization'),
        ('equipment_check', 'Equipment Check'),
        ('cleaning', 'Cleaning'),
        ('inventory_check', 'Inventory Check'),
        ('temperature_check', 'Temperature Check'),
        ('safety_check', 'Safety Check'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    booking = models.ForeignKey(TheaterBooking, on_delete=models.CASCADE, related_name='preparations')
    preparation_type = models.CharField(max_length=20, choices=PREPARATION_TYPE_CHOICES)
    
    description = models.TextField()
    estimated_duration = models.IntegerField(help_text="Duration in minutes")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    assigned_to = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='theater_preparations')
    
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    issues_encountered = models.TextField(blank=True)
    
    created_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='created_preparations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_start']
        verbose_name = 'Theater Preparation'
        verbose_name_plural = 'Theater Preparations'
    
    def __str__(self):
        return f"{self.booking.booking_id} - {self.get_preparation_type_display()}"
    
    @property
    def duration(self):
        if self.actual_start and self.actual_end:
            return self.actual_end - self.actual_start
        return None
    
    @property
    def is_overdue(self):
        return self.scheduled_end < timezone.now() and self.status not in ['completed', 'cancelled']


class TheaterUtilization(models.Model):
    """Theater utilization tracking"""
    operation_theater = models.ForeignKey(OperationTheater, on_delete=models.CASCADE, related_name='utilizations')
    date = models.DateField()
    
    total_scheduled_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_actual_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    total_surgeries = models.IntegerField(default=0)
    completed_surgeries = models.IntegerField(default=0)
    cancelled_surgeries = models.IntegerField(default=0)
    
    emergency_surgeries = models.IntegerField(default=0)
    
    # Efficiency metrics
    utilization_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    turnover_time = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Downtime tracking
    maintenance_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cleaning_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    idle_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['operation_theater', 'date']
        verbose_name = 'Theater Utilization'
        verbose_name_plural = 'Theater Utilizations'
    
    def __str__(self):
        return f"{self.operation_theater.name} - {self.date}"
    
    def calculate_utilization_rate(self):
        """Calculate theater utilization rate"""
        if self.total_scheduled_hours > 0:
            self.utilization_rate = (self.total_actual_hours / self.total_scheduled_hours) * 100
        else:
            self.utilization_rate = 0
        self.save()


class TheaterStaff(models.Model):
    """Theater staff assignments"""
    ROLE_CHOICES = [
        ('anesthesiologist', 'Anesthesiologist'),
        ('surgeon', 'Surgeon'),
        ('scrub_nurse', 'Scrub Nurse'),
        ('circulating_nurse', 'Circulating Nurse'),
        ('technician', 'Technician'),
        ('supervisor', 'Theater Supervisor'),
        ('coordinator', 'Theater Coordinator'),
    ]
    
    SHIFT_CHOICES = [
        ('morning', 'Morning Shift'),
        ('afternoon', 'Afternoon Shift'),
        ('night', 'Night Shift'),
        ('on_call', 'On Call'),
    ]
    
    user = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='theater_staff')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    operation_theater = models.ForeignKey(OperationTheater, on_delete=models.CASCADE, related_name='staff')
    
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    date = models.DateField()
    
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    is_primary = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    
    notes = models.TextField(blank=True)
    assigned_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='theater_staff_assignments')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        verbose_name = 'Theater Staff'
        verbose_name_plural = 'Theater Staff'
    
    def __str__(self):
        return f"{self.user.user.username} - {self.get_role_display()} - {self.operation_theater.name}"


class TheaterIncident(models.Model):
    """Theater incident reporting"""
    INCIDENT_TYPE_CHOICES = [
        ('equipment_failure', 'Equipment Failure'),
        ('safety_incident', 'Safety Incident'),
        ('staff_injury', 'Staff Injury'),
        ('patient_safety', 'Patient Safety'),
        ('contamination', 'Contamination'),
        ('protocol_violation', 'Protocol Violation'),
        ('communication_failure', 'Communication Failure'),
        ('other', 'Other'),
    ]
    
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('major', 'Major'),
        ('critical', 'Critical'),
    ]
    
    incident_id = models.CharField(max_length=20, unique=True, blank=True)
    operation_theater = models.ForeignKey(OperationTheater, on_delete=models.CASCADE, related_name='incidents')
    booking = models.ForeignKey(TheaterBooking, on_delete=models.CASCADE, null=True, blank=True, related_name='incidents')
    
    incident_type = models.CharField(max_length=30, choices=INCIDENT_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    
    description = models.TextField()
    occurred_at = models.DateTimeField()
    
    immediate_action_taken = models.TextField(blank=True)
    corrective_actions = models.TextField(blank=True)
    preventive_measures = models.TextField(blank=True)
    
    reported_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='reported_incidents')
    investigated_by = models.ForeignKey(HMSUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='investigated_incidents')
    
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-occurred_at']
        verbose_name = 'Theater Incident'
        verbose_name_plural = 'Theater Incidents'
    
    def save(self, *args, **kwargs):
        if not self.incident_id:
            self.incident_id = f"TI{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.incident_id} - {self.get_incident_type_display()}"


class TheaterInventory(models.Model):
    """Theater-specific inventory management"""
    ITEM_TYPE_CHOICES = [
        ('consumable', 'Consumable'),
        ('reusable', 'Reusable'),
        ('equipment', 'Equipment'),
        ('medication', 'Medication'),
        ('implant', 'Implant'),
        ('disposable', 'Disposable'),
    ]
    
    operation_theater = models.ForeignKey(OperationTheater, on_delete=models.CASCADE, related_name='inventory')
    item_name = models.CharField(max_length=200)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    
    current_stock = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=5)
    maximum_stock = models.IntegerField(default=50)
    
    unit_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    expiry_date = models.DateField(null=True, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    
    supplier = models.CharField(max_length=100, blank=True)
    last_restocked = models.DateTimeField(null=True, blank=True)
    
    is_critical = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['item_name']
        verbose_name = 'Theater Inventory'
        verbose_name_plural = 'Theater Inventories'
    
    def __str__(self):
        return f"{self.operation_theater.name} - {self.item_name}"
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.minimum_stock
    
    @property
    def is_overstocked(self):
        return self.current_stock > self.maximum_stock
    
    @property
    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False 