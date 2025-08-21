from django import forms
from .models import Cita
from patients.models import Paciente
from professionals.models import ProfesionalSalud

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
        widgets = {
            'fecha_hora_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_hora_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar todos los pacientes y profesionales disponibles
        self.fields['paciente'].queryset = Paciente.objects.all()
        self.fields['profesional'].queryset = ProfesionalSalud.objects.all() 