from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Div, Submit
from crispy_forms.bootstrap import TabHolder, Tab
from .models import (
    RadiologyTest, RadiologyImage, RadiologyReport, RadiologyTechnician,
    RadiologyEquipment, RadiologyModality, RadiologyTemplate, RadiologyRequest,
    RadiologyResult, RadiologyInterpretation, RadiologyWorkflow, RadiologyProtocol,
    RadiologyQualityControl, RadiologyDose, RadiologyContrast, RadiologyReferral,
    RadiologyAppointment, RadiologyBilling, RadiologyInstructions
)

class RadiologyTestForm(forms.ModelForm):
    class Meta:
        model = RadiologyTest
        fields = '__all__'
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'completed_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'instructions': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab('Basic Information',
                    Row(
                        Column('patient', css_class='form-group col-md-6'),
                        Column('test_type', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('referring_doctor', css_class='form-group col-md-6'),
                        Column('priority', css_class='form-group col-md-6'),
                    ),
                ),
                Tab('Test Details',
                    Row(
                        Column('body_part', css_class='form-group col-md-6'),
                        Column('modality', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('protocol', css_class='form-group col-md-6'),
                        Column('contrast_used', css_class='form-group col-md-6'),
                    ),
                    'instructions',
                ),
                Tab('Scheduling',
                    Row(
                        Column('scheduled_date', css_class='form-group col-md-6'),
                        Column('technician', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('equipment', css_class='form-group col-md-6'),
                        Column('status', css_class='form-group col-md-6'),
                    ),
                ),
                Tab('Results',
                    Row(
                        Column('completed_date', css_class='form-group col-md-6'),
                        Column('results_available', css_class='form-group col-md-6'),
                    ),
                    'notes',
                ),
            ),
            Submit('submit', 'Save Radiology Test', css_class='btn btn-primary')
        )

class RadiologyImageForm(forms.ModelForm):
    class Meta:
        model = RadiologyImage
        fields = '__all__'
        widgets = {
            'acquisition_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'annotations': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('test', css_class='form-group col-md-6'),
                Column('image_type', css_class='form-group col-md-6'),
            ),
            Row(
                Column('series_number', css_class='form-group col-md-6'),
                Column('instance_number', css_class='form-group col-md-6'),
            ),
            Row(
                Column('acquisition_date', css_class='form-group col-md-6'),
                Column('is_processed', css_class='form-group col-md-6'),
            ),
            'dicom_file',
            'description',
            'annotations',
            Submit('submit', 'Save Image', css_class='btn btn-primary')
        )

class RadiologyReportForm(forms.ModelForm):
    class Meta:
        model = RadiologyReport
        fields = '__all__'
        widgets = {
            'dictated_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'finalized_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'clinical_history': forms.Textarea(attrs={'rows': 4}),
            'technique': forms.Textarea(attrs={'rows': 4}),
            'comparison': forms.Textarea(attrs={'rows': 4}),
            'findings': forms.Textarea(attrs={'rows': 8}),
            'impression': forms.Textarea(attrs={'rows': 6}),
            'recommendations': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab('Report Information',
                    Row(
                        Column('test', css_class='form-group col-md-6'),
                        Column('radiologist', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('report_status', css_class='form-group col-md-6'),
                        Column('dictated_date', css_class='form-group col-md-6'),
                    ),
                ),
                Tab('Clinical Information',
                    'clinical_history',
                    'technique',
                    'comparison',
                ),
                Tab('Findings & Impression',
                    'findings',
                    'impression',
                    'recommendations',
                ),
                Tab('Quality & Review',
                    Row(
                        Column('quality_score', css_class='form-group col-md-6'),
                        Column('peer_reviewed', css_class='form-group col-md-6'),
                    ),
                    'reviewed_by',
                    'finalized_date',
                ),
            ),
            Submit('submit', 'Save Report', css_class='btn btn-primary')
        )

class RadiologyTechnicianForm(forms.ModelForm):
    class Meta:
        model = RadiologyTechnician
        fields = '__all__'
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'certification_date': forms.DateInput(attrs={'type': 'date'}),
            'skills': forms.Textarea(attrs={'rows': 4}),
            'equipment_authorized': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab('Basic Information',
                    Row(
                        Column('user', css_class='form-group col-md-6'),
                        Column('employee_id', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('specialization', css_class='form-group col-md-6'),
                        Column('hire_date', css_class='form-group col-md-6'),
                    ),
                ),
                Tab('Certification',
                    Row(
                        Column('license_number', css_class='form-group col-md-6'),
                        Column('certification_date', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('certification_body', css_class='form-group col-md-6'),
                        Column('is_active', css_class='form-group col-md-6'),
                    ),
                ),
                Tab('Skills & Equipment',
                    'skills',
                    'equipment_authorized',
                    'modalities_certified',
                ),
                Tab('Contact Information',
                    Row(
                        Column('phone', css_class='form-group col-md-6'),
                        Column('email', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('department', css_class='form-group col-md-6'),
                        Column('supervisor', css_class='form-group col-md-6'),
                    ),
                    'emergency_contact',
                ),
            ),
            Submit('submit', 'Save Technician', css_class='btn btn-primary')
        )

class RadiologyEquipmentForm(forms.ModelForm):
    class Meta:
        model = RadiologyEquipment
        fields = '__all__'
        widgets = {
            'installation_date': forms.DateInput(attrs={'type': 'date'}),
            'last_maintenance': forms.DateInput(attrs={'type': 'date'}),
            'next_maintenance': forms.DateInput(attrs={'type': 'date'}),
            'calibration_date': forms.DateInput(attrs={'type': 'date'}),
            'last_qc_date': forms.DateInput(attrs={'type': 'date'}),
            'specifications': forms.Textarea(attrs={'rows': 6}),
            'qc_results': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab('Basic Information',
                    Row(
                        Column('name', css_class='form-group col-md-6'),
                        Column('equipment_type', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('manufacturer', css_class='form-group col-md-6'),
                        Column('model', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('serial_number', css_class='form-group col-md-6'),
                        Column('installation_date', css_class='form-group col-md-6'),
                    ),
                ),
                Tab('Technical Specifications',
                    'specifications',
                    'location',
                    Row(
                        Column('status', css_class='form-group col-md-6'),
                        Column('usage_hours', css_class='form-group col-md-6'),
                    ),
                ),
                Tab('Maintenance',
                    Row(
                        Column('last_maintenance', css_class='form-group col-md-6'),
                        Column('next_maintenance', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('maintenance_contract', css_class='form-group col-md-6'),
                        Column('calibration_date', css_class='form-group col-md-6'),
                    ),
                ),
                Tab('Quality Control',
                    Row(
                        Column('qc_frequency', css_class='form-group col-md-6'),
                        Column('last_qc_date', css_class='form-group col-md-6'),
                    ),
                    'qc_results',
                ),
            ),
            Submit('submit', 'Save Equipment', css_class='btn btn-primary')
        )

class RadiologyRequestForm(forms.ModelForm):
    class Meta:
        model = RadiologyRequest
        fields = '__all__'
        widgets = {
            'request_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'clinical_information': forms.Textarea(attrs={'rows': 4}),
            'clinical_question': forms.Textarea(attrs={'rows': 4}),
            'special_instructions': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='form-group col-md-6'),
                Column('requesting_doctor', css_class='form-group col-md-6'),
            ),
            Row(
                Column('urgency', css_class='form-group col-md-6'),
                Column('request_date', css_class='form-group col-md-6'),
            ),
            Row(
                Column('exam_requested', css_class='form-group col-md-6'),
                Column('status', css_class='form-group col-md-6'),
            ),
            'clinical_information',
            'clinical_question',
            'special_instructions',
            Submit('submit', 'Save Request', css_class='btn btn-primary')
        )

class RadiologyAppointmentForm(forms.ModelForm):
    class Meta:
        model = RadiologyAppointment
        fields = '__all__'
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'preparation_instructions': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='form-group col-md-6'),
                Column('test_type', css_class='form-group col-md-6'),
            ),
            Row(
                Column('appointment_date', css_class='form-group col-md-6'),
                Column('duration', css_class='form-group col-md-6'),
            ),
            Row(
                Column('technician', css_class='form-group col-md-6'),
                Column('status', css_class='form-group col-md-6'),
            ),
            'preparation_instructions',
            'notes',
            Submit('submit', 'Save Appointment', css_class='btn btn-primary')
        )

class RadiologySearchForm(forms.Form):
    patient_name = forms.CharField(max_length=100, required=False)
    test_type = forms.CharField(max_length=100, required=False)
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(choices=[('', 'All')] + RadiologyTest.STATUS_CHOICES, required=False)
    technician = forms.ModelChoiceField(queryset=RadiologyTechnician.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            Row(
                Column('patient_name', css_class='form-group col-md-3'),
                Column('test_type', css_class='form-group col-md-3'),
                Column('date_from', css_class='form-group col-md-2'),
                Column('date_to', css_class='form-group col-md-2'),
                Column('status', css_class='form-group col-md-2'),
            ),
            Submit('submit', 'Search', css_class='btn btn-primary')
        )

class RadiologyQualityControlForm(forms.ModelForm):
    class Meta:
        model = RadiologyQualityControl
        fields = '__all__'
        widgets = {
            'test_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'test_parameters': forms.Textarea(attrs={'rows': 6}),
            'results': forms.Textarea(attrs={'rows': 6}),
            'corrective_actions': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('equipment', css_class='form-group col-md-6'),
                Column('test_type', css_class='form-group col-md-6'),
            ),
            Row(
                Column('test_date', css_class='form-group col-md-6'),
                Column('technician', css_class='form-group col-md-6'),
            ),
            Row(
                Column('result_status', css_class='form-group col-md-6'),
                Column('reviewed_by', css_class='form-group col-md-6'),
            ),
            'test_parameters',
            'results',
            'corrective_actions',
            Submit('submit', 'Save QC Test', css_class='btn btn-primary')
        )

class RadiologyDoseForm(forms.ModelForm):
    class Meta:
        model = RadiologyDose
        fields = '__all__'
        widgets = {
            'recorded_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'comments': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('test', css_class='form-group col-md-6'),
                Column('dose_type', css_class='form-group col-md-6'),
            ),
            Row(
                Column('dose_value', css_class='form-group col-md-6'),
                Column('unit', css_class='form-group col-md-6'),
            ),
            Row(
                Column('recorded_date', css_class='form-group col-md-6'),
                Column('is_within_limit', css_class='form-group col-md-6'),
            ),
            'comments',
            Submit('submit', 'Save Dose Record', css_class='btn btn-primary')
        )

class RadiologyBillingForm(forms.ModelForm):
    class Meta:
        model = RadiologyBilling
        fields = '__all__'
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('test', css_class='form-group col-md-6'),
                Column('billing_code', css_class='form-group col-md-6'),
            ),
            Row(
                Column('amount', css_class='form-group col-md-6'),
                Column('billing_date', css_class='form-group col-md-6'),
            ),
            Row(
                Column('payment_status', css_class='form-group col-md-6'),
                Column('payment_date', css_class='form-group col-md-6'),
            ),
            'notes',
            Submit('submit', 'Save Billing Record', css_class='btn btn-primary')
        ) 