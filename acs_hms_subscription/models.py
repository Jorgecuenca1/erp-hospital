from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from acs_hms_base.models import HMSUser, Patient
import uuid


class SubscriptionPlan(models.Model):
    """Hospital subscription plans"""
    PLAN_TYPE_CHOICES = [
        ('basic', 'Basic Plan'),
        ('standard', 'Standard Plan'),
        ('premium', 'Premium Plan'),
        ('enterprise', 'Enterprise Plan'),
        ('custom', 'Custom Plan'),
    ]
    
    BILLING_CYCLE_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
        ('annual', 'Annual'),
        ('lifetime', 'Lifetime'),
    ]
    
    name = models.CharField(max_length=200)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    description = models.TextField()
    
    # Pricing
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quarterly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    semi_annual_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    annual_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    lifetime_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Features
    max_patients = models.IntegerField(default=100)
    max_doctors = models.IntegerField(default=10)
    max_appointments = models.IntegerField(default=500)
    max_storage_gb = models.IntegerField(default=10)
    
    # Module Access
    includes_laboratory = models.BooleanField(default=True)
    includes_pharmacy = models.BooleanField(default=True)
    includes_radiology = models.BooleanField(default=False)
    includes_surgery = models.BooleanField(default=False)
    includes_telemedicine = models.BooleanField(default=False)
    includes_insurance = models.BooleanField(default=False)
    includes_billing = models.BooleanField(default=True)
    includes_inventory = models.BooleanField(default=True)
    includes_hr = models.BooleanField(default=False)
    includes_accounting = models.BooleanField(default=False)
    includes_reports = models.BooleanField(default=True)
    
    # Support Features
    email_support = models.BooleanField(default=True)
    phone_support = models.BooleanField(default=False)
    priority_support = models.BooleanField(default=False)
    dedicated_support = models.BooleanField(default=False)
    
    # Technical Features
    api_access = models.BooleanField(default=False)
    custom_integrations = models.BooleanField(default=False)
    white_labeling = models.BooleanField(default=False)
    multi_branch = models.BooleanField(default=False)
    
    # Trial and Discounts
    trial_days = models.IntegerField(default=14)
    setup_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'
    
    def __str__(self):
        return f"{self.name} - {self.get_plan_type_display()}"
    
    def get_price_by_cycle(self, cycle):
        """Get price based on billing cycle"""
        price_map = {
            'monthly': self.monthly_price,
            'quarterly': self.quarterly_price,
            'semi_annual': self.semi_annual_price,
            'annual': self.annual_price,
            'lifetime': self.lifetime_price,
        }
        return price_map.get(cycle, self.monthly_price)


class HospitalSubscription(models.Model):
    """Hospital subscription records"""
    STATUS_CHOICES = [
        ('trial', 'Trial'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]
    
    BILLING_CYCLE_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
        ('annual', 'Annual'),
        ('lifetime', 'Lifetime'),
    ]
    
    subscription_id = models.CharField(max_length=20, unique=True, blank=True)
    hospital_name = models.CharField(max_length=200)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hospital_subscriptions')
    
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='subscriptions')
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLE_CHOICES, default='monthly')
    
    # Subscription dates
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    trial_end_date = models.DateTimeField(null=True, blank=True)
    
    # Current status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trial')
    
    # Billing information
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Usage tracking
    current_patients = models.IntegerField(default=0)
    current_doctors = models.IntegerField(default=0)
    current_appointments = models.IntegerField(default=0)
    current_storage_gb = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Billing details
    billing_email = models.EmailField()
    billing_phone = models.CharField(max_length=20)
    billing_address = models.TextField()
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_country = models.CharField(max_length=100)
    billing_zip_code = models.CharField(max_length=20)
    
    # Payment information
    payment_method = models.CharField(max_length=50, blank=True)
    payment_gateway = models.CharField(max_length=50, blank=True)
    gateway_customer_id = models.CharField(max_length=100, blank=True)
    
    # Renewal settings
    auto_renewal = models.BooleanField(default=True)
    renewal_reminder_sent = models.BooleanField(default=False)
    
    # Cancellation
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cancelled_subscriptions')
    cancellation_reason = models.TextField(blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Hospital Subscription'
        verbose_name_plural = 'Hospital Subscriptions'
    
    def save(self, *args, **kwargs):
        if not self.subscription_id:
            self.subscription_id = f"SUB{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.subscription_id} - {self.hospital_name}"
    
    @property
    def is_trial(self):
        return self.status == 'trial'
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    @property
    def is_expired(self):
        return timezone.now() > self.end_date
    
    @property
    def days_until_expiry(self):
        if self.end_date:
            return (self.end_date - timezone.now()).days
        return None
    
    @property
    def usage_percentage(self):
        """Calculate usage percentage for various limits"""
        return {
            'patients': (self.current_patients / self.plan.max_patients) * 100 if self.plan.max_patients > 0 else 0,
            'doctors': (self.current_doctors / self.plan.max_doctors) * 100 if self.plan.max_doctors > 0 else 0,
            'appointments': (self.current_appointments / self.plan.max_appointments) * 100 if self.plan.max_appointments > 0 else 0,
            'storage': (float(self.current_storage_gb) / self.plan.max_storage_gb) * 100 if self.plan.max_storage_gb > 0 else 0,
        }


class SubscriptionInvoice(models.Model):
    """Subscription billing invoices"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    invoice_id = models.CharField(max_length=20, unique=True, blank=True)
    subscription = models.ForeignKey(HospitalSubscription, on_delete=models.CASCADE, related_name='invoices')
    
    # Invoice details
    invoice_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    paid_date = models.DateTimeField(null=True, blank=True)
    
    # Billing period
    billing_period_start = models.DateTimeField()
    billing_period_end = models.DateTimeField()
    
    # Amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Payment information
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-invoice_date']
        verbose_name = 'Subscription Invoice'
        verbose_name_plural = 'Subscription Invoices'
    
    def save(self, *args, **kwargs):
        if not self.invoice_id:
            self.invoice_id = f"INV{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        
        # Calculate total amount
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.invoice_id} - {self.subscription.hospital_name}"
    
    @property
    def is_overdue(self):
        return timezone.now() > self.due_date and self.status == 'pending'


class SubscriptionUsage(models.Model):
    """Monthly usage tracking for subscriptions"""
    subscription = models.ForeignKey(HospitalSubscription, on_delete=models.CASCADE, related_name='usage_records')
    
    # Usage period
    usage_month = models.DateField()
    
    # Usage metrics
    patients_count = models.IntegerField(default=0)
    doctors_count = models.IntegerField(default=0)
    appointments_count = models.IntegerField(default=0)
    storage_gb = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Module usage
    laboratory_usage = models.IntegerField(default=0)
    pharmacy_usage = models.IntegerField(default=0)
    radiology_usage = models.IntegerField(default=0)
    surgery_usage = models.IntegerField(default=0)
    telemedicine_usage = models.IntegerField(default=0)
    
    # API usage
    api_calls = models.IntegerField(default=0)
    
    # System usage
    login_count = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)
    
    # Calculated fields
    overage_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-usage_month']
        unique_together = ['subscription', 'usage_month']
        verbose_name = 'Subscription Usage'
        verbose_name_plural = 'Subscription Usage'
    
    def __str__(self):
        return f"{self.subscription.hospital_name} - {self.usage_month}"


class SubscriptionModuleAccess(models.Model):
    """Module access control for subscriptions"""
    subscription = models.ForeignKey(HospitalSubscription, on_delete=models.CASCADE, related_name='module_access')
    
    # Module names
    module_name = models.CharField(max_length=100)
    module_display_name = models.CharField(max_length=200)
    
    # Access control
    is_enabled = models.BooleanField(default=True)
    usage_limit = models.IntegerField(null=True, blank=True)
    current_usage = models.IntegerField(default=0)
    
    # Dates
    enabled_date = models.DateTimeField(auto_now_add=True)
    disabled_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['module_name']
        unique_together = ['subscription', 'module_name']
        verbose_name = 'Subscription Module Access'
        verbose_name_plural = 'Subscription Module Access'
    
    def __str__(self):
        return f"{self.subscription.hospital_name} - {self.module_display_name}"
    
    @property
    def is_over_limit(self):
        if self.usage_limit is None:
            return False
        return self.current_usage >= self.usage_limit


class SubscriptionDiscount(models.Model):
    """Discount codes and promotions"""
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed_amount', 'Fixed Amount'),
        ('free_months', 'Free Months'),
        ('free_trial', 'Extended Free Trial'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    # Usage limits
    usage_limit = models.IntegerField(null=True, blank=True)
    current_usage = models.IntegerField(default=0)
    per_customer_limit = models.IntegerField(default=1)
    
    # Applicable plans
    applicable_plans = models.ManyToManyField(SubscriptionPlan, blank=True)
    
    # Conditions
    minimum_billing_cycle = models.CharField(max_length=20, choices=SubscriptionPlan.BILLING_CYCLE_CHOICES, blank=True)
    first_time_customers_only = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Subscription Discount'
        verbose_name_plural = 'Subscription Discounts'
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def is_valid(self):
        now = timezone.now()
        return (self.valid_from <= now <= self.valid_until and 
                self.is_active and 
                (self.usage_limit is None or self.current_usage < self.usage_limit))
    
    def apply_discount(self, amount):
        """Apply discount to amount"""
        if self.discount_type == 'percentage':
            return amount * (self.discount_value / 100)
        elif self.discount_type == 'fixed_amount':
            return min(self.discount_value, amount)
        return 0


class SubscriptionPayment(models.Model):
    """Payment records for subscriptions"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    payment_id = models.CharField(max_length=20, unique=True, blank=True)
    subscription = models.ForeignKey(HospitalSubscription, on_delete=models.CASCADE, related_name='payments')
    invoice = models.ForeignKey(SubscriptionInvoice, on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(max_length=50)
    
    # Gateway information
    gateway = models.CharField(max_length=50)
    gateway_transaction_id = models.CharField(max_length=100, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    
    # Status and dates
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(null=True, blank=True)
    
    # Refund information
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    refund_reason = models.TextField(blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    
    # Discount applied
    discount = models.ForeignKey(SubscriptionDiscount, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date']
        verbose_name = 'Subscription Payment'
        verbose_name_plural = 'Subscription Payments'
    
    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = f"PAY{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.payment_id} - {self.subscription.hospital_name} - {self.amount}" 