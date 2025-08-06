from django import forms
from .models import CategoriaActivo, ActivoFijo, Mantenimiento, BajaActivo
from django.contrib.auth import get_user_model

User = get_user_model()

class CategoriaActivoForm(forms.ModelForm):
    class Meta:
        model = CategoriaActivo
        fields = '__all__'

class ActivoFijoForm(forms.ModelForm):
    class Meta:
        model = ActivoFijo
        fields = '__all__'
        widgets = {
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_ultimo_mantenimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsable'].queryset = User.objects.all()

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'proximo_mantenimiento_sugerido': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activo'].queryset = ActivoFijo.objects.filter(estado__in=['OPERATIVO', 'MANTENIMIENTO'])

class BajaActivoForm(forms.ModelForm):
    class Meta:
        model = BajaActivo
        fields = '__all__'
        widgets = {
            'fecha_baja': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activo'].queryset = ActivoFijo.objects.filter(estado__in=['OPERATIVO', 'MANTENIMIENTO'])
        self.fields['aprobado_por'].queryset = User.objects.all() 