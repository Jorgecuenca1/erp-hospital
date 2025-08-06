from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Div, Submit
from crispy_forms.bootstrap import TabHolder, Tab
from .models import (
    NursingAssessment, NursingCarePlan, NursingIntervention, NursingNote,
    NursingShift, NursingRound, NursingMedication, NursingVitalSigns,
    NursingEducation, NursingDischarge, NursingHandoff, NursingFlow,
    NursingProtocol, NursingAlert, NursingDocument, NursingSupervision,
    NursingAssignment, NursingStaff, NursingUnit, NursingReport,
    NursingQuality, NursingIncident, NursingSupply, NursingSkill,
    NursingTraining, NursingCompetency, NursingSchedule, NursingWorkload
)

class NursingAssessmentForm(forms.ModelForm):
    class Meta:
        model = NursingAssessment
        fields = '__all__'
        widgets = {
            'assessment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'next_assessment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'chief_complaint': forms.Textarea(attrs={'rows': 4}),
            'physical_assessment': forms.Textarea(attrs={'rows': 6}),
            'pain_assessment': forms.Textarea(attrs={'rows': 4}),
            'mental_status': forms.Textarea(attrs={'rows': 4}),
            'nursing_diagnosis': forms.Textarea(attrs={'rows': 4}),
            'goals': forms.Textarea(attrs={'rows': 4}),
            'interventions_planned': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab('Patient & Assessment Info',
                    Row(
                        Column('patient', css_class='form-group col-md-6'),
                        Column('nurse', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('assessment_type', css_class='form-group col-md-6'),
                        Column('priority_level', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('assessment_date', css_class='form-group col-md-6'),
                        Column('next_assessment_date', css_class='form-group col-md-6'),
                    ),
                ),
                Tab('Assessment Details',
                    'chief_complaint',
                    'physical_assessment',
                    'pain_assessment',
                    'mental_status',
                ),
                Tab('Vital Signs',
                    Row(
                        Column('blood_pressure', css_class='form-group col-md-6'),
                        Column('heart_rate', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('respiratory_rate', css_class='form-group col-md-6'),
                        Column('temperature', css_class='form-group col-md-6'),
                    ),
                    'oxygen_saturation',
                ),
                Tab('Nursing Diagnosis & Plan',
                    'nursing_diagnosis',
                    'goals',
                    'interventions_planned',
                    'follow_up_required',
                ),
                Tab('Documentation',
                    'notes',
                ),
            ),
            Submit('submit', 'Save Assessment', css_class='btn btn-primary')
        )

class NursingCarePlanForm(forms.ModelForm):
    class Meta:
        model = NursingCarePlan
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'review_date': forms.DateInput(attrs={'type': 'date'}),
            'nursing_diagnoses': forms.Textarea(attrs={'rows': 6}),
            'goals': forms.Textarea(attrs={'rows': 6}),
            'interventions': forms.Textarea(attrs={'rows': 6}),
            'expected_outcomes': forms.Textarea(attrs={'rows': 6}),
            'evaluation_notes': forms.Textarea(attrs={'rows': 4}),
            'outcomes_achieved': forms.Textarea(attrs={'rows': 4}),
            'modifications_made': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab('Basic Information',
                    Row(
                        Column('patient', css_class='form-group col-md-6'),
                        Column('nurse', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('care_plan_type', css_class='form-group col-md-6'),
                        Column('status', css_class='form-group col-md-6'),
                    ),
                ),
                Tab('Care Plan Details',
                    'nursing_diagnoses',
                    'goals',
                    'interventions',
                    'expected_outcomes',
                ),
                Tab('Timeline',
                    Row(
                        Column('start_date', css_class='form-group col-md-6'),
                        Column('end_date', css_class='form-group col-md-6'),
                    ),
                    'review_date',
                ),
                Tab('Evaluation',
                    'evaluation_notes',
                    'outcomes_achieved',
                    'modifications_made',
                ),
            ),
            Submit('submit', 'Save Care Plan', css_class='btn btn-primary')
        )

class NursingInterventionForm(forms.ModelForm):
    class Meta:
        model = NursingIntervention
        fields = '__all__'
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'completed_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'outcome': forms.Textarea(attrs={'rows': 4}),
            'complications': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='form-group col-md-6'),
                Column('nurse', css_class='form-group col-md-6'),
            ),
            Row(
                Column('intervention_type', css_class='form-group col-md-6'),
                Column('priority', css_class='form-group col-md-6'),
            ),
            Row(
                Column('scheduled_time', css_class='form-group col-md-6'),
                Column('completed_time', css_class='form-group col-md-6'),
            ),
            Row(
                Column('status', css_class='form-group col-md-6'),
                Column('duration_minutes', css_class='form-group col-md-6'),
            ),
            'description',
            'outcome',
            'complications',
            'notes',
            Submit('submit', 'Save Intervention', css_class='btn btn-primary')
        )

class NursingNoteForm(forms.ModelForm):
    class Meta:
        model = NursingNote
        fields = '__all__'
        widgets = {
            'note_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'note_content': forms.Textarea(attrs={'rows': 8}),
            'follow_up_required': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='form-group col-md-6'),
                Column('nurse', css_class='form-group col-md-6'),
            ),
            Row(
                Column('note_type', css_class='form-group col-md-6'),
                Column('note_date', css_class='form-group col-md-6'),
            ),
            Row(
                Column('is_critical', css_class='form-group col-md-6'),
                Column('is_confidential', css_class='form-group col-md-6'),
            ),
            'note_content',
            'follow_up_required',
            Submit('submit', 'Save Note', css_class='btn btn-primary')
        )

class NursingShiftForm(forms.ModelForm):
    class Meta:
        model = NursingShift
        fields = '__all__'
        widgets = {
            'shift_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'break_start': forms.TimeInput(attrs={'type': 'time'}),
            'break_end': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nurse', css_class='form-group col-md-6'),
                Column('shift_type', css_class='form-group col-md-6'),
            ),
            Row(
                Column('shift_date', css_class='form-group col-md-6'),
                Column('unit', css_class='form-group col-md-6'),
            ),
            Row(
                Column('start_time', css_class='form-group col-md-6'),
                Column('end_time', css_class='form-group col-md-6'),
            ),
            Row(
                Column('break_start', css_class='form-group col-md-6'),
                Column('break_end', css_class='form-group col-md-6'),
            ),
            Row(
                Column('patients_assigned', css_class='form-group col-md-6'),
                Column('is_overtime', css_class='form-group col-md-6'),
            ),
            'notes',
            Submit('submit', 'Save Shift', css_class='btn btn-primary')
        )

class NursingMedicationForm(forms.ModelForm):
    class Meta:
        model = NursingMedication
        fields = '__all__'
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'administration_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'administration_notes': forms.Textarea(attrs={'rows': 4}),
            'patient_response': forms.Textarea(attrs={'rows': 4}),
            'side_effects': forms.Textarea(attrs={'rows': 4}),
            'vital_signs_before': forms.Textarea(attrs={'rows': 3}),
            'vital_signs_after': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab('Patient & Medication',
                    Row(
                        Column('patient', css_class='form-group col-md-6'),
                        Column('nurse', css_class='form-group col-md-6'),
                    ),
                    'order_id',
                    Row(
                        Column('medication_name', css_class='form-group col-md-6'),
                        Column('dosage', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('route', css_class='form-group col-md-6'),
                        Column('frequency', css_class='form-group col-md-6'),
                    ),
                ),
                Tab('Administration',
                    Row(
                        Column('scheduled_time', css_class='form-group col-md-6'),
                        Column('administration_time', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('status', css_class='form-group col-md-6'),
                        Column('allergies_checked', css_class='form-group col-md-6'),
                    ),
                    'administration_notes',
                ),
                Tab('Monitoring',
                    'vital_signs_before',
                    'vital_signs_after',
                    'patient_response',
                    'side_effects',
                ),
            ),
            Submit('submit', 'Save Medication Administration', css_class='btn btn-primary')
        )

class NursingVitalSignsForm(forms.ModelForm):
    class Meta:
        model = NursingVitalSigns
        fields = '__all__'
        widgets = {
            'measurement_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='form-group col-md-6'),
                Column('nurse', css_class='form-group col-md-6'),
            ),
            'measurement_time',
            TabHolder(
                Tab('Vital Signs',
                    Row(
                        Column('blood_pressure', css_class='form-group col-md-6'),
                        Column('heart_rate', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('respiratory_rate', css_class='form-group col-md-6'),
                        Column('temperature', css_class='form-group col-md-6'),
                    ),
                    'oxygen_saturation',
                ),
                Tab('Additional Measurements',
                    Row(
                        Column('pain_score', css_class='form-group col-md-6'),
                        Column('blood_glucose', css_class='form-group col-md-6'),
                    ),
                    'glasgow_coma_scale',
                ),
                Tab('Assessment',
                    Row(
                        Column('is_critical', css_class='form-group col-md-6'),
                        Column('alert_triggered', css_class='form-group col-md-6'),
                    ),
                    'notes',
                ),
            ),
            Submit('submit', 'Save Vital Signs', css_class='btn btn-primary')
        )

class NursingEducationForm(forms.ModelForm):
    class Meta:
        model = NursingEducation
        fields = '__all__'
        widgets = {
            'education_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'content_provided': forms.Textarea(attrs={'rows': 6}),
            'materials_provided': forms.Textarea(attrs={'rows': 4}),
            'assessment_method': forms.Textarea(attrs={'rows': 4}),
            'barriers_identified': forms.Textarea(attrs={'rows': 4}),
            'follow_up_plan': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='form-group col-md-6'),
                Column('nurse', css_class='form-group col-md-6'),
            ),
            Row(
                Column('education_topic', css_class='form-group col-md-6'),
                Column('education_date', css_class='form-group col-md-6'),
            ),
            Row(
                Column('method_used', css_class='form-group col-md-6'),
                Column('duration_minutes', css_class='form-group col-md-6'),
            ),
            'content_provided',
            'materials_provided',
            'assessment_method',
            Row(
                Column('understanding_level', css_class='form-group col-md-6'),
                Column('patient_engagement', css_class='form-group col-md-6'),
            ),
            'barriers_identified',
            'follow_up_plan',
            Submit('submit', 'Save Education Record', css_class='btn btn-primary')
        )

class NursingStaffForm(forms.ModelForm):
    class Meta:
        model = NursingStaff
        fields = '__all__'
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'license_expiry': forms.DateInput(attrs={'type': 'date'}),
            'skills': forms.Textarea(attrs={'rows': 4}),
            'competencies': forms.Textarea(attrs={'rows': 4}),
            'certifications': forms.Textarea(attrs={'rows': 4}),
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
                        Column('nursing_level', css_class='form-group col-md-6'),
                        Column('specialization', css_class='form-group col-md-6'),
                    ),
                ),
                Tab('Certification & Licensing',
                    Row(
                        Column('license_number', css_class='form-group col-md-6'),
                        Column('license_expiry', css_class='form-group col-md-6'),
                    ),
                    'certifications',
                ),
                Tab('Employment',
                    Row(
                        Column('hire_date', css_class='form-group col-md-6'),
                        Column('years_experience', css_class='form-group col-md-6'),
                    ),
                    Row(
                        Column('department', css_class='form-group col-md-6'),
                        Column('unit', css_class='form-group col-md-6'),
                    ),
                    'supervisor',
                ),
                Tab('Skills & Competencies',
                    'skills',
                    'competencies',
                    Row(
                        Column('is_charge_nurse', css_class='form-group col-md-6'),
                        Column('is_float_pool', css_class='form-group col-md-6'),
                    ),
                ),
                Tab('Status',
                    'is_active',
                ),
            ),
            Submit('submit', 'Save Staff Information', css_class='btn btn-primary')
        )

class NursingSearchForm(forms.Form):
    patient_name = forms.CharField(max_length=100, required=False)
    nurse_name = forms.CharField(max_length=100, required=False)
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    unit = forms.ModelChoiceField(queryset=NursingUnit.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            Row(
                Column('patient_name', css_class='form-group col-md-3'),
                Column('nurse_name', css_class='form-group col-md-3'),
                Column('date_from', css_class='form-group col-md-2'),
                Column('date_to', css_class='form-group col-md-2'),
                Column('unit', css_class='form-group col-md-2'),
            ),
            Submit('submit', 'Search', css_class='btn btn-primary')
        )

class NursingIncidentForm(forms.ModelForm):
    class Meta:
        model = NursingIncident
        fields = '__all__'
        widgets = {
            'incident_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 6}),
            'immediate_action': forms.Textarea(attrs={'rows': 4}),
            'root_cause': forms.Textarea(attrs={'rows': 4}),
            'prevention_measures': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='form-group col-md-6'),
                Column('incident_type', css_class='form-group col-md-6'),
            ),
            Row(
                Column('incident_date', css_class='form-group col-md-6'),
                Column('severity', css_class='form-group col-md-6'),
            ),
            Row(
                Column('location', css_class='form-group col-md-6'),
                Column('reported_by', css_class='form-group col-md-6'),
            ),
            'description',
            'immediate_action',
            'root_cause',
            'prevention_measures',
            Submit('submit', 'Save Incident Report', css_class='btn btn-primary')
        ) 