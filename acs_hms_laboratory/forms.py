from django import forms
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import (
    LabTestOrder, LabSample, LabResult, LabReport, 
    LabQualityControl, LabWorkshift, LabTest
)
from acs_hms_base.models import Patient, HMSUser


class LabTestOrderForm(forms.ModelForm):
    """Form for creating lab test orders"""
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.filter(active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tests = forms.ModelMultipleChoiceField(
        queryset=LabTest.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = LabTestOrder
        fields = ['patient', 'clinical_notes', 'diagnosis', 'priority', 'tests']
        widgets = {
            'clinical_notes': forms.Textarea(attrs={'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='form-group col-md-6'),
                Column('priority', css_class='form-group col-md-6'),
            ),
            Row(
                Column('clinical_notes', css_class='form-group col-md-6'),
                Column('diagnosis', css_class='form-group col-md-6'),
            ),
            'tests',
            Submit('submit', 'Create Order', css_class='btn btn-primary')
        )


class LabSampleForm(forms.ModelForm):
    """Form for collecting samples"""
    
    class Meta:
        model = LabSample
        fields = ['sample_type', 'volume', 'container_type', 'collection_notes']
        widgets = {
            'sample_type': forms.TextInput(attrs={'class': 'form-control'}),
            'volume': forms.TextInput(attrs={'class': 'form-control'}),
            'container_type': forms.TextInput(attrs={'class': 'form-control'}),
            'collection_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('sample_type', css_class='form-group col-md-6'),
                Column('volume', css_class='form-group col-md-6'),
            ),
            'container_type',
            'collection_notes',
            Submit('submit', 'Collect Sample', css_class='btn btn-success')
        )


class LabResultForm(forms.ModelForm):
    """Form for entering test results"""
    
    class Meta:
        model = LabResult
        fields = [
            'result_value', 'numeric_value', 'result_text',
            'reference_range', 'units', 'abnormal_flag', 'critical_flag',
            'equipment_used', 'technician_comments'
        ]
        widgets = {
            'result_value': forms.TextInput(attrs={'class': 'form-control'}),
            'numeric_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'result_text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'reference_range': forms.TextInput(attrs={'class': 'form-control'}),
            'units': forms.TextInput(attrs={'class': 'form-control'}),
            'abnormal_flag': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'critical_flag': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'equipment_used': forms.Select(attrs={'class': 'form-control'}),
            'technician_comments': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('result_value', css_class='form-group col-md-6'),
                Column('numeric_value', css_class='form-group col-md-6'),
            ),
            'result_text',
            Row(
                Column('reference_range', css_class='form-group col-md-6'),
                Column('units', css_class='form-group col-md-6'),
            ),
            Row(
                Column('abnormal_flag', css_class='form-group col-md-6'),
                Column('critical_flag', css_class='form-group col-md-6'),
            ),
            'equipment_used',
            'technician_comments',
            Submit('submit', 'Save Result', css_class='btn btn-primary')
        )


class LabReportForm(forms.ModelForm):
    """Form for generating lab reports"""
    
    class Meta:
        model = LabReport
        fields = ['report_summary', 'interpretation', 'recommendations', 'status']
        widgets = {
            'report_summary': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'interpretation': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'recommendations': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'report_summary',
            'interpretation',
            'recommendations',
            'status',
            Submit('submit', 'Generate Report', css_class='btn btn-primary')
        )


class LabQualityControlForm(forms.ModelForm):
    """Form for quality control records"""
    
    class Meta:
        model = LabQualityControl
        fields = [
            'qc_date', 'qc_type', 'equipment', 'control_lot',
            'expected_value', 'actual_value', 'passed', 'notes',
            'corrective_action_required', 'corrective_action_taken'
        ]
        widgets = {
            'qc_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'qc_type': forms.Select(attrs={'class': 'form-control'}),
            'equipment': forms.Select(attrs={'class': 'form-control'}),
            'control_lot': forms.TextInput(attrs={'class': 'form-control'}),
            'expected_value': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_value': forms.TextInput(attrs={'class': 'form-control'}),
            'passed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'corrective_action_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'corrective_action_taken': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('qc_date', css_class='form-group col-md-6'),
                Column('qc_type', css_class='form-group col-md-6'),
            ),
            'equipment',
            Row(
                Column('control_lot', css_class='form-group col-md-6'),
                Column('passed', css_class='form-group col-md-6'),
            ),
            Row(
                Column('expected_value', css_class='form-group col-md-6'),
                Column('actual_value', css_class='form-group col-md-6'),
            ),
            'notes',
            'corrective_action_required',
            'corrective_action_taken',
            Submit('submit', 'Save QC Record', css_class='btn btn-primary')
        )


class LabWorkshiftForm(forms.ModelForm):
    """Form for work shifts"""
    
    class Meta:
        model = LabWorkshift
        fields = [
            'shift_date', 'shift_type', 'start_time', 'end_time',
            'supervisor', 'technicians', 'samples_processed',
            'tests_completed', 'shift_notes'
        ]
        widgets = {
            'shift_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'shift_type': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'supervisor': forms.Select(attrs={'class': 'form-control'}),
            'technicians': forms.CheckboxSelectMultiple(),
            'samples_processed': forms.NumberInput(attrs={'class': 'form-control'}),
            'tests_completed': forms.NumberInput(attrs={'class': 'form-control'}),
            'shift_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supervisor'].queryset = HMSUser.objects.filter(
            user_type__in=['DOCTOR', 'LABORATORY_TECHNICIAN']
        )
        self.fields['technicians'].queryset = HMSUser.objects.filter(
            user_type='LABORATORY_TECHNICIAN'
        )
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('shift_date', css_class='form-group col-md-6'),
                Column('shift_type', css_class='form-group col-md-6'),
            ),
            Row(
                Column('start_time', css_class='form-group col-md-6'),
                Column('end_time', css_class='form-group col-md-6'),
            ),
            'supervisor',
            'technicians',
            Row(
                Column('samples_processed', css_class='form-group col-md-6'),
                Column('tests_completed', css_class='form-group col-md-6'),
            ),
            'shift_notes',
            Submit('submit', 'Save Shift', css_class='btn btn-primary')
        ) 