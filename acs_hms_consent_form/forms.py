from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from crispy_forms.bootstrap import FormActions
from .models import (
    ConsentFormTemplate, ConsentForm, ConsentFormNotification
)
from acs_hms_base.models import Patient, HMSUser


class ConsentFormTemplateForm(forms.ModelForm):
    """Form for creating/editing consent form templates"""
    
    class Meta:
        model = ConsentFormTemplate
        fields = [
            'title', 'form_type', 'language', 'description', 
            'content', 'form_fields', 'is_active', 
            'requires_witness', 'requires_guardian', 'expires_after_days'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 10}),
            'form_fields': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-8 mb-0'),
                Column('form_type', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('language', css_class='form-group col-md-6 mb-0'),
                Column('expires_after_days', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'description',
            'content',
            'form_fields',
            Row(
                Column(
                    Div(
                        Field('is_active'),
                        Field('requires_witness'),
                        Field('requires_guardian'),
                        css_class='form-check-container'
                    ),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Save Template', css_class='btn btn-primary'),
                css_class='text-center'
            )
        )


class ConsentFormCreateForm(forms.ModelForm):
    """Form for creating new consent forms"""
    
    class Meta:
        model = ConsentForm
        fields = [
            'template', 'patient', 'guardian', 'doctor', 
            'procedure_name', 'procedure_date'
        ]
        widgets = {
            'procedure_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter active templates
        self.fields['template'].queryset = ConsentFormTemplate.objects.filter(is_active=True)
        
        # Filter active doctors
        self.fields['doctor'].queryset = HMSUser.objects.filter(
            user_type='DOCTOR', 
            active=True
        )
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'template',
            Row(
                Column('patient', css_class='form-group col-md-6 mb-0'),
                Column('guardian', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'doctor',
            Row(
                Column('procedure_name', css_class='form-group col-md-8 mb-0'),
                Column('procedure_date', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Create Consent Form', css_class='btn btn-primary'),
                css_class='text-center'
            )
        )
    
    def clean_procedure_date(self):
        date = self.cleaned_data.get('procedure_date')
        if date and date < timezone.now().date():
            raise ValidationError("Procedure date cannot be in the past")
        return date


class ConsentFormSignatureForm(forms.Form):
    """Form for capturing digital signatures"""
    signature_data = forms.CharField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        self.consent_form = kwargs.pop('consent_form', None)
        self.signature_type = kwargs.pop('signature_type', 'patient')
        super().__init__(*args, **kwargs)
        
        # Add witness fields if required
        if self.signature_type == 'witness':
            self.fields['witness_name'] = forms.CharField(
                max_length=200,
                required=True,
                widget=forms.TextInput(attrs={'class': 'form-control'})
            )
            self.fields['witness_relationship'] = forms.CharField(
                max_length=100,
                required=True,
                widget=forms.TextInput(attrs={'class': 'form-control'})
            )
        
        self.helper = FormHelper()
        
        if self.signature_type == 'witness':
            self.helper.layout = Layout(
                'witness_name',
                'witness_relationship',
                HTML('<div id="signature-pad-container"></div>'),
                'signature_data',
                FormActions(
                    Submit('submit', 'Sign as Witness', css_class='btn btn-primary'),
                    css_class='text-center'
                )
            )
        else:
            self.helper.layout = Layout(
                HTML('<div id="signature-pad-container"></div>'),
                'signature_data',
                FormActions(
                    Submit('submit', f'Sign as {self.signature_type.title()}', css_class='btn btn-primary'),
                    css_class='text-center'
                )
            )
    
    def clean_signature_data(self):
        signature_data = self.cleaned_data.get('signature_data')
        if not signature_data:
            raise ValidationError("Signature is required")
        return signature_data


class ConsentFormRevokeForm(forms.Form):
    """Form for revoking consent forms"""
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        required=True,
        label="Reason for revocation"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'reason',
            FormActions(
                Submit('submit', 'Revoke Consent', css_class='btn btn-danger'),
                css_class='text-center'
            )
        )


class ConsentFormNotificationForm(forms.ModelForm):
    """Form for sending notifications"""
    
    class Meta:
        model = ConsentFormNotification
        fields = [
            'notification_type', 'recipient_email', 'recipient_name',
            'subject', 'message'
        ]
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'notification_type',
            Row(
                Column('recipient_email', css_class='form-group col-md-6 mb-0'),
                Column('recipient_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'subject',
            'message',
            FormActions(
                Submit('submit', 'Send Notification', css_class='btn btn-primary'),
                css_class='text-center'
            )
        )


class ConsentFormSearchForm(forms.Form):
    """Form for searching consent forms"""
    SEARCH_TYPE_CHOICES = [
        ('', 'All Fields'),
        ('consent_id', 'Consent ID'),
        ('patient_name', 'Patient Name'),
        ('doctor_name', 'Doctor Name'),
        ('procedure_name', 'Procedure Name'),
    ]
    
    STATUS_CHOICES = [
        ('', 'All Statuses'),
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('signed', 'Signed'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]
    
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search...'})
    )
    search_type = forms.ChoiceField(
        choices=SEARCH_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('search_query', css_class='form-group col-md-4 mb-0'),
                Column('search_type', css_class='form-group col-md-2 mb-0'),
                Column('status', css_class='form-group col-md-2 mb-0'),
                Column('date_from', css_class='form-group col-md-2 mb-0'),
                Column('date_to', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Search', css_class='btn btn-primary'),
                css_class='text-center'
            )
        )


class ConsentFormBulkActionForm(forms.Form):
    """Form for bulk actions on consent forms"""
    ACTION_CHOICES = [
        ('', 'Select Action'),
        ('send_reminders', 'Send Reminders'),
        ('mark_expired', 'Mark as Expired'),
        ('export_pdf', 'Export to PDF'),
        ('send_notifications', 'Send Notifications'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    selected_items = forms.CharField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'action',
            'selected_items',
            FormActions(
                Submit('submit', 'Execute Action', css_class='btn btn-primary'),
                css_class='text-center'
            )
        )


class ConsentFormTemplateImportForm(forms.Form):
    """Form for importing consent form templates"""
    template_file = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'template_file',
            FormActions(
                Submit('submit', 'Import Template', css_class='btn btn-primary'),
                css_class='text-center'
            )
        )
    
    def clean_template_file(self):
        file = self.cleaned_data.get('template_file')
        if file:
            if not file.name.endswith('.json'):
                raise ValidationError("Only JSON files are allowed")
            
            if file.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("File size cannot exceed 5MB")
        
        return file


class ConsentFormConfigurationForm(forms.Form):
    """Form for configuring consent form settings"""
    signature_required = forms.BooleanField(required=False)
    allow_electronic_signature = forms.BooleanField(required=False)
    require_timestamp = forms.BooleanField(required=False)
    
    auto_send_notifications = forms.BooleanField(required=False)
    reminder_days_before_expiry = forms.IntegerField(
        min_value=1,
        max_value=365,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    require_ip_logging = forms.BooleanField(required=False)
    require_user_agent_logging = forms.BooleanField(required=False)
    
    auto_generate_pdf = forms.BooleanField(required=False)
    include_signatures_in_pdf = forms.BooleanField(required=False)
    
    track_consent_costs = forms.BooleanField(required=False)
    consent_processing_fee = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h5>Digital Signature Settings</h5>'),
            Row(
                Column(
                    Field('signature_required'),
                    Field('allow_electronic_signature'),
                    Field('require_timestamp'),
                    css_class='form-group col-md-6 mb-0'
                ),
                Column(
                    'reminder_days_before_expiry',
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            HTML('<h5>Email Settings</h5>'),
            Field('auto_send_notifications'),
            HTML('<h5>Security Settings</h5>'),
            Row(
                Column(
                    Field('require_ip_logging'),
                    Field('require_user_agent_logging'),
                    css_class='form-group col-md-6 mb-0'
                ),
                Column(
                    Field('auto_generate_pdf'),
                    Field('include_signatures_in_pdf'),
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            HTML('<h5>Accounting Integration</h5>'),
            Row(
                Column(
                    Field('track_consent_costs'),
                    css_class='form-group col-md-6 mb-0'
                ),
                Column(
                    'consent_processing_fee',
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Save Configuration', css_class='btn btn-primary'),
                css_class='text-center'
            )
        ) 