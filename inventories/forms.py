from django import forms
from .models import UbicacionAlmacen, CategoriaProducto, Producto, MovimientoInventario, OrdenDispensacion, DetalleOrdenDispensacion

class UbicacionAlmacenForm(forms.ModelForm):
    class Meta:
        model = UbicacionAlmacen
        fields = '__all__'

class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = '__all__'

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'fecha_caducidad': forms.DateInput(attrs={'type': 'date'}),
        }

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = '__all__'
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class OrdenDispensacionForm(forms.ModelForm):
    class Meta:
        model = OrdenDispensacion
        fields = '__all__'
        widgets = {
            'fecha_dispensacion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class DetalleOrdenDispensacionForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenDispensacion
        fields = '__all__' 