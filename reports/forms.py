from django import forms
from .models import ReporteGenerado

class ReporteGeneradoForm(forms.ModelForm):
    class Meta:
        model = ReporteGenerado
        fields = '__all__'
        widgets = {
            'fecha_generacion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        } 