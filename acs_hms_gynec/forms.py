from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import (
    GynecologyPatient, Pregnancy, AntenatalVisit, GynecologyProcedure,
    GynecologyMedicalRecord, ContraceptiveConsultation, MenopauseManagement
)

# Formularios para GynecologyPatient
class GynecologyPatientForm(ModelForm):
    class Meta:
        model = GynecologyPatient
        fields = '__all__'
        widgets = {
            'menarche_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'menopause_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'menstrual_cycle': forms.Select(attrs={'class': 'form-control'}),
            'cycle_length': forms.NumberInput(attrs={'class': 'form-control'}),
            'flow_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'last_menstrual_period': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gravida': forms.NumberInput(attrs={'class': 'form-control'}),
            'para': forms.NumberInput(attrs={'class': 'form-control'}),
            'term_deliveries': forms.NumberInput(attrs={'class': 'form-control'}),
            'preterm_deliveries': forms.NumberInput(attrs={'class': 'form-control'}),
            'abortions': forms.NumberInput(attrs={'class': 'form-control'}),
            'living_children': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_contraceptive': forms.Select(attrs={'class': 'form-control'}),
            'contraceptive_duration': forms.TextInput(attrs={'class': 'form-control'}),
            'last_pap_smear': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pap_smear_result': forms.TextInput(attrs={'class': 'form-control'}),
            'last_mammogram': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mammogram_result': forms.TextInput(attrs={'class': 'form-control'}),
            'surgical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'family_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Formularios para Pregnancy
class PregnancyForm(ModelForm):
    class Meta:
        model = Pregnancy
        fields = '__all__'
        widgets = {
            'pregnancy_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'last_menstrual_period': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expected_delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actual_delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'gestational_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'high_risk': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'risk_factors': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'delivery_type': forms.Select(attrs={'class': 'form-control'}),
            'birth_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'complications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Formularios para AntenatalVisit
class AntenatalVisitForm(ModelForm):
    class Meta:
        model = AntenatalVisit
        fields = '__all__'
        widgets = {
            'visit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gestational_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'blood_pressure_systolic': forms.NumberInput(attrs={'class': 'form-control'}),
            'blood_pressure_diastolic': forms.NumberInput(attrs={'class': 'form-control'}),
            'fundal_height': forms.NumberInput(attrs={'class': 'form-control'}),
            'fetal_heart_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'fetal_movement': forms.TextInput(attrs={'class': 'form-control'}),
            'presentation': forms.TextInput(attrs={'class': 'form-control'}),
            'hemoglobin': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'urine_protein': forms.TextInput(attrs={'class': 'form-control'}),
            'urine_glucose': forms.TextInput(attrs={'class': 'form-control'}),
            'ultrasound_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'estimated_fetal_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'amniotic_fluid': forms.TextInput(attrs={'class': 'form-control'}),
            'advice': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'next_visit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Formularios para GynecologyProcedure
class GynecologyProcedureForm(ModelForm):
    class Meta:
        model = GynecologyProcedure
        fields = '__all__'
        widgets = {
            'procedure_type': forms.Select(attrs={'class': 'form-control'}),
            'procedure_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'indication': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'procedure_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'findings': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'complications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'anesthesia_type': forms.Select(attrs={'class': 'form-control'}),
            'post_operative_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'follow_up_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'specimen_sent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'specimen_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pathology_report': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Formularios para GynecologyMedicalRecord
class GynecologyMedicalRecordForm(ModelForm):
    class Meta:
        model = GynecologyMedicalRecord
        fields = '__all__'
        widgets = {
            'external_genitalia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vaginal_examination': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cervical_examination': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bimanual_examination': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'breast_examination': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vaginal_discharge': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pelvic_pain': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'menstrual_irregularities': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'ultrasound_findings': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'laboratory_results': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'gynecological_diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hormonal_therapy': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'surgical_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# Formularios para ContraceptiveConsultation
class ContraceptiveConsultationForm(ModelForm):
    class Meta:
        model = ContraceptiveConsultation
        fields = '__all__'
        widgets = {
            'consultation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'current_method': forms.Select(attrs={'class': 'form-control'}),
            'satisfaction_with_current': forms.TextInput(attrs={'class': 'form-control'}),
            'desired_method': forms.Select(attrs={'class': 'form-control'}),
            'method_provided': forms.Select(attrs={'class': 'form-control'}),
            'counseling_topics': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'side_effects_discussed': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'follow_up_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'follow_up_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Formularios para MenopauseManagement
class MenopauseManagementForm(ModelForm):
    class Meta:
        model = MenopauseManagement
        fields = '__all__'
        widgets = {
            'assessment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'menopause_status': forms.Select(attrs={'class': 'form-control'}),
            'hot_flashes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'night_sweats': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'mood_changes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sleep_disturbances': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vaginal_dryness': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'decreased_libido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'symptom_severity': forms.Select(attrs={'class': 'form-control'}),
            'quality_of_life_impact': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'treatment_type': forms.Select(attrs={'class': 'form-control'}),
            'treatment_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bone_density_assessment': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cardiovascular_assessment': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'follow_up_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Formularios de búsqueda y filtros (mantener los existentes)
class GynecSearchForm(forms.Form):
    '''Formulario de búsqueda para Gynec'''
    
    q = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar...'
        }),
        label='Búsqueda',
        required=False
    )
    
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha Inicio',
        required=False
    )
    
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha Fin',
        required=False
    )
    
    estado = forms.ChoiceField(
        choices=[
            ('', 'Todos los estados'),
            ('ACTIVO', 'Activo'),
            ('INACTIVO', 'Inactivo'),
            ('PENDIENTE', 'Pendiente'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Estado',
        required=False
    )

class GynecFilterForm(forms.Form):
    '''Formulario de filtros para Gynec'''
    
    ordenar_por = forms.ChoiceField(
        choices=[
            ('nombre', 'Nombre'),
            ('fecha', 'Fecha'),
            ('estado', 'Estado'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Ordenar por',
        required=False
    )
    
    orden = forms.ChoiceField(
        choices=[
            ('asc', 'Ascendente'),
            ('desc', 'Descendente'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Orden',
        required=False
    )
    
    por_pagina = forms.ChoiceField(
        choices=[
            ('10', '10 por página'),
            ('25', '25 por página'),
            ('50', '50 por página'),
            ('100', '100 por página'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Por página',
        required=False
    )
