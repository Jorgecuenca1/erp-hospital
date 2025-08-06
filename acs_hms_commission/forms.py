from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.bootstrap import TabHolder, Tab
from .models import (
    CommissionStructure, CommissionAgent, CommissionRecord,
    CommissionPayment, CommissionReport, CommissionConfiguration
)


class CommissionStructureForm(forms.ModelForm):
    class Meta:
        model = CommissionStructure
        fields = '__all__'
        widgets = {
            'tier_structure': forms.Textarea(attrs={'rows': 6}),
            'custom_formula': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('service_type', css_class='form-group col-md-6'),
            ),
            Row(
                Column('calculation_type', css_class='form-group col-md-6'),
                Column('percentage_rate', css_class='form-group col-md-6'),
            ),
            Row(
                Column('flat_fee_amount', css_class='form-group col-md-6'),
                Column('minimum_service_amount', css_class='form-group col-md-6'),
            ),
            'tier_structure',
            'custom_formula',
            Row(
                Column('effective_date', css_class='form-group col-md-6'),
                Column('expiry_date', css_class='form-group col-md-6'),
            ),
            'is_active',
            Submit('submit', 'Save Commission Structure', css_class='btn btn-primary')
        )


class CommissionAgentForm(forms.ModelForm):
    class Meta:
        model = CommissionAgent
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('user', css_class='form-group col-md-6'),
                Column('agent_type', css_class='form-group col-md-6'),
            ),
            Row(
                Column('agent_code', css_class='form-group col-md-6'),
                Column('commission_threshold', css_class='form-group col-md-6'),
            ),
            Row(
                Column('phone', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
            ),
            'address',
            Row(
                Column('bank_name', css_class='form-group col-md-6'),
                Column('account_number', css_class='form-group col-md-6'),
            ),
            'routing_number',
            'default_commission_structure',
            'is_active',
            Submit('submit', 'Save Commission Agent', css_class='btn btn-primary')
        )


class CommissionRecordForm(forms.ModelForm):
    class Meta:
        model = CommissionRecord
        fields = '__all__'
        widgets = {
            'service_description': forms.Textarea(attrs={'rows': 3}),
            'service_date': forms.DateInput(attrs={'type': 'date'}),
            'approval_notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('agent', css_class='form-group col-md-6'),
                Column('structure', css_class='form-group col-md-6'),
            ),
            Row(
                Column('patient', css_class='form-group col-md-6'),
                Column('service_date', css_class='form-group col-md-6'),
            ),
            'service_description',
            Row(
                Column('service_amount', css_class='form-group col-md-6'),
                Column('commission_amount', css_class='form-group col-md-6'),
            ),
            'status',
            Submit('submit', 'Save Commission Record', css_class='btn btn-primary')
        )


class CommissionPaymentForm(forms.ModelForm):
    class Meta:
        model = CommissionPayment
        fields = '__all__'
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('agent', css_class='form-group col-md-6'),
                Column('total_amount', css_class='form-group col-md-6'),
            ),
            Row(
                Column('payment_method', css_class='form-group col-md-6'),
                Column('payment_date', css_class='form-group col-md-6'),
            ),
            'payment_reference',
            'commission_records',
            'notes',
            Submit('submit', 'Save Commission Payment', css_class='btn btn-primary')
        )


class CommissionReportForm(forms.ModelForm):
    class Meta:
        model = CommissionReport
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('report_type', css_class='form-group col-md-6'),
                Column('title', css_class='form-group col-md-6'),
            ),
            Row(
                Column('start_date', css_class='form-group col-md-6'),
                Column('end_date', css_class='form-group col-md-6'),
            ),
            'agent_filter',
            'structure_filter',
            Submit('submit', 'Generate Report', css_class='btn btn-primary')
        )


class CommissionConfigurationForm(forms.ModelForm):
    class Meta:
        model = CommissionConfiguration
        fields = '__all__'
        widgets = {
            'payment_frequency_days': forms.NumberInput(attrs={'min': 1, 'max': 365}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('auto_approve_under_amount', css_class='form-group col-md-6'),
                Column('minimum_payment_amount', css_class='form-group col-md-6'),
            ),
            Row(
                Column('payment_frequency_days', css_class='form-group col-md-6'),
                Column('default_commission_account', css_class='form-group col-md-6'),
            ),
            'notify_on_commission_earned',
            'notify_on_payment_processed',
            Submit('submit', 'Save Configuration', css_class='btn btn-primary')
        )


class CommissionSearchForm(forms.Form):
    agent = forms.ModelChoiceField(
        queryset=CommissionAgent.objects.all(), 
        required=False,
        empty_label="All Agents"
    )
    structure = forms.ModelChoiceField(
        queryset=CommissionStructure.objects.all(), 
        required=False,
        empty_label="All Structures"
    )
    date_from = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_to = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All')] + CommissionRecord.STATUS_CHOICES, 
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('agent', css_class='form-group col-md-6'),
                Column('structure', css_class='form-group col-md-6'),
            ),
            Row(
                Column('date_from', css_class='form-group col-md-4'),
                Column('date_to', css_class='form-group col-md-4'),
                Column('status', css_class='form-group col-md-4'),
            ),
            Submit('submit', 'Search', css_class='btn btn-primary')
        ) 