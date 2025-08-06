from django import forms
from .models import Medicamento, Receta, DetalleReceta
from patients.models import Paciente
from professionals.models import ProfesionalSalud
from inventories.models import Producto

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(tipo_producto='MEDICAMENTO', activo=True)

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = '__all__'
        widgets = {
            'fecha_emision': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_caducidad': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.all()
        self.fields['profesional_prescriptor'].queryset = ProfesionalSalud.objects.filter(activo=True)

class DetalleRecetaForm(forms.ModelForm):
    class Meta:
        model = DetalleReceta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medicamento'].queryset = Medicamento.objects.all() 