from django import forms
from .models import Consulta, Diagnostico, Procedimiento, SignosVitales, NotaEvolucion, DocumentoAdjunto
from patients.models import HistoriaClinica
from professionals.models import ProfesionalSalud

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = '__all__'
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['historia_clinica'].queryset = HistoriaClinica.objects.filter(activo=True)
        self.fields['profesional'].queryset = ProfesionalSalud.objects.filter(activo=True)

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = '__all__'

class ProcedimientoForm(forms.ModelForm):
    class Meta:
        model = Procedimiento
        fields = '__all__'
        widgets = {
            'fecha_hora_realizacion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class SignosVitalesForm(forms.ModelForm):
    class Meta:
        model = SignosVitales
        fields = '__all__'
        widgets = {
            'fecha_registro': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class NotaEvolucionForm(forms.ModelForm):
    class Meta:
        model = NotaEvolucion
        fields = '__all__'
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profesional'].queryset = ProfesionalSalud.objects.filter(activo=True)

class DocumentoAdjuntoForm(forms.ModelForm):
    class Meta:
        model = DocumentoAdjunto
        fields = '__all__' 