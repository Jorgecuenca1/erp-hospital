from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML, Submit, Row, Column
from .models import (
    Hospital, Department, Room, HMSUser, Patient, 
    Appointment, MedicalRecord, HospitalConfiguration
)


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'
        widgets = {
            'established_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-8 mb-0'),
                Column('code', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('license_number', css_class='form-group col-md-6 mb-0'),
                Column('registration_number', css_class='form-group col-md-6 mb-0'),
            ),
            'address',
            Row(
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('country', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('zip_code', css_class='form-group col-md-4 mb-0'),
                Column('phone', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('website', css_class='form-group col-md-6 mb-0'),
                Column('established_date', css_class='form-group col-md-6 mb-0'),
            ),
            'active',
            Submit('submit', 'Save Hospital')
        )


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-8 mb-0'),
                Column('code', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('hospital', css_class='form-group col-md-6 mb-0'),
                Column('head_of_department', css_class='form-group col-md-6 mb-0'),
            ),
            'description',
            Row(
                Column('location', css_class='form-group col-md-4 mb-0'),
                Column('phone', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
            ),
            'active',
            Submit('submit', 'Save Department')
        )


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        widgets = {
            'amenities': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('number', css_class='form-group col-md-4 mb-0'),
                Column('name', css_class='form-group col-md-8 mb-0'),
            ),
            Row(
                Column('room_type', css_class='form-group col-md-4 mb-0'),
                Column('department', css_class='form-group col-md-4 mb-0'),
                Column('floor', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('capacity', css_class='form-group col-md-4 mb-0'),
                Column('status', css_class='form-group col-md-4 mb-0'),
                Column('active', css_class='form-group col-md-4 mb-0'),
            ),
            'amenities',
            'notes',
            Submit('submit', 'Save Room')
        )


class HMSUserForm(forms.ModelForm):
    class Meta:
        model = HMSUser
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h4>Basic Information</h4>'),
            Row(
                Column('user', css_class='form-group col-md-6 mb-0'),
                Column('employee_id', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('user_type', css_class='form-group col-md-6 mb-0'),
                Column('hospital', css_class='form-group col-md-6 mb-0'),
            ),
            'department',
            HTML('<h4>Personal Information</h4>'),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-0'),
                Column('mobile', css_class='form-group col-md-6 mb-0'),
            ),
            'address',
            Row(
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('country', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('zip_code', css_class='form-group col-md-4 mb-0'),
                Column('date_of_birth', css_class='form-group col-md-4 mb-0'),
                Column('gender', css_class='form-group col-md-4 mb-0'),
            ),
            HTML('<h4>Professional Information</h4>'),
            Row(
                Column('license_number', css_class='form-group col-md-6 mb-0'),
                Column('qualification', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('experience_years', css_class='form-group col-md-6 mb-0'),
                Column('specialization', css_class='form-group col-md-6 mb-0'),
            ),
            HTML('<h4>Employment Information</h4>'),
            Row(
                Column('joining_date', css_class='form-group col-md-4 mb-0'),
                Column('salary', css_class='form-group col-md-4 mb-0'),
                Column('shift', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('photo', css_class='form-group col-md-6 mb-0'),
                Column('signature', css_class='form-group col-md-6 mb-0'),
            ),
            'active',
            Submit('submit', 'Save User')
        )


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
            'current_medications': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h4>Basic Information</h4>'),
            Row(
                Column('patient_id', css_class='form-group col-md-6 mb-0'),
                Column('medical_record_number', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('first_name', css_class='form-group col-md-4 mb-0'),
                Column('middle_name', css_class='form-group col-md-4 mb-0'),
                Column('last_name', css_class='form-group col-md-4 mb-0'),
            ),
            HTML('<h4>Demographics</h4>'),
            Row(
                Column('date_of_birth', css_class='form-group col-md-4 mb-0'),
                Column('gender', css_class='form-group col-md-4 mb-0'),
                Column('blood_group', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('marital_status', css_class='form-group col-md-6 mb-0'),
                Column('patient_type', css_class='form-group col-md-6 mb-0'),
            ),
            HTML('<h4>Contact Information</h4>'),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-0'),
                Column('mobile', css_class='form-group col-md-6 mb-0'),
            ),
            'email',
            'address',
            Row(
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('country', css_class='form-group col-md-4 mb-0'),
            ),
            'zip_code',
            HTML('<h4>Medical Information</h4>'),
            'primary_doctor',
            'allergies',
            'medical_history',
            'current_medications',
            HTML('<h4>Insurance Information</h4>'),
            Row(
                Column('insurance_number', css_class='form-group col-md-6 mb-0'),
                Column('insurance_provider', css_class='form-group col-md-6 mb-0'),
            ),
            HTML('<h4>Emergency Contact</h4>'),
            Row(
                Column('emergency_contact_name', css_class='form-group col-md-6 mb-0'),
                Column('emergency_contact_phone', css_class='form-group col-md-6 mb-0'),
            ),
            'emergency_contact_relationship',
            Row(
                Column('photo', css_class='form-group col-md-6 mb-0'),
                Column('registered_by', css_class='form-group col-md-6 mb-0'),
            ),
            'active',
            Submit('submit', 'Save Patient')
        )


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'chief_complaint': forms.Textarea(attrs={'rows': 3}),
            'symptoms': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'follow_up_notes': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h4>Basic Information</h4>'),
            Row(
                Column('appointment_id', css_class='form-group col-md-6 mb-0'),
                Column('patient', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('doctor', css_class='form-group col-md-6 mb-0'),
                Column('department', css_class='form-group col-md-6 mb-0'),
            ),
            'room',
            HTML('<h4>Scheduling</h4>'),
            Row(
                Column('appointment_date', css_class='form-group col-md-4 mb-0'),
                Column('appointment_time', css_class='form-group col-md-4 mb-0'),
                Column('estimated_duration', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('appointment_type', css_class='form-group col-md-6 mb-0'),
                Column('priority', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('status', css_class='form-group col-md-6 mb-0'),
                Column('booked_by', css_class='form-group col-md-6 mb-0'),
            ),
            HTML('<h4>Details</h4>'),
            'chief_complaint',
            'symptoms',
            'notes',
            HTML('<h4>Follow-up</h4>'),
            Row(
                Column('follow_up_required', css_class='form-group col-md-6 mb-0'),
                Column('follow_up_date', css_class='form-group col-md-6 mb-0'),
            ),
            'follow_up_notes',
            HTML('<h4>Financial</h4>'),
            Row(
                Column('consultation_fee', css_class='form-group col-md-6 mb-0'),
                Column('insurance_covered', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Save Appointment')
        )


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        widgets = {
            'chief_complaint': forms.Textarea(attrs={'rows': 3}),
            'history_of_present_illness': forms.Textarea(attrs={'rows': 4}),
            'physical_examination': forms.Textarea(attrs={'rows': 4}),
            'provisional_diagnosis': forms.Textarea(attrs={'rows': 3}),
            'final_diagnosis': forms.Textarea(attrs={'rows': 3}),
            'treatment_plan': forms.Textarea(attrs={'rows': 4}),
            'prescriptions': forms.Textarea(attrs={'rows': 4}),
            'lab_tests_ordered': forms.Textarea(attrs={'rows': 3}),
            'radiology_tests_ordered': forms.Textarea(attrs={'rows': 3}),
            'referrals': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h4>Basic Information</h4>'),
            Row(
                Column('patient', css_class='form-group col-md-6 mb-0'),
                Column('appointment', css_class='form-group col-md-6 mb-0'),
            ),
            'doctor',
            HTML('<h4>Examination</h4>'),
            'chief_complaint',
            'history_of_present_illness',
            'physical_examination',
            HTML('<h4>Vital Signs</h4>'),
            Row(
                Column('temperature', css_class='form-group col-md-4 mb-0'),
                Column('pulse_rate', css_class='form-group col-md-4 mb-0'),
                Column('respiratory_rate', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('blood_pressure_systolic', css_class='form-group col-md-6 mb-0'),
                Column('blood_pressure_diastolic', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('oxygen_saturation', css_class='form-group col-md-4 mb-0'),
                Column('weight', css_class='form-group col-md-4 mb-0'),
                Column('height', css_class='form-group col-md-4 mb-0'),
            ),
            HTML('<h4>Diagnosis & Treatment</h4>'),
            'provisional_diagnosis',
            'final_diagnosis',
            'treatment_plan',
            'prescriptions',
            HTML('<h4>Additional Information</h4>'),
            'lab_tests_ordered',
            'radiology_tests_ordered',
            'referrals',
            Submit('submit', 'Save Medical Record')
        )


class HospitalConfigurationForm(forms.ModelForm):
    class Meta:
        model = HospitalConfiguration
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h4>General Settings</h4>'),
            'hospital',
            Row(
                Column('allow_online_booking', css_class='form-group col-md-6 mb-0'),
                Column('booking_advance_days', css_class='form-group col-md-6 mb-0'),
            ),
            'appointment_duration',
            HTML('<h4>Financial Settings</h4>'),
            Row(
                Column('default_consultation_fee', css_class='form-group col-md-6 mb-0'),
                Column('currency', css_class='form-group col-md-6 mb-0'),
            ),
            HTML('<h4>Notification Settings</h4>'),
            Row(
                Column('send_appointment_reminders', css_class='form-group col-md-6 mb-0'),
                Column('reminder_hours_before', css_class='form-group col-md-6 mb-0'),
            ),
            HTML('<h4>Patient Portal Settings</h4>'),
            Row(
                Column('patient_portal_enabled', css_class='form-group col-md-6 mb-0'),
                Column('allow_patient_registration', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Save Configuration')
        ) 