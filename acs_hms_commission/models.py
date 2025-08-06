from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser, Patient
from accounting.models import AsientoContable, CuentaContable
import uuid


class CommissionStructure(models.Model):
    """Commission structure configuration"""
    CALCULATION_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('flat_fee', 'Flat Fee'),
        ('tiered', 'Tiered Structure'),
        ('custom', 'Custom Formula'),
    ]
    
    SERVICE_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('procedure', 'Procedure'),
        ('surgery', 'Surgery'),
        ('test', 'Diagnostic Test'),
        ('referral', 'Referral'),
        ('prescription', 'Prescription'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    calculation_type = models.CharField(max_length=20, choices=CALCULATION_TYPE_CHOICES)
    
    # Percentage-based commission
    percentage_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Flat fee commission
    flat_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Tiered structure (JSON)
    tier_structure = models.JSONField(
        default=dict,
        help_text="JSON structure for tiered commissions"
    )
    
    # Custom formula
    custom_formula = models.TextField(
        blank=True,
        help_text="Custom formula for commission calculation"
    )
    
    # Conditions
    minimum_service_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Minimum service amount to qualify for commission"
    )
    maximum_commission = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Maximum commission amount (null = no limit)"
    )
    
    # Settings
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commission_structures')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['service_type', 'name']
        verbose_name = 'Commission Structure'
        verbose_name_plural = 'Commission Structures'
    
    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"
    
    def calculate_commission(self, service_amount):
        """Calculate commission based on service amount"""
        if service_amount < self.minimum_service_amount:
            return 0
        
        commission = 0
        
        if self.calculation_type == 'percentage':
            commission = (service_amount * self.percentage_rate) / 100
        elif self.calculation_type == 'flat_fee':
            commission = self.flat_fee_amount
        elif self.calculation_type == 'tiered':
            commission = self._calculate_tiered_commission(service_amount)
        elif self.calculation_type == 'custom':
            commission = self._calculate_custom_commission(service_amount)
        
        # Apply maximum commission limit
        if self.maximum_commission and commission > self.maximum_commission:
            commission = self.maximum_commission
        
        return commission
    
    def _calculate_tiered_commission(self, service_amount):
        """Calculate tiered commission"""
        if not self.tier_structure:
            return 0
        
        # Example tier structure:
        # {
        #     "tiers": [
        #         {"min": 0, "max": 1000, "rate": 5},
        #         {"min": 1000, "max": 5000, "rate": 10},
        #         {"min": 5000, "max": null, "rate": 15}
        #     ]
        # }
        
        tiers = self.tier_structure.get('tiers', [])
        commission = 0
        
        for tier in tiers:
            tier_min = tier.get('min', 0)
            tier_max = tier.get('max')
            tier_rate = tier.get('rate', 0)
            
            if service_amount > tier_min:
                if tier_max is None or service_amount <= tier_max:
                    # Amount falls within this tier
                    applicable_amount = service_amount - tier_min
                    commission = (applicable_amount * tier_rate) / 100
                    break
                else:
                    # Amount exceeds this tier
                    applicable_amount = tier_max - tier_min
                    commission += (applicable_amount * tier_rate) / 100
        
        return commission
    
    def _calculate_custom_commission(self, service_amount):
        """Calculate custom commission (simplified)"""
        # This would need proper formula parsing
        # For now, return 0
        return 0


class CommissionAgent(models.Model):
    """Commission agent (doctor, referrer, etc.)"""
    AGENT_TYPE_CHOICES = [
        ('doctor', 'Doctor'),
        ('referrer', 'Referrer'),
        ('employee', 'Employee'),
        ('partner', 'Partner'),
        ('external', 'External Agent'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='commission_agent')
    agent_type = models.CharField(max_length=20, choices=AGENT_TYPE_CHOICES)
    
    # Agent details
    agent_code = models.CharField(max_length=50, unique=True)
    
    # Contact information
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Banking details
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    routing_number = models.CharField(max_length=20, blank=True)
    
    # Commission settings
    default_commission_structure = models.ForeignKey(
        CommissionStructure, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='default_agents'
    )
    
    # Settings
    is_active = models.BooleanField(default=True)
    commission_threshold = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Minimum commission amount before payout"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['agent_code']
        verbose_name = 'Commission Agent'
        verbose_name_plural = 'Commission Agents'
    
    def __str__(self):
        return f"{self.agent_code} - {self.user.get_full_name()}"
    
    def get_total_commission_earned(self):
        """Get total commission earned"""
        return self.commission_records.filter(
            status='approved'
        ).aggregate(
            total=models.Sum('commission_amount')
        )['total'] or 0
    
    def get_total_commission_paid(self):
        """Get total commission paid"""
        return self.commission_records.filter(
            status='paid'
        ).aggregate(
            total=models.Sum('commission_amount')
        )['total'] or 0
    
    def get_pending_commission(self):
        """Get pending commission amount"""
        return self.commission_records.filter(
            status__in=['pending', 'approved']
        ).aggregate(
            total=models.Sum('commission_amount')
        )['total'] or 0


class CommissionRecord(models.Model):
    """Individual commission record"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('disputed', 'Disputed'),
    ]
    
    # Reference
    commission_id = models.CharField(max_length=100, unique=True, editable=False)
    
    # Agent and structure
    agent = models.ForeignKey(CommissionAgent, on_delete=models.CASCADE, related_name='commission_records')
    structure = models.ForeignKey(CommissionStructure, on_delete=models.CASCADE, related_name='commission_records')
    
    # Service details
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='commission_records')
    service_description = models.TextField()
    service_amount = models.DecimalField(max_digits=12, decimal_places=2)
    service_date = models.DateField()
    
    # Commission calculation
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2)
    calculation_details = models.JSONField(
        default=dict,
        help_text="Details of commission calculation"
    )
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Approval
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_commissions'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_notes = models.TextField(blank=True)
    
    # Payment
    paid_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='paid_commissions'
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    
    # Accounting integration
    asiento_contable = models.ForeignKey(
        AsientoContable, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commission_records')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Commission Record'
        verbose_name_plural = 'Commission Records'
    
    def __str__(self):
        return f"{self.commission_id} - {self.agent.agent_code} - ${self.commission_amount}"
    
    def save(self, *args, **kwargs):
        if not self.commission_id:
            self.commission_id = f"COM{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        
        # Calculate commission if not set
        if not self.commission_amount:
            self.commission_amount = self.structure.calculate_commission(self.service_amount)
            self.calculation_details = {
                'structure_name': self.structure.name,
                'service_amount': float(self.service_amount),
                'commission_rate': float(self.structure.percentage_rate),
                'calculation_type': self.structure.calculation_type,
                'calculated_at': timezone.now().isoformat()
            }
        
        super().save(*args, **kwargs)
    
    def approve(self, approved_by, notes=''):
        """Approve commission"""
        self.status = 'approved'
        self.approved_by = approved_by
        self.approved_at = timezone.now()
        self.approval_notes = notes
        self.save()
    
    def pay(self, paid_by, payment_method, payment_reference=''):
        """Mark commission as paid"""
        self.status = 'paid'
        self.paid_by = paid_by
        self.paid_at = timezone.now()
        self.payment_method = payment_method
        self.payment_reference = payment_reference
        
        # Create accounting entry
        self.create_accounting_entry()
        self.save()
    
    def create_accounting_entry(self):
        """Create accounting entry for commission payment"""
        try:
            # Get or create commission expense account
            expense_account, created = CuentaContable.objects.get_or_create(
                codigo='6200',
                defaults={
                    'nombre': 'Commission Expenses',
                    'tipo': 'gasto',
                    'descripcion': 'Commission payments to agents'
                }
            )
            
            # Create accounting entry
            asiento = AsientoContable.objects.create(
                fecha=self.paid_at.date(),
                concepto=f'Commission payment - {self.agent.agent_code}',
                referencia=self.commission_id,
                monto=self.commission_amount
            )
            
            self.asiento_contable = asiento
            
        except Exception as e:
            print(f"Error creating accounting entry: {e}")


class CommissionPayment(models.Model):
    """Batch commission payments"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('cash', 'Cash'),
        ('paypal', 'PayPal'),
        ('other', 'Other'),
    ]
    
    # Reference
    payment_id = models.CharField(max_length=100, unique=True, editable=False)
    
    # Agent and amount
    agent = models.ForeignKey(CommissionAgent, on_delete=models.CASCADE, related_name='payments')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Payment details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateField()
    payment_reference = models.CharField(max_length=100, blank=True)
    
    # Commission records included
    commission_records = models.ManyToManyField(CommissionRecord, related_name='payments')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Processing
    processed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='processed_payments'
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Accounting integration
    asiento_contable = models.ForeignKey(
        AsientoContable, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commission_payments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Commission Payment'
        verbose_name_plural = 'Commission Payments'
    
    def __str__(self):
        return f"{self.payment_id} - {self.agent.agent_code} - ${self.total_amount}"
    
    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = f"PAY{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        
        super().save(*args, **kwargs)
    
    def process_payment(self, processed_by):
        """Process the payment"""
        self.status = 'processed'
        self.processed_by = processed_by
        self.processed_at = timezone.now()
        
        # Mark all commission records as paid
        for record in self.commission_records.all():
            record.pay(processed_by, self.payment_method, self.payment_reference)
        
        # Create accounting entry
        self.create_accounting_entry()
        self.save()
    
    def create_accounting_entry(self):
        """Create accounting entry for batch payment"""
        try:
            # Get or create commission expense account
            expense_account, created = CuentaContable.objects.get_or_create(
                codigo='6200',
                defaults={
                    'nombre': 'Commission Expenses',
                    'tipo': 'gasto',
                    'descripcion': 'Commission payments to agents'
                }
            )
            
            # Create accounting entry
            asiento = AsientoContable.objects.create(
                fecha=self.payment_date,
                concepto=f'Batch commission payment - {self.agent.agent_code}',
                referencia=self.payment_id,
                monto=self.total_amount
            )
            
            self.asiento_contable = asiento
            
        except Exception as e:
            print(f"Error creating accounting entry: {e}")


class CommissionReport(models.Model):
    """Commission reports"""
    REPORT_TYPE_CHOICES = [
        ('monthly', 'Monthly Report'),
        ('quarterly', 'Quarterly Report'),
        ('annual', 'Annual Report'),
        ('custom', 'Custom Report'),
    ]
    
    # Report details
    report_id = models.CharField(max_length=100, unique=True, editable=False)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    
    # Date range
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Filters
    agent_filter = models.ManyToManyField(CommissionAgent, blank=True)
    structure_filter = models.ManyToManyField(CommissionStructure, blank=True)
    
    # Report data (JSON)
    report_data = models.JSONField(default=dict)
    
    # File generation
    report_file = models.FileField(upload_to='commission_reports/', null=True, blank=True)
    
    # Metadata
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commission_reports')
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-generated_at']
        verbose_name = 'Commission Report'
        verbose_name_plural = 'Commission Reports'
    
    def __str__(self):
        return f"{self.report_id} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.report_id:
            self.report_id = f"REP{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        
        super().save(*args, **kwargs)


class CommissionConfiguration(models.Model):
    """Commission system configuration"""
    # Auto-approval settings
    auto_approve_under_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Auto-approve commissions under this amount"
    )
    
    # Payment settings
    minimum_payment_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=100.00,
        help_text="Minimum amount for batch payments"
    )
    payment_frequency_days = models.IntegerField(
        default=30,
        help_text="Payment frequency in days"
    )
    
    # Notification settings
    notify_on_commission_earned = models.BooleanField(default=True)
    notify_on_payment_processed = models.BooleanField(default=True)
    
    # Accounting integration
    default_commission_account = models.CharField(
        max_length=20,
        default='6200',
        help_text="Default account code for commission expenses"
    )
    
    # Metadata
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Commission Configuration'
        verbose_name_plural = 'Commission Configurations'
    
    def __str__(self):
        return f"Commission Configuration - Updated {self.updated_at}"
    
    def save(self, *args, **kwargs):
        # Ensure only one configuration instance exists
        if not self.pk and CommissionConfiguration.objects.exists():
            raise ValueError("Only one configuration instance is allowed")
        super().save(*args, **kwargs) 