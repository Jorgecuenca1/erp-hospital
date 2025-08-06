from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
from acs_hms_base.models import Patient, HMSUser, Hospital


class DrugCategory(models.Model):
    """Drug Category Management"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Drug Category"
        verbose_name_plural = "Drug Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    """Pharmaceutical Manufacturer"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Manufacturer Name")
    contact_person = models.CharField(max_length=100, blank=True, null=True, verbose_name="Contact Person")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    license_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="License Number")
    active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Drug(models.Model):
    """Drug Master Data"""
    DRUG_TYPE_CHOICES = [
        ('TABLET', 'Tablet'),
        ('CAPSULE', 'Capsule'),
        ('SYRUP', 'Syrup'),
        ('INJECTION', 'Injection'),
        ('CREAM', 'Cream'),
        ('OINTMENT', 'Ointment'),
        ('DROPS', 'Drops'),
        ('INHALER', 'Inhaler'),
        ('SPRAY', 'Spray'),
        ('POWDER', 'Powder'),
        ('SOLUTION', 'Solution'),
        ('SUSPENSION', 'Suspension'),
    ]
    
    SCHEDULE_CHOICES = [
        ('H', 'Schedule H'),
        ('H1', 'Schedule H1'),
        ('X', 'Schedule X'),
        ('G', 'Schedule G'),
        ('OTC', 'Over The Counter'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, verbose_name="Drug Name")
    generic_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Generic Name")
    brand_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Brand Name")
    
    # Classification
    category = models.ForeignKey(DrugCategory, on_delete=models.CASCADE, related_name='drugs')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='drugs')
    
    # Drug Details
    drug_type = models.CharField(max_length=20, choices=DRUG_TYPE_CHOICES, verbose_name="Drug Type")
    strength = models.CharField(max_length=50, verbose_name="Strength")
    unit = models.CharField(max_length=20, verbose_name="Unit")
    
    # Regulatory Information
    schedule = models.CharField(max_length=10, choices=SCHEDULE_CHOICES, verbose_name="Schedule")
    drug_license_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Drug License Number")
    
    # Pricing
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    mrp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="MRP")
    
    # Inventory Management
    minimum_stock = models.PositiveIntegerField(default=10, verbose_name="Minimum Stock Level")
    maximum_stock = models.PositiveIntegerField(default=1000, verbose_name="Maximum Stock Level")
    
    # Drug Information
    indications = models.TextField(blank=True, null=True, verbose_name="Indications")
    contraindications = models.TextField(blank=True, null=True, verbose_name="Contraindications")
    side_effects = models.TextField(blank=True, null=True, verbose_name="Side Effects")
    dosage_instructions = models.TextField(blank=True, null=True, verbose_name="Dosage Instructions")
    
    # Status
    active = models.BooleanField(default=True, verbose_name="Active")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    
    class Meta:
        verbose_name = "Drug"
        verbose_name_plural = "Drugs"
        ordering = ['name']
        unique_together = ['name', 'strength', 'manufacturer']
    
    def __str__(self):
        return f"{self.name} {self.strength} - {self.manufacturer.name}"


class DrugInventory(models.Model):
    """Drug Inventory Management"""
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='inventory')
    batch_number = models.CharField(max_length=50, verbose_name="Batch Number")
    manufacturing_date = models.DateField(verbose_name="Manufacturing Date")
    expiry_date = models.DateField(verbose_name="Expiry Date")
    
    # Quantity Management
    received_quantity = models.PositiveIntegerField(verbose_name="Received Quantity")
    current_stock = models.PositiveIntegerField(verbose_name="Current Stock")
    
    # Pricing
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Purchase Price")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Selling Price")
    
    # Supplier Information
    supplier = models.CharField(max_length=100, verbose_name="Supplier")
    purchase_order_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Purchase Order Number")
    
    # Dates
    received_date = models.DateField(verbose_name="Received Date")
    
    # Status
    active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Drug Inventory"
        verbose_name_plural = "Drug Inventories"
        ordering = ['expiry_date']
        unique_together = ['drug', 'batch_number']
    
    def __str__(self):
        return f"{self.drug.name} - Batch: {self.batch_number}"
    
    @property
    def is_expired(self):
        """Check if drug batch is expired"""
        return self.expiry_date < timezone.now().date()
    
    @property
    def days_to_expire(self):
        """Calculate days until expiry"""
        return (self.expiry_date - timezone.now().date()).days


class Prescription(models.Model):
    """Prescription Management"""
    PRESCRIPTION_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PARTIALLY_DISPENSED', 'Partially Dispensed'),
        ('DISPENSED', 'Dispensed'),
        ('CANCELLED', 'Cancelled'),
        ('EXPIRED', 'Expired'),
    ]
    
    # Basic Information
    prescription_number = models.CharField(max_length=20, unique=True, verbose_name="Prescription Number")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='prescriptions', limit_choices_to={'user_type': 'DOCTOR'})
    
    # Prescription Details
    prescription_date = models.DateField(verbose_name="Prescription Date")
    diagnosis = models.TextField(blank=True, null=True, verbose_name="Diagnosis")
    
    # Status
    status = models.CharField(max_length=20, choices=PRESCRIPTION_STATUS_CHOICES, default='PENDING', verbose_name="Status")
    
    # Financial Information
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total Amount")
    insurance_coverage = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Insurance Coverage")
    patient_payable = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Patient Payable")
    
    # Dates
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    
    class Meta:
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"
        ordering = ['-prescription_date']
    
    def __str__(self):
        return f"Prescription {self.prescription_number} - {self.patient.full_name}"


class PrescriptionItem(models.Model):
    """Prescription Items"""
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='prescription_items')
    
    # Dosage Information
    dosage = models.CharField(max_length=50, verbose_name="Dosage")
    frequency = models.CharField(max_length=50, verbose_name="Frequency")
    duration = models.CharField(max_length=50, verbose_name="Duration")
    instructions = models.TextField(blank=True, null=True, verbose_name="Instructions")
    
    # Quantity
    quantity_prescribed = models.PositiveIntegerField(verbose_name="Quantity Prescribed")
    quantity_dispensed = models.PositiveIntegerField(default=0, verbose_name="Quantity Dispensed")
    
    # Pricing
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")
    
    # Status
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PARTIALLY_DISPENSED', 'Partially Dispensed'),
        ('DISPENSED', 'Dispensed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")
    
    class Meta:
        verbose_name = "Prescription Item"
        verbose_name_plural = "Prescription Items"
    
    def __str__(self):
        return f"{self.drug.name} - {self.prescription.prescription_number}"
    
    @property
    def remaining_quantity(self):
        """Calculate remaining quantity to be dispensed"""
        return self.quantity_prescribed - self.quantity_dispensed


class PharmacyDispensing(models.Model):
    """Pharmacy Dispensing Records"""
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='dispensing_records')
    dispensing_date = models.DateTimeField(verbose_name="Dispensing Date")
    dispensed_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='dispensed_prescriptions', limit_choices_to={'user_type': 'PHARMACIST'})
    
    # Payment Information
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount Paid")
    payment_method = models.CharField(max_length=20, choices=[
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('INSURANCE', 'Insurance'),
        ('CREDIT', 'Credit'),
    ], verbose_name="Payment Method")
    
    # Receipt Information
    receipt_number = models.CharField(max_length=50, unique=True, verbose_name="Receipt Number")
    
    # Notes
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Pharmacy Dispensing"
        verbose_name_plural = "Pharmacy Dispensing"
        ordering = ['-dispensing_date']
    
    def __str__(self):
        return f"Dispensing {self.receipt_number} - {self.prescription.patient.full_name}"


class DispensingItem(models.Model):
    """Dispensing Item Details"""
    dispensing = models.ForeignKey(PharmacyDispensing, on_delete=models.CASCADE, related_name='items')
    prescription_item = models.ForeignKey(PrescriptionItem, on_delete=models.CASCADE, related_name='dispensing_items')
    drug_inventory = models.ForeignKey(DrugInventory, on_delete=models.CASCADE, related_name='dispensing_items')
    
    # Quantity
    quantity_dispensed = models.PositiveIntegerField(verbose_name="Quantity Dispensed")
    
    # Pricing
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")
    
    class Meta:
        verbose_name = "Dispensing Item"
        verbose_name_plural = "Dispensing Items"
    
    def __str__(self):
        return f"{self.prescription_item.drug.name} - {self.quantity_dispensed} units"


class PharmacyBilling(models.Model):
    """Pharmacy Billing"""
    BILL_TYPE_CHOICES = [
        ('PRESCRIPTION', 'Prescription'),
        ('OTC', 'Over The Counter'),
        ('EMERGENCY', 'Emergency'),
    ]
    
    # Basic Information
    bill_number = models.CharField(max_length=20, unique=True, verbose_name="Bill Number")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='pharmacy_bills')
    bill_date = models.DateTimeField(verbose_name="Bill Date")
    bill_type = models.CharField(max_length=20, choices=BILL_TYPE_CHOICES, verbose_name="Bill Type")
    
    # Financial Information
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Tax Amount")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Discount Amount")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount")
    
    # Payment Information
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount Paid")
    payment_method = models.CharField(max_length=20, choices=[
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('INSURANCE', 'Insurance'),
        ('CREDIT', 'Credit'),
    ], verbose_name="Payment Method")
    
    # Insurance Information
    insurance_coverage = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Insurance Coverage")
    insurance_claim_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Insurance Claim Number")
    
    # Staff Information
    billed_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='pharmacy_bills')
    
    class Meta:
        verbose_name = "Pharmacy Billing"
        verbose_name_plural = "Pharmacy Billings"
        ordering = ['-bill_date']
    
    def __str__(self):
        return f"Bill {self.bill_number} - {self.patient.full_name}"


class PharmacySettings(models.Model):
    """Pharmacy Configuration Settings"""
    hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE, related_name='pharmacy_settings')
    
    # Billing Settings
    enable_tax = models.BooleanField(default=True, verbose_name="Enable Tax")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Tax Rate (%)")
    
    # Inventory Settings
    low_stock_alert_days = models.PositiveIntegerField(default=30, verbose_name="Low Stock Alert (Days)")
    expiry_alert_days = models.PositiveIntegerField(default=90, verbose_name="Expiry Alert (Days)")
    
    # Prescription Settings
    prescription_validity_days = models.PositiveIntegerField(default=7, verbose_name="Prescription Validity (Days)")
    allow_partial_dispensing = models.BooleanField(default=True, verbose_name="Allow Partial Dispensing")
    
    # Pricing Settings
    markup_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=20.00, verbose_name="Markup Percentage")
    
    class Meta:
        verbose_name = "Pharmacy Settings"
        verbose_name_plural = "Pharmacy Settings"
    
    def __str__(self):
        return f"Pharmacy Settings - {self.hospital.name}"


class DrugInteraction(models.Model):
    """Drug Interaction Management"""
    INTERACTION_SEVERITY_CHOICES = [
        ('MILD', 'Mild'),
        ('MODERATE', 'Moderate'),
        ('SEVERE', 'Severe'),
        ('CONTRAINDICATED', 'Contraindicated'),
    ]
    
    drug1 = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='interactions_as_drug1')
    drug2 = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='interactions_as_drug2')
    
    # Interaction Details
    severity = models.CharField(max_length=20, choices=INTERACTION_SEVERITY_CHOICES, verbose_name="Severity")
    description = models.TextField(verbose_name="Description")
    clinical_significance = models.TextField(blank=True, null=True, verbose_name="Clinical Significance")
    management = models.TextField(blank=True, null=True, verbose_name="Management")
    
    # Status
    active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Drug Interaction"
        verbose_name_plural = "Drug Interactions"
        unique_together = ['drug1', 'drug2']
    
    def __str__(self):
        return f"{self.drug1.name} - {self.drug2.name} ({self.severity})"


class PharmacyStockAdjustment(models.Model):
    """Stock Adjustment Records"""
    ADJUSTMENT_TYPE_CHOICES = [
        ('INCREASE', 'Stock Increase'),
        ('DECREASE', 'Stock Decrease'),
        ('DAMAGE', 'Damage'),
        ('EXPIRED', 'Expired'),
        ('LOST', 'Lost'),
        ('RETURN', 'Return'),
    ]
    
    drug_inventory = models.ForeignKey(DrugInventory, on_delete=models.CASCADE, related_name='adjustments')
    adjustment_type = models.CharField(max_length=20, choices=ADJUSTMENT_TYPE_CHOICES, verbose_name="Adjustment Type")
    quantity = models.IntegerField(verbose_name="Quantity")
    reason = models.TextField(verbose_name="Reason")
    
    # Staff Information
    adjusted_by = models.ForeignKey(HMSUser, on_delete=models.CASCADE, related_name='stock_adjustments')
    adjustment_date = models.DateTimeField(auto_now_add=True, verbose_name="Adjustment Date")
    
    class Meta:
        verbose_name = "Stock Adjustment"
        verbose_name_plural = "Stock Adjustments"
        ordering = ['-adjustment_date']
    
    def __str__(self):
        return f"{self.drug_inventory.drug.name} - {self.adjustment_type} ({self.quantity})" 