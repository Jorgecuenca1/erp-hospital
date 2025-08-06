from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div
from crispy_forms.bootstrap import FormActions
from .models import (
    PatientPortalUser, PatientAppointment, PatientDocument, 
    PatientMessage, PatientBilling, PatientFeedback
)
from acs_hms_base.models import Patient, HMSUser


class PatientPortalUserRegistrationForm(UserCreationForm):
    """Patient portal user registration form"""
    email = forms.EmailField(required=True)
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        empty_label="Select Patient",
        required=True
    )
    
    # Preferences
    preferred_language = forms.ChoiceField(
        choices=[('en', 'English'), ('es', 'Spanish')],
        initial='en'
    )
    email_notifications = forms.BooleanField(
        required=False,
        initial=True,
        label="Receive email notifications"
    )
    sms_notifications = forms.BooleanField(
        required=False,
        initial=True,
        label="Receive SMS notifications"
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'patient',
            Row(
                Column('preferred_language', css_class='form-group col-md-6 mb-0'),
                Column(
                    Div(
                        Field('email_notifications'),
                        Field('sms_notifications'),
                        css_class='form-check-container'
                    ),
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Register', css_class='btn btn-primary'),
                css_class='text-center'
            )
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create patient portal user
            PatientPortalUser.objects.create(
                user=user,
                patient=self.cleaned_data['patient'],
                preferred_language=self.cleaned_data['preferred_language'],
                email_notifications=self.cleaned_data['email_notifications'],
                sms_notifications=self.cleaned_data['sms_notifications']
            )
        return user


class PatientAppointmentForm(forms.ModelForm):
    """Patient appointment booking form"""
    
    class Meta:
        model = PatientAppointment
        fields = [
            'doctor', 'appointment_date', 'appointment_time', 
            'duration_minutes', 'reason', 'special_instructions',
            'is_telehealth'
        ]
        widgets = {
            'appointment_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'appointment_time': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'reason': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
            'special_instructions': forms.Textarea(
                attrs={'rows': 2, 'class': 'form-control'}
            ),
        }
    
    def __init__(self, *args, **kwargs):
        self.patient_user = kwargs.pop('patient_user', None)
        super().__init__(*args, **kwargs)
        
        # Filter doctors to only show active ones
        self.fields['doctor'].queryset = HMSUser.objects.filter(
            user_type='DOCTOR', 
            active=True
        )
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('doctor', css_class='form-group col-md-6 mb-0'),
                Column('duration_minutes', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('appointment_date', css_class='form-group col-md-6 mb-0'),
                Column('appointment_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'reason',
            'special_instructions',
            Field('is_telehealth', template="crispy_forms/bootstrap4/layout/checkboxselectmultiple.html"),
            FormActions(
                Submit('submit', 'Book Appointment', css_class='btn btn-primary'),
                css_class='text-center'
            )
        )
    
    def clean_appointment_date(self):
        date = self.cleaned_data['appointment_date']
        if date < timezone.now().date():
            raise ValidationError("Appointment date cannot be in the past")
        return date
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('appointment_date')
        time = cleaned_data.get('appointment_time')
        doctor = cleaned_data.get('doctor')
        
        if date and time and doctor:
            # Check for conflicting appointments
            existing_appointments = PatientAppointment.objects.filter(
                doctor=doctor,
                appointment_date=date,
                appointment_time=time,
                status__in=['scheduled', 'confirmed']
            )
            
            if self.instance.pk:
                existing_appointments = existing_appointments.exclude(pk=self.instance.pk)
            
            if existing_appointments.exists():
                raise ValidationError("This time slot is already booked")
        
        return cleaned_data


class PatientDocumentForm(forms.ModelForm):
    """Patient document upload form"""
    
    class Meta:
        model = PatientDocument
        fields = ['title', 'document_type', 'description', 'file']
        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'document_type',
            'description',
            'file',
            FormActions(
                Submit('submit', 'Upload Document', css_class='btn btn-primary'),
                css_class='text-center'
            )
        )
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise ValidationError("File size cannot exceed 10MB")
            
            # Check file type
            allowed_types = [
                'application/pdf',
                'image/jpeg',
                'image/png',
                'image/gif',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ]
            
            if file.content_type not in allowed_types:
                raise ValidationError("File type not allowed")
        
        return file


class PatientMessageForm(forms.ModelForm):
    """Patient message form"""
    
    class Meta:
        model = PatientMessage
        fields = ['doctor', 'subject', 'message_type', 'message']
        widgets = {
            'message': forms.Textarea(
                attrs={'rows': 5, 'class': 'form-control'}
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter doctors to only show active ones
        self.fields['doctor'].queryset = HMSUser.objects.filter(
            user_type='DOCTOR', 
            active=True
        )
        self.fields['doctor'].required = False
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('doctor', css_class='form-group col-md-6 mb-0'),
                Column('message_type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'subject',
            'message',
            FormActions(
                Submit('submit', 'Send Message', css_class='btn btn-primary'),
                css_class='text-center'
            )
        )


class PatientFeedbackForm(forms.ModelForm):
    """Patient feedback form"""
    
    class Meta:
        model = PatientFeedback
        fields = ['doctor', 'rating', 'title', 'feedback']
        widgets = {
            'feedback': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control'}
            ),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter doctors to only show active ones
        self.fields['doctor'].queryset = HMSUser.objects.filter(
            user_type='DOCTOR', 
            active=True
        )
        self.fields['doctor'].required = False
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('doctor', css_class='form-group col-md-6 mb-0'),
                Column('rating', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'title',
            'feedback',
            FormActions(
                Submit('submit', 'Submit Feedback', css_class='btn btn-primary'),
                css_class='text-center'
            )
        )


class PatientProfileForm(forms.ModelForm):
    """Patient profile update form"""
    
    class Meta:
        model = PatientPortalUser
        fields = [
            'preferred_language', 'preferred_timezone',
            'email_notifications', 'sms_notifications'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('preferred_language', css_class='form-group col-md-6 mb-0'),
                Column('preferred_timezone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    Field('email_notifications'),
                    css_class='form-group col-md-6 mb-0'
                ),
                Column(
                    Field('sms_notifications'),
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Update Profile', css_class='btn btn-primary'),
                css_class='text-center'
            )
        )


class AppointmentReschedulingForm(forms.Form):
    """Appointment rescheduling form"""
    new_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    new_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        required=False,
        label="Reason for rescheduling"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('new_date', css_class='form-group col-md-6 mb-0'),
                Column('new_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'reason',
            FormActions(
                Submit('submit', 'Reschedule Appointment', css_class='btn btn-primary'),
                css_class='text-center'
            )
        )
    
    def clean_new_date(self):
        date = self.cleaned_data['new_date']
        if date < timezone.now().date():
            raise ValidationError("New appointment date cannot be in the past")
        return date 