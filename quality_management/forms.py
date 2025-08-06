from django import forms
from .models import Incidente, Auditoria, HallazgoAuditoria, PlanMejora, DocumentoCalidad
from django.contrib.auth import get_user_model
from professionals.models import ProfesionalSalud
from patients.models import Paciente

User = get_user_model()

class IncidenteForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = '__all__'
        widgets = {
            'fecha_hora_incidente': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_cierre': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reportado_por'].queryset = User.objects.all()
        self.fields['investigador_asignado'].queryset = ProfesionalSalud.objects.filter(activo=True)
        self.fields['paciente_afectado'].queryset = Paciente.objects.filter(activo=True)

class AuditoriaForm(forms.ModelForm):
    class Meta:
        model = Auditoria
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['equipo_auditor'].queryset = ProfesionalSalud.objects.filter(activo=True)

class HallazgoAuditoriaForm(forms.ModelForm):
    class Meta:
        model = HallazgoAuditoria
        fields = '__all__'
        widgets = {
            'fecha_limite_correccion': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsable_correccion'].queryset = User.objects.all()

class PlanMejoraForm(forms.ModelForm):
    class Meta:
        model = PlanMejora
        fields = '__all__'
        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
            'fecha_cierre': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsable'].queryset = User.objects.all()

class DocumentoCalidadForm(forms.ModelForm):
    class Meta:
        model = DocumentoCalidad
        fields = '__all__'
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'fecha_revision': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['aprobado_por'].queryset = User.objects.all() 