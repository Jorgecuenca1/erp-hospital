from django.db import models
from django.contrib.auth.models import User


class RentalEquipment(models.Model):
    """Medical equipment available for rental"""
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=[
        ('diagnostic', 'Diagnostic Equipment'),
        ('monitoring', 'Monitoring Equipment'),
        ('therapeutic', 'Therapeutic Equipment'),
        ('surgical', 'Surgical Equipment'),
        ('mobility', 'Mobility Equipment'),
        ('respiratory', 'Respiratory Equipment')
    ])
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    weekly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired')
    ], default='available')
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.serial_number}"


class RentalAgreement(models.Model):
    """Rental agreements"""
    agreement_number = models.CharField(max_length=50, unique=True)
    equipment = models.ForeignKey(RentalEquipment, on_delete=models.CASCADE)
    renter_name = models.CharField(max_length=200)
    renter_contact = models.CharField(max_length=50)
    renter_address = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    rental_period = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom')
    ])
    rental_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('overdue', 'Overdue')
    ], default='active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.agreement_number} - {self.equipment.name}"


class RentalPayment(models.Model):
    """Rental payments"""
    agreement = models.ForeignKey(RentalAgreement, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[
        ('cash', 'Cash'),
        ('card', 'Credit Card'),
        ('transfer', 'Bank Transfer'),
        ('check', 'Check')
    ])
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_type = models.CharField(max_length=20, choices=[
        ('rental', 'Rental Payment'),
        ('deposit', 'Security Deposit'),
        ('penalty', 'Late Fee'),
        ('damage', 'Damage Charge')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.amount} - {self.agreement.agreement_number}"


class RentalInspection(models.Model):
    """Equipment inspection records"""
    agreement = models.ForeignKey(RentalAgreement, on_delete=models.CASCADE)
    inspection_type = models.CharField(max_length=20, choices=[
        ('pre_rental', 'Pre-Rental'),
        ('post_rental', 'Post-Rental'),
        ('periodic', 'Periodic'),
        ('damage', 'Damage Assessment')
    ])
    inspection_date = models.DateField()
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    condition = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('damaged', 'Damaged')
    ])
    notes = models.TextField(blank=True)
    damage_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inspection {self.inspection_type} - {self.agreement.agreement_number}" 