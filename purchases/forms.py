from django import forms
from django.forms import ModelForm
from .models import (
    Proveedor, ProductoCompra, OrdenCompra, DetalleOrdenCompra,
    FacturaCompra, DetalleFacturaCompra, PagoCompra, RecepcionCompra,
    CotizacionCompra, DetalleCotizacionCompra
)

class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_proveedor': forms.Select(attrs={'class': 'form-control'}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contacto_principal': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'email_contacto': forms.EmailInput(attrs={'class': 'form-control'}),
            'terminos_pago': forms.TextInput(attrs={'class': 'form-control'}),
            'limite_credito': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'saldo_actual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'calificacion': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProductoCompraForm(ModelForm):
    class Meta:
        model = ProductoCompra
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'requiere_autorizacion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class OrdenCompraForm(ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['proveedor', 'fecha_entrega_esperada', 'estado', 'prioridad', 'descuento', 'notas']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'fecha_entrega_esperada': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DetalleOrdenCompraForm(ModelForm):
    class Meta:
        model = DetalleOrdenCompra
        fields = ['producto', 'cantidad', 'precio_unitario', 'descuento', 'notas']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class FacturaCompraForm(ModelForm):
    class Meta:
        model = FacturaCompra
        fields = ['proveedor', 'orden_compra', 'fecha_recepcion', 'fecha_vencimiento', 'estado', 'descuento', 'notas']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'orden_compra': forms.Select(attrs={'class': 'form-control'}),
            'fecha_recepcion': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DetalleFacturaCompraForm(ModelForm):
    class Meta:
        model = DetalleFacturaCompra
        fields = ['producto', 'cantidad', 'precio_unitario', 'descuento']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
        }

class PagoCompraForm(ModelForm):
    class Meta:
        model = PagoCompra
        fields = ['factura', 'fecha_pago', 'monto', 'metodo_pago', 'referencia', 'notas']
        widgets = {
            'factura': forms.Select(attrs={'class': 'form-control'}),
            'fecha_pago': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class RecepcionCompraForm(ModelForm):
    class Meta:
        model = RecepcionCompra
        fields = ['orden_compra', 'fecha_recepcion', 'estado', 'notas']
        widgets = {
            'orden_compra': forms.Select(attrs={'class': 'form-control'}),
            'fecha_recepcion': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CotizacionCompraForm(ModelForm):
    class Meta:
        model = CotizacionCompra
        fields = ['proveedor', 'fecha_respuesta', 'fecha_validez', 'estado', 'notas']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'fecha_respuesta': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_validez': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DetalleCotizacionCompraForm(ModelForm):
    class Meta:
        model = DetalleCotizacionCompra
        fields = ['producto', 'cantidad', 'precio_unitario', 'observaciones']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# Formularios de búsqueda y filtros
class PurchasesSearchForm(forms.Form):
    '''Formulario de búsqueda para Purchases'''
    
    q = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar...'
        }),
        label='Búsqueda',
        required=False
    )
    
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha Inicio',
        required=False
    )
    
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha Fin',
        required=False
    )
    
    estado = forms.ChoiceField(
        choices=[
            ('', 'Todos los estados'),
            ('BORRADOR', 'Borrador'),
            ('RECIBIDA', 'Recibida'),
            ('PAGADA', 'Pagada'),
            ('ANULADA', 'Anulada'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Estado',
        required=False
    )

class PurchasesFilterForm(forms.Form):
    '''Formulario de filtros para Purchases'''
    
    ordenar_por = forms.ChoiceField(
        choices=[
            ('fecha', 'Fecha'),
            ('proveedor', 'Proveedor'),
            ('total', 'Total'),
            ('estado', 'Estado'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Ordenar por',
        required=False
    )
    
    orden = forms.ChoiceField(
        choices=[
            ('asc', 'Ascendente'),
            ('desc', 'Descendente'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Orden',
        required=False
    )
    
    por_pagina = forms.ChoiceField(
        choices=[
            ('10', '10 por página'),
            ('25', '25 por página'),
            ('50', '50 por página'),
            ('100', '100 por página'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Por página',
        required=False
    ) 