from django import forms
from .models import PlanSuscripcion, Suscripcion, PagoSuscripcion

class PlanSuscripcionForm(forms.ModelForm):
    class Meta:
        model = PlanSuscripcion
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'notas': forms.Textarea(attrs={'rows': 3}),
        }

class PagoSuscripcionForm(forms.ModelForm):
    class Meta:
        model = PagoSuscripcion
        fields = '__all__'
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
        } 