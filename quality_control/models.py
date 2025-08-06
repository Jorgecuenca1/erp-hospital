from django.db import models
from django.contrib.auth.models import User


class QualityStandard(models.Model):
    """Quality standards for hospital services"""
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=[
        ('patient_safety', 'Patient Safety'),
        ('infection_control', 'Infection Control'),
        ('medication_safety', 'Medication Safety'),
        ('clinical_excellence', 'Clinical Excellence'),
        ('service_quality', 'Service Quality'),
        ('regulatory_compliance', 'Regulatory Compliance')
    ])
    description = models.TextField()
    target_value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually')
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class QualityAudit(models.Model):
    """Quality audit records"""
    audit_type = models.CharField(max_length=100, choices=[
        ('internal', 'Internal Audit'),
        ('external', 'External Audit'),
        ('regulatory', 'Regulatory Audit'),
        ('accreditation', 'Accreditation Audit')
    ])
    department = models.CharField(max_length=100)
    auditor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    audit_date = models.DateField()
    scope = models.TextField()
    findings = models.TextField()
    recommendations = models.TextField()
    compliance_score = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=50, choices=[
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('follow_up', 'Follow-up Required')
    ], default='scheduled')
    next_audit_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.audit_type} - {self.department} - {self.audit_date}"


class QualityMetric(models.Model):
    """Quality metrics tracking"""
    standard = models.ForeignKey(QualityStandard, on_delete=models.CASCADE)
    measurement_date = models.DateField()
    actual_value = models.DecimalField(max_digits=10, decimal_places=2)
    measured_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    variance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_compliant = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.standard.target_value:
            self.variance = self.actual_value - self.standard.target_value
            self.is_compliant = abs(self.variance) <= (self.standard.target_value * 0.1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.standard.name} - {self.measurement_date}"


class IncidentReport(models.Model):
    """Quality incident reports"""
    incident_type = models.CharField(max_length=100, choices=[
        ('patient_safety', 'Patient Safety'),
        ('medication_error', 'Medication Error'),
        ('equipment_failure', 'Equipment Failure'),
        ('infection_control', 'Infection Control'),
        ('documentation', 'Documentation Error'),
        ('staff_performance', 'Staff Performance')
    ])
    severity = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])
    department = models.CharField(max_length=100)
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    incident_date = models.DateTimeField()
    description = models.TextField()
    immediate_action = models.TextField()
    root_cause = models.TextField(blank=True)
    corrective_action = models.TextField(blank=True)
    preventive_action = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=[
        ('reported', 'Reported'),
        ('investigating', 'Under Investigation'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], default='reported')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_incidents')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.incident_type} - {self.incident_date}"


class QualityImprovement(models.Model):
    """Quality improvement initiatives"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    department = models.CharField(max_length=100)
    responsible_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    target_completion = models.DateField()
    actual_completion = models.DateField(null=True, blank=True)
    expected_outcome = models.TextField()
    actual_outcome = models.TextField(blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled')
    ], default='planned')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 