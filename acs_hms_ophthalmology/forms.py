from django import forms
from django.forms import ModelForm, DateInput, DateTimeInput, TextInput, Textarea
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, HTML
from crispy_forms.bootstrap import FormActions
from .models import (
    EyeExamination, OphthalmologyProcedure, EyeDisease, OpticalPrescription,
    VisualFieldTest, OphthalmologyEquipment
)

class EyeExaminationForm(ModelForm):
    class Meta:
        model = EyeExamination
        fields = [
            'patient', 'appointment', 'ophthalmologist', 'examination_date',
            'chief_complaint', 'history_present_illness',
            'va_right_uncorrected', 'va_left_uncorrected', 'va_right_corrected', 'va_left_corrected',
            'sphere_right', 'cylinder_right', 'axis_right', 'sphere_left', 'cylinder_left', 'axis_left',
            'iop_right', 'iop_left', 'iop_method',
            'diagnosis', 'treatment_plan', 'medications', 'follow_up_date'
        ]
        widgets = {
            'examination_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'follow_up_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'chief_complaint': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'history_present_illness': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'diagnosis': Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'treatment_plan': Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'medications': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class OphthalmologyProcedureForm(ModelForm):
    class Meta:
        model = OphthalmologyProcedure
        fields = [
            'patient', 'eye_examination', 'procedure_type', 'procedure_name', 'description',
            'eye_operated', 'scheduled_date', 'primary_surgeon', 'preop_diagnosis', 'status'
        ]
        widgets = {
            'scheduled_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'preop_diagnosis': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class OpticalPrescriptionForm(ModelForm):
    class Meta:
        model = OpticalPrescription
        fields = [
            'patient', 'eye_examination', 'prescribed_by', 'prescription_date',
            'sphere_right', 'cylinder_right', 'axis_right', 'add_right',
            'sphere_left', 'cylinder_left', 'axis_left', 'add_left',
            'lens_type', 'pupillary_distance', 'valid_until'
        ]
        widgets = {
            'prescription_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'valid_until': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class VisualFieldTestForm(ModelForm):
    class Meta:
        model = VisualFieldTest
        fields = [
            'patient', 'eye_examination', 'test_date', 'performed_by',
            'test_type', 'eye_tested', 'test_strategy', 
            'mean_deviation', 'pattern_standard_deviation', 'visual_field_index',
            'interpretation'
        ]
        widgets = {
            'test_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'interpretation': Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class OphthalmologyEquipmentForm(ModelForm):
    class Meta:
        model = OphthalmologyEquipment
        fields = [
            'equipment_name', 'equipment_type', 'model', 'manufacturer', 'serial_number',
            'location', 'purchase_date', 'installation_date', 'status'
        ]
        widgets = {
            'purchase_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'installation_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

# Formulario de búsqueda simple
class OphthalmologySearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar pacientes, diagnósticos, procedimientos...'
        })
    )



