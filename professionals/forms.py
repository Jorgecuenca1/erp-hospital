from django import forms
from .models import Especialidad, ProfesionalSalud

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = '__all__'

class ProfesionalSaludForm(forms.ModelForm):
    class Meta:
        model = ProfesionalSalud
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        } 