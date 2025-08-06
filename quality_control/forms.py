from django import forms
from .models import QualityStandard, QualityAudit, QualityMetric, IncidentReport, QualityImprovement


class QualityStandardForm(forms.ModelForm):
    """Form for quality standard creation and editing"""
    class Meta:
        model = QualityStandard
        fields = ['name', 'category', 'description', 'target_value', 'unit', 'frequency', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Standard Name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'target_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit of measurement'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class QualityAuditForm(forms.ModelForm):
    """Form for quality audit creation and editing"""
    class Meta:
        model = QualityAudit
        fields = ['audit_type', 'department', 'auditor', 'audit_date', 'scope',
                 'findings', 'recommendations', 'compliance_score', 'status', 'next_audit_date']
        widgets = {
            'audit_type': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'auditor': forms.Select(attrs={'class': 'form-control'}),
            'audit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'scope': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'findings': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'compliance_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'max': '100', 'min': '0'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'next_audit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }


class QualityMetricForm(forms.ModelForm):
    """Form for quality metric creation and editing"""
    class Meta:
        model = QualityMetric
        fields = ['standard', 'measurement_date', 'actual_value', 'measured_by', 'notes']
        widgets = {
            'standard': forms.Select(attrs={'class': 'form-control'}),
            'measurement_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actual_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'measured_by': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


class IncidentReportForm(forms.ModelForm):
    """Form for incident report creation and editing"""
    class Meta:
        model = IncidentReport
        fields = ['incident_type', 'severity', 'department', 'reporter', 'incident_date',
                 'description', 'immediate_action', 'root_cause', 'corrective_action',
                 'preventive_action', 'assigned_to']
        widgets = {
            'incident_type': forms.Select(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'reporter': forms.Select(attrs={'class': 'form-control'}),
            'incident_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'immediate_action': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'root_cause': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'corrective_action': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preventive_action': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'})
        }


class QualityImprovementForm(forms.ModelForm):
    """Form for quality improvement initiative creation and editing"""
    class Meta:
        model = QualityImprovement
        fields = ['title', 'description', 'department', 'responsible_person',
                 'start_date', 'target_completion', 'expected_outcome', 'budget', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Initiative Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'responsible_person': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'target_completion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expected_outcome': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        } 