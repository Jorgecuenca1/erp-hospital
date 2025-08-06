from django import forms
from django.contrib.auth.models import User
from .models import ESGReport, EnvironmentalMetric, SocialMetric, GovernanceMetric, ESGGoal


class ESGReportForm(forms.ModelForm):
    """Form for creating and editing ESG reports"""
    
    class Meta:
        model = ESGReport
        fields = [
            'title', 'report_type', 'period', 'start_date', 'end_date',
            'executive_summary', 'environmental_score', 'social_score',
            'governance_score', 'overall_esg_score', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter report title'
            }),
            'report_type': forms.Select(attrs={'class': 'form-select'}),
            'period': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'executive_summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Enter executive summary...'
            }),
            'environmental_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01'
            }),
            'social_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01'
            }),
            'governance_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01'
            }),
            'overall_esg_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01'
            }),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data


class EnvironmentalMetricForm(forms.ModelForm):
    """Form for environmental metrics"""
    
    class Meta:
        model = EnvironmentalMetric
        fields = [
            'metric_type', 'value', 'unit', 'target_value',
            'beds_count', 'patient_days'
        ]
        widgets = {
            'metric_type': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., kWh, tons CO2, liters'
            }),
            'target_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'beds_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'patient_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            })
        }


class SocialMetricForm(forms.ModelForm):
    """Form for social metrics"""
    
    class Meta:
        model = SocialMetric
        fields = [
            'metric_type', 'value', 'unit', 'target_value'
        ]
        widgets = {
            'metric_type': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., %, score, hours'
            }),
            'target_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            })
        }


class GovernanceMetricForm(forms.ModelForm):
    """Form for governance metrics"""
    
    class Meta:
        model = GovernanceMetric
        fields = [
            'metric_type', 'value', 'unit', 'target_value', 'certification_status'
        ]
        widgets = {
            'metric_type': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., %, score, compliance rate'
            }),
            'target_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'certification_status': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., ISO 14001 Certified'
            })
        }


class ESGGoalForm(forms.ModelForm):
    """Form for ESG goals"""
    
    class Meta:
        model = ESGGoal
        fields = [
            'title', 'description', 'category', 'priority',
            'target_value', 'current_value', 'unit',
            'start_date', 'target_date', 'department'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter goal title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the goal in detail...'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'target_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'current_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., %, tons, hours'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'target_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Responsible department'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        target_date = cleaned_data.get('target_date')
        current_value = cleaned_data.get('current_value')
        target_value = cleaned_data.get('target_value')
        
        if start_date and target_date:
            if target_date <= start_date:
                raise forms.ValidationError("Target date must be after start date.")
        
        if current_value is not None and target_value is not None:
            if current_value < 0:
                raise forms.ValidationError("Current value cannot be negative.")
            if target_value <= 0:
                raise forms.ValidationError("Target value must be positive.")
        
        return cleaned_data


class ESGFilterForm(forms.Form):
    """Form for filtering ESG reports and metrics"""
    
    YEAR_CHOICES = [(year, year) for year in range(2020, 2030)]
    
    report_type = forms.ChoiceField(
        choices=[('', 'All Types')] + ESGReport.REPORT_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    period = forms.ChoiceField(
        choices=[('', 'All Periods')] + ESGReport.REPORT_PERIODS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    year = forms.ChoiceField(
        choices=[('', 'All Years')] + YEAR_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + ESGGoal.GOAL_CATEGORIES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    priority = forms.ChoiceField(
        choices=[('', 'All Priorities')] + ESGGoal.PRIORITY_LEVELS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    ) 