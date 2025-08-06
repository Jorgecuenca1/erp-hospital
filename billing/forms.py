from django import forms
from .models import Factura, DetalleFactura, TransaccionDIAN
from patients.models import Paciente
from inventories.models import Producto

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
        widgets = {
            'fecha_emision': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.all()

class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(activo=True)

class TransaccionDIANForm(forms.ModelForm):
    class Meta:
        model = TransaccionDIAN
        fields = '__all__'
        widgets = {
            'fecha_transaccion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        } 