from django.db import models
from django.contrib.auth.models import User


class ResourceType(models.Model):
    """Types of hospital resources"""
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=[
        ('staff', 'Staff'),
        ('equipment', 'Equipment'),
        ('room', 'Room/Space'),
        ('vehicle', 'Vehicle'),
        ('supply', 'Supply')
    ])
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ResourceAllocation(models.Model):
    """Resource allocation planning"""
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    planned_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    allocated_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    responsible_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], default='medium')
    status = models.CharField(max_length=20, choices=[
        ('planned', 'Planned'),
        ('approved', 'Approved'),
        ('allocated', 'Allocated'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='planned')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resource_type.name} - {self.department}"


class StaffSchedule(models.Model):
    """Staff scheduling and planning"""
    staff_member = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    shift_type = models.CharField(max_length=20, choices=[
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night'),
        ('on_call', 'On Call')
    ])
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    role = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff_member.username} - {self.start_datetime.date()}"


class CapacityPlanning(models.Model):
    """Hospital capacity planning"""
    department = models.CharField(max_length=100)
    planning_period = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual')
    ])
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    current_capacity = models.DecimalField(max_digits=10, decimal_places=2)
    planned_capacity = models.DecimalField(max_digits=10, decimal_places=2)
    utilization_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    forecasted_demand = models.DecimalField(max_digits=10, decimal_places=2)
    gap_analysis = models.TextField(blank=True)
    action_plan = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.department} - {self.resource_type.name}" 