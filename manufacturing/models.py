from django.db import models
from django.contrib.auth.models import User


class MedicalDevice(models.Model):
    """Medical device product model"""
    name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, unique=True)
    manufacturing_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('discontinued', 'Discontinued')
    ], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.serial_number}"


class ProductionOrder(models.Model):
    """Production order for medical devices"""
    order_number = models.CharField(max_length=100, unique=True)
    device = models.ForeignKey(MedicalDevice, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    priority = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium')
    status = models.CharField(max_length=50, choices=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='draft')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number} - {self.device.name}"


class QualityCheck(models.Model):
    """Quality control for manufactured devices"""
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE)
    check_type = models.CharField(max_length=100)
    result = models.CharField(max_length=50, choices=[
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('pending', 'Pending')
    ], default='pending')
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QC {self.check_type} - {self.result}"


class BillOfMaterials(models.Model):
    """Bill of materials for medical devices"""
    device = models.ForeignKey(MedicalDevice, on_delete=models.CASCADE)
    component_name = models.CharField(max_length=200)
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=200)
    is_critical = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.component_name} for {self.device.name}" 