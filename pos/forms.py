from django import forms
from .models import PuntoVenta, Caja, SesionCaja, MetodoPagoPOS, VentaPOS, LineaVentaPOS

class PuntoVentaForm(forms.ModelForm):
    class Meta:
        model = PuntoVenta
        fields = '__all__'

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = '__all__'

class SesionCajaForm(forms.ModelForm):
    class Meta:
        model = SesionCaja
        fields = '__all__'

class MetodoPagoPOSForm(forms.ModelForm):
    class Meta:
        model = MetodoPagoPOS
        fields = '__all__'

class VentaPOSForm(forms.ModelForm):
    class Meta:
        model = VentaPOS
        fields = '__all__'

class LineaVentaPOSForm(forms.ModelForm):
    class Meta:
        model = LineaVentaPOS
        fields = '__all__' 