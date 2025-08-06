from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ESGReport(models.Model):
    """ESG (Environmental, Social, Governance) Report"""
    
    REPORT_TYPES = [
        ('environmental', 'Environmental'),
        ('social', 'Social'),
        ('governance', 'Governance'),
        ('comprehensive', 'Comprehensive ESG'),
    ]
    
    REPORT_PERIODS = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
    ]
    
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, default='comprehensive')
    period = models.CharField(max_length=20, choices=REPORT_PERIODS, default='quarterly')
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Report content
    executive_summary = models.TextField(blank=True)
    environmental_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    social_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    governance_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    overall_esg_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'ESG Report'
        verbose_name_plural = 'ESG Reports'
    
    def __str__(self):
        return f"{self.title} ({self.period} {self.start_date.year})"


class EnvironmentalMetric(models.Model):
    """Environmental metrics for ESG reporting"""
    
    METRIC_TYPES = [
        ('energy_consumption', 'Energy Consumption'),
        ('water_usage', 'Water Usage'),
        ('waste_generation', 'Waste Generation'),
        ('carbon_emissions', 'Carbon Emissions'),
        ('renewable_energy', 'Renewable Energy Usage'),
        ('recycling_rate', 'Recycling Rate'),
    ]
    
    report = models.ForeignKey(ESGReport, on_delete=models.CASCADE, related_name='environmental_metrics')
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPES)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    unit = models.CharField(max_length=50)  # kWh, liters, kg, tons CO2, etc.
    target_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Hospital-specific context
    beds_count = models.IntegerField(null=True, blank=True)  # Normalize by hospital size
    patient_days = models.IntegerField(null=True, blank=True)  # Normalize by activity
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Environmental Metric'
        verbose_name_plural = 'Environmental Metrics'
    
    def __str__(self):
        return f"{self.get_metric_type_display()}: {self.value} {self.unit}"
    
    def achievement_rate(self):
        """Calculate achievement rate vs target"""
        if self.target_value:
            return (self.value / self.target_value) * 100
        return None


class SocialMetric(models.Model):
    """Social metrics for ESG reporting"""
    
    METRIC_TYPES = [
        ('employee_satisfaction', 'Employee Satisfaction'),
        ('patient_satisfaction', 'Patient Satisfaction'),
        ('diversity_ratio', 'Diversity Ratio'),
        ('training_hours', 'Training Hours'),
        ('workplace_safety', 'Workplace Safety'),
        ('community_investment', 'Community Investment'),
        ('healthcare_access', 'Healthcare Access'),
    ]
    
    report = models.ForeignKey(ESGReport, on_delete=models.CASCADE, related_name='social_metrics')
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPES)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    unit = models.CharField(max_length=50)  # %, hours, ratio, score, etc.
    target_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Demographic breakdown
    gender_breakdown = models.JSONField(null=True, blank=True)  # Store gender statistics
    age_breakdown = models.JSONField(null=True, blank=True)  # Store age statistics
    department_breakdown = models.JSONField(null=True, blank=True)  # Store department statistics
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Social Metric'
        verbose_name_plural = 'Social Metrics'
    
    def __str__(self):
        return f"{self.get_metric_type_display()}: {self.value} {self.unit}"


class GovernanceMetric(models.Model):
    """Governance metrics for ESG reporting"""
    
    METRIC_TYPES = [
        ('board_diversity', 'Board Diversity'),
        ('ethics_training', 'Ethics Training'),
        ('audit_compliance', 'Audit Compliance'),
        ('data_privacy', 'Data Privacy'),
        ('regulatory_compliance', 'Regulatory Compliance'),
        ('transparency_score', 'Transparency Score'),
        ('risk_management', 'Risk Management'),
    ]
    
    report = models.ForeignKey(ESGReport, on_delete=models.CASCADE, related_name='governance_metrics')
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPES)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    unit = models.CharField(max_length=50)  # %, score, compliance rate, etc.
    target_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Compliance details
    certification_status = models.CharField(max_length=100, blank=True)
    compliance_frameworks = models.JSONField(null=True, blank=True)  # HIPAA, ISO, etc.
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Governance Metric'
        verbose_name_plural = 'Governance Metrics'
    
    def __str__(self):
        return f"{self.get_metric_type_display()}: {self.value} {self.unit}"


class ESGGoal(models.Model):
    """ESG Goals and Targets"""
    
    GOAL_CATEGORIES = [
        ('environmental', 'Environmental'),
        ('social', 'Social'),
        ('governance', 'Governance'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=GOAL_CATEGORIES)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    
    # Target details
    target_value = models.DecimalField(max_digits=15, decimal_places=2)
    current_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    unit = models.CharField(max_length=50)
    
    # Timeline
    start_date = models.DateField()
    target_date = models.DateField()
    
    # Status
    is_active = models.BooleanField(default=True)
    is_achieved = models.BooleanField(default=False)
    achievement_date = models.DateField(null=True, blank=True)
    
    # Ownership
    responsible_person = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', 'target_date']
        verbose_name = 'ESG Goal'
        verbose_name_plural = 'ESG Goals'
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
    
    def progress_percentage(self):
        """Calculate progress towards goal"""
        if self.target_value > 0:
            return min((self.current_value / self.target_value) * 100, 100)
        return 0
    
    def days_remaining(self):
        """Calculate days remaining to achieve goal"""
        from django.utils import timezone
        if self.target_date > timezone.now().date():
            return (self.target_date - timezone.now().date()).days
        return 0 