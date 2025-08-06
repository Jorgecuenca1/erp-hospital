from django.db import models
from django.contrib.auth.models import User


class MedicalEquipment(models.Model):
    """Medical equipment model for maintenance tracking"""
    name = models.CharField(max_length=200)
    equipment_type = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=200)
    purchase_date = models.DateField()
    warranty_expiry = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[
        ('operational', 'Operational'),
        ('maintenance', 'Under Maintenance'),
        ('repair', 'Needs Repair'),
        ('out_of_service', 'Out of Service'),
        ('decommissioned', 'Decommissioned')
    ], default='operational')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.serial_number}"


class MaintenanceSchedule(models.Model):
    """Maintenance schedule for medical equipment"""
    equipment = models.ForeignKey(MedicalEquipment, on_delete=models.CASCADE)
    maintenance_type = models.CharField(max_length=100, choices=[
        ('preventive', 'Preventive'),
        ('corrective', 'Corrective'),
        ('calibration', 'Calibration'),
        ('inspection', 'Inspection'),
        ('cleaning', 'Deep Cleaning')
    ])
    frequency = models.CharField(max_length=50, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually')
    ])
    next_maintenance = models.DateField()
    assigned_technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    estimated_duration = models.DurationField()
    priority = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], default='medium')
    status = models.CharField(max_length=50, choices=[
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.equipment.name} - {self.maintenance_type}"


class MaintenanceRecord(models.Model):
    """Record of completed maintenance"""
    equipment = models.ForeignKey(MedicalEquipment, on_delete=models.CASCADE)
    maintenance_date = models.DateField()
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    maintenance_type = models.CharField(max_length=100)
    description = models.TextField()
    parts_used = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    downtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    issues_found = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    next_maintenance_due = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment.name} - {self.maintenance_date}"


class MaintenanceAlert(models.Model):
    """Maintenance alerts and notifications"""
    equipment = models.ForeignKey(MedicalEquipment, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=100, choices=[
        ('due_maintenance', 'Maintenance Due'),
        ('overdue_maintenance', 'Overdue Maintenance'),
        ('warranty_expiry', 'Warranty Expiring'),
        ('equipment_failure', 'Equipment Failure'),
        ('calibration_due', 'Calibration Due')
    ])
    message = models.TextField()
    priority = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], default='medium')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.equipment.name} - {self.alert_type}" 