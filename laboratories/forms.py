from django import forms
from .models import TipoExamen, EquipoLaboratorio, OrdenExamen, ResultadoExamen
from patients.models import Paciente
from professionals.models import ProfesionalSalud
from medical_records.models import Consulta

class TipoExamenForm(forms.ModelForm):
    class Meta:
        model = TipoExamen
        fields = '__all__'

class EquipoLaboratorioForm(forms.ModelForm):
    class Meta:
        model = EquipoLaboratorio
        fields = '__all__'

class OrdenExamenForm(forms.ModelForm):
    class Meta:
        model = OrdenExamen
        fields = '__all__'
        widgets = {
            'fecha_orden': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_toma_muestra': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.all()
        self.fields['profesional_solicitante'].queryset = ProfesionalSalud.objects.filter(activo=True)
        self.fields['tipo_examen'].queryset = TipoExamen.objects.all()
        self.fields['consulta'].queryset = Consulta.objects.all()

class ResultadoExamenForm(forms.ModelForm):
    class Meta:
        model = ResultadoExamen
        fields = '__all__'
        widgets = {
            'fecha_resultado': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['orden_examen'].queryset = OrdenExamen.objects.filter(estado__in=['TOMADA', 'PROCESANDO'])
        self.fields['profesional_responsable'].queryset = ProfesionalSalud.objects.filter(activo=True)
        self.fields['equipo_utilizado'].queryset = EquipoLaboratorio.objects.filter(activo=True) 